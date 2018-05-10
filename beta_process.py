import sublime
import sublime_plugin
import subprocess
from .get_setting import get_setting
from .initialize_pretext_vagrant import VagrantException
import os, time, re

def to_vagrant(st):
    vagrantroot = get_setting('vagrantroot', "C:\\\\PreTeXt\\\\")
    result = re.sub(vagrantroot, '/vagrant/', st, flags=re.IGNORECASE)
    result = re.sub(r'\\', '/', result)
    return result

def from_vagrant(st):
    vagrantroot = get_setting('vagrantroot', "C:\\\\PreTeXt\\\\")
    return re.sub('/vagrant/', vagrantroot, st, flags=re.IGNORECASE)


def retrieve(key, val, ddict, id='name'):
    """
    Given a dict of dicts, return the value of id for the dict whose
    key is val. Otherwise return None. Caller guarantees at most one
    match.
    """

    match = next((ddict[x][id] for x in ddict if ddict[x][key] == val))
    if not match:
        return None
    else:
        return match

def get_pretext_project_setting(setting, default, proj_name):
    """Given a setting (string), returns the value associated to that
    key in the dictionary for proj_name."""

    projects = get_setting('pretext_projects')
    if proj_name not in projects.keys():
        sublime.message_dialog("Error 32: invalid project")
        raise VagrantException
    if setting in projects[proj_name].keys():
        return projects[proj_name][setting]
    else:
        return default

def get_pretext_project(vu):
    """Given a view with associated filename, returns the associated
    key of project in settings (pretext_projects).
    """

    fn = vu.file_name()
    if fn is None:
        sublime.message_dialog("Error 26: File is not saved to disk")
        raise VagrantException

    projects = get_setting('pretext_projects', {})

    if not projects:
        sublime.message_dialog("Error 28: No projects available")
        raise VagrantException

    while fn:
        if re.match(r':\\', fn):
            # we've descended to the root without matching
            sublime.message_dialog("Error 30: couldn't find project")
            raise VagrantException
        fn = os.path.dirname(fn)
        match = retrieve('path', fn, projects)
        if match:
            return match

