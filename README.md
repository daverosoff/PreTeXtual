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
  - Enable VT-X virtualization
  - Install other required software
- A tour of the automated build systems
  - Initialize your setup
  - Adding projects
  - Installing the Vagrant box
  - Install PreTeXt with one easy step
  - Adding new projects
    - Add via git
    - Add by creating directory
  - Compiling to HTML or PDF
  - Building images
  - Editing settings manually
      - Available settings
  - Conclusion
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

The build systems are also intended for *beginning* PreTeXt users, who may
wish to just get started as soon as possible without working too hard on
configuration or learning too much. So none of the possible configuration one
can do is described here at present. PreTeXtual can do things more flexibly
than described here, but this documentation has been written for simplicity
and the details are omitted.

The build systems are intended primarily for Windows users, since PreTeXt is
much more difficult and tedious to install on Windows. As of this release, it
has only been successfully used on Windows 10. Windows 7 users are welcome to
try to follow the directions, but Windows 7 seems to have some difficulty
installing current versions of Vagrant, see below. Future support for Windows
7 is devoutly to be wished.

If your Windows 7 is 32-bits, it is unlikely that you will be able to use the
build systems with this version of PreTeXtual. Please open an issue if you
need 32-bit support. If there is sufficient demand, it is possible to create
compatible Vagrant boxes. (However you will still need to use Vagrant, which
may not always play nice with Windows 7, as described above)

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

#### Enable VT-X virtualization

This is the hardest step, regrettably necessary for the current version of
PreTeXtual. Feel free to skip it and come back to it later if things don't
work properly.

Follow the directions linked below--very carefully! It is possible to
really mess up your system doing this. There is always "Quit without Saving"
option you can use if you get really stuck or scared.

Windows users will want to [follow these directions][vtxdirs], using steps 1
through 5 only.

#### Install other required software

At present, the build systems require the use of two other applications,
Virtualbox and Vagrant. Install these on your computer. Agree to the default
whenever you are prompted for a decision. *Not choosing default values will
break the PreTeXtual build systems.*

1. In Sublime Text, use Package Control to install the SideBarEnhancements
   plugin
