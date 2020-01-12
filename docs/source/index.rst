.. inkscapeMadeEasy documentation master file, created by
   sphinx-quickstart on Mon May  2 09:03:50 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to inkscapeMadeEasy's documentation!
********************************************

This set of python modules is intended to extend Aaron Spike's inkex.py module, adding functions to help the development of new extensions for Inkscape <https://inkscape.org>.

Here you will find methods and classes to deal with drawings, styles, markers, texts, plots, etc. It is a work-in-progress project and new features will be added in the future. However there is no roadmap right now.

.. image:: ../imagesDocs/samples_01.png
          :width: 800px

This project is not intended to provide an end-user Inkscape extension by itself but to provide easier backstage functions and classes to facilitate the development of Inkscape extensions.

For end-user extensions see my other projects on GitHub (more to come soon):

  - **createMarkers**           <https://github.com/fsmMLK/inkscapeCreateMarkers>

  - **cartesianAxes2D**         <https://github.com/fsmMLK/inkscapeCartesianAxes2D>

  - **cartesianPlotFunction2D** <https://github.com/fsmMLK/inkscapeCartesianPlotFunction2D>

  - **cartesianPlotData2D**     <https://github.com/fsmMLK/inkscapeCartesianPlotData2D>

  - **cartesianStemPlot**       <https://github.com/fsmMLK/inkscapeCartesianStemPlot>

  - **polarAxes2D**             <https://github.com/fsmMLK/inkscapePolarAxes2D>

  - **logicGates**              <https://github.com/fsmMLK/inkscapeLogicGates>

  - **circuitSymbols**          <https://github.com/fsmMLK/inkscapeCircuitSymbols>

  - **dimensions**              <https://github.com/fsmMLK/inkscapeDimensions>

  - **SlopeField**             <https://github.com/fsmMLK/inkscapeSlopeField>

History and Objectives
----------------------

Historically this project started as a way to help myself while creating extensions, namely focusing on scientific/academic diagrams and graphs. In the academy, it is very common to prepare plots/diagrams to explain concepts during lectures, seminars or congresses.

There are many consecrated mathematical tools that can produce them, e.g., gnuplot, octave, matlab, R, etc. They all can produce nice plots, however it might be a little complicated if we want to add other elements to these plots, like texts, comments, arrows, etc. These packages have tools to do it but they are cumbersome to use. A better approach would be using a proper graphic software.

One possible approach is to export these plots as raster images and use a raster graphic software to produce the annotations, like Gimp. Personally, I prefer to have the plots in a vector graphic format to keep it aesthetically pleasing and add the annotations in a vector graphic software. For this, Inkscape is very sound.

Unfortunately, exporting the plots as vector graphics is not always successful in the sense that the resulting document is quite "dirty" (unorganized groups, isolated elements, etc.). Therefore I decided to make my own plotting/diagram tools for Inkscape.


In the process of creating these tools (I will upload them to GitHub in a near future) I realized that many of the low level classes and methods used to manipulate elements of the svg file could be grouped in a general purpose set of core modules that extended inkex.py module. **inkscapeMadeEasy** was born! The core modules I created do not intend to provide an extensive array of methods and classes to cover all possibilities of manipulations/transformations and drawing. These modules were born and expanded as I felt the necessity to have new methods to help my workflow. Nevertheless the number of methods created allows many possibilities and is still under development so new features can (will) appear in future versions.

**Obs:** Since it is not very easy to find documentation on other Inkscape modules, there might be other modules with similar/better features that I was not aware of when I was producing my extensions.



Enough mumbo-jumbo. Let's start! =D



Contents:
-------------

.. toctree::
   :maxdepth: 2


`Main Features`_

`Installation and requirements`_

`Usage`_

`Module definitions`_

Main Features
-------------


Optional LaTeX support via textext extension
============================================

.. Important note:: LaTeX support is an optional feature, **enabled by default**. Please refer to :ref:`latexSupport` on how to disable it.

Many of the functions implemented in this project can use LaTeX to generate text if the support is enabled. To this end I decided to employ the excellent extension **textext** by Pauli Virtanen  <https://pav.iki.fi/software/textext/>. 

Since I made very few modifications to his module, I decided to include the modified files here. The modifications
were merely designed to facilitate debugging and to remove additional GUI modules (GTK or TkInter). If you prefer,
you can stick with the original version.

**Please keep in mind that you will need to install 'pstoedit' converter.** Linux users can install from your preferred package manager. Windows users can download it from its website.


Scientific plotting system
============================================

