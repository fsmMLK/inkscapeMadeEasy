Changelog
==========


2024-10oct-23
-------------

inkscapeMadeEasy_Draw.py
   - added methods to copy and paste line styles
   - fixed a bug in the create markers, introduced after changes in inkex.py


2024-04apr-18
-------------

inkscapeMadeEasy_Base.py
   - fixed a bug in the output of getSegmentParameters

2022-10oct-01
-------------

inkscapeMadeEasy_Base.py
   - fixed a bug in arc.startEndRadius
   - improved method ellipseArc.centerAngStartAngEnd

2022-08aug-19
-------------

inkscapeMadeEasy_Base.py
   - new method createEmptySVG()
   - new method cleanDefs()
   - the method getPoints() also accepts 'rectangle' elements
   - added option [=v2] to siunix import in the latext preamble file.

2022-02feb-19
-------------

inkscapeMadeEasy_Draw.py
   - new class ellipseArc with functions to draw arcs of ellipses
   - new method lineStyle.createDashedLinePattern

inkscapeMadeEasy_Base.py
   - new input argument added to importSVG() method
   - new input argument added to unifyDefs() method
   - fixed a bug in getTransformMatrix() when translation operation has only one argument
   - fixed a bug in getPoints() when the element is 'use'

2021-09sep-12
-------------

Updated latex preamble to comply with SIunitx v2-v3

inkscapeMadeEasy_Base.py
   - importSVG() now accepts two new arguments
   - new function addAttribute()

2021-04apr-28
-------------

Fixed example of the documentation

2021-04apr-25
-------------

inkscapeMadeEasy_Draw.py
   - alpha channel support was added to color() class.
   - The following functions have now one additional input argument: color.defined(), color.RGB()  color.rgb(), and color.gray()
   - The function color.parseColorPicker() has new output
   - added new function color.val2hex()

2021-04apr-04
-------------

inkscapeMadeEasy_Base.py
   - exportSVG() corrected text encoding when creating empty SVG file.
   - exportSVG() now the blank SVG file will be in px.
   - moveElement() fixed quick return if distance is 0.0
   - getPoints() now it returns a 2D numpy array instead of a list of lists.
   - getBoundingBox() now it returns a 2D numpy array instead of a list.

2021-03mar-20
-------------

inkscapeMadeEasy_Draw.py
   - new function arc.threePoints that creates an arc based on 3 points in the arc
   - new function circle.threePoints that creates a circle based on 3 points in the circle

2020-10oct-06
-------------

inkscapeMadeEasy_Base.py and inkscapeMadeEasy_Draw.py
   - fixed a bug in text.latex that would result in wrong font size.

inkscapeMadeEasy_Draw.py
   - fixed a bug in color.rgb() method.

2020-10oct-02
-------------