class BetaCommand(sublime_plugin.WindowCommand):
    # def _verbose(msg):
    #     """Write a message to the console on program progress"""
    #     global args
    #     # None if not set at all
    #     if args.verbose and args.verbose >= 1:
    #         print('MBX: {}'.format(msg))

    # get project settings
    # xinclude: boolean
    # output: string (absolute path name for vagrant)
    # stringparams: dict{string:string}

    def run(self, cmd, fmt):
        sublime.set_timeout_async(lambda: self.doit(cmd, fmt), 0)

    def doit(self, cmd, fmt):

        print("This is the beta processing command...")
        filename = self.window.active_view().file_name()
        # filepath = re.sub(r"\\", "/", os.path.dirname(filename))
        filepath = os.path.dirname(filename)

        vagrant = get_setting('pretext_use_vagrant', True)
        # TODO: use vagrant or not based on this value

        vagrantpath = get_setting('vagrantpath', "C:\\HashiCorp\\Vagrant\\bin\\vagrant.exe")
        vagrantroot = get_setting('vagrantroot', "C:\\PreTeXt\\")
        vagrantcommand = get_setting('vagrantcommand',
            "{} ssh --command".format(vagrantpath))

        # most users will not have values set for vagrantpath, vagrantroot,
        # vagrantcommand; assume these sensible default values; only users who
        # are customizing to fit an existing system will need to override the
        # defaults

        # most users will not override these defaults
        pretext_stylesheets = get_setting('pretext_stylesheets', {
            "html": to_vagrant(vagrantroot + "mathbook/xsl/mathbook-html.xsl"),
            "latex": to_vagrant(vagrantroot + "mathbook/xsl/mathbook-latex.xsl"),
        })

        if not pretext_stylesheets:
            # print("Cannot find PreTeXt stylesheets, check settings :(")
            sublime.message_dialog("Error 44: Can't find PreTeXt stylesheets")
            raise VagrantException

        project_name = get_pretext_project(sublime.active_window().active_view())

        # xinclude = get_setting('xinclude', True)
        xinclude = get_pretext_project_setting('xinclude', True, project_name)
        # stringparam = get_setting('stringparam', {})
        stringparam = get_pretext_project_setting('stringparam', {}, project_name)
        root_file = get_pretext_project_setting('root_file', "", project_name)
        if not root_file:
            sublime.message_dialog("Error 24: Couldn't find project root file")
            raise VagrantException
        path = get_pretext_project_setting('path', "", project_name)
        if not path:
            sublime.message_dialog("Error 34: Couldn't find project path")
            raise VagrantException

        # pretext_root_file = get_setting('pretext_root_file', filename)
        # filepath_list = filepath.split('/')
        # pretext_root_file = ""
        # while filepath_list:
        #     print(filepath_list)
        #     print(vagrant_projects)
        #     try:
        #         pretext_root_file = next((vagrant_projects[proj]['name'] for proj in vagrant_projects
        #             if vagrant_projects[proj]['path'].split(r'\\') == filepath_list))
        #     except StopIteration:
        #         filepath_list = filepath_list[:-1]
        # if not pretext_root_file:

        # Note: trailing slash is added later, no need for it here
        pretext_output = get_pretext_project_setting('pretext_output',
            os.path.join(path, 'output'), project_name)
        if not pretext_output:
            sublime.message_dialog("Error 36: something bad happened")
            raise VagrantException
            # pretext_output_list = filepath.split('/')[:-1]
            # pretext_output_list.append("output")
            # if cmd == "xsltproc":
            #     pretext_output_list.append(fmt)
            # pretext_output = '/'.join(pretext_output_list)
        pretext_output_html = get_pretext_project_setting('pretext_output_html',
            os.path.join(pretext_output, 'html'), project_name)
        pretext_output_latex = get_pretext_project_setting('pretext_output_latex',
            os.path.join(pretext_output, 'latex'), project_name)
        pretext_output_epub = get_pretext_project_setting('pretext_output_epub',
            os.path.join(pretext_output, 'epub'), project_name)
        pretext_images = get_pretext_project_setting('pretext_images',
            os.path.join(pretext_output, 'images'), project_name)
        pretext_html_images = get_pretext_project_setting('pretext_html_images',
            os.path.join(pretext_output_html, 'images'), project_name)
        pretext_latex_images = get_pretext_project_setting('pretext_latex_images',
            os.path.join(pretext_output_latex, 'images'), project_name)
        pretext_epub_images = get_pretext_project_setting('pretext_epub_images',
            os.path.join(pretext_output_epub, 'images'), project_name)
        pretext_epub_images = get_pretext_project_setting()
        # if not pretext_images:
        #     # pretext_images = '/'.join([pretext_output, 'images'])
        #     sublime.message_dialog("Error 38: something bad happened")
        #     raise VagrantException
        # if not pretext_html_images:
        #     # pretext_html_images = '/'.join([pretext_output, 'html', 'images'])
        #     sublime.message_dialog("Error 40: something bad happened")
        #     raise VagrantException
        # if not pretext_latex_images:
        #     # pretext_latex_images = '/'.join([pretext_output, 'latex', 'images'])
        #     sublime.message_dialog("Error 42: something bad happened")
        #     raise VagrantException


        # if not pretext_root_file:
        #     print("Need to set PreTeXt root file :(")
        #     raise VagrantException

        if cmd == "xsltproc":
            print("Invoking xsltproc...{}".format(time.gmtime(time.time())))

            xp_prefix = "xsltproc "
            if xinclude:
                xp_prefix += "--xinclude"
            xp_prefix += "--output {}/{}/".format(to_vagrant(pretext_output), fmt)

            xp_sps = ""
            if stringparam:
                for k, v in stringparam.items():
                    xp_sps = "{} --stringparam {} \\\"{}\\\"".format(xp_sps, k, v)
            xp_suffix = " {} {}".format(pretext_stylesheets[fmt], to_vagrant(root_file))

            cmd_string = "{} \"{}\"".format(vagrantcommand, xp_prefix + xp_sps + xp_suffix)
            print("Calling: {}".format(cmd_string))
            sublime.message_dialog("Processing via xsltproc, please wait a few moments...")
            # subprocess.run is not available in python 3.3.6 which ST3 uses as of 3162

        elif cmd == "mbx":
            print("Invoking mbx...{}".format(time.gmtime(time.time())))
            mbx_prefix = "mkdir --parents {}; ".format(to_vagrant(pretext_images))
            mbx_prefix += "{}mathbook/script/mbx".format(to_vagrant(vagrantroot))
            # remove 'v' key from mbx_switches to disable verbose
            # change 'v' value to "v" to enable maximum verbosity
            image_format = image_fmt if image_fmt else "all"
            mbx_switches = {'v': "", 'c': fmt,
                'd': to_vagrant(pretext_images), 'f': image_fmt}
            for k, v in mbx_switches.items():
                mbx_prefix += " -{} {}".format(k, v)
            mbx_suffix = " {}".format(to_vagrant(root_file))
            cmd_string = "{} \"{}\"".format(vagrantcommand, mbx_prefix
                + mbx_suffix)
            print("Calling: {}".format(cmd_string))
            sublime.message_dialog("Building images via mbx, please wait a few moments...")
        else:
            sublime.message_dialog("Error 4: No valid process selected")
            raise VagrantException
        proc = subprocess.Popen(cmd_string,
            cwd=from_vagrant(os.path.dirname(root_file)), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            try:
                data = proc.stdout.readline().decode(encoding="UTF-8")
                if re.match("VM must be running", data):
                    print("Starting Vagrant box...")
                    subprocess.Popen("{} up".format(vagrantpath),
                        cwd=vagrantroot, shell=True)
                    # built = False
                print(data, end="")
            except:
                # if built:
                sublime.message_dialog("Build complete.")
                return
        # if built:
        if cmd == "mbx":
            print("Copying images from {} to {}...".format(pretext_images, pretext_html_images))
            import shutil
            if os.access(pretext_html_images, os.F_OK):
                shutil.rmtree(pretext_html_images)
            if os.access(pretext_latex_images, os.F_OK):
                shutil.rmtree(pretext_latex_images)
            shutil.copytree(pretext_images, pretext_html_images)
            shutil.copytree(pretext_images, pretext_latex_images)
        sublime.message_dialog("Build complete.")
