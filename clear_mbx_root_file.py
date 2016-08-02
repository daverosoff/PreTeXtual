import sublime
import sublime_plugin

try:
    from .set_mbx_root_file import SetMbxRootFileCommand
except ImportError:
    from set_mbx_root_file import SetMbxRootFileCommand

class ClearMbxRootFileCommand(SetMbxRootFileCommand):

    def run(self):
        self.set_user_prefs("")
