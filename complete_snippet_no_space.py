import sublime
import sublime_plugin
import re


if sublime.version() < '3000':
    _ST3 = False
else:
    _ST3 = True

# try:
#     from .mbx_ref_completions import MbxToolsReplaceCommand
# except ImportError:
#     from mbx_ref_completions import MbxToolsReplaceCommand

# class MbxToolsReplaceCommand(sublime_plugin.TextCommand):
#     def run(self, edit, a, b, replacement):
#         #print("DEBUG: types of a and b are " + repr(type(a)) + " and " + repr(type(b)))
#         # On ST2, a and b are passed as long, but received as floats
#         # It's probably a bug. Convert to be safe.
#         if _ST3:
#             region = sublime.Region(a, b)
#         else:
#             region = sublime.Region(long(a), long(b))
#         self.view.replace(edit, region, replacement)

class CompleteSnippetNoSpaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        triggermap = {
            "amp": "<ampersand />",
            "ell": "<ellipsis />",
            "md": "<mdash />",
            "nd": "<ndash />",
            "pct": "<percent />",
            "ptx": "<pretext />",
        }
        # print("YES!!")
        view = self.view
        sels = view.sel()
        for s in sels:
            point = s.b
            word = view.word(s.b)
            content = view.substr(word)
            new_b = s.b
            for k, v in triggermap.items():
                if content.endswith(k):
                    print("content:" + content)
                    prefix = re.sub(k, '', content)
                    print("prefix:" + prefix)
                    new_a = new_b - len(k)
                    # new_a = point
                    region = sublime.Region(new_a, new_b)
                    # print("YES!")
                    view.replace(edit, region, v)
                    return

    # def is_enabled(a, b):
        # if _ST3:
        #     region = sublime.Region(a, b)
        # else:
        #     region = sublime.Region(long(a), long(b))
        # return True
