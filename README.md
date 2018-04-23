# PreTeXtual: a Sublime Text package for PreTeXt

PreTeXtual is a Sublime Text 3 package designed to assist authors using
[PreTeXt](https://github.com/rbeezer/mathbook) (formerly known as MathBook
XML). It is very experimental and may behave unexpectedly.

The package is inspired by the excellent
[LaTeXTools](https://github.com/SublimeText/LaTeXTools) package, which I have
enjoyed using for many years. I have borrowed very liberally from the
LaTeXTools codebase in order to implement the features I thought would be most
useful to MBX authors. Please let me know of any bugs you find or any features
you would like to include.

Support for Sublime Text 2 is limited and there are no plans to extend it.

### Installation

*Note: We assume you are familiar with running Sublime Text commands via the
Command Palette. To bring up the palette, hit <kbd>Ctrl+p</kbd>
(<kbd>Cmd+p</kbd> on OS X). Then start typing the name of the command you want
to filter the list of results.*

It is recommended to install PreTeXtual via Package Control. If you have not
installed Package Control yet, you should
[do that first](https://packagecontrol.io) (and restart Sublime Text afterward).

After Package Control is installed, use the `Install Package` command to
search for the PreTeXtual package, and select it from the Quick Panel to
install. This method of installation allows Package Control to automatically
update your installation and show you appropriate release notes.

You may also install PreTeXtual via `git`. Change directories into your
`Packages` folder. To find the `Packages` folder, select Browse Packages from
the Preferences menu (from the Sublime Text 3 menu on OS X). Make sure you are
in the `Packages` folder and *not* `Packages/User`.

Then, run
```
git clone https://github.com/daverosoff/PreTeXtual.git
```
and restart Sublime Text (probably not necessary).

### Keybindings

PreTeXtual is inspired by
[LaTeXTools](https://packagecontrol.io/packages/LaTeXTools), and like that
package uses a <kbd>Ctrl+l</kbd> prefix for many commands. The Expand Selection
to Line command is bound to <kbd>Ctrl+l</kbd> by default. PreTeXtual rebinds that
command to <kbd>Ctrl+l, Ctrl+l</kbd>. Note that this is a keyboard shortcut
consisting of two separate keystroke combinations. Most PreTeXtual shortcuts are
like this.

### Usage

You can activate the package features by enabling the PreTeXt syntax. The
syntax definition looks for `.ptx` or the legacy `.mbx` file extension. If
your MathBook XML files end with `.xml` (or something else), you have several
choices.

1. Use the Preferences menu or the Command Palette to run the command `Set
   PreTeXt File Extensions`, and use the input panel to add `.xml` or other
   extensions of your choice to the comma-separated list. Sublime will look
   for a project settings file first, then update user preferences if it
   doesn't find one. If you have multiple PreTeXt projects, or if you edit XML
   other than PreTeXt, it is best to start using Sublime Text projects so that
   you can have project-specific settings.

3. Enable the syntax manually using the command palette. To enable it
   manually, open a PreTeXt file and press <kbd>Ctrl+Shift+P</kbd>
   (<kbd>Cmd+Shift+P</kbd> on OS X) and type `ptx`. Select `Set Syntax:
   PreTeXt` from the list of options.

You should see the text `PreTeXt` in the lower right corner if you have
the status bar visible (command palette: Toggle Status Bar). Please excuse
the image which still shows the former name `MathBook XML`.

![Image of status bar showing MathBook XML active](media/mbx-syntax-active.png)

Here is a (non-exhaustive) list of features.

1. New in 0.6.0: an extensive interface with Vagrant virtual machine management
   software is included, to enable Sublime Text 3 to behave more like an API
   for PreTeXt. See the
   [PreTeXt Author's Guide](https://mathbook.pugetsound.edu/doc/author-guide/html/author-guide.html)
   for more information.

1. If you have some subdivisions (with `xml:id`) in your PreTeXt file, hit
   <kbd>Ctrl+R</kbd> (<kbd>Cmd+R</kbd> on OS X) to run the Goto Symbol command.
   You should see a panel showing all your available sections. Select one to
   jump to it in the active view. This tool does not index subdivisions without
   an `xml:id` attribute.

![Image of quick panel showing sections](media/quickpanel-sections.png)

2. Open your entire source folder as a project and use Goto Symbol in Project
   (<kbd>Ctrl+Shift+R</kbd>/<kbd>Cmd+Shift+R</kbd>) to see all the `xml:id`
   for all the MathBook XML files in the project (must use `.mbx` or `.ptx`
   extension for indexing to succeed).

3. If you have been using `xml:id` to label your stuff, try typing `<xref
   ref="` (the beginning of a cross-reference). Sublime Text should show you a
   panel containing all xml:id values along with the elements they go with.
   Choose one to insert it at the caret and close the `xref` tag.
   Alternatively, type `ref` and hit <kbd>Tab</kbd> to activate the `xref`
   snippet. Then hit <kbd>Ctrl+L, X</kbd> or <kbd>Ctrl+L, Ctrl+Space</kbd> to
   bring up the completions menu. There are several variants of the `ref`
   snippet, namely `refa`, `refp`, and `refpa`.

![Image of quick panel showing xml id values](media/quickpanel-xrefs.png)

4. If you set a PreTeXt root file, then ref completion as described above will
   recursively search for `xml:id` through all your `xi:includes` starting
   with the indicated root file. Run the command "Set PreTeXt Root File" from
   the Preferences menu or the Command Palette. Be sure to use an absolute
   path name for the value of the setting, as well as forward slashes (yes,
   Windows too).

5. Type `chp`, `sec`, `ssec`, or `sssec` and hit `Tab` to activate the
   subdivision snippets. A blank `title` element is provided and the cursor
   positioned within it. As you type, the `xml:id` field for the subdivision
   is filled with similar text mirroring the title you are entering.

### Known issues

* The `ref` snippet does not bring up the quick panel. Should it?
* Some of the snippets could be improved.
* Symbol finding could be improved.
