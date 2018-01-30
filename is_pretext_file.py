# Copyright 2016-2018 David W. Rosoff

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

def get_pretext_extensions():
    # view = sublime.active_window().active_view()
    # You can change settings in Packages/User/MBXTools
    # Default is that only .mbx, .ptx files are recognized by extension
    # so other .xml files will be ignored
    pretext_file_exts = get_setting('pretext_file_exts', ['.ptx', '.mbx'])

    return [s.lower() for s in set(pretext_file_exts)]

def is_pretext_file(file_name):
    if not isinstance(file_name, strbase):
        raise TypeError('file_name must be a string')

    pretext_file_exts = get_pretext_extensions()
    for ext in pretext_file_exts:
        if file_name.lower().endswith(ext):
            return True
    return False
