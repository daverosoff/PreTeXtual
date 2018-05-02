import sublime
import sublime_plugin
import subprocess
from .get_setting import get_setting
from .initialize_pretext_vagrant import VagrantException
import os, time, re

def to_vagrant(st):
    vagrantroot = get_setting('vagrantroot', "C:/PreTeXt/")
    return re.sub(vagrantroot, '/vagrant/', st)

def from_vagrant(st):
    vagrantroot = get_setting('vagrantroot', "C:/PreTeXt/")
    return re.sub('/vagrant/', vagrantroot, st)

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
        filepath = re.sub(r"\\", "/", os.path.dirname(filename))

        vagrant = get_setting('pretext_use_vagrant', True)
        # TODO: use vagrant or not based on this value
        vagrantpath = get_setting('vagrantpath', "C:/HashiCorp/Vagrant/bin/vagrant.exe")
        vagrantroot = get_setting('vagrantroot', "C:/PreTeXt/")
        vagrantcommand = get_setting('vagrantcommand', "vagrant ssh --command")
        vagrant_projects = get_setting('vagrant_projects', {})
        # TODO: migrate xinclude, stringparam to vagrant settings
        xinclude = get_setting('xinclude', True)
        stringparam = get_setting('stringparam', {})
        # pretext_root_file = get_setting('pretext_root_file', filename)

        filepath_list = filepath.split('/')
        pretext_root_file = ""
        while filepath_list:
            print(filepath_list)
            print(vagrant_projects)
            try:
                pretext_root_file = next((vagrant_projects[proj]['name'] for proj in vagrant_projects
                    if vagrant_projects[proj]['path'].split(r'\\') == filepath_list))
            except StopIteration:
                filepath_list = filepath_list[:-1]
        if not pretext_root_file:
            sublime.message_dialog("Error 24: Couldn't find root file")
            raise VagrantException

        pretext_output = get_setting('pretext_output')
        if not pretext_output:
            pretext_output_list = filepath.split('/')[:-1]
            pretext_output_list.append("output")
            if cmd == "xsltproc":
                pretext_output_list.append(fmt)
            pretext_output = '/'.join(pretext_output_list)
        pretext_images = get_setting('pretext_images')
        pretext_html_images = get_setting('pretext_html_images')
        pretext_latex_images = get_setting('pretext_latex_images')
        if not pretext_images:
            pretext_images = '/'.join([pretext_output, 'images'])
        if not pretext_html_images:
            pretext_html_images = '/'.join([pretext_output, 'html', 'images'])
        if not pretext_latex_images:
            pretext_latex_images = '/'.join([pretext_output, 'latex', 'images'])
        pretext_stylesheets = get_setting('pretext_stylesheets', {
            "html": to_vagrant(vagrantroot + "mathbook/xsl/mathbook-html.xsl"),
            "latex": to_vagrant(vagrantroot + "mathbook/xsl/mathbook-latex.xsl"),
        })

        if not pretext_stylesheets:
            print("Cannot find PreTeXt stylesheets, check settings :(")
            raise VagrantException
        if not pretext_root_file:
            print("Need to set PreTeXt root file :(")
            raise VagrantException
        if cmd == "xsltproc":
            print("Invoking xsltproc...{}".format(time.gmtime(time.time())))
            if xinclude:
                xp_prefix = "xsltproc --xinclude --output {} ".format(to_vagrant(pretext_output))
            else:
                xp_prefix = "xsltproc --output {} ".format(to_vagrant(pretext_output))
            xp_sps = ""
            if stringparam:
                for k, v in stringparam.items():
                    xp_sps = "{} --stringparam {} \\\"{}\\\"".format(xp_sps, k, v)
            xp_suffix = " {} {}".format(pretext_stylesheets[fmt], to_vagrant(pretext_root_file))
            cmd_string = "{} \"{}\"".format(vagrantcommand, xp_prefix + xp_sps + xp_suffix)
            print("Calling: {}".format(cmd_string))
            sublime.message_dialog("Processing via xsltproc, please wait a few moments...")
            # subprocess.run is not available in python 3.3.6 which ST3 uses as of 3162
        elif cmd == "mbx":
            print("Invoking mbx...{}".format(time.gmtime(time.time())))
            mbx_prefix = "mkdir -p {}; {}mathbook/script/mbx".format(
                to_vagrant(pretext_images), to_vagrant(vagrantroot))
            mbx_switches = {'v': "", 'c': fmt,
                'd': to_vagrant(pretext_images), 'f': "all"}
            for k, v in mbx_switches.items():
                mbx_prefix = mbx_prefix + " -{} {}".format(k, v)
            mbx_suffix = " {}".format(to_vagrant(pretext_root_file))
            cmd_string = "{} \"{}\"".format(vagrantcommand, mbx_prefix
                + mbx_suffix)
            print("Calling: {}".format(cmd_string))
            sublime.message_dialog("Building images via mbx, please wait a few moments...")
        else:
            sublime.message_dialog("Error 4: Something bad happened")
            raise VagrantException
        proc = subprocess.Popen(cmd_string,
            cwd=from_vagrant(os.path.dirname(pretext_root_file)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            try:
                data = proc.stdout.readline().decode(encoding="UTF-8")
                if re.match("VM must be running", data):
                    print("Starting Vagrant box...")
                    subprocess.Popen("vagrant up", cwd=vagrantroot, shell=True)
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
