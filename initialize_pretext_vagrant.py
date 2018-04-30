import sublime
import sublime_plugin
import subprocess, urllib, os, re#, time

class VagrantException(Exception):
    def is_vagrant_exception(self):
        return True

def reverse_virgules(st):
    return re.sub('/', r"\\", st)

def slashes(st):
    return re.sub(r"\\", '/', st)

class InitializePretextVagrantCommand(sublime_plugin.WindowCommand):

    # def is_enabled(self):
    #     self.pretext_vagrant_root_exists = os.access(self.pretext_vagrant_root, os.F_OK)
    #     print("Checking {}...{}".format(self.pretext_vagrant_root, self.pretext_vagrant_root_exists))
    #     self.pretext_vagrantfile_exists = os.access(self.pretext_vagrantfile, os.F_OK)
    #     print("Checking {}...{}".format(self.pretext_vagrantfile, self.pretext_vagrantfile_exists))
    #     return not (self.pretext_vagrant_root_exists and self.pretext_vagrantfile_exists)

    def acquire_vagrantfile(self, n, loc):
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
        elif len(projdata['folders']) > 1:
        # close all but top folder after user confirms
            remove_ok = sublime.ok_cancel_dialog("Multiple folders are open in\
                the project. OK to remove all folders except {} and make {}\
                the root PreTeXt folder?".format(projdata['folders'][0]))
            if remove_ok:
                projdata['folders'] = projdata['folders'][0:1]
                # ensure a list of length 1 is returned
            else:
                sublime.message_dialog("PreTeXt Vagrant initialization\
                    cancelled.")
                return

        pretext_vagrant_root = projdata['folders'][0]['path']
        projdata['pretext_vagrant_root'] = pretext_vagrant_root
        self.window.set_project_data(projdata)

        pretext_vagrantfile = os.sep.join([pretext_vagrant_root,
            "Vagrantfile"])
        pretext_vagrant_root_exists = os.access(pretext_vagrant_root, os.F_OK)
        pretext_vagrantfile_exists = os.access(pretext_vagrantfile, os.F_OK)

        # print("pretext_vagrant_root: {}".format(self.pretext_vagrant_root))
        # print("pretext_vagrantfile: {}".format(self.pretext_vagrantfile))

        if not pretext_vagrant_root_exists:
            # this should never happen since either we created the default
            # or the user added an existing folder
            sublime.message_dialog("Error 14: something bad happened")
            raise VagrantException

            # try:
            #     os.mkdir(self.pretext_vagrant_root)
            # except FileExistsError as e:
            #     sublime.message_dialog("Error 6: Directory already exists; continuing")

        # now get the rest of the settings in place to manage projects

        projdata = self.window.project_data()
        projdata['pretext_vagrant_root'] = pretext_vagrant_root
        projdata['pretext_vagrantfile'] = pretext_vagrantfile
        ls = os.listdir(pretext_vagrant_root)

        def is_project(dirnm):
            dotted = dirnm[0] == '.'
            isdir = os.path.isdir(os.path.join(pretext_vagrant_root, dirnm))
            return not dotted and isdir

        def is_present(dirnm, projli):
            # projli is a list of dict with entries name and path
            # name is typically a relative path from the vagrant root
            for d in projli:
                if "name" in d and d['name'] == dirnm:
                    return True
            return False

        projlist = [d, os.path.join(pretext_vagrant_root, d)) for d in ls if is_project(d)]

        # Add all or some project folders to the settings file, converting to absolute paths
        # so projlist is a list of pairs of paths

        add_all = sublime.yes_no_cancel_dialog(
            "OK to add {} writing projects to PreTeXtual management? (Select No to add one by one.)".format(
                len(projlist)
            )
        )
        if add_all == sublime.DIALOG_YES:
            for rel, absol in projlist:
                if 'vagrant_projects' not in projdata:
                    projdata['vagrant_projects'] = []
                if not is_present(rel, projdata['vagrant_projects']):
                    projdata['vagrant_projects'].append({"path": absol, "name": rel})
        elif add_all == sublime.DIALOG_CANCEL:
            sublime.message_dialog("No projects added.")
            return
        elif add_all == sublime.DIALOG_NO:
            for rel, absol in projlist:
                add = sublime.yes_no_cancel_dialog(
                    "OK to add {} to PreTeXtual management? Select No to proceed to next project.".format(rel))
                if add == sublime.DIALOG_YES:
                    if 'vagrant_projects' not in projdata:
                        projdata['vagrant_projects'] = []
                    if not is_present(rel, projdata['vagrant_projects']):
                        projdata['vagrant_projects'].append({"path": absol, "name": rel})
                elif add == sublime.DIALOG_CANCEL:
                    sublime.message_dialog("Project addition cancelled.")
                    return
                elif add == sublime.DIALOG_NO:
                    continue
                else:
                    sublime.message_dialog("Error 18: something bad happened")
                    raise VagrantException
        else:
            sublime.message_dialog("Error 16: something bad happened")
            raise VagrantException

        self.window.set_project_data(projdata)

        set_root_files = sublime.ok_cancel_dialog("Do you want to set "
            "root files for the projects you just added?")

        def set_root_file(projname):
            def on_done_root(st):
                projdata = self.window.project_data()
                projli = projdata['vagrant_projects']
                for d in projli:
                    if d['name'] == projname:
                        d.update({'root_file': st})
            self.window.show_input_panel("Enter full path to root "
                "file for project {}:".format(reverse_virgules(projname)),
                pretext_vagrant_root, on_done_root, None, None)

        if set_root_files:
            projdata = self.window.project_data()
            projnames = projdata['vagrant_projects']
            for proj in projnames:
                set_root_file(proj['name'])
        else:
            sublime.message_dialog("No root files set. You can add these "
                "later in the user settings.")

        usersettings = sublime.load_settings("User.sublime-settings")
        usersettings.set('vagrant_projects', projdata['vagrant_projects'])
        sublime.save_settings("User.sublime-settings")

        # sublime.message_dialog("Click OK to bring up a quick panel to select "
        #     "a PreTeXt installation. This step can take a long time, perhaps "
        #     "an hour or more. Be patient and do not worry if it seems like "
        #     "your system is hanging. Just watch and wait. If you don't know "
        #     "what you want, select PreTeXt-lite.")

        # options = [
        #             "Install PreTeXt",
        #             "Install PreTeXt-lite",
        #             "Install PreTeXt-barebones",
        #             "Install PreTeXt-no-images"
        #         ],

        # def on_done(n):
        #     return self.acquire_vagrantfile(n, pretext_vagrant_root)

        # if not pretext_vagrantfile_exists:
        #     self.window.show_quick_panel(options, on_done)

        # sublime.message_dialog("The next step you must do yourself; the "
        #     "Sublime Text application can't do this for you (yet?). IT IS "
        #     "VERY IMPORTANT AND NOTHING WILL WORK WITHOUT IT.")

        # sublime.message_dialog("Choose Project/Save Project As... from the "
        #     "Sublime Text menu. Enter a filename in which to save your "
        #     "\"project settings\". Don't worry too much about what this means "
        #     "exactly right now; it's a way for Sublime Text to manage your "
        #     "writing projects and save your preferences between editing "
        #     "sessions.")
