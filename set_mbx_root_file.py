# Copyright 2016 David W. Rosoff

# This file is part of MBXTools, a package for Sublime Text.

# MBXTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MBXTools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with MBXTools.  If not, see <http://www.gnu.org/licenses/>.

import sublime
import sublime_plugin

try:
    from .get_setting import get_setting
except ImportError:
    from get_setting import get_setting

class SetMbxRootFileCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        window = self.window
        # view = self.active_view()
        # project = window.project_file_name()

        def load_settings(self):
            return sublime.load_settings('Preferences.sublime-settings')

        def set_user_prefs(filename):
            if window.project_file_name():
                data = window.project_data()
                if 'settings' not in data:
                    data['settings'] = {'mbx_root_file': filename}
                else:
                    data['settings'].update({'mbx_root_file': filename})
                window.set_project_data(data)
            else: # fall back on user prefs
                plugin_settings = sublime.load_settings('Preferences.sublime-settings')
                plugin_settings.set('mbx_root_file', filename)
                sublime.save_settings('Preferences.sublime-settings')
            sublime.status_message('MBX root file: ' + filename)

        def on_done(filename):
            set_user_prefs(filename)

        if 'filename' in kwargs:
            set_user_prefs(kwargs['filename'])
        else:
            current_root = get_setting('mbx_root_file')
            if current_root:
                window.show_input_panel("Absolute path to root MBX file:",
                    current_root, on_done, None, None)
            else:
                window.show_input_panel("Absolute path to root MBX file:",
                    "", on_done, None, None)