.. important::
    - inkscapeMadeEasy is now compatible with 1.0
    - The older version, compatible with inkscape 0.9x is now under the directory 0.9x.
    - latex support now uses an updated version of textext (https://github.com/textext/textext), simplifying installation.

inkscapeMadeEasy_Base.py
   - getDocumentScale() was renamed as getDocumentScaleFactor
   - scaleElement() Changed scaleY=0.0 to scaleY = None to indicate scaleY=scaleX.
   - blankSVG: new member variable with a string representing a blank svg file

inkscapeMadeEasy_Draw.py
   - arc.startEndRadius and arc.centerAngStartAngEnd now have a new argument, 'arcType' that replace and extends the old 'flagOpen' argument
   - new function color.rgb() that accepts normalized input color values in the range 0.0-1.0
   - the function marker.createInfLineMarker was renamed as marker.createElipsisMarker
   - the argument 'fillColor' of marker.createCrossMarker was removed.
   - the argument 'strokeColor' of marker.createElipsisMarker was removed.

inkscapeMadeEasty_Plot.py
  - axis.cartesian
      - the argument ExtraLenghtAxisX was renamed as ExtraLengthAxisX
      - the argument ExtraLenghtAxisY was renamed as ExtraLengthAxisY
  - axis.polar
      - the argument ExtraLenghtAxisR was renamed as ExtraLengthAxisR
  - plot.cartesian
      - the argument ExtraLenghtAxisX was renamed as ExtraLengthAxisX
      - the argument ExtraLenghtAxisY was renamed as ExtraLengthAxisY
  - plot.polar
      - the argument ExtraLenghtAxisR was renamed as ExtraLengthAxisR
  - plot.stem
      - the argument ExtraLenghtAxisX was renamed as ExtraLengthAxisX
      - the argument ExtraLenghtAxisY was renamed as ExtraLengthAxisY


2020-01jan-12
-------------

inkscapeMadeEasy_Base.py
  - Added a new function: importSVG


2020-01jan-11
-------------

added LaTeX installation instructions for windows users.

inkscapeMadeEasy_Base.py
  - Now ungroup method returns a list with the elements previously contained in the removed group

2020-01jan-05
-------------

inkscapeMadeEasy_Base.py
  - Added a new functions: unifyDefs, getDefsByTag, getDefsById, ungroup
  - Changed the name of getElemAtrib -> getElemAttrib
  - method getPoints also can process <use> nodes

inkscapeMadeEasy_Draw.py
  - Modified text.latex method to try to fix some issues under Windows.

2020-01jan-02
-------------

inkscapeMadeEasy_Draw.py
  - Added a new class: cubicBezier
  - Added new option for line.absCoords and line.relCoords. Now it is possible to close the path, connecting the
start and end points.
  - fixed documentation

inkscapeMadeEasy_Base.py
  - Added a new function: exportSVG, getDocumentScale
  - fixed documentation

inkscapeMadeEasy_Plot.py
  - fixed documentation

2019-12dec-29
-------------

inkscapeMadeEasy_Base.py
  - Added a new function: getDocumentScale
  - new optional argument for scaleElement function.

2019-12dec-22
-------------

inkscapeMadeEasy_Draw.py
  - fixed a bug introduced in my last commit

2019-12dec-17
-------------

inkscapeMadeEasy_Base.py
  - added new function: copyElement
  - fixed documentation
  - reformatted the code using pycharm

inkscapeMadeEasy_Draw.py, inkscapeMadeEasy_Plot.py
  - fixed documentation
  - reformatted the code using pycharm

2019-04apr-04
-------------

 - fixed documentation on installation procedure

2018-11nov-14
-------------

inkscapeMadeEasy_Base.py
  - added new functions: getElemFromXpath, getElemAtrib, getDocumentName, getDocumentUnit, getcurrentLayer, unit2userUnit, userUnit2unit, unit2unit

2018-07jul-31
-------------

inkscapeMadeEasy_Base.py
  - added two new functions: getSegmentParameters and getSegmentFromPoints
  - Removed the GUI of the textex module and its dependencies with GUI modules. It might be easier now to run the extensions under Windows/Mac

2017-11nov-19
-------------

inkscapeMadeEasy_Base.py
  - added a function to erase elements:  removeElement(element)
  - escaped some backslashes missing in the documentation sections. This caused issues for some users.


2017-08aug-04
-------------

inkscapeMadeEasy_Draw.py
  - now text.write() allows multi-line text.

2017-05may-18
-------------

inkscapeMadeEasy_Draw.py
  - fixed documentation on predefined color 'purple'

2017-05may-06
-------------

inkscapeMadeEasy_Draw.py
  - added a class and two methods to draw rectangles.

2017-06jun-18
-------------

inkscapeMadeEasy_Base.py
  - fix a bug in getPoints method.

2016-11nov-02
-------------

inkscapeMadeEasy_Draw.py
  - fix text.latex() method in case LaTeX support is disabled. There was a bug when angleDeg was different than zero.

2016-11nov-02
-------------

inkscapeMadeEasy_Draw.py
  - small modification in text.latex() method to fix incompatibility with temporary diretory under windows.

2016-10oct-31
-------------

inkscapeMadeEasy_Draw.py, inkscapeMadeEasy_Plot.py
  - LaTeX support is now optional. See documentation on how to enable/disable it.


2016-10oct-28
-------------

inkscapeMadeEasy_Base.py
  - Changes in inkscapeMadeEasy.getPoints() to become compatible with Python 2.6

2016-10oct-12
-------------

inkscapeMadeEasy_Base.py
  - Fix inkscapeMadeEasy.displayMsg() definition.


2016-09sep-21
-------------

inkscapeMadeEasy_Base.py
  - New method inkscapeMadeEasy.displayMsg() to show messages to the user

inkscapeMadeEasy_Draw.py
  - New method displayMsg() to show messages to the user
  - Minor documentation changes

inkscapeMadeEasy_Plot.py
  - New method displayMsg() to show messages to the user
  - Changed argument names containing '__Mark__' to '__Tick__' to comply with other plotting packages. Attention: This might break your code.
