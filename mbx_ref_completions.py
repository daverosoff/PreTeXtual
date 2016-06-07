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

from __future__ import print_function 
import sublime, sublime_plugin

if sublime.version() < '3000':
    # we are on ST2 and Python 2.X
    _ST3 = False
    # import getTeXRoot
    # from latextools_utils.is_tex_file import is_tex_file, get_tex_extensions
    # from latextools_utils import get_setting
else:
    _ST3 = True   
    # from . import getTeXRoot
    # from .latextools_utils.is_tex_file import is_tex_file, get_tex_extensions
    # from .latextools_utils import get_setting

import os, os.path, sys
import re
import codecs

if sys.version_info < (3, 0):
    strbase = basestring
else:
    strbase = str

try:
    from is_mbx_file import is_mbx_file
except ImportError:
    from .is_mbx_file import is_mbx_file

def get_setting(setting, default=None):
    global_settings = sublime.load_settings('MBXTools.sublime-settings')

    try:
        result = sublime.active_window().active_view().settings().get(setting)
    except AttributeError:
        # no view defined
        result = None

    if result is None:
        result = global_settings.get(setting, default)

    if result is None:
        result = default
    
    # if isinstance(result, sublime.Settings) or isinstance(result, dict):
    #     result = SettingsWrapper(setting, result)

    return result


# def is_mbx_file(file_name):
#     if not isinstance(file_name, strbase):
#         raise TypeError('file_name must be a string')

#     mbx_file_exts = ['.mbx', '.xml']
#     for ext in mbx_file_exts:
#         if file_name.lower().endswith(ext):
#             return True
#     return False

class UnrecognizedRefFormatError(Exception): pass

# _ref_special_commands = "|".join(["", "eq", "page", "v", "V", "auto", "name", "c", "C", "cpage"])[::-1]

# OLD_STYLE_REF_REGEX = re.compile(r"([^_]*_)?(p)?fer(" + _ref_special_commands + r")?(?:\\|\b)")
# NEW_STYLE_REF_REGEX = re.compile(r"([^{}]*)\{fer(" + _ref_special_commands + r")?\\(\()?")
# REF_REGEX = re.compile(r'<\s*xref\s*ref\s*=\s*[\'"]([A-Za-z][A-Za-z0-9_-]*)[\'"]\s*/>')
# REF_REGEX = re.compile(r'<\s*xref\s+ref\s*=\s*[\'"]')
REF_REGEX = re.compile(r'[\'"]\s*=\s*(?:lanoisivorp|fer)(?:.*)\s+ferx<')
# forward: <xref\s+(?:(?:ref|provisional|autoname|detail|first|last)\s*=\s*(['"])([^'"]+)\1\s*)*\s*/>
def match(rex, str):
    m = rex.search(str)
    if m:
        return m.group(0)
    else:
        return None


