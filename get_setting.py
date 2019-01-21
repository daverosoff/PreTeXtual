# Copyright 2016-2018 David W. Rosoff

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

def get_setting(setting, default=None):
    global_settings = sublime.load_settings('PreTeXtual.sublime-settings')

    try:
        result = sublime.active_window().active_view().settings().get(setting)
    except AttributeError:
        # no view defined
        result = None

    # if result is None:
    if not result:
        result = global_settings.get(setting, default)

    # if result is None:
    if not result:
        result = default

    # if isinstance(result, sublime.Settings) or isinstance(result, dict):
    #     result = SettingsWrapper(setting, result)

    return result
