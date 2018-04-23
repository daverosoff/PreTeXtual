# Copyright 2016-18 David W. Rosoff

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

try:
    from .get_setting import get_setting
except ImportError:
    from get_setting import get_setting

class SetPretextRootFileCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        window = self.window
        # view = self.active_view()
        project = window.project_file_name()

        def load_settings():
            return sublime.load_settings('Preferences.sublime-settings')

        def set_user_prefs(filename):
            if project:
                data = window.project_data()
                if 'settings' not in data:
                    data['settings'] = {'pretext_root_file': filename}
                else:
                    data['settings'].update({'pretext_root_file': filename})
                window.set_project_data(data)
            else: # fall back on user prefs
                plugin_settings = load_settings()
                plugin_settings.set('pretext_root_file', filename)
                sublime.save_settings('Preferences.sublime-settings')
            sublime.status_message('PreTeXt root file: ' + filename)

        def on_done(filename):
            set_user_prefs(filename)

        if 'filename' in kwargs:
            set_user_prefs(kwargs['filename'])
        else:
            current_root = get_setting('pretext_root_file')
            if current_root:
                window.show_input_panel("Absolute path to root PreTeXt file:",
                    current_root, on_done, None, None)
            else:
                window.show_input_panel("Absolute path to root PreTeXt file:",
                    "", on_done, None, None)

class ClearPretextRootFileCommand(SetPretextRootFileCommand):
    def run(self):
        SetPretextRootFileCommand.run(self, filename="")

class SetCurrentFileAsRootCommand(SetPretextRootFileCommand):
    def is_enabled(self):
        if self.window.active_view().file_name():
            return True
        return False

    def run(self):
        import re
        fn = self.window.active_view().file_name()
        SetPretextRootFileCommand.run(self, filename=re.sub(r"\\", '/', fn))
