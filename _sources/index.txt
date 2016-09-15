.. inkscapeMadeEasy documentation master file, created by
   sphinx-quickstart on Mon May  2 09:03:50 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to inkscapeMadeEasy's documentation!
********************************************

This set of python modules is intended to extend Aaron Spike's inkex.py module, adding functions to help the development of new extensions for inkscape <https://inkscape.org>.

Here you will find methods and classes to deal with drawings, styles, markers, texts, plots, etc. It is a work-in-progress project and new features will be added in the future. However there is no roadmap right now.

This project is not intended to provide an end-user inkscape extension by itself but to provide easier backstage functions and classes to facilitate the development of inkscape extensions.

For end-user extensions see my other projects on GitHub (they will be uploaded soon).

Historically this project started as a way to help myself while creating extensions, namely focusing on scientific/academic diagrams and graphs. Therefore these modules do not intend to provide an extensive array of functions and classes to cover all possibilities of configurations, styles and etc. The modules were born and expanded as I felt the necessity to have new functions to help my workflow. Due to this, there might be other modules with similar/better features that I didn't find before.

Enough mumbo-jumbo. Let's start! =D





.. image:: ../imagesDocs/samples_01.png
          :width: 800px
Contents:
==========================================

.. toctree::
   :maxdepth: 2


`Main Features`_

`Installation and requirements`_

`Usage`_

`Module definitions`_

Main Features
=============

LaTeX support via textext.py extension
--------------------------------------

Many of the functions implemented in this project uses LaTeX to generate text. To this end I decided to use the excellent extension 'textext' from Pauli Virtanen  <https://pav.iki.fi/software/textext/>. 

Since I made a very few modifications to his module, I decided to include it in this project. The modifications were merely designed to facilitate debugging. No deep modifications were made to it. If you prefer, you can stick with the original version.

Instalation procedure and requirements of the modified 'textext.py' are exactly the same of the original. Please refer to the installation section on Pauli Virtanen's page to get further instructions.

  **Modifications**

  Here is the full list of changes::

    # Changes: line  67-68: added a few variables to control debug mode
    # Changes: line 944: changed order of programs (It worked better in my machine)
    # Changes: line 665: debug option to save temporary files to an easy access directory
    # Changes: line 696: debug option to keep the .tex file

Scientific plotting system
--------------------------

inkscapeMadeEasy_Plot module provides simple yet powerful tools to generate 2D Cartesian and Polar axes and 2D plots (lines and Octave's stem plot style). It was inspired by Tavmjong Bah's (and collaborators) extension 'Function Plotter' already presented in inkscape. Function Plotter extension is not required here.

Control over text styles, line markers and other drawing features
-----------------------------------------------------------------

inkscapeMadeEasy_Draw module provides powerful tools to:

 - manipulate colors, including pre-defined named colors, gray scale, RGB conversion and the color picker widget of .inx
 - create custom markers, including a few pre-defined often used types. All can be assigned to custom colors in both stroke and filling colors
 - create line styles, with or without custom markers and custom line dash pattern
 - create text styles
 - create LaTeX contents (thanks to 'textext' from Pauli Virtanen)
 - direct control over text size and color of LaTeX contents
 - draw straight polylines using absolute or relative coordinates
 - draw arcs given the start and end points and its radius
 - draw arcs given the center point and start and end angles
 - draw circles/ellipses given center and radius

Useful backstage functions
---------------------------------------------------------

inkscapeMadeEasy_Base module inherits inkex.py module, extending it by providing useful core functions:

 - Dump objects to a text file. Rationale: As of today, 2016, inkscape does not return the stdout() during python code run. This method overcomes partially this issue by sending the object to a text file.
 - unique ID number generator (adapted from inkex.py)
 - list defined elements (e.g. markers) in the current documentation
 - create groups
 - get the resulting transformation matrix of an object, even when multiple transformations are stacked
 - rotate, scale and move objects
 - find markers
 - get the list of points of an object or group. If the object is a group the method searches points recursively. All transformations are properly applied to all points
 - get the bounding box of an object or group
 - get the center of the bounding box of an object or group

Installation and requirements
==========================================

These modules were partially developed in inkscape 0.48 and partially in 0.91 in Linux (Kubuntu 12.04 and 14.04). They should work on both versions of inkscape. Also, they should work in differente OSs too as long as all requirements are installed.

The following python modules are required: inkex, re, lxml, numpy, math, simplestyle (inkex submodule), textext, sys and os.

In order to install inkscapeMadeEasy, your inkscape extension directory must contains the following structure

>>> inkscape/extensions/
>>>             |-- inkscapeMadeEasy_Base.py
>>>             |-- inkscapeMadeEasy_Draw.py
>>>             |-- inkscapeMadeEasy_Plot.py
>>>             `-- textextLib
>>>                 |-- __init__.py
>>>                 |-- basicLatexPackages.tex
>>>                 |-- textext.inx
>>>                 |-- textext.py

You can find all the files in github

Usage
==========================================

These modules are not intended to serve as extensions by themselves. Instead you can import them into your projects to take advantage of the classes and methods developed here.

For examples on how to use, please take a look at the examples provided below and also check my other extension projects on GitHub (they will be uploaded soon).

Module definitions
==================

inkscapeMadeEasy_Base
----------------------


.. automodule:: inkscapeMadeEasy_Base
    :members:
    :undoc-members:
    :show-inheritance:

inkscapeMadeEasy_Draw
----------------------

.. automodule:: inkscapeMadeEasy_Draw
    :members:
    :undoc-members:
    :show-inheritance:

inkscapeMadeEasy_Plot
----------------------

.. automodule:: inkscapeMadeEasy_Plot
    :members:
    :undoc-members:
    :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

