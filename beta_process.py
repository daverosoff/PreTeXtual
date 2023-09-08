# Copyright 2016-2019 David W. Rosoff

# This file is part of PreTeXtual, a package for Sublime Text.

# PreTeXtual is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PreTeXtual is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PreTeXtual.  If not, see <http://www.gnu.org/licenses/>.

import sublime
import sublime_plugin
import subprocess
import os, time, re, shutil
from distutils.dir_util import copy_tree
from .get_setting import get_setting
from .initialize_pretext_vagrant import VagrantException

#I am not sure I understand the use of the functions "to_vagrant" and "from vagrant". My guess was that they return a string
#that seems to be the path of the vagrant directory?

def to_vagrant(st): 
    vagrantroot = get_setting('vagrantroot', r"C:\\PreTeXt\\")
    # I looked at the get_setting module, but I don't understand how line 13 gets executed. A better way to say it is that 
    # I don't really understand how the get-setting function works and what it does.
    result = re.sub(vagrantroot, '/vagrant/', st, flags=re.IGNORECASE)
    result = re.sub(r'\\', '/', result)
    return result

def from_vagrant(st):
    vagrantroot = get_setting('vagrantroot', r"C:\\PreTeXt\\")
    return re.sub('/vagrant/', vagrantroot, st, flags=re.IGNORECASE)

#Is this the equivalent of a hashtable?
def retrieve(key, val, ddict, id='name'):
    """
    Given a dict of dicts, return the value of id for the dict whose
    key is val. Otherwise return None. Caller guarantees at most one
    match.
    """

    try:
        match = next((ddict[x][id] for x in ddict if ddict[x][key] == val))
        return match
    except StopIteration:
        return None

