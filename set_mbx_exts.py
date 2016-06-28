import sublime
import sublime_plugin
import re

try:
    from .get_setting import get_setting
except:
    from get_setting import get_setting

class SetMbxExtsCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        window = self.window
        
        def load_settings(self):
            return sublime.load_settings('Preferences.sublime-settings')

        def li_to_str(exts_list):
            return ", ".join(exts_list)

        def str_to_li(exts):
            sep = re.compile(r',? *')
            print("exts is " + repr(exts))
            return sep.split(exts)

        def set_user_prefs(exts_list):
            if type(exts_list) is not type([]):
                raise ValueError("exts must be a list")
            exts_pretty = li_to_str(exts_list)
            if window.project_file_name():
                data = window.project_data()
                if 'settings' not in data:
                    data['settings'] = {'mbx_file_exts': exts_list}
                else:
                    data['settings'].update({'mbx_file_exts': exts_list})
                window.set_project_data(data)
            else: # fall back on user prefs
                plugin_settings = sublime.load_settings('Preferences.sublime-settings')
                plugin_settings.set('mbx_file_exts', exts_list)
                sublime.save_settings('Preferences.sublime-settings')
            sublime.status_message('MBX file extensions: ' + exts_pretty)

        def on_done(exts):
            set_user_prefs(str_to_li(exts))

        if 'exts' in kwargs:
            set_user_prefs(kwargs['exts'])
        else:
            current_exts = get_setting('mbx_file_exts')
            if current_exts:
                window.show_input_panel("Extensions for MBXTools to recognize:",
                    li_to_str(current_exts), on_done, None, None)
            else:
                window.show_input_panel("Extensions for MBXTools to recognize:",
                    "", on_done, None, None)


