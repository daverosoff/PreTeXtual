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

from __future__ import print_function
import sublime, sublime_plugin

if sublime.version() < '3000':
    _ST3 = False
else:
    _ST3 = True

import os, os.path, sys
import re
import codecs

if sys.version_info < (3, 0):
    strbase = basestring
else:
    strbase = str

try:
    from is_pretext_file import is_pretext_file
    from is_pretext_file import get_pretext_extensions
    from get_setting import get_setting
except ImportError:
    from .is_pretext_file import is_pretext_file
    from .is_pretext_file import get_pretext_extensions
    from .get_setting import get_setting

class UnrecognizedRefFormatError(Exception): pass

REF_REGEX = re.compile(r'[\'"]\s*=\s*(?:fer)(?:.*)\s+ferx<')
# forward: <xref\s+(?:(?:ref|provisional|autoname|detail|first|last)\s*=\s*(['"])([^'"]+)\1\s*)*\s*/>
COMPLETED_REF_REGEX = re.compile(r'([\'"])(?:[^\'"]+)\1\s*=\s*(?:fer)(?:.*)\s+ferx<')
# forward: <xref\s+(?:.*)(?:ref)\s*=\s*(['"])(?:[^'"]+)\1)
def match(rex, str):
    m = rex.search(str)
    if m:
        return m.group(0)
    else:
        return None

# recursively search all linked files to find all
# included <... xml:id=""> attrs in the document and extract
def find_xmlids_in_files(rootdir, src, xmlids):
    if not is_pretext_file(src):
        src_pretext_file = None
        for ext in get_pretext_extensions():
            src_pretext_file = ''.join((src, ext))
            if os.path.exists(os.path.join(rootdir, src_pretext_file)):
                src = src_pretext_file
                break
        if src != src_pretext_file:
            print("Could not find file {0}".format(src))
            return

    file_path = os.path.normpath(os.path.join(rootdir, src))
    print ("Searching file: " + repr(file_path))

    # read src file and extract all xml:id attributes

    # We open with utf-8 by default. If you use a different encoding, too bad.
    try:
        src_file = codecs.open(file_path, "r", "UTF-8")
    except IOError:
        sublime.status_message("PreTeXtual WARNING: cannot find included file " + file_path)
        print ("WARNING! I can't find it! Check your xi:include's." )
        return

    # src_content = re.sub("%.*", "", src_file.read())
    src_content = src_file.read()
    src_file.close()

    m = re.search(r"<\?xml.*encoding=\"([^\"]*)\"", src_content)
    if m and (m.group(1) not in ["utf8", "UTF-8", "utf-8"]):
        print("reopening with encoding " + m.group(1))
        f = None
        try:
            f = codecs.open(file_path, "r", m.group(1))
            src_content = re.sub("%.*", "", f.read())
        except:
            print("Uh-oh, could not read file " + file_path + " with encoding " + m.group(1))
        finally:
            if f and not f.closed:
                f.close()

    xmlids += re.findall(r'<\s*([A-Za-z][A-Za-z0-9_-]*)\s+xml:id\s*=\s*"([A-Za-z][A-Za-z0-9_-]*)"\s*>', src_content)

    for f in re.findall(r'<\s*xi:include\s*href\s*=\s*"([^"]+)"', src_content):
        find_xmlids_in_files(rootdir, f, xmlids)


# get_ref_completions forms the guts of the parsing shared by both the
# autocomplete plugin and the quick panel command
def get_ref_completions(view, point, autocompleting=False):
    # Get contents of line from start up to point and from point to the end
    line = view.substr(sublime.Region(view.line(point).a, point))
    rest = view.substr(sublime.Region(point, view.line(point).b))
    # print line

    # Reverse, to simulate having the regex
    # match backwards (cool trick jps btw!)
    line = line[::-1]
    # the point of the trick is that the user has just typed the
    # ref string, so the cursor is at the end of it. This allows us to
    # use a simpler regex and re.match instead of re.search

    # Check the first location looks like a ref, but backward
    # dwr: not backward
    rex = REF_REGEX
    expr = match(rex, line)
    # print(expr)

    if not expr:
        raise UnrecognizedRefFormatError()

    prefix = rex.match(expr).group(0)
    if prefix:
        prefix = prefix[::-1]   # reverse
    else:
        prefix = ""

    pre_snippet = "<xref ref=\""
    post_snippet_rex = re.compile(r"\"\s*/>")
    post_snippet_rex_noquo = re.compile(r"\s*/>")
    post_expr = match(post_snippet_rex, rest)
    post_expr_noquo = match(post_snippet_rex_noquo, rest)
    if not post_expr:
        if len(rest) > 0 and rest[0] == "\"":
            post_snippet = " />"
        elif post_expr_noquo:
            post_snippet = "\""
        else:
            post_snippet = "\" />"
    else:
        post_snippet = ""

    new_point_a = point - len(prefix)
    new_point_b = point

    completions = []
    # Check the file buffer first:
    #    1) in case there are unsaved changes
    #    2) if this file is unnamed and unsaved, get_tex_root will fail
    view.find_all(r'<\s*([A-Za-z][A-Za-z0-9_\-]*)\s+xml:id\s*=\s*"([A-Za-z][A-Za-z0-9_\-]*)"\s*>', 0, '\\1: \\2', completions)

    root = get_setting('pretext_root_file')
    print ("PreTeXt root: " + repr(root))
    if root and not root == view.file_name():
        find_xmlids_in_files(os.path.dirname(root), root, completions)
    # else:
    #     find_xmlids_in_files(os.path.dirname(view), os.path.basename(view), completions)
    # remove duplicates
    completions = list(set(completions))
    # this screws up the list for some reason?
    # fixed with a wretched hack
    tuple = type((1,2,3))
    completions = [": ".join(c) if type(c) is tuple else c for c in completions]
    print(repr(completions))
    # raise RuntimeError

    return completions, prefix, post_snippet, new_point_a, new_point_b

