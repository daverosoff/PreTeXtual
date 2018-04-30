import sublime
import sublime_plugin
import subprocess, urllib, os, re#, time

class VagrantException(Exception):
    def is_vagrant_exception(self):
        return True

class InitializePretextVagrantCommand(sublime_plugin.WindowCommand):

    # def is_enabled(self):
    #     self.pretext_vagrant_root_exists = os.access(self.pretext_vagrant_root, os.F_OK)
    #     print("Checking {}...{}".format(self.pretext_vagrant_root, self.pretext_vagrant_root_exists))
    #     self.pretext_vagrantfile_exists = os.access(self.pretext_vagrantfile, os.F_OK)
    #     print("Checking {}...{}".format(self.pretext_vagrantfile, self.pretext_vagrantfile_exists))
    #     return not (self.pretext_vagrant_root_exists and self.pretext_vagrantfile_exists)

    # def install_vagrant_box(st):
    #     allowed = ["PreTeXt","PreTeXt-lite","PreTeXt-barebones","PreTeXt-no-images"]
    #     allowed_ext = lambda x: x.split('-')[-1]
    #     if st in allowed:
    #         base_url = "https://raw.githubusercontent.com/daverosoff/pretext-vagrant/master/Vagrantfile-PreTeXt"
    #         url = '-'.join(base_url, allowed_ext(st))
    #         with urllib.request.urlopen(url, unverifiable=True) as vagrantfile_data:
    #             with open(self.pretext_vagrantfile) as vf:
    #                 try:
    #                     vf.write(vagrantfile_data.read())
    #                 except OSError as e:
    #                     sublime.message_dialog("Error 10: Couldn't write Vagrantfile")
    #     else:
    #         sublime.message_dialog("Error 8: Invalid Vagrantfile")
    #         raise VagrantException

    def run(self):
        print("pretext_vagrant_root: {}".format(self.pretext_vagrant_root))
        print("pretext_vagrantfile: {}".format(self.pretext_vagrantfile))

        def acquire_vagrantfile(n, loc):
            if n == -1:
                # quick panel was cancelled
                return
            base_url = "https://raw.githubusercontent.com/daverosoff/pretext-vagrant/master/Vagrantfile-PreTeXt"
            url_exts = ["", "-lite", "-barebones", "-no-images"]
            box_name = "daverosoff/pretext" + url_exts[n]
            proc = subprocess.Popen("vagrant init {}".format(box_name), cwd=loc,
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while proc.poll() is None:
                try:
                    data = proc.stdout.readline().decode(encoding="UTF-8")
                    print(data, end="")
                except:
                    return
            # subprocess.call("vagrant init {}".format(box_name), cwd=loc)
            proc = subprocess.Popen("vagrant up", cwd=loc,
                )
            while proc.poll() is None:
                try:
                    data = proc.stdout.readline().decode(encoding="UTF-8")
                    print(data, end="")
                except:
                    return
            # subprocess.call("vagrant init {}".format(box_name), cwd=loc)
            proc = subprocess.Popen("vagrant suspend", cwd=loc,
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while proc.poll() is None:
                try:
                    data = proc.stdout.readline().decode(encoding="UTF-8")
                    print(data, end="")
                except:
                    return
            # subprocess.call("vagrant init {}".format(box_name), cwd=loc)
            # with urllib.request.urlopen(base_url + url_exts[n]) as url:
            #     try:
            #         with open(loc, 'wb') as u:
            #             u.write(url.read())
            #             sett = sublime.load_settings("Vagrant.sublime-settings")
            #             sett.set('vagrantfile_path', re.sub('/', r"\\", os.path.dirname(self.pretext_vagrantfile)))
            #             print("Attempting to set {}: {}".format('vagrantfile_path', sett.get('vagrantfile_path')))
            #             sublime.save_settings("Vagrant.sublime-settings")
            #     except OSError as e:
            #         print("Writing {}...{}, {}".format(self.pretext_vagrantfile, e.args, e.filename))
            #         sublime.message_dialog("Error 12: Couldn't open Vagrantfile location")

        if not self.pretext_vagrant_root_exists:
            try:
                os.mkdir(self.pretext_vagrant_root)
            except FileExistsError as e:
                sublime.message_dialog("Error 6: Directory already exists; continuing")
        if not self.pretext_vagrantfile_exists:
            self.window.show_quick_panel(
                [
                    "Install PreTeXt",
                    "Install PreTeXt-lite",
                    "Install PreTeXt-barebones",
                    "Install PreTeXt-no-images",
                ],
                lambda n: acquire_vagrantfile(n, self.pretext_vagrant_root)
                #<flags>,
                #<selected_index>,
                #<on_highlighted>
            )
        projdata = self.window.project_data() or {}
        if not projdata["folders"]:
            projdata["folders"] = []
        projdata["folders"].append({"path": "C:/PreTeXt"})
        self.window.set_project_data(projdata)
