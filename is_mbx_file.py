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
import sys
import re

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
    view = sublime.active_window().active_view()
    first_line = sublime.Region(0,view.line(0).b)
    line = view.substr(first_line)
    rex = re.compile(r"<!-- MBX -->")
    if rex.search(line):
        return True
    return False
