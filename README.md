# MBXTools: a Sublime Text package for MathBook XML

MBXTools is a Sublime Text package designed to assist authors using
[MathBook XML](https://github.com/rbeezer/mathbook). It is very experimental
and may behave unexpectedly.

The package is inspired by the excellent
[LaTeXTools](https://github.com/SublimeText/LaTeXTools) package, which I have
enjoyed using for many years. I have borrowed very liberally from the
LaTeXTools codebase in order to implement the features I thought would be most
useful to MBX authors. Please let me know of any bugs you find or any features
you would like to include.

### Installation

I am not yet included in Package Control, so you must install via `git`. Change
directories into your `Packages` folder. To find the `Packages` folder, select Browse Packages from the Preferences menu (from the Sublime Text 3 menu on OS X). Make sure you are in the `Packages` folder and *not* `Packages/User`.

Then, run
```
git clone https://github.com/daverosoff/MBXTools.git
```
and restart Sublime Text (probably not necessary).

### Usage

You can activate the package features by enabling the MathBook XML syntax. The
syntax definition looks for `.mbx` file extensions, which most of us don't use
(yet?). If your MBX files end with `.xml`, you will either need to add a
comment to the first line of each file:
```
<!-- MBX -->
```
or you will need to enable the syntax manually using the command palette. To
enable it manually, open an MBX file and press `Ctrl+Shift+P` (`Cmd+Shift+P`
on OS X) and type `mbx`. Select `Set Syntax: MathBook XML` from the list of
options.

You should see the text `MathBook XML` in the lower right corner if you have
the status bar visible (command palette: Toggle Status Bar).

![Image of status bar showing MathBook XML active](media/mbx-syntax-active.png)

There are only a few features implemented so far.

1. If you have some sectioning in your MBX file, hit `Ctrl-R` (`Cmd-R` on OS X)
    to run the Go To Symbol command. You should see a panel showing all your
    available sections.

![Image of quick panel showing sections](media/quickpanel-sections.png)

2. If you have been using `@xml:id` to label your stuff, try typing `<xref
   ref="` (the beginning of a cross-reference). Sublime Text should show you a
   panel containing all xml:id values along with the elements they go with.
   Choose one to insert it at the caret and close the `xref` tag.
   Alternatively, type `ref` and hit `Tab` to activate the `xref` snippet. Then
   hit `Ctrl+l` followed by `x` or `Ctrl+l` followed by `Ctrl+Space` to bring
   up the completions menu. There are several variants of the `ref` snippet, namely `refa`, `refp`, and `refpa`.

![Image of quick panel showing xml id values](media/quickpanel-xrefs.png)

3. Type `chp`, `sec`, `ssec`, or `sssec` and hit `Tab` to activate the
   subdivision snippets. A blank `title` element is provided and the cursor positioned within it. As you type, the `@xml:id` field for the subdivision is filled with similar text mirroring the title you are entering.

### Known issues

* Syntax highlighting is not always consistent.
* The `ref` snippet does not bring up the quick panel. Should it?
* Recursive search through included files for labels is not yet implemented.
  This will only work for xref completion, not Go To Symbol.
* Nothing has been tested on OS X or Linux.
* When adding attributes other than ref to an xref element, errors are thrown.