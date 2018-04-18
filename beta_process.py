import sublime
import sublime_plugin
import subprocess
from .get_setting import get_setting
import os, time

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

    def run(self, cmd, format, **kwargs):
        filename = self.window.active_view().file_name()
        filepath = os.path.dirname(filename)

        vagrantpath = get_setting('vagrantpath', "C:/HashiCorp/Vagrant/bin/vagrant.exe")
        vagrantroot = get_setting('vagrantroot', "C:/PreTeXt/")
        vagrantcommand = get_setting('vagrantcommand', None)
        xinclude = get_setting('xinclude', False)
        stringparam = get_setting('stringparam', {})
        pretext_root_file = get_setting('pretext_root_file', filename)
        pretext_output = get_setting('pretext_output', filepath)
        pretext_images = get_setting('pretext_images', os.path.join(filepath, "images"))
        pretext_stylesheets = get_setting('pretext_stylesheets', {})

        if not pretext_stylesheets:
            print("Cannot find PreTeXt stylesheets, check settings :(")
            return
        if cmd == "xsltproc":
            print("Invoking xsltproc...{}".format(time.gmtime(time.time())))
            if xinclude:
                xp_prefix = "xsltproc --xinclude --output {} ".format(pretext_output)
            else:
                xp_prefix = "xsltproc --output {} ".format(pretext_output)
            xp_sps = ""
            if stringparam:
                for k, v in stringparam.items():
                    xp_sps = "{} --stringparam {} \\\"{}\\\"".format(xp_sps, k, v)
            xp_suffix = " {} {}".format(pretext_stylesheets[format], pretext_root_file)
            cmd_string = "{} \"{}\"".format(vagrantcommand, xp_prefix + xp_sps + xp_suffix)
            print("Calling: {}".format(cmd_string))
            # subprocess.run is not available in python 3.3.6 which ST3 uses as of 3162
            try:
                result = subprocess.check_output(cmd_string, shell=True)
            except subprocess.CalledProcessError as e:
                print("Build warning (nonzero exit code): {}".format(e.output))
                pass
            print("Build complete.")