inkscapeMadeEasy_Plot module provides simple yet powerful tools to generate 2D Cartesian and Polar axes and 2D plots (lines and Octave's stem plot style). It was inspired by Tavmjong Bah's (and collaborators) extension **Function Plotter** already presented in Inkscape. Function Plotter extension is not required here.

Control over text styles, line markers and other drawing features
=================================================================

inkscapeMadeEasy_Draw module provides powerful tools to:

 - manipulate colors, including pre-defined named colors, gray scale, RGB conversion and the color picker widget of .inx
 - create custom markers, including a few pre-defined often used types. All can be assigned to custom colors in both stroke and filling colors
 - create line styles, with or without custom markers and custom line dash pattern
 - create text styles
 - create LaTeX contents (thanks to **textext** by Pauli Virtanen)
 - direct control over text size and color of LaTeX contents
 - draw straight polylines using absolute or relative coordinates
 - draw arcs given the start and end points and its radius
 - draw arcs given the center point and start and end angles
 - draw circles/ellipses given center and radius

Useful backstage functions
============================================

inkscapeMadeEasy_Base module inherits inkex.py module, extending it by providing useful core functions:

 - Dump objects to a text file. Rationale: As of today, 2016, Inkscape does not return the stdout() during python code run. This method partially overcomes this issue by sending the object to a text file.
 - unique ID number generator (adapted from inkex.py)
 - list defined elements (e.g. markers) in the current document
 - create groups
 - get the resulting transformation matrix of an object, even when multiple transformations are stacked
 - rotate, scale and move objects
 - find markers
 - get the list of point coordinates of an object or group. If the object is a group the method searches points recursively. Any eventual transformations are properly applied to the points before listing them
 - get the bounding box of an object or group
 - get the center of the bounding box of an object or group

.. _latexSupport:

Installation and requirements (all users)
-----------------------------------------

These modules were partially developed in Inkscape 0.48, 0.91, 0.92 in Linux (Kubuntu 12.04 and 14.04). They should
work on both versions of Inkscape. Also, they should work in different OSs too as long as all requirements are met.

The following python modules are required: inkex (comes with inkscape), re, lxml, numpy, math, simplestyle (comes
with inkscape), copy, tempfile, sys and os.

**Please keep in mind that you will need to install 'pstoedit' converter if you want to use LaTeX support.**  Linux users can install from your preferred package manager. Windows users can download it from its website.

In order to install inkscapeMadeEasy, you must download inkscapeMadeEasy files from github and place them inside Inkscape's extension directory (see below how to find it). In the end you must have the following files and directories in your Inkscape extension directory.

>>> inkscape/extensions/
>>>             |-- inkscapeMadeEasy_Base.py
>>>             |-- inkscapeMadeEasy_Draw.py
>>>             |-- inkscapeMadeEasy_Plot.py
>>>             `-- textextLib
>>>                 |-- __init__.py
>>>                 |-- basicLatexPackages.tex
>>>                 |-- textext.inx
>>>                 |-- textext.py

**Inkscape's extension directory** Your inkscape extension directory location can be found opening Inkscape and selecting ``Edit>Preferences>System`` and checking ``User Extensions``  field. (Windows users: you can easily open this directory using Windows Explorer by copying the text in this field and pasting on Windows Explorer's search bar)

**LaTeX package requirement**

If LaTeX support is enabled (see below), you will need in your system the following LaTeX packages: amsmath, amsthm, amsbsy, amsfonts, amssymb, siunitx, steinmetz.

Linux users: You might find useful installing the packages ``texlive-science``,   ``texlive-pictures`` and ``texlive-latex-base`` (Debian based distros) from your package manager. They should provide most (all?) needed LaTeX packages.

Windows users: please check ``Installation and requirements (windows users)`` section

**Disabling LaTeX support**

LaTeX support via textext extension requires LaTeX typesetting system in your computer (it's free and awesome! =] ). It  might be a problem to install for non-Linux systems.

Since many people don't use LaTeX and/or don't have it installed (it might be a pain to install it on Windows machines), LaTeX support is now optional. **By default, LaTeX support is ENABLED.**

If you don't want LaTeX support or your system does not allow it, you can still use **inkscapeMadeEasy** as long as you disable it. You can easily do it by setting a flag in ``inkscapeMadeEasy_Draw.py``:

 1- Open ``inkscapeMadeEasy_Draw.py`` in any text editor (e.g. Notepad in Windows)

 2- Search for the line containing ``#useLatex=False``. It should be somewhere at the beginning of the file.

 3- Remove the comment character ``#`` of this line, leaving just ``useLatex=False``.

 4- Save the file.

LaTeX installation  (windows users)
-----------------------------------

**1) Install Miktex:**

Download and install Miktex (https://miktex.org/). You must make sure the following minimal testing example compiles
correctly using pdflatex using the command prompt. Se
instructions below::

   \documentclass[11pt]{article}
   \usepackage[utf8]{inputenc}
   \usepackage{amsmath,amsthm,amsbsy,amsfonts,amssymb}
   \usepackage[per=slash]{siunitx}
   \usepackage{steinmetz}
   \begin{document}
   Minimal example. woo-hoo!
   \begin{align}
   E=mc^2
   \end{align}
   \end{document}

**1.2) testing pdflatex (for LaTeX experienced users)**

Check whether you can call pdflatex from any folder, in other words, check if pdflatex folder is in the PATH
environment variable.

Check whether your pdflatex can compile the testing example from the command prompt.
Compiling this example will also make sure you have all packages inkscapeMadeEasy requires.

**1.3) testing pdflatex (for LaTeX beginners)**

   1.3.1) Open notepad and create a text file with the contents of the testing example and save it somewhere.

   1.3.2) In File Explorer, go to the folder where you saved the file and click the address bar to select it (or press
   Alt+D).
   Type “cmd” into the address bar and hit Enter to open the Command Prompt with the path of the current folder already set.
    
   1.3.3) type:  pdflatex <name_of_the_file_you_just_saved>. Lots of stuff should appear on your console window.
   Obs: Miktex might require to install additional packages. Depending on how you installed Miktex, it can install
   automatically the needed packages or ask you to confirm. Confirm it!

   1.3.4) Check whether pdflatex created a new pdf file with the same name. Open the pdf and see if you can read the
   short message and equation.


**2) install pstoedit (install version 3.73!)**

windows 32 bits
https://sourceforge.net/projects/pstoedit/files/pstoedit/3.73/pstoeditsetup_win32.exe

windows 64 bits
https://sourceforge.net/projects/pstoedit/files/pstoedit/3.73/pstoeditsetup_x64.exe

2.1) Add pstoedit folder to windows PATH environment variable (if it is not there already)

   2.2.1) On the Windows desktop, right-click 'My Computer'.

   2.2.2-) In the pop-up menu, click Properties.

   2.2.3-) In the System Properties window, click the Advanced tab, and then click Environment Variables.

   2.2.4-) In the System Variables window, highlight PATH, and click Edit.

   2.2.5-) Create a new entry and provide the path where pstoedit was installed. On my machine the folder was 'C:\\Program Files\\pstoedit'


3) Install ghostscript (install version 9.26!)

windows 32 bits
https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs926/gs926aw32.exe

windows 64 bits
https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs926/gs926aw64.exe

Usage
-------------

These modules are not intended to serve as extensions by themselves. Instead you can import them into your projects to take advantage of the classes and methods developed here.

For examples on how to use, please take a look at the examples provided below and also check my other extension projects on GitHub (more to come soon):

  - **createMarkers**           <https://github.com/fsmMLK/inkscapeCreateMarkers>

  - **cartesianAxes2D**         <https://github.com/fsmMLK/inkscapeCartesianAxes2D>

  - **cartesianPlotFunction2D** <https://github.com/fsmMLK/inkscapeCartesianPlotFunction2D>

  - **cartesianPlotData2D**     <https://github.com/fsmMLK/inkscapeCartesianPlotData2D>

  - **polarAxes2D**             <https://github.com/fsmMLK/inkscapePolarAxes2D>

  - **logicGates**              <https://github.com/fsmMLK/inkscapeLogicGates>

  - **circuitSymbols**          <https://github.com/fsmMLK/inkscapeCircuitSymbols>

  - **dimensions**              <https://github.com/fsmMLK/inkscapeDimensions>

Module definitions
------------------

inkscapeMadeEasy_Base
=====================


.. automodule:: inkscapeMadeEasy_Base
    :members:
    :undoc-members:
    :show-inheritance:

inkscapeMadeEasy_Draw
=====================

.. automodule:: inkscapeMadeEasy_Draw
    :members:
    :undoc-members:
    :show-inheritance:

inkscapeMadeEasy_Plot
=====================

.. automodule:: inkscapeMadeEasy_Plot
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: generateListOfTicksLinear,generateListOfTicksLog10,findOrigin,getPositionAndText

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