# ST3 cannot use an edit object after the TextCommand has returned; and on_done gets
# called after TextCommand has returned. Thus, we need this work-around (works on ST2, too)
# Used by both cite and ref completion
class PretextToolsReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, a, b, replacement):
        #print("DEBUG: types of a and b are " + repr(type(a)) + " and " + repr(type(b)))
        # On ST2, a and b are passed as long, but received as floats
        # It's probably a bug. Convert to be safe.
        if _ST3:
            region = sublime.Region(a, b)
        else:
            region = sublime.Region(long(a), long(b))
        self.view.replace(edit, region, replacement)


class PretextRefCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        # Only trigger within xref
        if not view.match_selector(locations[0],
                "markup.other.reference.xref.pretext"):
            return []

        point = locations[0]

        try:
            completions, prefix, post_snippet, new_point_a, new_point_b = get_ref_completions(view, point, autocompleting=True)
        except UnrecognizedRefFormatError:
            return []

        r = [(label + post_snippet) for label in completions]
        print(r)
        return (r, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

### Ref completions using the quick panel

class PretextRefCommand(sublime_plugin.TextCommand):

    # Remember that this gets passed an edit object
    def run(self, edit):
        # get view and location of first selection, which we expect to be just the cursor position
        view = self.view
        point = view.sel()[0].b
        print (point)
        # Only trigger within PreTeXt
        # Note using score_selector rather than match_selector
        if not view.score_selector(point,
                "text.xml.pretext"):
            return

        try:
            completions, prefix, post_snippet, new_point_a, new_point_b = get_ref_completions(view, point)
        except UnrecognizedRefFormatError:
            sublime.error_message("Not a recognized format for reference completion")
            return

        # filter! Note matching is "less fuzzy" than ST2. Room for improvement...
        completions = [c for c in completions if prefix in c]

        if not completions:
            sublime.error_message("No label matches %s !" % (prefix,))
            return

        # Note we now generate refs on the fly. Less copying of vectors! Win!
        def on_done(i):
            print ("pretext_ref_completion called with index %d" % (i,))

            # Allow user to cancel
            if i<0:
                return

            refname = re.search(r': (.*)$', completions[i]).group(1)

            ref = prefix + refname + post_snippet

            # Replace ref expression with reference and possibly post_snippet
            # The "latex_tools_replace" command is defined in latex_ref_cite_completions.py
            view.run_command("pretext_tools_replace", {"a": new_point_a, "b": new_point_b, "replacement": ref})
            # Unselect the replaced region and leave the caret at the end
            caret = view.sel()[0].b
            view.sel().subtract(view.sel()[0])
            view.sel().add(sublime.Region(caret, caret))

        print(repr(completions))
        view.window().show_quick_panel(completions, on_done)

class PretextRefCiteCommand(sublime_plugin.TextCommand):

    # Remember that this gets passed an edit object
    def run(self, edit, insert_char=""):
        # get view and location of first selection, which we expect to be just the cursor position
        view = self.view
        point = view.sel()[0].b
        print (point)
        # Only trigger within PreTeXt
        # Note using score_selector rather than match_selector
        if not view.score_selector(point, "text.xml.pretext"):
            return

        if insert_char:
            point += len(insert_char)
            # insert the char to every selection
            for sel in view.sel():
                view.insert(edit, sel.b, insert_char)
            # Get prefs and toggles to see if we are auto-triggering
            # This is only the case if we also must insert , or {, so we don't need a separate arg
            do_ref = get_setting('ref_auto_trigger', True)
        else: # if we didn't autotrigger, we must surely run
            do_ref = True

        print (do_ref)

        # Get the contents of the current line, from the beginning of the line to
        # the current point
        line = view.substr(sublime.Region(view.line(point).a, point))
        # print line

        # Reverse
        line = line[::-1]

        if re.match(REF_REGEX, line):
            if do_ref:
                print ("Dispatching ref")
                view.run_command("pretext_ref")
            else:
                pass # Don't do anything if we match ref completion but we turned it off
        elif re.search(COMPLETED_REF_REGEX, line):
            pass # Don't do anything if the ref is actually complete already
        else: # here we match nothing, so error out regardless of autotrigger settings
            print(repr(REF_REGEX.pattern))
            print(line)
            sublime.error_message("Ref/cite: unrecognized format.")
            return
