import sublime
import sublime_plugin
import subprocess

class CloneProjectCommand(sublime_plugin.TextCommand):
    # def clone_url_and_add_to_project(st):
    #     proj = st.split('/')[-1].split('.')[0]
    #     newfolder = 'C:\\Users\\drosoff\\pv\\' + proj
    #     pdata = win.project_data()
    #     if pdata['folders']:
    #         folders = pdata['folders']
    #         folders.append({'path': newfolder})
    #         pdata['folders'] = folders
    #     else:
    #         win.set_project_data(pdata)

    def run(self, edit):
        #self.view.insert(edit, 0, "Hello, World!")
        # win = sublime.active_window()
        vu = self.view
        win = vu.window()
        win.show_input_panel("Enter a URL to clone from:", "https://github.com/", lambda st: subprocess.call(["git", "clone", st]), None, None)
        # win.show_input_panel(
        #     "Enter a URL to clone from:",
        #     "https://github.com/",
        #     lambda st: subprocess.call(["git", "clone", st]),
        #     # self.clone_url_and_add_to_project,
        #     None,
        #     None
        # )
