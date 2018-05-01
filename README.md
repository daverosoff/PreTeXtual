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

As of version 0.5.0, Sublime Text 2 is no longer supported.

<!-- MarkdownTOC -->

- Installation
- Additional setup to use the automatic build systems
   - Read before continuing
   - Install other required software
   - Choose a Vagrant box
   - Install PreTeXt with one easy step
   - Populate your environment
   - Compiling to HTML or PDF
   - Building images
- Keybindings
- Usage
- Known issues

<!-- /MarkdownTOC -->

### Installation

*Note: We assume you are familiar with running Sublime Text commands via the
Command Palette. To bring up the palette, hit <kbd>Ctrl+p</kbd>
(<kbd>Cmd+p</kbd> on OS X). Then start typing the name of the command you want
to filter the list of results.*

It is recommended to install PreTeXtual via Package Control. If you have not
installed Package Control yet, you should
[do that first](https://packagecontrol.io) (and restart Sublime Text afterward).

After Package Control is installed, use the `Install Package` command (in the
Command Palette) to search for the PreTeXtual package, and select it from the
Quick Panel to install. This method of installation allows Package Control to
automatically update your installation and show you appropriate release notes.

You may also install PreTeXtual via `git`. Change directories into your
`Packages` folder. To find the `Packages` folder, select Browse Packages from
the Preferences menu (from the Sublime Text 3 menu on OS X). Make sure you are
in the `Packages` folder and *not* `Packages/User`.

Then, run
```
git clone https://github.com/daverosoff/PreTeXtual.git
```
and restart Sublime Text (probably not necessary).

### Additional setup to use the automatic build systems

PreTeXtual now comes with build systems that can process your PreTeXt source
into HTML or LaTeX and build your latex-image images into all image formats.
The result is output that is ready to preview in a browser (HTML) or compile
to PDF (LaTeX). All of this can be done from the command palette, if you
carefully follow the directions below.

#### Read before continuing

The build systems are intended primarily for Windows users, since PreTeXt is
much more difficult and tedious to install on Windows. As of this release, it
has only been successfully used on Windows 10. Windows 7 users are welcome to
try to follow the directions, but Windows 7 seems to have some difficulty
installing current versions of Vagrant, see below. Future support for Windows
7 is devoutly to be wished.

If your Windows 7 is 32-bits, it is unlikely that you will be able to use the
build system. Please open an issue if you need 32-bit support. If there is
sufficient demand, it is possible to create compatible Vagrant boxes. (However
you will still need to use Vagrant, which may not always play nice with
Windows 7, as described above)

Users of other operating systems will not find the build systems in this
release useful without manual editing of some of the package resources. You
are welcome to [open an
issue](https://github.com/daverosoff/PreTeXtual/issues) with questions about
how to accomplish this. A future release will support use of the build systems
without Vagrant, which is preferable for any Mac OS or Linux users who might
want to use the build systems for convenience.

As you continue with the installation, it would be good to [visit this README
in a browser](https://packagecontrol.io/packages/PreTeXtual) so that you can
follow along while you do things in Sublime Text and other programs.

#### Install other required software

At present, the build systems require the use of two other applications,
Virtualbox and Vagrant. Install these on your computer. Agree to the default
whenever you are prompted for a decision. *Not choosing default values will
break the PreTeXtual build systems.*

1. In Sublime Text, use Package Control to install the SideBarEnhancements
   plugin
1. [Download Virtualbox](https://www.virtualbox.org/wiki/Downloads)
2. [Download Vagrant](https://www.vagrantup.com/downloads.html)

#### Choose a Vagrant box

After downloading and installing from the above links, open a Sublime Text
window and run the command (from the Command Palette) "Initialize PreTeXt
Vagrant". This will take some time, depending on your selections. You will see
a menu with several choices. Most people will want either "PreTeXt" or
"PreTeXt-lite". If you need Sage or Asymptote, choose "PreTeXt" (note that
these image types are not supported in this release but support is coming very
soon). If you need a full LaTeX installation but not Sage or Asymptote, choose
"PreTeXt-lite". If you only need to process HTML, you can try "PreTeXt-
barebones". The last option, "PreTeXt-no-images", is only for testing.

The full "PreTeXt" option will take between 45 and 60 minutes to download and
install. The others will take less time, but even the barebones option might
take 10 to 15 minutes. You should see new windows opening to advise you of
progress and reassure you that something is happening. When no more of these
windows are visible, go on to the next step.

#### Install PreTeXt with one easy step

Note: This step will merge with the previous one in a future release.

From the Command Palette, run the command "Clone repository". You will see a
message at the bottom of the screen prompting you for a URL. Enter the text

    https://github.com/rbeezer/mathbook.git

and hit Enter. Another new window will pop up during the installation, which
should only take a few seconds.

#### Populate your environment

The previous sections created a new folder `C:\PreTeXt` on your machine. This
is where all your writing projects will live. You have a few ways to get them
into place.

* Move existing projects to the `C:\PreTeXt` folder. This is probably be st to
  do using the Windows file browser.
* Clone existing git repositories using the "Clone repository" command.
* Create an empty folder for a new project. Put it under `C:\PreTeXt` and call
  it whatever you want (no spaces!)

Whatever way you choose, verify the following for each project you add.

1. Project folder has subfolder called `src`
2. `src` folder contains all PreTeXt source files for the project

#### Compiling to HTML or PDF

Now the fun starts. In an existing writing project, open the root PreTeXt file
(the one with the `<mathbook>` element). Use the Command Palette
(<kbd>Ctrl+Shift+P</kbd>) to run the command "Set current file as PreTeXt
root". Then, bring up the build menu by pressing <kbd>Ctrl+Shift+B</kbd>.
Select "Process PreTeXt to HTML" from the menu. If you are watching the
sidebar, you will see an `output` folder appear next to your `src` folder. If
you expand it in the sidebar you can watch the HTML files appear as they are
generated. When the build is finished, Sublime Text should alert you to this
fact with a dialog box.

Open the `output\html` folder and right-click one of the HTML files. Select
"Open in browser". Marvel at the relative simplicity of this process.

To compile to LaTeX, you can select "Process PreTeXt to LaTeX" from the menu.
To convert to PDF, I recommend you use the excellent LaTeXtools plugin, to
which PreTeXtual owes a great deal. A future version (coming very soon) will
support compilation from within Sublime Text without the use of LaTeXtools.

#### Building images

Note: this part of the build system may still be a bit buggy. In particular it
will probably fail if you chose `pretext-barebones` above.

Building images should be as simple as processing to HTML or LaTeX. Use the
<kbd>Ctrl+Shift+B</kbd> menu to select "Build images" (this will take a while
if you have a large project). Then refresh your HTML output in the browser to
check that the images appear.

This concludes the tour of the build system.

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

* There are quite a few edge cases and bugs in the build system left to fix in
  the next rc version.
* The `ref` snippet does not bring up the quick panel. Should it?
* Some of the snippets could be improved.
* Symbol finding could be improved.
