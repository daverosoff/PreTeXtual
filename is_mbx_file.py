import sublime
import sys

# try:
#     from latextools_utils import get_setting
# except:
#     from .settings import get_setting

if sys.version_info < (3, 0):
    strbase = basestring
else:
    strbase = str

def get_mbx_extensions():
    # view = sublime.active_window().active_view()
    # tex_file_exts = get_setting('tex_file_exts', ['.tex'])

    return ['mbx']
    # return [s.lower() for s in set(tex_file_exts)]

def is_mbx_file(file_name):
    if not isinstance(file_name, strbase):
        raise TypeError('file_name must be a string')

    mbx_file_exts = get_mbx_extensions()
    for ext in mbx_file_exts:
        if file_name.lower().endswith(ext):
            return True
    return False
