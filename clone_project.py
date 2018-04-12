import sublime
import sublime_plugin
import subprocess

class CloneProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # self.view.insert(edit, 0, "Hello, World!")
        win = sublime.active_window()
        print("Yes!")
        vu = self.view
        win = vu.window()
        # win.show_input_panel("Enter a URL to clone from:", "https://github.com/", lambda st: subprocess.call(["git", "clone", st]), None, None)
        win.show_input_panel(
            "Enter a URL to clone from:",
            "https://github.com/",
            lambda st: subprocess.call(["git", "clone", st, win.folders()[0] + "/" + st.split("/")[-1].split(".")[0]]),
            # lambda st: print(win.folders()[0] + "/" + st.split("/")[-1].split(".")[0]),
            # self.clone_url_and_add_to_project,
            None,
            None
        )