# recursively search all linked mbx files to find all
# included <... xml:id=""> attrs in the document and extract
def find_xmlids_in_files(rootdir, src, xmlids):
    if not is_mbx_file(src):
        src_mbx_file = None
        for ext in get_mbx_extensions():
            src_mbx_file = ''.join((src, ext))
            if os.path.exists(os.path.join(rootdir, src_mbx_file)):
                src = src_mbx_file
                break
        if src != src_mbx_file:
            print("Could not find file {0}".format(src))
            return

    file_path = os.path.normpath(os.path.join(rootdir, src))
    print ("Searching file: " + repr(file_path))
    # The following was a mistake:
    #dir_name = os.path.dirname(file_path)
    # THe reason is that \input and \include reference files **from the directory
    # of the master file**. So we must keep passing that (in rootdir).

    # read src file and extract all label tags

    # We open with utf-8 by default. If you use a different encoding, too bad.
    # If we really wanted to be safe, we would read until \begin{document},
    # then stop. Hopefully we wouldn't encounter any non-ASCII chars there. 
    # But for now do the dumb thing.
    try:
        src_file = codecs.open(file_path, "r", "UTF-8")
    except IOError:
        sublime.status_message("MBXTools WARNING: cannot find included file " + file_path)
        print ("WARNING! I can't find it! Check your xi:include's." )
        return

    src_content = re.sub("%.*", "", src_file.read())
    src_file.close()

    # If the file uses inputenc with a DIFFERENT encoding, try re-opening
    # This is still not ideal because we may still fail to decode properly, but still... 
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

    # labels += re.findall(r'\\label\{([^{}]+)\}', src_content)
    xmlids += re.findall(r'<\s*([A-Za-z][A-Za-z0-9_-]*)\s+xml:id\s*=\s*"([A-Za-z][A-Za-z0-9_-]*)"\s*>', src_content)

    # search through input tex files recursively
    # for f in re.findall(r'\\(?:input|include)\{([^\{\}]+)\}', src_content):
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

    # if expr:
    #     # Do not match on plain "ref" when autocompleting,
    #     # in case the user is typing something else
    #     # if autocompleting and re.match(r"p?fer(?:" + _ref_special_commands + r")?\\?", expr):
    #     # if autocompleting and re.match(r"ref\s*=\s*['\"]", expr):
    #     #     raise UnrecognizedRefFormatError()
    #     # Return the matched bits, for mangling
    #     prefix, has_p, special_command = rex.match(expr).groups()
    #     preformatted = False
    #     if prefix:
    #         prefix = prefix[::-1]   # reverse
    #         prefix = prefix[1:]     # chop off "_"
    #     else:
    #         prefix = ""
    #     #print prefix, has_p, special_command

    # else:
    #     # Check to see if the location matches a preformatted "\ref{blah"
    # rex = REF_REGEX
    # expr = match(rex, line)

    if not expr:
        raise UnrecognizedRefFormatError()

    # preformatted = True
    # # Return the matched bits (barely needed, in this case)
    # prefix, special_command, has_p = rex.match(expr).groups()
    prefix = rex.match(expr).group(0)
    if prefix:
        prefix = prefix[::-1]   # reverse
    else:
        prefix = ""
    # #print prefix, has_p, special_command

    # pre_snippet = "\\" + special_command[::-1] + "ref{"
    # post_snippet = "}"

    # prefix = rex.match(expr).group(0)
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


    # If we captured a parenthesis, we need to put it back in
    # However, if the user had paren automatching, we don't want to add
    # another one. So by default we don't, unless the user tells us to
    # in the settings.
    # (HACKISH: I don't actually remember why we matched the initial paren!)
    # if has_p:
    #     pre_snippet = "(" + pre_snippet
    #     add_paren = get_setting("ref_add_parenthesis", False)
    #     if add_paren:
    #         post_snippet = post_snippet + ")"

    # if not preformatted:
    #     # Replace ref_blah with \ref{blah
    #     # The "latex_tools_replace" command is defined in latex_ref_cite_completions.py
    #     view.run_command("latex_tools_replace", {"a": point-len(expr), "b": point, "replacement": pre_snippet + prefix})
    #     # save prefix begin and endpoints points
    #     new_point_a = point - len(expr) + len(pre_snippet)
    #     new_point_b = new_point_a + len(prefix)
    #     view.end_edit(ed)

    # else:
        # Don't include post_snippet if it's already present
    # suffix = view.substr(sublime.Region(point, point + len(post_snippet)))
    new_point_a = point - len(prefix)
    new_point_b = point
    # if post_snippet == suffix:
    #     post_snippet = "\""

    completions = []
    # Check the file buffer first:
    #    1) in case there are unsaved changes
    #    2) if this file is unnamed and unsaved, get_tex_root will fail
    # view.find_all(r'\\label\{([^\{\}]+)\}', 0, '\\1', completions)
    view.find_all(r'<\s*([A-Za-z][A-Za-z0-9_-]*)\s+xml:id\s*=\s*"([A-Za-z][A-Za-z0-9_-]*)"\s*>', 0, '\\1 : \\2', completions)

    root = view.settings().get("mbx_root_file")
    if root and not root == view.file_name():
        print ("MBX root: " + repr(root))
        find_xmlids_in_files(os.path.dirname(root), root, completions)

    # remove duplicates
    completions = list(set(completions))

    return completions, prefix, post_snippet, new_point_a, new_point_b


# Based on html_completions.py
#
# It expands references; activated by 
# ref<tab>
# refp<tab> [this adds parentheses around the ref]
# eqref<tab> [obvious]
#
# Furthermore, you can "pre-filter" the completions: e.g. use
#
# ref_sec
#
# to select all labels starting with "sec". 
#
# There is only one problem: if you have a label "sec:intro", for instance,
# doing "ref_sec:" will find it correctly, but when you insert it, this will be done
# right after the ":", so the "ref_sec:" won't go away. The problem is that ":" is a
# word boundary. Then again, TextMate has similar limitations :-)


