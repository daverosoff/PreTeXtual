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

    def run(self):

        default_pretext_vagrant_root = "C:/PreTeXt"

        projdata = self.window.project_data()
        if projdata is None or "folders" not in projdata:
        # no open folder, setup defaults
            # test for existence of default folder
            if not os.access(default_pretext_vagrant_root, os.F_OK):
                create_folder_ok = sublime.ok_cancel_dialog("OK to create\
                    default folder C:/PreTeXt? (Cancel, create new folder,\
                    add to project, and initialize again to override default")
                if create_folder_ok:
                    os.mkdir(default_pretext_vagrant_root)
                else:
                    sublime.message_dialog("PreTeXt Vagrant initialization\
                    cancelled.")
                    return
            projdata = {"folders": [{"path": "C:/PreTeXt"}]}
            pretext_vagrant_root = projdata['folders'][0]['path']
            projdata['pretext_vagrant_root'] = pretext_vagrant_root
            self.window.set_project_data(projdata)
        elif len(projdata['folders']) > 1:
        # close all but top folder after user confirms
            remove_ok = sublime.ok_cancel_dialog("Multiple folders are open in\
                the project. OK to remove all folders except {} and make {}\
                the root PreTeXt folder?".format(projdata['folders'][0]))
            if remove_ok:
                projdata['folders'] = projdata['folders'][0:1]
                pretext_vagrant_root = projdata['folders'][0]['path']
                projdata['pretext_vagrant_root'] = pretext_vagrant_root
                self.window.set_project_data(projdata)
            else:
                sublime.message_dialog("PreTeXt Vagrant initialization\
                    cancelled.")
                return

        pretext_vagrant_root = projdata['pretext_vagrant_root']
        pretext_vagrantfile = os.sep.join([pretext_vagrant_root,
            "Vagrantfile"])
        pretext_vagrant_root_exists = os.access(pretext_vagrant_root, os.F_OK)
        pretext_vagrantfile_exists = os.access(pretext_vagrantfile, os.F_OK)

        # print("pretext_vagrant_root: {}".format(self.pretext_vagrant_root))
        # print("pretext_vagrantfile: {}".format(self.pretext_vagrantfile))

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
