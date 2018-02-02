# Copyright 2016-18 David W. Rosoff

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
import re

if sublime.version() < '3000':
    _ST3 = False
else:
    _ST3 = True

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
