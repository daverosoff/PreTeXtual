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
        # project = window.project_file_name()

        def load_settings(self):
            return sublime.load_settings('Preferences.sublime-settings')

        def set_user_prefs(filename):
            if window.project_file_name():
                data = window.project_data()
                if 'settings' not in data:
                    data['settings'] = {'pretext_root_file': filename}
                else:
                    data['settings'].update({'pretext_root_file': filename})
                window.set_project_data(data)
            else: # fall back on user prefs
                plugin_settings = sublime.load_settings('Preferences.sublime-settings')
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