#
def get_pretext_project_setting(setting, default, proj_name):
    """Given a setting (string), returns the value associated to that
    key in the dictionary for proj_name."""

    projects = get_setting('pretext_projects')
    if proj_name not in projects.keys():
        sublime.message_dialog("Error 32: invalid project {}".format(proj_name))
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
        match = retrieve('path', fn, projects) # name of project is retained
        if match:
            # print("Found {}".format(match))
            return match

    sublime.message_dialog("Error 102: Something bad happened")
    raise VagrantException

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
    # stringparam: dict{string:string}

    def run(self, cmd, fmt):
        sublime.set_timeout_async(lambda: self.doit(cmd, fmt), 0)

    def doit(self, cmd, fmt):

        print("This is the beta processing command...")
        filename = self.window.active_view().file_name()
        # filepath = re.sub(r"\\", "/", os.path.dirname(filename))
        filepath = os.path.dirname(filename)

        vagrant = get_setting('pretext_use_vagrant', True)
        # TODO: use vagrant or not based on this value

        vagrantpath = get_setting('vagrantpath',
            "C:\\HashiCorp\\Vagrant\\bin\\vagrant.exe")
        vagrantroot = get_setting('vagrantroot', "C:\\PreTeXt\\")
        vagrantcommand = get_setting('vagrantcommand',
            "{} ssh --command".format(vagrantpath))

        def acquire_settings(vu):

            settings = sublime.Settings(vu.id()) #Cpnstruction of a settings object
            
            settings.set('project_name',get_pretext_project(vu))

            settings.set('pretext_stylesheets',get_pretext_project_setting(
                'pretext_stylesheets', {
                    "html": to_vagrant(vagrantroot
                        + "mathbook/xsl/mathbook-html.xsl"),
                    "latex": to_vagrant(vagrantroot
                        + "mathbook/xsl/mathbook-latex.xsl"),
                # "epub": to_vagrant(vagrantroot + "mathbook/xsl/mathbook-epub.xsl"),
            }, settings.get('project_name')))

            # if not pretext_stylesheets:
            #     # print("Cannot find PreTeXt stylesheets, check settings :(")
            #     sublime.message_dialog("Error 44: Can't find PreTeXt stylesheets")
            #     raise VagrantException

            # xinclude = get_setting('xinclude', True)

            settings.set('xinclude',get_pretext_project_setting('xinclude', True,
                settings.get('project_name')))
            # stringparam = get_setting('stringparam', {})
            settings.set('stringparam',get_pretext_project_setting('stringparam', {},
                settings.get('project_name')))
            settings.set('stringparam',get_pretext_project_setting('root_file', "",
                settings.get('project_name')))
            # TODO: some attempt at intelligent root file detection assuming
            # sensible structure
            if settings.get('root_file') is None:
                sublime.message_dialog("Error 24: Couldn't find project "
                    "root file")
                raise VagrantException
            settings.set('path', get_pretext_project_setting('path', "", settings.get('project_name')))
            # if not path:
            #     sublime.message_dialog("Error 34: Couldn't find project path")
            #     raise VagrantException

            # Note: trailing slash is added later, no need for it here
            settings.set('pretext_output',get_pretext_project_setting('pretext_output',
                os.path.join(settings.get('path'), 'output'), settings.get('project_name')))
            if settings.get(pretext_output) is None:
                sublime.message_dialog("Error 36: something bad happened")
                raise VagrantException
                # pretext_output_list = filepath.split('/')[:-1]
                # pretext_output_list.append("output")
                # if cmd == "xsltproc":
                #     pretext_output_list.append(fmt)
                # pretext_output = '/'.join(pretext_output_list)
            settings.set('pretext_output_html',get_pretext_project_setting('pretext_output_html',
                os.path.join(settings.get('pretext_output', 'html'), settings.get('project_name'))))
            settings.set('pretext_output_latex',get_pretext_project_setting('pretext_output_latex',
                os.path.join(settings.get('pretext_output', 'latex'), settings.get('project_name'))))
            # pretext_output_epub = get_pretext_project_setting('pretext_output_epub',
            #     os.path.join(pretext_output, 'epub'), project_name)
            settings.set('pretext_images',get_pretext_project_setting('pretext_images',
                os.path.join(settings.get('pretext_output', 'images'), settings.get('project_name'))))
            settings.set('pretext_html_images',get_pretext_project_setting('pretext_html_images',
                os.path.join(settings.get('pretext_output', 'images'), settings.get('project_name'))))
            settings.set('pretext_latex_images',get_pretext_project_setting('pretext_latex_images',
                os.path.join(settings.get('pretext_output', 'images'), settings.get('project_name'))))
            # pretext_epub_images = get_pretext_project_setting('pretext_epub_images',
            #     os.path.join(pretext_output_epub, 'images'), project_name)
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

            return settings

        if cmd == "update_pretext":
            #### FUNCTION EXITS FROM THIS BLOCK
            # test for existing installation
            s = acquire_settings(self.window.active_view())
            loc = to_vagrant(os.path.join(vagrantroot, "mathbook"))
            cmd_string = "mkdir --parents {}; cd {}; ".format(loc, loc)
            if os.access(os.path.join(vagrantroot, "mathbook"), os.F_OK):
                cmd_string += "git pull"
            else:
                cmd_string += "git clone https://github.com/rbeezer/mathbook.git ."
            print("Calling {} \"{}\"".format(vagrantcommand,
                cmd_string))
            proc = subprocess.Popen("{} \"{}\"".format(vagrantcommand, cmd_string),
                shell=True, stdout=subprocess.PIPE,
                cwd=from_vagrant(os.path.dirname(s['root_file'])),
                stderr=subprocess.STDOUT)
            while proc.poll() is None:
                try:
                    data = proc.stdout.readline().decode(encoding="UTF-8")
                    print(data, end="")
                except:
                    # if built:
                    sublime.message_dialog("Build complete.")
            return

        def refresh_images(s):
            # if os.access(s['pretext_html_images'], os.F_OK):
            #     shutil.rmtree(s['pretext_html_images'])
            # if os.access(s['pretext_latex_images'], os.F_OK):
            #     shutil.rmtree(s['pretext_latex_images'])
            # if os.access(s['pretext_epub_images'], os.F_OK):
            #     shutil.rmtree(s['pretext_epub_images'])
            print("Copying images from {} to {}...".format(s['pretext_images'],
                s['pretext_html_images']))
            copy_tree(s['pretext_images'], s['pretext_html_images'])
            print("Copying images from {} to {}...".format(s['pretext_images'],
                s['pretext_latex_images']))
            copy_tree(s['pretext_images'], s['pretext_latex_images'])
            # print("Copying images from {} to {}...".format(s['pretext_images'],
                # s['pretext_epub_images']))
            # shutil.copy_tree(s['pretext_images'], s['pretext_epub_images'])

        def do_process(s, cmd, cmd_string):
            proc = subprocess.Popen(cmd_string,
                cwd=from_vagrant(os.path.dirname(s['root_file'])), shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while proc.poll() is None:
                try:
                    data = proc.stdout.readline().decode(encoding="UTF-8")
                    # if re.match("VM must be running", data):
                    #     print("Starting Vagrant box...")
                    #     subprocess.Popen("{} up".format(vagrantpath),
                    #         cwd=vagrantroot, shell=True)
                    #     # built = False
                    print(data, end="")
                except:
                    # if built:
                    sublime.message_dialog("{} build execution complete.".format(cmd))

        # if cmd == "xsltproc":
        def xsl_process(s, cmd, fmt):
            print("Invoking xsltproc...{}".format(time.gmtime(time.time())))

            xp_prefix = "xsltproc "
            if s['xinclude']:
                xp_prefix += "--xinclude "
            xp_prefix += "--output {}/{}/".format(to_vagrant(s['pretext_output']),
                fmt)

            xp_sps = ""
            if s['stringparam']:
                for k, v in s['stringparam'].items():
                    xp_sps = "{} --stringparam {} \\\"{}\\\"".format(xp_sps,
                        k, v)
            xp_suffix = " {} {}".format(s['pretext_stylesheets'][fmt],
                to_vagrant(s['root_file']))

            cmd_string = "{} \"{}\"".format(vagrantcommand, xp_prefix + xp_sps
                + xp_suffix)
            print("Calling: {}".format(cmd_string))
            sublime.message_dialog("Processing via xsltproc, please wait a "
                "few moments...")
            # subprocess.run is not available in python 3.3.6 which ST3 uses as of 3162

            do_process(s, cmd, cmd_string)

        # elif cmd == "mbx":
        def mbx_process(s, cmd, fmt):
            print("Invoking mbx...{}".format(time.gmtime(time.time())))
            mbx_prefix = "mkdir --parents {}; ".format(to_vagrant(s['pretext_images']))
            mbx_prefix += "{}mathbook/script/mbx".format(to_vagrant(vagrantroot))

            # source format (-c) specified via build sys
            # we build all allowed outputs for the source according
            # to this dictionary
            allowed_formats = {
                "tikz": ["source", "svg", "pdf"],
                "asy": ["source", "svg", "pdf", "eps"],
                "sageplot": ["source", "svg", "pdf"],
                "latex-image": ["source", "svg", "pdf", "eps", "png"],
                "youtube": [],
                "mom": [],
                "webwork": ["tex", "xml"]
            }

            if fmt not in allowed_formats.keys():
                sublime.message_dialog("Error 46: Something bad happened")
                raise VagrantException

            # remove 'v' key from mbx_switches to disable verbose
            # change 'v' key to "vv" to enable maximum verbosity
            mbx_switches = {'vv': "", 'c': fmt,
                'd': to_vagrant(s['pretext_images'])}

            # def on_done(st, mbx_p, mbx_s):
            for image_outfmt in allowed_formats[fmt]:
                mbx_cmd = mbx_prefix
                mbx_switches_c = mbx_switches
                mbx_switches_c.update({'f': image_outfmt})
                for k, v in mbx_switches_c.items():
                    mbx_cmd += " -{} {}".format(k, v)
                mbx_cmd += " {}".format(to_vagrant(s['root_file']))
                cmd_string = "{} \"{}\"".format(vagrantcommand, mbx_cmd)
                print("Calling: {}".format(cmd_string))
                if fmt == "youtube":
                    sublime.message_dialog("Fetching YouTube thumbnails "
                        "via mbx, please wait a few moments...")
                elif fmt == "webwork":
                    sublime.message_dialog("Extracting WeBWorK problems "
                        "into {} format via mbx, ".format(image_outfmt)
                            + "please wait a few moments...")
                elif fmt == "mom":
                    sublime.message_dialog("Extracting MyOpenMath "
                        "static problems via mbx, please wait a "
                        "few moments...")
                else:
                    sublime.message_dialog("Building {} images into {} format "
                        "via mbx, please wait a few moments...".format(fmt,
                            image_outfmt))

                do_process(s, cmd, cmd_string)

                # if built:
                # if cmd == "mbx":

        sett = acquire_settings(self.window.active_view())

        if cmd == "xsltproc":
            xsl_process(sett, cmd, fmt)
        if cmd == "mbx":
            mbx_process(sett, cmd, fmt)
            refresh_images(sett)

        sublime.message_dialog("End of PreTeXtual build routine.")
                # if cmd == "xsltproc" and fmt == "latex":
                #     tex_prefix = "xelatex"
                #     root_file_suffix = os.path.basename(to_vagrant(root_file)).split('.')[-1]
                #     root_file_suffix += '$' # only match at end
                #     tex_source = re.sub(root_file_suffix, 'tex',
                #         os.path.basename(root_file))
                #     tex_source = to_vagrant(os.path.join(pretext_output_latex, tex_source))
                #     tex_cmd_string = "{} {}".format(tex_prefix, tex_source)
                #     print("Calling {}...".format(tex_cmd_string))
                #     proc = subprocess.Popen(tex_cmd_string,
                #         # cwd=from_vagrant(os.path.dirname(root_file)),
                #         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                #     while proc.poll() is None:
                #         try:
                #             data = proc.stdout.readline().decode(encoding="UTF-8")
                #             print(data, end="")
                #         except:
                #             # if built:
                #             sublime.message_dialog("tex build execution complete.")

                # self.window.show_input_panel("Enter an output format (one of "
                #     "{}): ".format(", ".join(allowed_formats[fmt])),
                #     "", lambda s: on_done(s, mbx_prefix, mbx_switches), None, None)

        # else:
        #     sublime.message_dialog("Error 4: No valid process selected")
        #     raise VagrantException

