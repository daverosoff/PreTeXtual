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

class CloneProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # self.view.insert(edit, 0, "Hello, World!")
        # win = sublime.active_window()
        vu = self.view
        win = vu.window()
        win.show_input_panel("Enter a URL to clone from:",
            "https://github.com/", lambda st: subprocess.call(["git", "clone",
            st, win.folders()[0] + "/" + st.split("/")[-1].split(".")[0]]),
            None, None
        )
