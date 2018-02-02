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
import sublime_plugin

try:
    from is_pretext_file import is_pretext_file
except ImportError:
    from .is_pretext_file import is_pretext_file

PRETEXT_SYNTAX = 'Packages/MBXTools/PreTeXt.sublime-syntax'

class PretextSyntaxListener(sublime_plugin.EventListener):
    def on_load(self, view):
        self.detect_and_apply_syntax(view)

    def on_post_save(self, view):
        self.detect_and_apply_syntax(view)

    def detect_and_apply_syntax(self, view):
        if view.is_scratch() or not view.file_name():
            return

        file_name = view.file_name()
        if is_pretext_file(file_name):
            view.set_syntax_file(PRETEXT_SYNTAX)

        if view.score_selector(0, "text.xml.pretext"):
            return
