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
