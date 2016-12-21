# Copyright 2016-17 David W. Rosoff

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

try:
    from .get_setting import get_setting
except:
    from get_setting import get_setting

if sys.version_info < (3, 0):
    strbase = basestring
else:
    strbase = str

def get_mbx_extensions():
    # view = sublime.active_window().active_view()
    # You can change settings in Packages/User/MBXTools
    # Default is that only .mbx files are recognized by extension
    # so other .xml files will be ignored unless they carry
    # the <!-- MBX --> magic comment in line 1
    mbx_file_exts = get_setting('mbx_file_exts', ['.mbx'])

    # return ['mbx']
    return [s.lower() for s in set(mbx_file_exts)]

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
    try:
        mbx_ident = re.compile("<!--\s*MBX\s*-->")
    except TypeError:
        print("MEH!")
    if mbx_ident.search(line):
        return True
    return False