# ST3 cannot use an edit object after the TextCommand has returned; and on_done gets 
# called after TextCommand has returned. Thus, we need this work-around (works on ST2, too)
# Used by both cite and ref completion
class MbxToolsReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, a, b, replacement):
        #print("DEBUG: types of a and b are " + repr(type(a)) + " and " + repr(type(b)))
        # On ST2, a and b are passed as long, but received as floats
        # It's probably a bug. Convert to be safe.
        if _ST3:
            region = sublime.Region(a, b)
        else:
            region = sublime.Region(long(a), long(b))
        self.view.replace(edit, region, replacement)


class MbxRefCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MBX xref
        if not view.match_selector(locations[0],
                "tag.reference.internal.xml.mbx"):
            return []

        point = locations[0]

        try:
            completions, prefix, post_snippet, new_point_a, new_point_b = get_ref_completions(view, point, autocompleting=True)
        except UnrecognizedRefFormatError:
            return []

        # r = [(label + "\t\\ref{}", label + post_snippet) for label in completions]
        r = [(label, label + post_snippet) for label in completions]
        #print r
        return (r, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)


### Ref completions using the quick panel

class MbxRefCommand(sublime_plugin.TextCommand):

    # Remember that this gets passed an edit object
    def run(self, edit):
        # get view and location of first selection, which we expect to be just the cursor position
        view = self.view
        point = view.sel()[0].b
        print (point)
        # Only trigger within LaTeX
        # Note using score_selector rather than match_selector
        if not view.score_selector(point,
                "text.xml.mbx"):
            return

        try:
            completions, prefix, post_snippet, new_point_a, new_point_b = get_ref_completions(view, point)
        except UnrecognizedRefFormatError:
            sublime.error_message("Not a recognized format for reference completion")
            return

        # filter! Note matching is "less fuzzy" than ST2. Room for improvement...
        # completions = [c for c in completions if prefix in c]

        if not completions:
            sublime.error_message("No label matches %s !" % (prefix,))
            return

        # Note we now generate refs on the fly. Less copying of vectors! Win!
        def on_done(i):
            print ("mbx_ref_completion called with index %d" % (i,))
            
            # Allow user to cancel
            if i<0:
                return

            refname = re.search(r' : (.*)$', completions[i]).group(1)   

            ref = prefix + refname + post_snippet
            
            # Replace ref expression with reference and possibly post_snippet
            # The "latex_tools_replace" command is defined in latex_ref_cite_completions.py
            view.run_command("mbx_tools_replace", {"a": new_point_a, "b": new_point_b, "replacement": ref})
            # Unselect the replaced region and leave the caret at the end
            caret = view.sel()[0].b
            view.sel().subtract(view.sel()[0])
            view.sel().add(sublime.Region(caret, caret))

        print(repr(completions))
        view.window().show_quick_panel(completions, on_done)

class MbxRefCiteCommand(sublime_plugin.TextCommand):

    # Remember that this gets passed an edit object
    def run(self, edit, insert_char=""):
        # get view and location of first selection, which we expect to be just the cursor position
        view = self.view
        point = view.sel()[0].b
        print (point)
        # Only trigger within MBX
        # Note using score_selector rather than match_selector
        if not view.score_selector(point, "text.xml.mbx"):
            return

        if insert_char:
            point += len(insert_char)
            # insert the char to every selection
            for sel in view.sel():
                view.insert(edit, sel.b, insert_char)
            # Get prefs and toggles to see if we are auto-triggering
            # This is only the case if we also must insert , or {, so we don't need a separate arg
            do_ref = get_setting('ref_auto_trigger', True)
            do_cite = get_setting('cite_auto_trigger', True)
        else: # if we didn't autotrigger, we must surely run
            do_ref = True
            do_cite = True

        print (do_ref, do_cite)

        # Get the contents of the current line, from the beginning of the line to
        # the current point
        line = view.substr(sublime.Region(view.line(point).a, point))
        # print line

        # Reverse
        line = line[::-1]


        # if re.match(OLD_STYLE_REF_REGEX, line) or re.match(NEW_STYLE_REF_REGEX, line):
        if re.match(REF_REGEX, line):
            if do_ref:
                print ("Dispatching ref")
                view.run_command("mbx_ref")
            else:
                pass # Don't do anything if we match ref completion but we turned it off
        # elif re.match(OLD_STYLE_CITE_REGEX, line) or re.match(NEW_STYLE_CITE_REGEX, line):
        #     if do_cite:
        #         print ("Dispatching cite")
        #         view.run_command("latex_cite")
        #     else:
        #         pass # ditto for cite
        else: # here we match nothing, so error out regardless of autotrigger settings
            print(repr(REF_REGEX.pattern))
            print(line)
            sublime.error_message("Ref/cite: unrecognized format.")
            return
