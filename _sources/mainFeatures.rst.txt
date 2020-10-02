Optional LaTeX support via textext extension
============================================

Many of the functions implemented in inkscapeMadeEasy can use LaTeX to generate text if the support is enabled. To this end, I decided to employ the excellent extension `TexText <https://github.com/textext/textext>`_ by `awesome people <https://textext.github.io/textext/authors.html>`_.

.. note:: LaTeX support is an optional feature, **enabled by default**. Please refer to :ref:`disableLatexSupport` on how to disable it.

Scientific plotting system
==========================

**inkscapeMadeEasy_Plot** provides simple yet powerful tools to generate 2D Cartesian and Polar axes and plots (lines and Octave's stem plot style). This functionality was inspired by Tavmjong Bah's (and collaborators) extension **Function Plotter** already presented in Inkscape. Function Plotter extension is not required here.

Control over text styles, line markers and other drawing features
==================================================================

**inkscapeMadeEasy_Draw** module provides powerful tools to:

- manipulate colours, including pre-defined named colours, grayscales, RGB conversion and the colour picker widget of .inx
- create custom markers, including a few pre-defined often used types. They can be assigned to custom colours, stroke and filling independently
- create line styles, with or without custom markers and custom line dash pattern
- create text styles
- create LaTeX contents (thanks to **TexText**)
- direct control over text size and colour of LaTeX contents
- draw straight polylines and bezier curves using absolute or relative coordinates
- draw arcs, rectangles, ellipses and circles using different methods, based on their geometrical characteristics.

Useful backstage functions
============================================

**inkscapeMadeEasy_Base** module inherits inkex.py module, extending it by providing useful core functions:

 - Dump objects to a text file. Rationale: As of today (2020) Inkscape does not return the stdout() during python code run. This method partially overcomes this issue by sending the object to a text file.
 - unique ID number generator (adapted from inkex.py, but using consecutive numbering)
 - list defined elements (e.g. markers) in the current document
 - create/remove groups
 - remove elements
 - extract the transformation matrix of an object, even when multiple transformations are stacked
 - rotate, scale and move objects
 - find markers
 - import SVG files
 - export selected elements to new SVG file
 - manipulate def nodes
 - get the list of coordinates of the points of an object or group. If the object is a group the method searches points recursively. Any eventual transformations are properly applied to the points before listing them
 - get the bounding box of an object or group
 - get the centre of the bounding box of an object or group
