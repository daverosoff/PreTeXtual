import sublime
import sublime_plugin
import subprocess

class BetaCommand(sublime_plugin.WindowCommand):
    # def _verbose(msg):
    #     """Write a message to the console on program progress"""
    #     global args
    #     # None if not set at all
    #     if args.verbose and args.verbose >= 1:
    #         print('MBX: {}'.format(msg))

    def run(self, cmd, **kwargs):
        if cmd == "xsltproc":
            prefix = "vagrant ssh --command \"xsltproc "
            print("Invoking xsltproc")
            # last 2 args are XSL stylesheet and PTX source
            # process kwargs
            suffix = "{} {}\"".format(kwargs['xsl'], kwargs['pretext'])
            for k, v in kwargs.items():
                if k == "xinclude":
                    prefix = prefix + "--xinclude " if v else prefix
                if k == "output":
                    # validating: either through vagrant (slow) or via text xfrm?
                    # for now, do nothing
                    # import os.path
                    # if not(os.path.isdir(v)):
                        # raise ValueError("directory {} does not exist".format(v))
                    if v[-1] != '/':
                        v = v + '/'
                    prefix = prefix + "--output {} ".format(v)
                # receive stringparam as a dict of k-v pairs
                if k == "stringparam":
                    for param, val in v.items():
                        print("processing stringparam {} {}".format(param, val))
                        prefix = prefix + "--stringparam {} {} ".format(param, val)
            cmd_string = prefix + suffix
            print("Calling: {}".format(cmd_string))
            # subprocess.run is not available in python 3.3.6 which ST3 uses as of 3162
            try:
                result = subprocess.check_output(cmd_string, shell=True)
            except subprocess.CalledProcessError as e:
                print(e.output)
                print("Build failed.")
                return
            print("Build complete.")


