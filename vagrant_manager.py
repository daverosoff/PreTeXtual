# Copyright 2016-2019 David W. Rosoff

# This file is part of PreTeXtual, a package for Sublime Text.

# PreTeXtual is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PreTeXtual is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PreTeXtual.  If not, see <http://www.gnu.org/licenses/>.

import sublime
import sublime_plugin
import subprocess
from .get_setting import get_setting
import os, re

from .beta_process import to_vagrant, from_vagrant

class VagrantSettings(sublime.Settings):
    def set_vagrant_path(self, vagrant_path):
        self.set("vagrant_path", vagrant_path)


class AddVagrantManagedProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        data = sublime.load_settings('Vagrant.sublime-settings')
        new_project = {
            'project_root_file': "",
            'project_html_output': "",
            'project_latex_output': "",
            'project_images': ""
        }
        if not data.has('vagrant_managed_projects'):
            pass
            
class TestVagrantManagerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        add = VagrantSettings()
        add.set('vagrantfile_path', "C:/PreTeXt")
        add.set('pretext_path', "C:/PreTeXt/mathbook")
        add.set('vagrant_managed_projects', [
            "C:/PreTeXt/gfa",
            "C:/PreTeXt/MAT101AlgebraProbability",
            "C:/PreTeXt/minimal",
            "C:/PreTeXt/sabbatical-2016",
        ])
