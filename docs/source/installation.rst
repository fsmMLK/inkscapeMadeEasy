Inkscape Version
================

.. attention:: The procedure bellow  refers to inkscapeMadeEasy **version 1.0 or later**  only. For older versions, please see the pdf manual inside the `legacy folder 0.9x <https://github.com/fsmMLK/inkscapeMadeEasy/tree/master/0.9x>`_.

InkscapeMadeEasy was developed using Inkscape 1.0 in Linux (Kubuntu 18.04). It should work in different OSs too as long as all requirements are met.

Requirements
============

0) You will need `Inkscape 1.0 or later <https://inkscape.org/>`_ (duh!  =) ) 

1) You will need Python 3 in your machine. InkscapeMadeEasy will not work properly with python 2. The following python modules are required: math, os, re, sys, copy, numpy, lxml, tempfile. Make sure your python installation has these modules.

2) If you want LaTeX support, install a latex distribution for your OS. You will need in your system the following LaTeX packages: amsmath, amsthm, amsbsy, amsfonts, amssymb, siunitx, steinmetz.

3) You will need `TexText <https://textext.github.io/textext/>`_ version **1.0**

.. note:: Starting from InkscapeMadeEasy 1.0, you don't need pstoedit, ghostscript and pdf2svg anymore. Thanks TexText team! =)


Installation procedure (v1.0 only)
==================================

1) Install python 3 in your machine if you don't have it yet. You can download it from `here <https://www.python.org/>`_ or use your package manager. See the instructions for `Linux <https://docs.python.org/3/using/unix.html>`_,  `Windows  <https://docs.python.org/3/using/windows.html>`_ or  `Mac <https://docs.python.org/3/using/mac.html>`_ if you need help.


   .. note :: **Windows users:** make sure you check **Add Python 3.x to PATH** on the bottom of the installer screen.

   Install the following python modules: math, os, re, sys, copy, numpy, lxml, tempfile.

2) Install `Inkscape 1.0 <https://inkscape.org/>`_.

   .. note :: **Windows users:** Make sure that you checked the **Python** option in Program Files as well as the **Extensions** options in Inkscape Data during the installation of Inkscape (by default this is the case).

        .. image:: ../imagesDocs/inkscape-install-options-windows.png
              :width: 400px

3) **if you want LaTeX support:** Install a LaTeX distribution . See `LaTeX installation`_ on further instructions for Linux, Mac and Windows users. 

4) **if you don't want LaTeX support:** follow the instructions of section :ref:`disableLatexSupport` to disable it.

5) Install `TexText <https://textext.github.io/textext/>`_ version **1.0**. Follow the instructions on the link.

6) inkscapeMadeEasy installation

  a) Go to Inkscape's extension directory with a file browser. Your inkscape extension directory can be accessed by opening Inkscape and selecting ``Edit > Preferences > System``. Look for the item **User Extensions**  field. There is a button on the right of the field  that will open a file explorer window in that specific folder.

  b) Create a subfolder in the extension directory with the name ``inkscapeMadeEasy``.

   .. warning::  Be careful with upper and lower case letters. You must write as presented above.

  c) Download `inkscapeMadeEasy <https://github.com/fsmMLK/inkscapeMadeEasy>`_ files and place them inside the directory you just created.

   You don't have to copy all files from Github. The files you will need are `inkscapeMadeEasy_Base.py`, `inkscapeMadeEasy_Draw.py`, `inkscapeMadeEasy_Plot.py`, and  `basicLatexPackages.tex`. **You can find these files inside the ``latest`` folder**. In the end you must have the following files and directories in your Inkscape extension directory.

.. code-block::
    
   inkscape
    ┣━━extensions
    ┋   ┣━━ inkscapeMadeEasy   <-- inkscapeMadeEasy folder
        ┃    ┣━━ inkscapeMadeEasy_Base.py
        ┃    ┣━━ inkscapeMadeEasy_Draw.py
        ┃    ┣━━ inkscapeMadeEasy_Plot.py
        ┃    ┗━━ basicLatexPackages.tex
        ┃
        ┣━━ textext   <-- textext folder (if you installed textText)
        ┋

.. note::  You might have other sub folders inside the extensions directory. They don't interfere with inkscapeMadeEasy.



LaTeX installation
------------------

Linux users
~~~~~~~~~~~

You might find useful installing the packages ``texlive-science``, ``texlive-pictures`` and ``texlive-latex-base`` (Debian based distros) from your package manager. They should provide most (all?) needed LaTeX packages. Other unix flavour should have similar packages. After installation, see if you can compile this `Minimal LaTex example`_


Windows users
~~~~~~~~~~~~~

1) **Install Miktex:**
   Download and install `Miktex <https://miktex.org/>`_.

2) **testing pdflatex (for LaTeX experienced users):**

   You must make sure the `Minimal LaTex example`_ compiles correctly using pdflatex from the command prompt.
    
   Check whether you can call pdflatex from any folder, in other words, check if pdflatex is in the PATH environment variable.

2) **testing pdflatex (for LaTeX beginners)**

   a) Open notepad and create a text file with the contents of the `Minimal LaTex example`_ and save it somewhere with the name ``example.tex``.

   b) In File Explorer, go to the folder where you saved the file and click the address bar to select it (or press Alt+D).
   
      Type “cmd” into the address bar and hit Enter to open the Command Prompt with the path of the current folder already set.
    
   c) type:  ``pdflatex example.tex`` in the command line and hit ENTER.

      Lots of text should appear on your console window.

      .. note:: Miktex might require you authorization to install additional packages. Depending on how you installed Miktex, it can install automatically without asking or ask you to confirm. Confirm it!

   d) Check whether pdflatex created a new pdf file with the same name. Open the pdf and see if you can read the    short message and equation.


Minimal LaTeX example
~~~~~~~~~~~~~~~~~~~~~

You should be able to compile the following example on your system. Compiling this example will also make sure you have all packages inkscapeMadeEasy requires.::
    
       \documentclass[11pt]{article}
       \usepackage[utf8]{inputenc}
       \usepackage{amsmath,amsthm,amsbsy,amsfonts,amssymb}
       \usepackage[per=slash]{siunitx}
       \usepackage{steinmetz}
       \begin{document}
       Minimal example. Woo-hoo!
       \begin{align}
       E=mc^2
       \end{align}
       \end{document}
       

.. _disableLatexSupport:

Disabling LaTeX support
=======================

.. warning:: **By default, LaTeX support is ENABLED.**

LaTeX support via TexText extension requires LaTeX typesetting system in your computer (it's free and awesome! =] ). This might be a problem to install for non-Linux systems.

Since many people don't want to use LaTeX and/or don't have it installed, LaTeX support is optional. 

If you don't want LaTeX, you can still use **inkscapeMadeEasy** as long as you disable the support. You can
easily do
it by setting a flag in ``inkscapeMadeEasy_Draw.py``:

 1- Open ``inkscapeMadeEasy_Draw.py`` in any text editor (e.g. Notepad in Windows. DO NOT use Microsoft word!)

 2- Search for the line containing ``#useLatex=False``. It is near the the beginning of the file.

 3- Remove the comment character ``#`` of this line, leaving just ``useLatex=False``.

 4- Save the file, close the text editor, and restart inkscape if already opened.


