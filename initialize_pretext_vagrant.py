import sublime
import sublime_plugin
import subprocess, urllib, os, re#, time
from .get_setting import get_setting

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
            print("Quick panel for vagrant box cancelled")
            sublime.message_dialog("No vagrant box installed. Get help "
                "at https://github.com/daverosoff/PreTeXtual/issues")
            return
        vagrantpath = get_setting('vagrantpath', r"C:\\HashiCorp\\Vagrant\\bin\\vagrant.exe")
        base_url = "https://raw.githubusercontent.com/daverosoff/pretext-vagrant/master/Vagrantfile-PreTeXt"
        url_exts = ["", "-lite", "-barebones", "-no-images"]
        box_name = "daverosoff/pretext" + url_exts[n]
        print("Attempting to fetch {}".format(box_name))
        proc = subprocess.Popen("{} init {}".format(vagrantpath,
            box_name), cwd=loc, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        while proc.poll() is None:
            try:
                data = proc.stdout.readline().decode(encoding="UTF-8")
                print(data, end="")
            except:
                return
        # subprocess.call("vagrant init {}".format(box_name), cwd=loc)
        proc = subprocess.Popen("{} up".format(vagrantpath), cwd=loc,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            try:
                data = proc.stdout.readline().decode(encoding="UTF-8")
                print(data, end="")
            except:
                return
        # subprocess.call("vagrant init {}".format(box_name), cwd=loc)
        proc = subprocess.Popen("{} suspend".format(vagrantpath), cwd=loc,
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

        default_pretext_vagrant_root = r"C:\\PreTeXt"

        projdata = self.window.project_data()
        if projdata is None or "folders" not in projdata:
        # no open folder, setup defaults
            # test for existence of default folder
            if not os.access(default_pretext_vagrant_root, os.F_OK):
                create_folder_ok = sublime.ok_cancel_dialog("OK to create "
                    "default folder C:\\PreTeXt? (Cancel, create new folder, "
                    "add to project, and initialize again to override default)")
                if create_folder_ok:
                    os.mkdir(default_pretext_vagrant_root)
                else:
                    sublime.message_dialog("PreTeXt Vagrant initialization "
                    "cancelled.")
                    return
            projdata = {"folders": [{"path": r"C:\\PreTeXt"}]}
        elif len(projdata['folders']) > 1:
        # close all but top folder after user confirms
            remove_ok = sublime.ok_cancel_dialog("Multiple folders are open in "
                "the project. OK to remove all folders except {} and make {}"
                "the root PreTeXt folder?".format(projdata['folders'][0]))
            if remove_ok:
                projdata['folders'] = projdata['folders'][0:1]
                # ensure a list of length 1 is returned
            else:
                sublime.message_dialog("PreTeXt Vagrant initialization "
                    "cancelled.")
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

        projlist = [(d, os.path.join(pretext_vagrant_root, d))
            for d in ls if is_project(d) and d != "mathbook"]

        # Add all or some project folders to the settings file, converting to absolute paths
        # so projlist is a list of pairs of paths

        if len(projlist) > 0:
            add_all = sublime.yes_no_cancel_dialog(
                "OK to add {} writing projects to PreTeXtual "
                "management? (Select No to add one by one.)".format(
                    len(projlist)
                )
            )
        else:
            sublime.message_dialog("No subfolders detected. See "
                "documentation for details on adding projects.")

        def add_some_projects(add_q, projli):
            """
            add_q is one of sublime.DIALOG_YES, _NO, or _CANCEL
            projli is of type [{'name': {}}]
            """
            if add_q == sublime.DIALOG_YES:
                for rel, absol in projli:
                    if 'pretext_projects' not in projdata.keys():
                        projdata['pretext_projects'] = {}
                    if not is_present(rel, projdata['pretext_projects']):
                        projdata['pretext_projects'].update({rel: {"path": absol, "name": rel, "root_file": ""}})
            elif add_q == sublime.DIALOG_CANCEL:
                sublime.message_dialog("No projects added.")
                return
            elif add_q == sublime.DIALOG_NO:
                for rel, absol in projli:
                    add = sublime.yes_no_cancel_dialog(
                        "OK to add {} to PreTeXtual management? Select No to proceed to next project.".format(rel))
                    if add == sublime.DIALOG_YES:
                        if 'pretext_projects' not in projdata.keys():
                            projdata['pretext_projects'] = {}
                        if not is_present(rel, projdata['pretext_projects']):
                            projdata['pretext_projects'].update({rel: {"path": absol, "name": rel, "root_file": ""}})
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

        if len(projlist) > 0:
            add_some_projects(add_all, projlist)

        self.window.set_project_data(projdata)
        if 'pretext_projects' in projdata.keys():
            pretext_projects = projdata['pretext_projects']
        else:
            pretext_projects = {}

        # print("About to set root files "
        #     + "with output_dict: {}".format(pretext_projects))

        # We need to ask one at a time or the input panels all
        # collide and we don't get to see the first n-1 of them.
        # Thanks to OdatNurd on the Sublime Text freenode chat
        # for this idea.
        # def set_root_file_keys(key_list, key_index, output_dict):
        #     print("srfk: {}, {}, {}".format(key_list, key_index, output_dict))
        #     key = key_list[key_index]
        #     self.window.show_input_panel("Enter full path to root "
        #         "file for project {}:".format(key),
        #         os.path.normpath(pretext_vagrant_root),
        #         lambda v: set_root_file_values(v, key_list, key_index,
        #             output_dict),
        #         None, None)

        # def set_root_file_values(key_value, key_list, key_index, output_dict):
        #     print("srfv: {}, {}, {}, {}".format(key_value, key_list, key_index, output_dict))
        #     key = key_list[key_index]
        #     output_dict[key].update({'root_file': os.path.normpath(key_value)})

        #     key_index += 1
        #     if key_index < len(key_list):
        #         set_root_file_keys(key_list, key_index, output_dict)
        #     else:
        #         print("Finished with: {}".format(output_dict))

        # # if 'pretext_projects' in projdata.keys():
        # if pretext_projects:
        #     set_root_files = sublime.ok_cancel_dialog("Set "
        #         "root files for the projects you just added?")

        #     if set_root_files:
        #         projnames = list(pretext_projects.keys())
        #         if projnames:
        #             set_root_file_keys(projnames, 0, pretext_projects)
        #         print("keys exhausted, new pretext_projects is {}".format(pretext_projects))
        #         projdata.update({'pretext_projects': pretext_projects})
        #         print("keys exhausted, new projdata is {}".format(projdata))
        #         self.window.set_project_data(projdata)
        #     else:
        #         sublime.message_dialog("No root files set. You can add these "
        #             "later in the user settings.")

        sublime.message_dialog("Make sure to check your User Settings"
            " and set root files for all the packages you have added."
            " Nothing will work unless you do this.")

        # projdata = self.window.project_data()
        usersettings = sublime.load_settings("Preferences.sublime-settings")
        if 'pretext_projects' in projdata.keys():
            print("updating user settings: setting 'pretext_projects' to {}".format(pretext_projects))
            usersettings.set('pretext_projects', pretext_projects)
            # usersettings.set('pretext_projects', projdata['pretext_projects'])
        else:
            usersettings.set('pretext_projects', {})
        sublime.save_settings("Preferences.sublime-settings")

        options = ["Install PreTeXt", "Install PreTeXt-lite",
            "Install PreTeXt-barebones", "Install PreTeXt-no-images"]

            # "A comprehensive kitchen-sink installation"
            # "Sufficient for most needs"
            # "If you only need HTML"
            # "For testing only, very limited"

        def on_done(n):
            self.acquire_vagrantfile(n, pretext_vagrant_root)

        if not pretext_vagrantfile_exists:
            sublime.message_dialog("Click OK to bring up a quick panel to select "
                "a PreTeXt installation. This step can take a long time, perhaps "
                "an hour or more. Be patient and do not worry if it seems like "
                "your system is hanging. Just watch and wait. If you don't know "
                "what you want, select PreTeXt-lite.")
            self.window.show_quick_panel(options, on_done)

        vagrantpath = get_setting('vagrantpath', r"C:\\HashiCorp\\Vagrant\\bin\\vagrant.exe")
        if vagrantpath:
            vp = get_setting('vagrant_path')
            settings = sublime.load_settings("Preferences.sublime-settings")
            settings.set('vagrant_path', vagrantpath)
            sublime.save_settings("Preferences.sublime-settings")

        # sublime.message_dialog("The next step you must do yourself; the "
        #     "Sublime Text application can't do this for you (yet?). IT IS "
        #     "VERY IMPORTANT AND NOTHING WILL WORK WITHOUT IT.")

        # sublime.message_dialog("Choose Project/Save Project As... from the "
        #     "Sublime Text menu. Enter a filename in which to save your "
        #     "\"project settings\". Don't worry too much about what this means "
        #     "exactly right now; it's a way for Sublime Text to manage your "
        #     "writing projects and save your preferences between editing "
        #     "sessions.")
