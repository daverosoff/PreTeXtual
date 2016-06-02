<!-- Copyright 2016 David W. Rosoff -->

<!-- This file is part of MBXTools, a package for Sublime Text. -->

<!-- MBXTools is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->

<!-- MBXTools is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU General Public License for more details. -->

<!-- You should have received a copy of the GNU General Public License -->
<!-- along with MBXTools.  If not, see <http://www.gnu.org/licenses/>. -->

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
(yet?). If your MBX files end with `.xml`, you will need to enable the syntax
manually using the command palette. Open an MBX file and press `Ctrl+Shift+P`
(`Cmd+Shift+P` on OS X) and type `mbx`. Select `Set Syntax: MathBook XML` from
the list of options. 

You should see the text `MathBook XML` in the lower right corner if you have
the status bar visible (command palette: Toggle Status Bar).

![Image of status bar showing MathBook XML active](media/mbx-syntax-active.png)

There are only a few features implemented so far. 

1. If you have some sectioning in your MBX file, hit `Ctrl-R` (`Cmd-R` on OS X)
    to run the Go To Anything command. You should see a panel showing all your
    available sections. 

![Image of quick panel showing sections](media/quickpanel-sections.png)

2. If you have been using `@xml:id` to label your stuff, try typing `<xref
   ref="` (the beginning of a cross-reference). Sublime Text should show you a
   panel containing all xml:id values along with the elements they go with.
   Choose one to insert it at the caret and close the `xref` tag.
   Alternatively, type `ref` and hit `Tab` to activate the `xref` snippet. Then
   hit `Ctrl+l` followed by `x` or `Ctrl+l` followed by `Ctrl+Space` to bring
   up the completions menu.

![Image of quick panel showing xml id values](media/quickpanel-xrefs.png)

### Known issues

* Syntax highlighting is not always consistent.
* The `ref` snippet does not bring up the quick panel. Should it?
* Recursive search through included files for labels is not yet implemented.
  This will only work for xref completion, not Go To Anything.
* Nothing has been tested on OS X or Linux.