1. [Download Virtualbox](https://www.virtualbox.org/wiki/Downloads)
2. [Download Vagrant](https://www.vagrantup.com/downloads.html)
2. (optional) In Sublime Text, use Package Control to install the Vagrant plugin.
   This plugin may need some configuration not described in this README. Its
   use is not assumed or required in the rest of this document.

### A tour of the automated build systems

#### Initialize your setup

At the present moment, the PreTeXtual build systems all make use of a Vagrant
virtual machine to do the XSL processing and image building steps of the PTX
document generation process. If you don't want to use Vagrant, then this version
of PreTeXtual's build systems won't work for you.

After downloading and installing from the above links, open a Sublime Text
window and run the command (from the Command Palette) "Initialize PreTeXt
Vagrant". This will take some time, depending on your selections. Then follow
the prompts. PreTeXtual will set up a directory called `C:\PreTeXt`, which
will hold many subdirectories: one for each of your writing projects, and one
for PreTeXt itself (still called `mathbook` as of 2018-05-14.) If you already
have such a directory, or if you create one now before continuing, PreTeXtual
will notice and preserve it.

#### Adding projects

If you have a `C:\PreTeXt` directory, each folder one level underneath it will
be recognized as a writing project. These will be added to PreTeXtual's simple
project management system. You can store some options for each project in your
User settings. At the time of initialization, you will be prompted to type a
root file for each one. The root file of a PreTeXt project is the file
containing the `<mathbook>` XML element. You will need to enter the paths with
slashes `/` rather than the more typical backslash `\`. A typical path might
look like

    C:/PreTeXt/AATA/src/aata.xml

**Warning.** While Windows usually doesn't care much about capitalization in
paths, PreTeXtual does. You must enter all letters in your path names with
the correct case, or things may not work as desired.

You can always enter the paths later by editing your Preferences file directly.

#### Installing the Vagrant box

*Note: this step is required, even if you already have installed PreTeXt.*

After you have finished importing projects as described above, you will see a
menu with several choices. Most people will want either "PreTeXt" or
"PreTeXt-lite". If you need Sage or Asymptote, choose "PreTeXt".  If you need
a full LaTeX installation but not Sage or Asymptote, choose "PreTeXt-lite". If
you only need to process HTML, you can try "PreTeXt-barebones". The last option,
"PreTeXt-no-images", is only for testing.

The full "PreTeXt" option will take between 45 and 60 minutes to download and
install. The others will take less time, but even the barebones option might
take 10 to 15 minutes. You should see new windows opening to advise you of
progress and reassure you that something is happening, but even if you don't,
please don't worry! When no more of these windows are visible, open a command
shell (Start menu/type `cmd`/hit Enter) and run

    cd C:\PreTeXt
    vagrant up

before you go on to the next step.

#### Install PreTeXt with one easy step

*Note: this step is required, even if you already have installed PreTeXt.*

Note: This step will merge with the previous one in a future release.

From the Command Palette, run the command `PreTeXtual: Update PreTeXt`. If it
is not available, try saving an empty file with the `.ptx` extension and try
again from within this file. You may see a new window open with some
`git`-related hieroglyphics. A directory named `mathbook` should appear in
your `C:\PreTeXt` folder. All done!

#### Adding new projects

Currently, there is no separate command to add a project. There are two ways you
can do it by hand.

##### Add via git

PreTeXtual has a simple command to clone an existing Git repository into your
`C:\PreTeXt` folder. Run the command `PreTeXtual: Clone repository` from the
Command Palette, and enter the URL of the repository in the input panel.

Make sure to re-run the `PreTeXtual: Initialize PreTeXt Vagrant` command afterward,
to add your new repo to the PreTeXtual project database.

##### Add by creating directory

Simply create a directory under `C:\PreTeXt`, put a (possibly empty) root file
in it, and re-run the `PreTeXtual: Initialize PreTeXt Vagrant` command, to add
your new repo to the PreTeXtual project database.

#### Compiling to HTML or PDF

Now the fun starts. In an existing writing project, open any PreTeXt file.
Make sure that "PreTeXt" is showing in the far lower right corner of the
screen. Some commands will only be available in PreTeXt mode (provided by the
PreTeXtual plugin). If your source files end in `.xml` rather than `.ptx` or
`.mbx` you will need to do some configuration (use the `PreTeXtual: Set
PreTeXt File Exts` command, see below).

Having opened a PreTeXt file, bring up the build menu by pressing
<kbd>Ctrl+Shift+B</kbd>. Select "Process PreTeXt to HTML" from the menu. If
you are watching the sidebar, you will see an `output` folder appear next to
your `src` folder. If you expand it in the sidebar you can watch the HTML
files appear as they are generated. When the build is finished, Sublime Text
should alert you to this fact with a dialog box.

**Warning.** The dialog boxes are not very big or very insistent, but they
block Sublime Text from continuing. If you think your editor has crashed,
check first for any dialog boxes that may have gotten lost behind another
window.

Open the `output\html` folder and right-click one of the HTML files. Select
"Open in browser". Marvel at the relative simplicity of this process.

To compile to LaTeX, you can select "Process PreTeXt to LaTeX" from the menu.
To convert to PDF, I recommend you use the excellent LaTeXtools plugin, to
which PreTeXtual owes a great deal. A future version may support compilation
from within Sublime Text without the use of LaTeXtools. You will need to install
LaTeX on your computer to perform this step, not presently documented here.

#### Building images

*Note.* This part of the build system may still be a bit buggy. In particular
it will probably fail if you chose `pretext-barebones` above. Moreover, it can
be time-consuming, especially for longer documents. Finally, some Asymptote 3D
images are not yet supported and raise exceptions that will stop the image
build process.

*Note.* Including images that are not generated from source is not yet
supported. If you urgently need this feature,
[open an issue](https://github.com/daverosoff/PreTeXtual/issues).

Building images should be as simple as processing to HTML or LaTeX. Use the
<kbd>Ctrl+Shift+B</kbd> menu to select a "Build images" command (this will
take a while if you have a large project). Dismiss the dialogs that appear as
the images are generated and do not be alarmed if Sublime Text should appear
to hang or become unresponsive. Just wait! After the final message "End of
PreTeXtual build routine", you can refresh your HTML output in the browser to
check that the images appear. They will now also be available for LaTeX compilation.

This concludes the tour of the build system. Run `vagrant suspend` in a command
shell before shutting down your system (Windows will complain that something is
stopping you from shutting down otherwise).

#### Editing settings manually

All the PreTeXtual information is stored in the `pretext_projects` setting in
your User settings file. To edit it, select "Preferences/Settings" from the
Sublime Text 3 menu. A new Sublime Text window with two panes will appear. The
left side is for reference only and should not be edited. In the right side,
you should be able to find the `pretext_projects` setting. You can change the
values and save the file as you wish.

###### Available settings

1. `name`: each project has an internal id called `name`. By default this is the
   same as the name of the directory it lives in.
2. `path`: each project knows the path to its directory. You need to escape the
   backslashes (enter each backslash as `\\`).
3. `root_file`: each project knows the absolute path to its root file.
4. `xinclude`: (default: True) if you would like to disable the `xinclude` behavior
   for some reason, set this value to `false` (note: no quotes).
5. `stringparam`: if you need some custom stringparams, enter them here as a
   dictionary/hash of key-value pairs:

        "stringparam": {
          "html.css.file": "https://www.my.site/path/to/my.css",
          "latex.font.size": "20pt"
        }
6. (experts only) There are a few other settings that PreTeXt will recognize
   that are not yet documented here. Inspect the file `beta_process.py` to
   find out more about them.

#### Conclusion

This concludes the section of the documentation about the build system. Thank you
for reading and please address questions to the pretext-support Google group:

    https://groups.google.com/forum/#!forum/pretext-support

or open an issue at

    https://github.com/daverosoff/PreTeXtual/issues

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

1. New in 0.6.0: an extensive interface with Vagrant virtual machine
   management software is included, to enable Sublime Text 3 to behave more
   like an API for PreTeXt. See the related section of this README for more
   information.

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
  the next version.
* The root file detection is ambiguous. There is a systemwide PreTeXt root file
  used for generating symbol lists, but this is ignored by the build systems.
  They use a completely different setting scheme for finding the root file of
  a project. The documentation does not adequately address this.
* The `ref` snippet does not bring up the quick panel. Should it?
* Some of the snippets could be improved.
* Symbol finding could be improved.

[vtxdirs]: https://docs-old.fedoraproject.org/en-US/Fedora/13/html/Virtualization_Guide/sect-Virtualization-Troubleshooting-Enabling_Intel_VT_and_AMD_V_virtualization_hardware_extensions_in_BIOS.html
