#!/usr/bin/python

# --------------------------------------------------------------------------------------
#
#    inkscapeMadeEasy: - Helper module that extends Aaron Spike's inkex.py module,
#                        focusing productivity in inkscape extension development
#
#    Copyright (C) 2016 by Fernando Moura
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------

# Please uncomment (remove the # character) in the following line to disable LaTeX support via textext extension.
# useLatex=False


import os
import sys

try:
    useLatex
except NameError:
    useLatex = True
else:
    useLatex = False

import math

import numpy as np

import inkex
from lxml import etree
import re

if useLatex:
    sys.path.append('../textext')
    import textext.base as textext

import tempfile
import copy

def displayMsg(msg):
    """Display a message to the user.

    :param msg: message
    :type msg: string

    :returns: nothing
    :rtype: -

    .. note:: Identical function has been also defined inside :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy` class

    """
    sys.stderr.write(msg + '\n')


def Dump(obj, file='./dump_file.txt', mode='w'):
    """Function to easily output the result of ``str(obj)`` to a file

    :param obj: python object to sent to a file. Any object can be used, as long as ``str(obj)`` is implemented (see ``__str__()`` metaclass definition of your object)
    :param file: file path. Default: ``./dump_file.txt``
    :param mode: writing mode of the file Default: ``w`` (write)
    :type obj: any
    :type file: string
    :type mode: string
    :returns: nothing
    :rtype: -

    .. note:: Identical function has been also defined inside :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy` class

    This function was created to help debugging the code while it is running under inkscape. Since inkscape does not possess a terminal as today (2016),
    this function overcomes partially the issue of sending things to stdout by dumping result of the function ``str()`` in a text file.

    **Example**

    >>> vector1=[1,2,3,4,5,6]
    >>> inkDraw.Dump(vector1,file='~/temporary.txt',mode='w')   # writes the list to a file
    >>> vector2=[7,8,9,10]
    >>> inkDraw.Dump(vector2,file='~/temporary.txt',mode='a')   # append the list to a file
    """

    with open(file, mode) as file:
        file.write(str(obj) + '\n')


def circle3Points(P1, P2, P3):
    """Find the center and radius of a circle based on 3 points on the circle.

    Returns [None,None] either if the points are aligned and no (finite radius) circle can be defined or if two of the points are coincident.

    :param P1,P2,P3: points [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!
    :type P1,P2,P3: list

    :returns: [center, radius]
    :rtype: [numpy array, float]

    """
    # check if points are aligned
    v1 = np.array(P1) - np.array(P2)
    v2 = np.array(P1) - np.array(P3)

    if np.sqrt((v1[0] ** 2 + v1[1] ** 2))==0  or  np.sqrt((v2[0] ** 2 + v2[1] ** 2))==0:
        displayMsg('Error: Two of the points are coincident. Aborting it...')
        return [None, None]

    v1 = v1 / np.sqrt((v1[0] ** 2 + v1[1] ** 2))
    v2 = v2 / np.sqrt((v2[0] ** 2 + v2[1] ** 2))
    cosTheta = v1.dot(v2)

    if abs(cosTheta) > 0.99999:
        displayMsg('Error: The 3 points are collinear (or very close). Aborting it...')
        return [None, None]

    # find the center
    A = np.array([[-2 * P1[0], -2 * P1[1], 1], [-2 * P2[0], -2 * P2[1], 1], [-2 * P3[0], - 2 * P3[1], 1]])
    b = np.array([-P1[0] ** 2 - P1[1] ** 2, -P2[0] ** 2 - P2[1] ** 2, -P3[0] ** 2 - P3[1] ** 2])
    x = np.linalg.solve(A, b)
    center = np.array([x[0], x[1]])
    radius = np.sqrt(x[0] ** 2 + x[1] ** 2 - x[2])
    return [center, radius]

class color():
    """
    This class manipulates color information, generating a string in inkscape's expected format ``#RRGGBBAA``

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.

    """

    @staticmethod
    def defined(colorName,alpha=1.0):
        """ Return the color string representing a predefined color name

        :param colorName: prededined color name. See figure below
        :type colorName: string
        :param alpha: alpha channel. Values between 0.0 and 1.0
        :type alpha: float
        :returns:  string representing the color in inkscape's expected format ``#RRGGBBAA``
        :rtype: string

        **Available pre defined colors**

        .. image:: ../imagesDocs/Default_colors.png
          :width: 400px

        **Example**

        >>> colorString = inkDraw.color.defined('red',1.0)        # returns #ff0000ff representing red color

        """
        if colorName not in ['Dred', 'red', 'Lred', 'Dblue', 'blue', 'Lblue', 'Dgreen', 'green', 'Lgreen', 'Dyellow', 'yellow', 'Lyellow', 'Dmagen',
                             'magen', 'Lmagen', 'black', 'white']:
            sys.exit("InkscapeDraw.color.defined() :  Error. color -->" + colorName + "<-- not defined")

        if colorName == 'Dred':
            colorStr = '#800000'
        if colorName == 'red':
            colorStr = '#FF0000'
        if colorName == 'Lred':
            colorStr = '#FF8181'

        if colorName == 'Dblue':
            colorStr = '#000080'
        if colorName == 'blue':
            colorStr = '#0000FF'
        if colorName == 'Lblue':
            colorStr = '#8181FF'

        if colorName == 'Dgreen':
            colorStr = '#008000'
        if colorName == 'green':
            colorStr = '#00FF00'
        if colorName == 'Lgreen':
            colorStr = '#81FF81'

        if colorName == 'black':
            colorStr = '#000000'
        if colorName == 'white':
            colorStr = '#FFFFFF'

        if colorName == 'Dyellow':
            colorStr = '#808000'
        if colorName == 'yellow':
            colorStr = '#FFFF00'
        if colorName == 'Lyellow':
            colorStr = '#FFFF81'

        if colorName == 'Dmagen':
            colorStr = '#800080'
        if colorName == 'magen':
            colorStr = '#FF00FF'
        if colorName == 'Lmagen':
            colorStr = '#FF81FF'

        colorStr += color.val2hex(alpha*255)

        return colorStr

    @staticmethod
    def RGB(RGBlist,alpha=255):
        """ return a string representing a color specified by RGB level in the range 0-255

        :param RGBlist: list containing RGB levels in the range 0-225 each
        :type RGBlist: list of ints
        :param alpha: alpha channel. Values in the range 0-225. Default: 255
        :type alpha: int
        :returns:  string representing the color in inkscape's expected format ``#RRGGBBAA``
        :rtype: string

        **Example**

        >>> colorString = inkDraw.color.RGB([120,80,0],255)        # returns a string representing the color R=120, G=80, B=0, A=255

        """
        hexVal='#'
        for c in RGBlist:
            hexVal += color.val2hex(c)

        hexVal += color.val2hex(alpha)
        return hexVal

    @staticmethod
    def rgb(RGBlist,alpha=1.0):
        """ Return a string representing a color specified by RGB level in the range 0.0-1.0

        :param RGBlist: list containing RGB levels in the range 0.0-1.0 each
        :type RGBlist: list of floats
        :param alpha: alpha channel. Values in the range 0.0-1.0. Default: 1.0
        :type alpha: int
        :returns:  string representing the color in inkscape's expected format ``#RRGGBBAA``
        :rtype: string

        **Example**

        >>> colorString = color.rgb([0.5,0.8,0.0],255)                   # returns a string representing the color R=127, G=204, B=0, A=255

        """
        hexVal='#'
        for c in RGBlist:
            hexVal += color.val2hex(c*255)

        hexVal += color.val2hex(alpha*255)
        return hexVal

    # ---------------------------------------------
    @staticmethod
    def gray(percentage,alpha=1.0):
        """ Return a string representing a gray color based on white percentage between 0.0 (black) and 1.0 (white)

         - if percentage is higher than 1.0, percentage is truncated to 1.0 (white)
         - if percentage is lower than 0.0, percentage is truncated to 0.0 (black)

        :param percentage: value between 0.0 (black) and 1.0 (white)
        :type percentage: float
        :param alpha: alpha channel. Values in the range 0.0-1.0. Default: 1.0
        :type alpha: int
        :returns: string representing the color in inkscape's expected format ``#RRGGBBAA``
        :rtype: string

        **Example**

        >>> colorString = color.gray(0.6,1.0)                   # returns a string representing the gray level with 60% of white, alpha=100%

        """

        return color.rgb([percentage] * 3,alpha)

    @staticmethod
    def val2hex(value):
        """ return a string representing a color specified by level in the range 0-255

        If value is not in the range 0-255, the result will be truncated in this range

        :param value: color value in the range 0-255
        :type value: int
        :returns:  string representing the color in hexadecimal
        :rtype: string

        **Example**


        >>> colorString = color.val2hex(255)                   # returns FF
        >>> colorString = color.val2hex(127)                   # returns 7F
        >>> colorString = color.val2hex(-1)                   # returns 00
        >>> colorString = color.val2hex(300)                   # returns FF

        """
        if value > 255:
            value = 255
        if value < 0.0:
            value = 0

        if value < 16:
            hexVal = '0' + hex(int(value))[2:].upper()
        else:
            hexVal = hex(int(value))[2:].upper()
        return hexVal

    @staticmethod
    def splitColorAlpha(colorString):
        """ Split color and alpha channel from colorSting in #RRGGBBAA format

        :param:  string representing the color in hexadecimal in #RRGGBBAA format
        :type: string
        :returns: a list of strings: [color,alpha]
                    - color: string in ``#RRGGBB`` format
                    - alpha: string in ``AA`` format
        :rtype: list


        **Example**

        >>> colorComponents = color.splitColorAlpha('#FFF700FF')                   # returns ['#FFF700', 'FF']

        """

        return [colorString[0:7],colorString[7:]]

    # ---------------------------------------------
    @staticmethod
    def colorPickerToRGBalpha(colorPickerString):
        """ Function that converts the string returned by  the widget 'color' in the .inx file into 2 strings,
        one representing the color in format ``#RRGGBB`` and the other representing the alpha channel ``AA``

        .. hint:: you probably don't need to use this function. Consider using the method :meth:`color.parseColorPicker`

        :param colorPickerString: string returned by 'color' widget
        :type colorPickerString: string
        :returns: a list of strings: [color,alpha]
                    - color: string in ``#RRGGBB`` format
                    - alpha: string in ``AA`` format
        :rtype: list


        .. note:: For more information on this widget, see `this <http://wiki.inkscape.org/wiki/index.php/INX_Parameters>`_.

        **Usage**

        1-  You must have one parameter of the type 'color' in your inx file::

          <param name="myColorPicker" type="color"></param>

        2- Parse it as a string in your .py file::

           self.OptionParser.add_argument("--myColorPicker", type=str, dest="myColorPickerVar", default='#00000000')

        3- call this function to convert self.options.myColorPickerVar into two strings
                 - #RRGGBB   with RGB values in hex
                 - AA       with alpha value in hex

        **Example**

        Let your .inx file contain a widget of type 'color' with the name myColorPicker::

        <param name="myColorPicker" type="color"></param>

        Then in the .py file

         >>> import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
         >>> import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
         >>> import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot
         >>>
         >>> class myExtension(inkBase.inkscapeMadeEasy):
         >>>   def __init__(self):
         >>>     inkBase.inkscapeMadeEasy.__init__(self)
         >>>     self.OptionParser.add_argument("--myColorPicker", type=str, dest="myColorPickerVar", default='#000000FF')  # parses the input parameter
         >>>
         >>>   def effect(self):
         >>>     color,alpha = inkDraw.color.colorPickerToRGBalpha(self.options.myColorPickerVar)       # returns the string representing the selected color and alpha channel

        """
        # [2:] removes the 0x ,  zfill adds the leading zeros, upper: uppercase
        colorHex = hex(int(colorPickerString) & 0xffffffff)[2:].zfill(8).upper()
        RGB = '#' + colorHex[0:6]
        alpha = colorHex[6:]
        return [RGB, alpha]

    # ---------------------------------------------
    @staticmethod
    def parseColorPicker(stringColorOption, stringColorPicker):
        """ Function that converts the string returned by  the widgets 'color' and 'optiongroup' in the .inx file into a string,
        in format ``#RRGGBBAA``

        You must have in your .inx both 'optiongroup' and 'color' widgets as defined below. You don't have to have all the color options presented in the example.
        The example presents the most complete list with all the default colors in color.defined method.


        :param stringColorOption: string returned by 'optiongroup' widget
        :type stringColorOption: string
        :param stringColorPicker: string returned by 'color' widget
        :type stringColorPicker: string
        :returns: color string in ``#RRGGBBAA`` format
        :rtype: string

        .. note:: For more information on this widget, see `this link <http://wiki.inkscape.org/wiki/index.php/INX_Parameters>`_

        **Example**

        It works in the following manner: The user select in the optiongroup list the desired color. All pre defined colors in inkscapeMadeEasy are listed there.
        There is also a 'my default color' option where you can set your preferred default color and an 'use color picker' option to activate the color picker widget.
        Keep in mind that the selected color in the color picker widget will be considered **ONLY** if 'use color picker' option is selected.

          a) Example with full form of ``color`` widget. In this example a ``use color picker`` is selected from the optiongroup widget. Therefore the color picker widget will have effect

            .. image:: ../imagesDocs/colorPicker02.png
              :width: 400px

          b) Example with compact form of ``color`` widget. In this example a color is selected from the optiongroup widget. Therefore the color picker widget will have no effect

            .. image:: ../imagesDocs/colorPicker01.png
              :width: 400px

        Bellow is the template 'color' widget with name 'myColorPicker' and an 'optiongroup' with the name 'myColorOption' for the .inx file::

         <param name="myColorOption" type="optiongroup" appearance="minimal" _gui-text="some text here">
             <_option value="#FF0022FF">my default color</_option>    <--you can set your pre define color in the form #RRGGBBAA
             <_option value="none">none</_option>                   <-- no color
             <_option value="black">black</_option>
             <_option value="red">red</_option>
             <_option value="blue">blue</_option>
             <_option value="yellow">yellow</_option>
             <_option value="green">green</_option>          <-- these are all standardized colors in inkscapeMadeEasy_Draw.color class!
             <_option value="magen">magenta</_option>
             <_option value="white">white</_option>
             <_option value="Lred">Lred</_option>
             <_option value="Lblue">Lblue</_option>
             <_option value="Lyellow">Lyellow</_option>
             <_option value="Lgreen">Lgreen</_option>
             <_option value="Lmagen">Lmagenta</_option>
             <_option value="Dred">Dred</_option>
             <_option value="Dblue">Dblue</_option>
             <_option value="Dyellow">Dyellow</_option>
             <_option value="Dgreen">Dgreen</_option>
             <_option value="Dmagen">Dmagenta</_option>
             <_option value="picker">use color picker</_option>     <-- indicate that the color must be taken from the colorPicker attribute
         </param>
         <param name="myColorPicker" type="color"></param>

        Then in the .py file

        >>> import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
        >>> import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot
        >>>
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     inkBase.inkscapeMadeEasy.__init__(self)
        >>>     self.OptionParser.add_argument("--myColorPicker", type=str, dest="myColorPickerVar", default='0')       # parses the input parameters
        >>>     self.OptionParser.add_argument("--myColorOption", type=str, dest="myColorOptionVar", default='black')   # parses the input parameter
        >>> 
        >>>   def effect(self):
        >>>     so = self.options
        >>>     colorString = inkDraw.color.parseColorPicker(so.myColorOptionVar,so.myColorPickerVar)

        """
        if stringColorOption.startswith("#"):
            return stringColorOption
        else:
            if stringColorOption == 'none':
                colorString = 'none'
            else:
                if stringColorOption == 'picker':
                    [colorString, alphaString] = color.colorPickerToRGBalpha(stringColorPicker)
                    colorString += alphaString
                else:
                    colorString = color.defined(stringColorOption)
        return colorString


class marker():
    """
    Class to manipulate markers.

    This class is used to create new custom markers. Markers can be used with the :meth:`inkscapeMadeEasy_Draw.lineStyle` class to define line types that include start, mid and end markers

    The base method of this class is :meth:`marker.createMarker` that can create custom markers. There are also other methods that simplify the creation of commonly used markers. The implemented predefined markers are presented in the figure below.

    .. image:: ../imagesDocs/marker_predefined.png
        :width: 400px

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.

    """

    # ---------------------------------------------
    @staticmethod
    def createMarker(ExtensionBaseObj, nameID, markerPath, RenameMode=0, strokeColor=color.defined('black'), fillColor=color.defined('black'),
                     lineWidth=1.0, markerTransform=None):
        """Create a custom line marker

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param nameID: nameID of the marker
        :param markerPath: Path definition. Must follow 'd' attribute format. See `this link <https://www.w3.org/TR/SVG/paths.html#PathElement>`_ for further information
        :param RenameMode: Renaming behavior mode

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified.
             - 1: overwrite marker definition if nameID is already taken

                .. Warning:: when a marker is created using RenameMode=1, any marker with the same name will disapear from inkscape's canvas. This is an inkscape issue. Save the document and reload it, everything should be fine.
             - 2: Create a new unique nameID, adding a suffix number (Please refer to :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy.uniqueIdNumber()`
        :param strokeColor: Stroke color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :param fillColor: Filling color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :param lineWidth: Line width of the marker. Default: 1.0
        :param markerTransform: custom transform applied to marker's path. Default: ``None``

           .. note:: The transform must follow 'transform' attribute format. See `this link <https://www.w3.org/TR/SVG/coords.html#TransformAttribute>`_ for further information

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type nameID: string
        :type markerPath: string
        :type RenameMode: int
        :type strokeColor: string
        :type fillColor: string
        :type lineWidth: float
        :type markerTransform: string

        :returns: NameID of the new marker
        :rtype: string

        **System of coordinates**

        The system of coordinates of the marker depends on the point under consideration. The following figure presents the coordinate system for all cases

        .. image:: ../imagesDocs/marker_Orientation.png
          :width: 600px

        **Example**

        >>> nameID='myMarker'
        >>> markerPath='M 3,0 L 0,1 L 0,-1 z'   # defines a path forming an triangle with vertices (3,0) (0,1) (0,-1)
        >>> strokeColor=inkDraw.color.defined('red')
        >>> fillColor=None
        >>> RenameMode=1
        >>> width=1
        >>> markerTransform=None
        >>> markerID=inkDraw.marker.createMarker(self,nameID,markerPath,RenameMode,strokeColor,fillColor,width,markerTransform)
        >>> myLineStyle = inkDraw.lineStyle.set(1.0, markerEnd=markerID,lineColor=inkDraw.color.defined('black'))  # see lineStyle class for further information on this function
        >>> 
        >>> #tries to make another marker with the same nameID, changing RenameMode
        >>> strokeColor=inkDraw.color.defined('blue')
        >>> RenameMode=0
        >>> markerID=inkDraw.marker.createMarker(self,nameID,RenameMode,scale,strokeColor,fillColor) # this will not modify the marker
        >>> RenameMode=1
        >>> markerID=inkDraw.marker.createMarker(self,nameID,RenameMode,scale,strokeColor,fillColor) # modifies the marker 'myMarker'
        >>> RenameMode=2
        >>> markerID=inkDraw.marker.createMarker(self,nameID,RenameMode,scale,strokeColor,fillColor) # creates a new marker with nameID='myMarker-0001'

        .. note:: In the future, path definition and transformation will be modified to make it easier to design custom markers. =)
        """

        if RenameMode == 0 and ExtensionBaseObj.findMarker(nameID):
            return nameID

        if RenameMode == 2:
            numberID = 1
            new_id = nameID + '_n%05d' % numberID
            while new_id in ExtensionBaseObj.svg.get_ids():
                numberID += 1
                new_id = nameID + '_n%05d' % numberID
            ExtensionBaseObj.svg.get_ids().add(nameID)
            nameID = new_id

        if RenameMode == 1 and ExtensionBaseObj.findMarker(nameID):
            defs = ExtensionBaseObj.getDefinitions()
            for obj in defs.iter():
                if obj.get('id') == nameID:
                    defs.remove(obj)

        # creates a new marker
        marker_attribs = {inkex.addNS('stockid', 'inkscape'): nameID, 'orient': 'auto', 'refY': '0.0', 'refX': '0.0', 'id': nameID,
                          'style': 'overflow:visible'}

        newMarker = etree.SubElement(ExtensionBaseObj.getDefinitions(), 'marker', marker_attribs)

        if fillColor is None:
            fillColor = 'none'
            opacityFill = '1.0'
        if strokeColor is None:
            strokeColor = 'none'
            opacityStroke = '1.0'

        # set color and opacity
        if fillColor.startswith('#'):
            [fillColor,alphaFill] = color.splitColorAlpha(fillColor)
            opacityFill = str(int(alphaFill, 16)/255.0)

        if strokeColor.startswith('#'):
            [strokeColor, alphaStroke] = color.splitColorAlpha(strokeColor)
            opacityStroke = str(int(alphaStroke, 16)/255.0)

        marker_style = {'fill-rule': 'evenodd', 'fill': fillColor, 'stroke': strokeColor, 'stroke-width': str(lineWidth),'fill-opacity':opacityFill,'stroke-opacity':opacityStroke}

        marker_lineline_attribs = {'d': markerPath, 'style': str(inkex.Style(marker_style))}

        if markerTransform:
            marker_lineline_attribs['transform'] = markerTransform

        etree.SubElement(newMarker, 'path', marker_lineline_attribs)

        ExtensionBaseObj.svg.get_ids().add(nameID)

        return nameID

    # ---------------------------------------------
    @staticmethod
    def createDotMarker(ExtensionBaseObj, nameID, RenameMode=0, scale=0.4, strokeColor=color.defined('black'), fillColor=color.defined('black')):
        """Create circular dot markers, exactly like inkscape default dotS dotM or dotL markers.

        .. image:: ../imagesDocs/marker_predefined_dot.png
          :width: 300px
          :align: center

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param nameID: nameID of the marker
        :param RenameMode: Renaming behavior mode

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified.
             - 1: overwrite marker definition if nameID is already taken

                .. Warning:: when a marker is created using RenameMode=1, any marker with the same name will disapear from inkscape's canvas. This is an inkscape issue. Save the document and reload it, everything should be fine.
             - 2: Create a new unique nameID, adding a suffix number (Please refer to :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy.uniqueIdNumber()`
        :param scale: Scale factor of the marker. To exactly copy inkscape sizes dotS/M/L, use 0.2, 0.4 and 0.8 respectively. Default: 0.4
        :param strokeColor: Stroke color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :param fillColor: Filling color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type nameID: string
        :type RenameMode: int
        :type scale: float
        :type strokeColor: string
        :type fillColor: string    

        :returns: NameID of the new marker
        :rtype: string

        **Example**

        >>> myMarker=inkDraw.marker.createDotMarker(self,nameID='myDotMarkerA',RenameMode=1,scale=0.5,strokeColor=inkDraw.color.defined('red'),fillColor=None)
        >>> myLineStyle = inkDraw.lineStyle.set(1.0, markerEnd=myMarker,lineColor=inkDraw.color.defined('black'))  # see lineStyle class for further information on this function
        """

        markerPath = 'M -2.5,-1.0 C -2.5,1.7600000 -4.7400000,4.0 -7.5,4.0 C -10.260000,4.0 -12.5,1.7600000 -12.5,-1.0 C -12.5,-3.7600000 -10.260000,-6.0 -7.5,-6.0 C -4.7400000,-6.0 -2.5,-3.7600000 -2.5,-1.0 z '
        width = 1.0
        markerTransform = 'scale(' + str(scale) + ') translate(7.4, 1)'
        return marker.createMarker(ExtensionBaseObj, nameID, markerPath, RenameMode, strokeColor, fillColor, width, markerTransform)

    # ---------------------------------------------
    @staticmethod
    def createCrossMarker(ExtensionBaseObj, nameID, RenameMode=0, scale=0.4, strokeColor=color.defined('black')):
        """Create a cross marker

        .. image:: ../imagesDocs/marker_predefined_cross.png
          :width: 300px
          :align: center

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param nameID: nameID of the marker
        :param RenameMode: Renaming behavior mode

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified.
             - 1: overwrite marker definition if nameID is already taken

                .. Warning:: when a marker is created using RenameMode=1, any marker with the same name will disapear from inkscape's canvas. This is an inkscape issue. Save the document and reload it, everything should be fine.
             - 2: Create a new unique nameID, adding a suffix number (Please refer to :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy.uniqueIdNumber()`
        :param scale: Scale of the marker. Default: 0.4
        :param strokeColor: Stroke color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type nameID: string
        :type RenameMode: int
        :type scale: float
        :type strokeColor: string

        :returns: NameID of the new marker
        :rtype: string

        **Example**

        >>> myMarker=inkDraw.marker.createCrossMarker(self,nameID='myDotMarkerA',RenameMode=1,scale=0.5,strokeColor=inkDraw.color.defined('red'))
        >>> myLineStyle = inkDraw.lineStyle.set(1.0, markerEnd=myMarker,lineColor=inkDraw.color.defined('black'))  # see lineStyle class for further information on this function
        """

        markerPath = 'M -4,4 L 4,-4 M 4,4 L -4,-4'
        markerTransform = 'scale(' + str(scale) + ')'
        width = 1.0
        return marker.createMarker(ExtensionBaseObj, nameID, markerPath, RenameMode, strokeColor, None, width, markerTransform)

    # ---------------------------------------------
    @staticmethod
    def createArrow1Marker(ExtensionBaseObj, nameID, RenameMode=0, scale=0.4, strokeColor=color.defined('black'), fillColor=color.defined('black')):
        """Create arrow markers (both start and end markers)

        .. image:: ../imagesDocs/marker_predefined_arrow.png
          :width: 300px
          :align: center

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param nameID: nameID of the marker.

            .. note:: Start and End markers will have 'Start' and 'End' suffixes respectively

        :param RenameMode: Renaming behavior mode

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified.
             - 1: overwrite marker definition if nameID is already taken

                .. Warning:: when a marker is created using RenameMode=1, any marker with the same name will disapear from inkscape's canvas. This is an inkscape issue. Save the document and reload it, everything should be fine.
             - 2: Create a new unique nameID, adding a suffix number (Please refer to :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy.uniqueIdNumber()`

        :param scale: scale of the marker. Default: 0.4
        :param strokeColor: Stroke color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :param fillColor: Filling color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type nameID: string
        :type RenameMode: int
        :type scale: float
        :type strokeColor: string
        :type fillColor: string    

        :returns: a list of strings: [startArrowMarker,endArrowMarker]
                    - startArrowMarker: nameID of start marker
                    - endArrowMarker: nameID of end marker
        :rtype: list

        **Example**

        >>> StartArrowMarker,EndArrowMarker=inkDraw.marker.createArrow1Marker(self,nameID='myArrow',RenameMode=1,scale=0.5,strokeColor=inkDraw.color.defined('red'),fillColor=None)
        >>> myLineStyle = inkDraw.lineStyle.set(1.0, markerStart=StartArrowMarker,markerEnd=EndArrowMarker,lineColor='#000000')  # see lineStyle class for further information on this function
        """

        # transform="scale(0.8) rotate(180) translate(12.5,0)" />
        # transform="scale(0.4) rotate(180) translate(10,0)" />
        # transform="scale(0.2) rotate(180) translate(6,0)" />
        # translation=12.5-17.5/(scale*10)
        # linear regression from data of small medium and large
        translation = 10.17 * scale + 4.75
        width = 1.0

        markerPath = 'M 0.0,0.0 L 5.0,-5.0 L -12.5,0.0 L 5.0,5.0 L 0.0,0.0 z '
        markerTransform = 'scale(' + str(scale) + ') rotate(0) translate(' + str(translation) + ',0)'
        nameStart = marker.createMarker(ExtensionBaseObj, nameID + 'Start', markerPath, RenameMode, strokeColor, fillColor, width, markerTransform)
        markerTransform = 'scale(' + str(scale) + ') rotate(180) translate(' + str(translation) + ',0)'
        nameEnd = marker.createMarker(ExtensionBaseObj, nameID + 'End', markerPath, RenameMode, strokeColor, fillColor, width, markerTransform)

        return [nameStart, nameEnd]

    # ---------------------------------------------
    @staticmethod
    def createElipsisMarker(ExtensionBaseObj, nameID, RenameMode=0, scale=1.0, fillColor=color.defined('black')):
        """Create ellipsis markers, both start and end markers.

        .. image:: ../imagesDocs/marker_predefined_elipsis.png
          :width: 300px
          :align: center

        .. note:: These markers differ from inkscape's default ellipsis since these markers are made such that the diameter of the dots are equal to the line width.

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param nameID: nameID of the marker. Start and End markers will have 'Start' and 'End' suffix respectively
        :param RenameMode: Renaming behavior mode

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified.
             - 1: overwrite marker definition if nameID is already taken

                .. Warning:: when a marker is created using RenameMode=1, any marker with the same name will disapear from inkscape's canvas. This is an inkscape issue. Save the document and reload it, everything should be fine.
             - 2: Create a new unique nameID, adding a suffix number (Please refer to :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy.uniqueIdNumber()`
        :param scale: Scale of the marker. Default 1.0
        :param fillColor: Filling color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black'). See :meth:`inkscapeMadeEasy_Draw.color` for functions to create color strings
        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type nameID: string
        :type RenameMode: int
        :type scale: float
        :type fillColor: string

        :returns: a list of strings: [startInfMarker,endInfMarker]
                    - startInfMarker: nameID of start marker
                    - endInfMarker: nameID of end marker
        :rtype: list

        **Example**

        >>> startInfMarker,endInfMarker=inkDraw.marker.createElipsisMarker(self,nameID='myInfMarker',RenameMode=1,scale=1.0,fillColor='#00FF00FF')
        >>> myLineStyle = inkDraw.lineStyle.set(1.0, markerStart=startInfMarker,markerEnd=endInfMarker,lineColor='#000000FF')  # see lineStyle class for further information on this function
        """

        # build path for 3 circles
        markerPath = ''
        radius = scale / 2.0

        for i in range(3):

            prefix = 'M %f %f ' % (i * 2 + radius, 0)
            arcStringA = 'a %f %f 0 1 1 %f %f ' % (radius, radius, -2 * radius, 0)
            arcStringB = 'a %f %f 0 1 1 %f %f ' % (radius, radius, 2 * radius, 0)

            markerPath = markerPath + prefix + arcStringA + arcStringB + 'z '

        if scale != 1.0:
            markerTransform = 'translate(' + str(-6.0 * scale) + ', 0) scale(' + str(scale) + ')'
        else:
            markerTransform = 'translate(' + str(-6.0 * scale) + ', 0)'

        width = 1.0
        # add small line segment

        nameStart = marker.createMarker(ExtensionBaseObj, nameID + 'Start', markerPath, RenameMode, None, fillColor, width, markerTransform)

        if scale != 1.0:
            markerTransform = 'translate(' + str(2.0 * scale) + ', 0) scale(' + str(scale) + ')'
        else:
            markerTransform = 'translate(' + str(2.0 * scale) + ', 0)'

        nameEnd = marker.createMarker(ExtensionBaseObj, nameID + 'End', markerPath, RenameMode, None, fillColor, width, markerTransform)

        return [nameStart, nameEnd]


class lineStyle():
    """
    Class to manipulate line styles.

    This class is used to define line styles. It is capable of setting stroke and filling colors, line width, linejoin and linecap, markers (start, mid, and end) and stroke dash array

    The base method of this class is :meth:`lineStyle.set` that can create custom line types.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.

    """

    # ---------------------------------------------
    @staticmethod
    def set(lineWidth=1.0, lineColor=color.defined('black'), fillColor=None, lineJoin='round', lineCap='round', markerStart=None, markerMid=None,
            markerEnd=None, strokeDashArray=None):
        """ Create a new line style

        :param lineWidth: Line width. Default: 1.0
        :param lineColor: Color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fillColor: Color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: ``None``
        :param lineJoin: Shape of the lines at the joints. Valid values 'miter', 'round', 'bevel'. See image below. Default: round.
        :param lineCap: Shape of the lines at the ends. Valid values 'butt', 'square', 'round'. See image below. Default: round
        :param markerStart: Marker at the start node. Default: ``None``
        :param markerMid: Marker at the mid nodes. Default: ``None``
        :param markerEnd: Marker at the end node. Default: ``None``
        :param strokeDashArray: Dashed line pattern definition. Default: ``None``. See `this link <https://www.geeksforgeeks.org/css-stroke-dasharray-property/>`_ for further information

        :type lineWidth: float     
        :type lineColor: string
        :type fillColor: string
        :type lineJoin: string
        :type lineCap: string
        :type markerStart: string
        :type markerMid: string
        :type markerEnd: string
        :type strokeDashArray: string

        :returns: line definition following the provided specifications
        :rtype: string

        **Line node types**

        .. image:: ../imagesDocs/line_nodes.png
          :width: 600px

        **Example**

        >>> # creates a line style using a dot marker at its end node
        >>> myMarker=inkDraw.marker.createDotMarker(self,nameID='myMarker',RenameMode=1,scale=0.5,strokeColor=color.defined('red'),fillColor=None)   # see marker class for further information on this function
        >>> myLineStyle = inkDraw.lineStyle.set(lineWidth=1.0, markerEnd=myMarker,lineColor=inkDraw.color.defined('black'),fillColor=inkDraw.color('red'))
        >>> 
        >>> # creates a line style with dashed line (5 units dash , 10 units space
        >>> myDashedStyle = inkDraw.lineStyle.set(lineWidth=1.0,lineColor=inkDraw.color.defined('black'),fillColor=inkDraw.color,strokeDashArray='5,10')
        >>> # creates a line style with a more complex pattern (5 units dash , 10 units space, 2 units dash, 3 units space
        >>> myDashedStyle = inkDraw.lineStyle.set(lineWidth=1.0,lineColor=inkDraw.color.defined('black'),fillColor=inkDraw.color,strokeDashArray='5,10,2,3')
        """

        if fillColor is None:
            fillColor = 'none'
            opacityFill = '1.0'
        if lineColor is None:
            lineColor = 'none'
            opacityStroke = '1.0'

        # set color and opacity
        if fillColor.startswith('#'):
            [fillColor,alphaFill] = color.splitColorAlpha(fillColor)
            opacityFill = str(int(alphaFill, 16)/255.0)

        if lineColor.startswith('#'):
            [lineColor, alphaLine] = color.splitColorAlpha(lineColor)
            opacityStroke = str(int(alphaLine, 16)/255.0)

        if not strokeDashArray:
            strokeDashArray = 'none'

        # dictionary with the styles
        lineStyle = {'stroke': lineColor, 'stroke-width': str(lineWidth), 'stroke-dasharray': strokeDashArray, 'fill': fillColor,'fill-opacity':opacityFill,'stroke-opacity':opacityStroke}

        # Endpoint and junctions
        lineStyle['stroke-linecap'] = lineCap
        lineStyle['stroke-linejoin'] = lineJoin

        # add markers if needed
        if markerStart:
            lineStyle['marker-start'] = 'url(#' + markerStart + ')'

        if markerMid:
            lineStyle['marker-mid'] = 'url(#' + markerMid + ')'

        if markerEnd:
            lineStyle['marker-end'] = 'url(#' + markerEnd + ')'

        return lineStyle

    # ---------------------------------------------
    @staticmethod
    def setSimpleBlack(lineWidth=1.0):
        """Define a standard black line style.

        The only adjustable parameter is its width. The fixed parameters are: lineColor=black, fillColor=None, lineJoin='round', lineCap='round', no markers, no dash pattern

        :param lineWidth: line width. Default: 1.0
        :type lineWidth: float     

        :returns: line definition following the provided specifications
        :rtype: string

        **Example**

        >>> mySimpleStyle = inkDraw.lineStyle.setSimpleBlack(lineWidth=2.0)

        """
        return lineStyle.set(lineWidth)


class textStyle():
    """
    Class to create text styles.

    This class is used to define text styles. It is capable of setting font size, justification, text color, font family, font style, font weight, line spacing, letter spacing and word spacing

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.

    """

    # ---------------------------------------------
    @staticmethod
    def set(fontSize=10, justification='left', textColor=color.defined('black'), fontFamily='Sans', fontStyle='normal', fontWeight='normal',
            lineSpacing='100%', letterSpacing='0px', wordSpacing='0px'):
        """Define a new text style

        :param fontSize: Size of the font in px. Default: 10
        :param justification: Text justification. ``left``, ``right``, ``center``. Default: ``left``
        :param textColor: Color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fontFamily: Font family name. Default ``Sans``

            .. warning:: This method does NOT verify whether the font family is installed in your machine or not.

        :param fontStyle: ``normal``  or ``italic``. Default: ``normal``
        :param fontWeight: ``normal``  or ``bold``. Default: ``normal``
        :param lineSpacing: Spacing between lines in percentage. Default: ``100%``
        :param letterSpacing: Extra space between letters. Format: ``_px``. Default: ``0px``
        :param wordSpacing: Extra space between words. Format: ``_px``. Default: ``0px``

        :type fontSize: float     
        :type justification: string
        :type textColor: string
        :type fontFamily: string
        :type fontStyle: string
        :type fontWeight: string
        :type lineSpacing: string
        :type letterSpacing: string
        :type wordSpacing: string

        :returns: text style definition following the provided specifications
        :rtype: string

        **Example**

        >>> myTextStyle=inkDraw.textStyle.set(fontSize=10, justification='left', textColor=color.defined('black',0.5), fontFamily='Sans',
        >>>                                   fontStyle='normal', fontWeight='normal', lineSpacing='100%', letterSpacing='0px', wordSpacing='0px')
        """

        if not textColor:
            textColor = 'none'
            opacityFill = '1.0'

        # set color and opacity
        if textColor.startswith('#'):
            [textColor, alphaFill] = color.splitColorAlpha(textColor)
            opacityFill = str(int(alphaFill, 16) / 255.0)

        if justification == 'left':
            justification = 'start'
            anchor = 'start'
        if justification == 'right':
            justification = 'end'
            anchor = 'end'
        if justification == 'center':
            anchor = 'middle'

        textStyle = {'font-size': str(fontSize) + 'px', 'font-style': fontStyle, 'font-weight': fontWeight, 'text-align': justification,
                     # start, center, end
                     'line-height': lineSpacing, 'letter-spacing': letterSpacing, 'word-spacing': wordSpacing, 'text-anchor': anchor,
                     # start, middle, end
                     'fill': textColor, 'fill-opacity': opacityFill, 'stroke': 'none', 'font-family': fontFamily}

        return textStyle

    # ---------------------------------------------
    @staticmethod
    def setSimpleBlack(fontSize=10, justification='left'):
        """Define a standard black text style

        The only adjustable parameter are font size and justification. The fixed parameters are: textColor=color.defined('black'), fontFamily='Sans',
        fontStyle='normal', fontWeight='normal', lineSpacing='100%', letterSpacing='0px', wordSpacing='0px.

        :param fontSize: Size of the font in px. Default: 10
        :param justification: Text justification. ``left``, ``right``, ``center``. Default: ``left``

        :type fontSize: float     
        :type justification: string

        :returns: text style definition following the provided specifications
        :rtype: string

        **Example**

        >>> mySimpleStyle = inkDraw.textStyle.setSimpleBlack(fontSize=20,justification='center')

        """
        return textStyle.set(fontSize, justification)

    # ---------------------------------------------
    @staticmethod
    def setSimpleColor(fontSize=10, justification='left', textColor=color.defined('black')):
        """Define a standard colored text style

        The only adjustable parameter are font size, justification and textColor. The fixed parameters are: fontFamily='Sans', fontStyle='normal',
        fontWeight='normal', lineSpacing='100%', letterSpacing='0px', wordSpacing='0px.

        :param fontSize: Size of the font in px. Default: 10
        :param justification: Text justification. ``left``, ``right``, ``center``. Default: ``left``
        :param textColor: Color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')

        :type fontSize: float     
        :type justification: string
        :type textColor: string

        :returns: text style definition following the provided specifications
        :rtype: string

        **Example**

        >>> mySimpleStyle = inkDraw.textStyle.setSimpleColor(fontSize=20,justification='center',textColor=inkDraw.color.gray(0.5))
        """
        return textStyle.set(fontSize, justification, textColor)


class text():
    """ Class for writing texts.

    This class allows the cration of regular inkscape's text elements or LaTeX text. For the later, TexText is incorporated here.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.
    
    .. warning:: LaTeX support is an optional feature, **enabled by default**. Please refer to :ref:`disableLatexSupport` on how to disable it.
    
    """

    @staticmethod
    def write(ExtensionBaseObj, text, coords, parent, textStyle=textStyle.setSimpleBlack(fontSize=10, justification='left'), fontSize=None,
              justification=None, angleDeg=0.0):
        """Add a text line to the document

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param text: Text contents. Use \\\\n in the string to start a new line
        :param coords: Position [x,y]
        :param parent: Parent object
        :param textStyle: Text style to be used. See class ``textStyle``. Default: textStyle.setSimpleBlack(fontSize=10,justification='left')
        :param fontSize: Size of the font in px.
                - ``None``: Uses fontSize of textStyle argument (Default)
                - number: takes precedence over the size on textStyle
        :param justification: Text justification. ``left``, ``right``, ``center``
                - ``None``: Uses justification of textStyle argument (Default)
                - ``left``, ``right``, ``center``: takes precedence over the justification set on textStyle
        :param angleDeg: Angle of the text, counterclockwise, in degrees. Default: 0

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type text: string
        :type coords: list
        :type parent: inkscape element object
        :type textStyle: textStyle object
        :type fontSize: float
        :type justification: string
        :type angleDeg: float

        :returns: the new text object
        :rtype: text Object

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> mySimpleStyle = inkDraw.textStyle.setSimpleBlack(fontSize=20,justification='center')  # creates a simple text style.
        >>>
        >>> #adds a two-line text, at the point x=5.0,y=6.0
        >>> #               L1: 'foo bar who-hoo!'
        >>> #               L2: 'second line!'
        >>> myText='foo bar who-hoo!\\nsecond line!'
        >>> inkDraw.text.write(self, text=myText, coords=[5.0,6.0], parent=root_layer, textStyle=mySimpleStyle, fontSize=None, justification=None, angleDeg=0.0)
        >>> 
        >>> # creates a group in root-layer and add text to it
        >>> myGroup = self.createGroup(root_layer,'textGroup')
        >>> #adds a text 'foo bar', rotated 45 degrees, at the point x=0,y=0, overriding justification of mySimpleStyle
        >>> inkDraw.text.write(self, text='foo bar', coords=[0.0,0.0], parent=myGroup, textStyle=mySimpleStyle, fontSize=None, justification='left', angleDeg=45.0)

        """

        if justification == 'left':
            textStyle['text-align'] = 'start'
            textStyle['text-anchor'] = 'start'
        if justification == 'right':
            textStyle['text-align'] = 'end'
            textStyle['text-anchor'] = 'end'
        if justification == 'center':
            textStyle['text-align'] = 'center'
            textStyle['text-anchor'] = 'middle'

        if fontSize:
            textStyle['font-size'] = str(fontSize) + 'px'

        AttribsText = {inkex.addNS('space', 'xml'): "preserve", 'style': str(inkex.Style(textStyle)), 'x': str(coords[0]), 'y': str(coords[1]),
                       inkex.addNS('linespacing', 'sodipodi'): textStyle['line-height']}

        # textObj = etree.SubElement(parent, inkex.addNS('text','svg'), AttribsText )

        textObj = etree.Element(inkex.addNS('text', 'svg'), AttribsText)
        parent.append(textObj)

        AttribsLineText = {inkex.addNS('role', 'sodipodi'): "line", 'x': str(coords[0]), 'y': str(coords[1])}

        textLines = text.split('\\n')

        for n in range(len(textLines)):
            myTspan = etree.SubElement(textObj, inkex.addNS('tspan', 'svg'), AttribsLineText)
            myTspan.text = textLines[n]

        if angleDeg != 0:
            ExtensionBaseObj.rotateElement(textObj, center=coords, angleDeg=angleDeg)  # negative angle bc inkscape is upside down

        return textObj

    # ---------------------------------------------
    @staticmethod
    def latex(ExtensionBaseObj, parent, LaTeXtext, position, fontSize=10, refPoint='cc', textColor=color.defined('black'), LatexCommands=' ',
              angleDeg=0, preambleFile=None):
        """Creates text element using LaTeX. You can use any LaTeX contents here.

        .. note:: LaTeX support is an optional feature that requires a few extra packages to be installed outside inkscape. **It is enabled by default**.
            Please refer to :ref:`disableLatexSupport` on how to disable it. If disabled, this function will still work, internally calling the :meth:`text.write`.

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param parent: parent object        
        :param LaTeXtext: Contents of the text. Can contain any latex command
        :param position: Position of the reference point [x,y]
        :param fontSize: Size of the font. Assume any capitql letter of ``\\normalsize`` will have this size. Default: 10
        :param refPoint: Text reference Point. See figure below for options. Default: ``cc``
        :param textColor: Color in the format ``#RRGGBBAA`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param LatexCommands: Commands to be included before LaTeXtext (default: ' '). If LaTeX support is disabled, this parameter has no effect.
        :param angleDeg: Angle of the text, counterclockwise, in degrees. Default: 0
        :param preambleFile: Optional preamble file to be included. Default: None. If LaTeX support is disabled, this parameter has no effect.

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type parent: inkscape element object
        :type LaTeXtext: string
        :type position: list  
        :type fontSize: float
        :type refPoint: string
        :type textColor: string
        :type LatexCommands: string
        :type angleDeg: float
        :type preambleFile: string

        :returns: the new text object
        :rtype: text Object

        .. note:: This function does not use ``textStyle`` class elements.

        **Reference point options**

        .. image:: ../imagesDocs/LaTeX_reference_Point.png
          :width: 300px

        **Standard Preamble file**

        When a preamble file is not provided, inkscapeMadeEasy assumes a standard preamble file located at ``./textextLib/basicLatexPackages.tex``. By default, its contents is::

          \\usepackage{amsmath,amsthm,amsbsy,amsfonts,amssymb}
          \\usepackage[per=slash]{siunitx}
          \\usepackage{steinmetz}
          \\usepackage[utf8]{inputenc}

        You will need these packages installed. This file can be modified to include extra default packages and/or commands.

        **LaTeX .tex document structure**      

        LaTeX .tex document have the following structure. Note that LatexCommands lies within document environment::

          \\documentclass[landscape,a0]{article}

          [contents of Preamble file]

          \\pagestyle{empty}

          \\begin{document}
          \\noindent

          [contents of LatexCommands]

          [contens of LaTeXtext]

          \\end{document}


        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> customCommand = r'\\newcommand{\\fooBar}{\\textbf{Foo Bar Function! WhooHoo!}}'   # do not forget the r to avoid backslash escape.
        >>> inkDraw.text.latex(self, root_layer,r'This is one equation \\begin{align} x=y^2\\end{align} And this is my \\fooBar{}',
        >>>                    position=[0.0,0.0], fontSize=10, refPoint='cc', textColor=inkDraw.color.defined('black'), LatexCommands=customCommand, angleDeg=0, preambleFile=None)
        """
        newTmp = True

        # write an empty svg file.

        if not LaTeXtext:  # check whether text is empty
            return 0

        if useLatex:  # set useLatex=False to replace latex by an standard text (much faster for debugging =)  )

            if newTmp:
                tmpf = tempfile.NamedTemporaryFile(mode='w', prefix='temp_svg_inkscapeMadeEasy_Draw_', suffix='.svg', delete=False)
                tempFilePath = tmpf.name
                tmpf.write(ExtensionBaseObj.blankSVG)
                tmpf.close()
            else:
                tempDir = tempfile.gettempdir()
                tempFilePath = tempDir + '/temp_svg_inkscapeMadeEasy_Draw.txt'
                Dump(ExtensionBaseObj.blankSVG, tempFilePath, 'w')

            # return
            # temp instance for determining font height. Draws a F letter just to find the height of the font
            if False:  # turning off this part of the code.
                texTemp = textext.TexText()  # start textText (awesome extension! =] )
                texTemp.run([r'--text=' + 'F', '--scale-factor=1', tempFilePath], output=os.devnull)

                for child in texTemp.document.getroot():
                    if child.typename == 'TexTextElement':
                        groupLatex = child

                BboxMin, BboxMax = ExtensionBaseObj.getBoundingBox(groupLatex)
                Height0 = BboxMax[1] - BboxMin[1]

                scale = ExtensionBaseObj.getDocumentScaleFactor()
                ExtensionBaseObj.displayMsg('H0=%f\nscaleFactor=%f' % (Height0,scale ))

            else:
                # running the code above, we get a 'F' with height of 6.76, with scale 1.0 from textext. This will be used to scale the text accordingly to fit user specification 'fontSize'
                # Height0 = 6.76
                Height0 = 9.041644

            scale = fontSize / Height0

            tex = textext.TexText()  # start textText (awesome extension! =] )

            if preambleFile:
                tex.run([r'--text=' + LatexCommands + LaTeXtext, '--scale-factor=1', '--preamble-file=' + preambleFile, tempFilePath],
                        output=os.devnull)  # in case we want to save the svg file with the text element, uncomment the fllowing line.  # tex.document.write(tempFilePath)
            else:
                tex.run(
                    [r'--text=' + LatexCommands + LaTeXtext, '--scale-factor=1', '--preamble-file=' + ExtensionBaseObj.getBasicLatexPackagesFile(),
                     tempFilePath], output=os.devnull)

            if newTmp:
                os.unlink(tmpf.name)

            for child in tex.document.getroot():
                if child.typename == 'TexTextElement':
                    groupLatex = child

            if textColor is None:
                textColor = 'none'
                opacityFill = '1.0'

            # set color and opacity
            if textColor.startswith('#'):
                [textColor, alphaFill] = color.splitColorAlpha(textColor)
                opacityFill = str(int(alphaFill, 16) / 255.0)

            # change color
            for obj in groupLatex.iter():
                oldStyle = obj.get('style')
                if oldStyle is not None:
                    newStyle = re.sub('fill:#[0-9a-fA-F]+', 'fill:' + textColor, oldStyle)
                    newStyle = re.sub('fill-opacity:[0-9]+', 'fill-opacity:' + opacityFill, newStyle)
                    newStyle = re.sub('stroke:#[0-9a-fA-F]+', 'stroke:' + textColor, newStyle)
                    newStyle = re.sub('stroke-opacity:[0-9]+', 'stroke-opacity:' + opacityFill, newStyle)
                    obj.set('style', newStyle)

            ExtensionBaseObj.scaleElement(groupLatex, scaleX=scale, scaleY=scale)  # scale to fit font size
        else:
            if refPoint[1] == 'l':
                justification = 'left'

            if refPoint[1] == 'c':
                justification = 'center'

            if refPoint[1] == 'r':
                justification = 'right'

            mytextStyle = textStyle.setSimpleColor(fontSize=fontSize / 0.76, justification='left', textColor=textColor)
            groupLatex = text.write(ExtensionBaseObj, LaTeXtext, [0, 0], parent, textStyle=mytextStyle, fontSize=fontSize / 0.76,
                                    justification=justification, angleDeg=0.0)  # attention! keep angleDeg=0.0 here bc it will be rotated below

        parent.append(groupLatex)

        BboxMin, BboxMax = ExtensionBaseObj.getBoundingBox(groupLatex)

        if useLatex:  # set useLatex=False to replace latex by an standard text (much faster for debugging =)  )
            if refPoint[0] == 't':
                refPointY = BboxMin[1]  # BboxMin bc inkscape is upside down

            if refPoint[0] == 'c':
                refPointY = (BboxMax[1] + BboxMin[1]) / 2.0

            if refPoint[0] == 'b':
                refPointY = BboxMax[1]  # BboxMax bc inkscape is upside down

            if refPoint[1] == 'l':
                refPointX = BboxMin[0]

            if refPoint[1] == 'c':
                refPointX = (BboxMax[0] + BboxMin[0]) / 2.0

            if refPoint[1] == 'r':
                refPointX = BboxMax[0]
        else:
            refPointX = BboxMin[0]
            if refPoint[0] == 't':
                refPointY = BboxMin[1] - fontSize  # BboxMin bc inkscape is upside down

            if refPoint[0] == 'c':
                refPointY = BboxMin[1] - fontSize / 2.0  # BboxMin bc inkscape is upside down

            if refPoint[0] == 'b':
                refPointY = BboxMax[1]  # BboxMax bc inkscape is upside down

        ExtensionBaseObj.moveElement(groupLatex, [-refPointX, -refPointY])  # move to origin
        ExtensionBaseObj.moveElement(groupLatex, [position[0], position[1]])
        if angleDeg != 0:
            ExtensionBaseObj.rotateElement(groupLatex, center=[position[0], position[1]], angleDeg=angleDeg)

        return groupLatex


class cubicBezier():
    """ This is a class with different methods for drawing cubic bezier lines.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.
    """

    @staticmethod
    def addNode(NodeList, coord=[0, 0], cPbefore=[-1, 0], cPafter=[1, 0], typeNode='corner', flagAbsCoords=True):
        """Add a new node to the list of nodes of the cubic bezier line.

        .. important:: This function does not draw the curve. To draw the curve see :meth:`cubicBezier.draw` method.

        :param NodeList: Lst of nodes that will receive (append) the new node.
        :param coord: List with the coordinates of the node
        :param cPbefore: List with the coordinates of the control point before the node.
        :param cPafter: List with the coordinates of the control point after the node. Used only if 'typeNode' is 'smooth' or 'corner'
        :param typeNode: type of node to be added. See image below

          - ``corner``: Node without smoothness constraint. The bezier curve can have a sharp edge at this node

          - ``smooth``: Node with smoothness constraint. The bezier curve will be smooth at this node. If the control points do not form a straight line, then they are modified to form a straight line. See image below

          -  ``symmetric``: same as ``smooth``, but the control points are forced to be symmetric with respect to the node.

        :param flagAbsCoords: Indicate absolute or relative coordinates. See section below on how reference system works.
            .. warning:: All nodes in a given list must be defined in the same reference system (absolute or relative).

        :type NodeList: list
        :type coord: list [x,y]
        :type cPbefore: list [x,y]
        :type cPafter: list [x,y]
        :type typeNode: string
        :type flagAbsCoords: bool

        :returns: None
        :rtype: -

        **Node Types**

        The image below presents the types of nodes

        .. image:: ../imagesDocs/bezier_nodeTypes.png
              :width: 500px

        **Smoothing control nodes**

        Image below present the process of smoothing control nodes not completely aligned when  ``smooth`` is selected.

        .. image:: ../imagesDocs/bezier_smoothProcess.png
              :width: 500px

        **Absolute and relative coordinate systems**

        Cubic bezier curves are composed by segments which are defined by 4 coordinates, two node coordinates and two control points.

        .. image:: ../imagesDocs/bezier_definitions.png
          :width: 500px

        In absolute coordinate system, all node and control point locations are specified using the origin as reference.
        In relative coordinate system, control point localizations are specified using its node as reference, and each node
        use the previous node as reference (the first node use the origin as reference). See image below.

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        .. image:: ../imagesDocs/bezier_references.png
          :width: 700px

        **Example**

        .. note:: In the following example, the control point before the first node and after the last node are important when the bezier curve must be closed. See method ``draw``

        .. image:: ../imagesDocs/bezier_example.png
          :width: 400px

        >>> # create a list of nodes using absolute coordinate system
        >>> nodeListABS=[]
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[4,4], cPbefore=[6,6], cPafter=[2,6], typeNode='corner', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[8,12], cPbefore=[4,12], cPafter=[10,12], typeNode='smooth', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[12,8], cPbefore=[8,8], cPafter=[12,10], typeNode='corner', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[16,8], cPbefore=[14,10], cPafter=None, typeNode='symmetric', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[12,4], cPbefore=[16,4], cPafter=[10,6], typeNode='corner', flagAbsCoords=True)

        >>> # create a list of nodes using relative coordinate system
        >>> nodeListREL=[]
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, 4], cPbefore=[2,2], cPafter=[-2,2], typeNode='corner', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, 8], cPbefore=[-4,0], cPafter=[2,0], typeNode='smooth', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, -4], cPbefore=[-4,0], cPafter=[0,2], typeNode='corner', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, 0], cPbefore=[-2,2], cPafter=None, typeNode='symmetric', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[-4,-4], cPbefore=[4,0], cPafter=[-2,2], typeNode='corner', flagAbsCoords=False)

        """

        if typeNode.lower() == 'symmetric':
            typeNodeSodipodi = 'z'

        if typeNode.lower() == 'smooth':
            typeNodeSodipodi = 's'

        if typeNode.lower() == 'corner':
            typeNodeSodipodi = 'c'

        if typeNodeSodipodi.lower() == 'c':  # corner
            NodeList.append({'node': coord, 'cPoint_before': cPbefore, 'cPoint_after': cPafter, 'type': typeNodeSodipodi, 'absCoords': flagAbsCoords})

        if typeNodeSodipodi.lower() == 'z':  # symmetric
            if flagAbsCoords:
                deltaX = coord[0] - cPbefore[0]
                deltaY = coord[1] - cPbefore[1]
                NodeList.append(
                    {'node': coord, 'cPoint_before': cPbefore, 'cPoint_after': [coord[0] + deltaX, coord[1] + deltaY], 'type': typeNodeSodipodi,
                     'absCoords': flagAbsCoords})
            else:
                NodeList.append({'node': coord, 'cPoint_before': cPbefore, 'cPoint_after': [-cPbefore[0], -cPbefore[1]], 'type': typeNodeSodipodi,
                                 'absCoords': flagAbsCoords})

        if typeNodeSodipodi.lower() == 's':  # smooth

            # projects the directions of the control points to a commom direction, perpendicular to both
            delta1 = np.array(cPbefore)
            delta2 = np.array(cPafter)

            if abs(delta1.dot(delta2)) < 1.0:

                if flagAbsCoords:
                    delta1 -= np.array(coord)
                    delta2 -= np.array(coord)

                # https://math.stackexchange.com/questions/2285965/how-to-find-the-vector-formula-for-the-bisector-of-given-two-vectors
                bisectorVector = np.linalg.norm(delta2) * delta1 + np.linalg.norm(delta1) * delta2
                tangentVersor = np.array([-bisectorVector[1], bisectorVector[0]])
                tangentVersor /= np.linalg.norm(tangentVersor)

                cPbeforeNew = np.linalg.norm(delta1) * tangentVersor
                cPafterNew = np.linalg.norm(delta2) * tangentVersor

                if flagAbsCoords:
                    cPbeforeNew += np.array(coord)
                    cPafterNew += np.array(coord)

                NodeList.append({'node': coord, 'cPoint_before': cPbeforeNew.tolist(), 'cPoint_after': cPafterNew.tolist(), 'type': typeNodeSodipodi,
                                 'absCoords': flagAbsCoords})
            else:
                NodeList.append(
                    {'node': coord, 'cPoint_before': cPbefore, 'cPoint_after': cPafter, 'type': typeNodeSodipodi, 'absCoords': flagAbsCoords})

    @staticmethod
    def draw(parent, NodeList, offset=np.array([0, 0]), label='none', lineStyle=lineStyle.setSimpleBlack(), closePath=False):
        """draws the bezier line, given a list of nodes, built using :meth:`cubicBezier.addNode` method


        :param parent: parent object
        :param NodeList: list of nodes. See :`cubicBezier.addNode` method
        :param offset: offset coords. Default [0,0]
        :param label: label of the line. Default 'none'
        :param lineStyle: line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()
        :param closePath: Connects the first point to the last. Default: False

        :type parent: inkscape element object
        :type NodeList: list of nodes
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type closePath: bool

        :returns: the new line object
        :rtype: line Object

        **Example**

        .. note:: In the following example, the control point before the first node and after the last node are important
            when the bezier curve must be closed.

        .. image:: ../imagesDocs/bezier_example.png
          :width: 400px

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle = set(lineWidth=1.0, lineColor=color.defined('red'))

        >>> # create a list of nodes using absolute coordinate system
        >>> nodeListABS=[]
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[4,4], cPbefore=[6,6], cPafter=[2,6], typeNode='corner', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[8,12], cPbefore=[4,12], cPafter=[10,12], typeNode='smooth', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[12,8], cPbefore=[8,8], cPafter=[12,10], typeNode='corner', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[16,8], cPbefore=[14,10], cPafter=None, typeNode='symmetric', flagAbsCoords=True)
        >>> inkDraw.cubicBezier.addNode(nodeListABS, coord=[12,4], cPbefore=[16,4], cPafter=[10,6], typeNode='corner', flagAbsCoords=True)

        >>> # create a list of nodes using relative coordinate system
        >>> nodeListREL=[]
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, 4], cPbefore=[2,2], cPafter=[-2,2], typeNode='corner', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, 8], cPbefore=[-4,0], cPafter=[2,0], typeNode='smooth', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, -4], cPbefore=[-4,0], cPafter=[0,2], typeNode='corner', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[4, 0], cPbefore=[-2,2], cPafter=None, typeNode='symmetric', flagAbsCoords=False)
        >>> inkDraw.cubicBezier.addNode(nodeListREL, coord=[-4,-4], cPbefore=[4,0], cPafter=[-2,2], typeNode='corner', flagAbsCoords=False)

        >>> C1 = inkDraw.cubicBezier.draw(root_layer,nodeListABS, offset=[0, 0],closePath=False)
        >>> C2 = inkDraw.cubicBezier.draw(root_layer,nodeListABS, offset=[0, 0],closePath=True)
        >>> C3 = inkDraw.cubicBezier.draw(root_layer,nodeListREL, offset=[0, 0],closePath=False)
        >>> C4 = inkDraw.cubicBezier.draw(root_layer,nodeListREL, offset=[0, 0],closePath=True)

        Result of the example

        .. image:: ../imagesDocs/bezier_example_draw.png
          :width: 800px

        """

        # first node
        if NodeList[0]['absCoords']:
            string_coords = 'M %f,%f ' % (NodeList[0]['node'][0] + offset[0], NodeList[0]['node'][0] + offset[1])
        else:
            string_coords = 'M %f,%f ' % (NodeList[0]['node'][0] + offset[0], NodeList[0]['node'][0] + offset[1])

        string_nodeTypes = ''
        Ptotal = np.zeros(2)
        for i in range(len(NodeList) - 1):
            currNode = NodeList[i]
            nextNode = NodeList[i + 1]

            if currNode['absCoords']:
                bezier = 'C %f,%f ' % (currNode['cPoint_after'][0] + offset[0], currNode['cPoint_after'][1] + offset[1])  # first control point
                bezier += '%f,%f ' % (nextNode['cPoint_before'][0] + offset[0], nextNode['cPoint_before'][1] + offset[1])  # second control point
                bezier += '%f,%f ' % (nextNode['node'][0] + offset[0], nextNode['node'][1] + offset[1])  # second node
            else:
                bezier = 'c %f,%f ' % (currNode['cPoint_after'][0], currNode['cPoint_after'][1])  # first control point
                bezier += '%f,%f ' % (
                nextNode['cPoint_before'][0] + nextNode['node'][0], nextNode['cPoint_before'][1] + nextNode['node'][1])  # second control point
                bezier += '%f,%f ' % (nextNode['node'][0], nextNode['node'][1])  # second node
                Ptotal += np.array(currNode['node'])

            string_nodeTypes += currNode['type']
            string_coords = string_coords + bezier

        if closePath:
            currNode = NodeList[-1]
            nextNode = copy.deepcopy(NodeList[0])

            if currNode['absCoords']:
                bezier = 'C %f,%f ' % (currNode['cPoint_after'][0] + offset[0], currNode['cPoint_after'][1] + offset[1])  # first control point
                bezier += '%f,%f ' % (nextNode['cPoint_before'][0] + offset[0], nextNode['cPoint_before'][1] + offset[1])  # second control point
                bezier += '%f,%f ' % (nextNode['node'][0] + offset[0], nextNode['node'][1] + offset[1])  # second node
            else:
                # writes the coordinates of the first node, relative to the last node.
                Ptotal += np.array(currNode['node'])
                nextNode['node'][0] = NodeList[0]['node'][0] - Ptotal[0]
                nextNode['node'][1] = NodeList[0]['node'][1] - Ptotal[1]

                bezier = 'c %f,%f ' % (currNode['cPoint_after'][0], currNode['cPoint_after'][1])  # first control point
                bezier += '%f,%f ' % (
                nextNode['cPoint_before'][0] + nextNode['node'][0], nextNode['cPoint_before'][1] + nextNode['node'][1])  # second control point
                bezier += '%f,%f ' % (nextNode['node'][0], nextNode['node'][1])  # second node

            string_nodeTypes += currNode['type'] + nextNode['type']
            string_coords = string_coords + bezier + ' Z'
        else:
            string_nodeTypes += currNode['type']

        # M = move, L = line, H = horizontal line, V = vertical line, C = curve, S = smooth curve,
        # Q = quadratic Bezier curve, T = smooth quadratic Bezier curve, A = elliptical Arc,Z = closepath
        Attribs = {inkex.addNS('label', 'inkscape'): label, 'style': str(inkex.Style(lineStyle)), 'd': string_coords,
                   inkex.addNS('nodetypes', 'sodipodi'): string_nodeTypes}

        return etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)


class line():
    """ class with methods for drawing lines (paths).

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.
    """

    @staticmethod
    def absCoords(parent, coordsList, offset=[0, 0], label='none', lineStyle=lineStyle.setSimpleBlack(), closePath=False):
        """Draw a (poly)line based on a list of absolute coordinates


        :param parent: Parent object
        :param coordsList: List with coords x and y. ex:  [[x1,y1], ..., [xN,yN]]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param offset: Offset coords. Default [0,0]
        :param label: Label of the line. Default 'none'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()
        :param closePath: Connects the first point to the last. Default: False

        :type parent: inkscape element object
        :type coordsList: list of list
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type closePath: bool

        :returns: the new line object
        :rtype: line Object

        **Example**

        .. image:: ../imagesDocs/lineExample.png
          :width: 250px

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle = inkDraw.lineStyle.set(lineWidth=1.0, lineColor=color.defined('red'))
        >>> 
        >>> # creates a polyline passing through points (0,0) (0,1) (1,1) (1,2) (2,2), and using absolute coordinates
        >>> coords=[ [0,0], [0,1], [1,1], [1,2], [2,2] ]
        >>> inkDraw.line.absCoords(root_layer, coordsList=coords, offset=[0, 0], label='fooBarLine', lineStyle=myLineStyle)
        >>>
        >>> # creates the same polyline translated to point (5,6). Note we just have to change the offset
        >>> inkDraw.line.absCoords(root_layer, coordsList=coords, offset=[5, 6], label='fooBarLine', lineStyle=myLineStyle)
        """

        # string with coordinates
        string_coords = ''

        for point in coordsList:
            string_coords = string_coords + ' ' + str(point[0] + offset[0]) + ',' + str(point[1] + offset[1])

        if closePath:
            string_coords += ' Z'

        # M = move, L = line, H = horizontal line, V = vertical line, C = curve, S = smooth curve,
        # Q = quadratic Bezier curve, T = smooth quadratic Bezier curve, A = elliptical Arc,Z = closepath
        Attribs = {inkex.addNS('label', 'inkscape'): label, 'style': str(inkex.Style(lineStyle)), 'd': 'M ' + string_coords}

        return etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)

    # ---------------------------------------------
    @staticmethod
    def relCoords(parent, coordsList, offset=[0, 0], label='none', lineStyle=lineStyle.setSimpleBlack(), closePath=False):
        """Draw a (poly)line based on a list of relative coordinates

        :param parent: Parent object
        :param coordsList: List with distances dx and dy for all points.  ex  [[dx1,dy1], ..., [dxN,dyN]]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param offset: Offset coords. Default [0,0]
        :param label: Label of the line. Default 'none'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()
        :param closePath: Connects the first point to the last. Default: False

        :type parent: inkscape element object
        :type coordsList: list of list
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type closePath: bool

        :returns: the new line object
        :rtype: line Object

        **Example**

        .. image:: ../imagesDocs/lineExample.png
          :width: 250px

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle = inkDraw.lineStyle.setSimpleBlack(lineWidth=1.0)
        >>>
        >>> # creates a polyline passing through points (0,0) (0,1) (1,1) (1,2) (2,2) using relative coordinates
        >>> coords=[ [0,1], [1,0], [0,1], [1,0] ]
        >>> inkDraw.line.relCoords(root_layer, coordsList=coords, offset=[0, 0], label='fooBarLine', lineStyle=myLineStyle)
        >>>
        >>> # creates the same polyline translated to point (5,6)
        >>> inkDraw.line.relCoords(root_layer, coordsList=coords, offset=[5, 6], label='fooBarLine', lineStyle=myLineStyle)
        """

        # string with coordinates
        string_coords = ''
        for dist in coordsList:
            string_coords = string_coords + ' ' + str(dist[0]) + ',' + str(dist[1])

        if closePath:
            string_coords += ' Z'

        # M = move, L = line, H = horizontal line, V = vertical line, C = curve, S = smooth curve,
        # Q = quadratic Bezier curve, T = smooth quadratic Bezier curve, A = elliptical Arc,Z = closepath
        Attribs = {inkex.addNS('label', 'inkscape'): label, 'style': str(inkex.Style(lineStyle)),
                   'd': 'm ' + str(offset[0]) + ' ' + str(offset[1]) + string_coords}

        return etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)


class arc():
    """ Class with methods for drawing arcs.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.
    """

    @staticmethod
    def startEndRadius(parent, Pstart, Pend, radius, offset=[0, 0], label='arc', lineStyle=lineStyle.setSimpleBlack(), flagRightOf=True,
                       arcType='open', largeArc=False):
        """Draw a circle arc from ``Pstart`` to ``Pend`` with a given radius

        .. image:: ../imagesDocs/arc_startEndRadius.png
          :width: 80px

        :param parent: Parent object
        :param Pstart: Start coordinate [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param Pend: End coordinate [x,y]
        :param radius: Arc radius
        :param offset: Extra offset coords [x,y]. Default [0,0]
        :param label: Label of the line. Default 'arc'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()
        :param flagRightOf: Sets the side of the vector Pend-Pstart which the arc must be drawn. See image below

          - True: Draws the arc to the right (Default)
          - False: Draws the arc to the left

        :param arcType: type of arc. Valid values: 'open', 'slice', 'chord'. See image below. Default: 'open'

        :param largeArc: Sets the largest arc to be drawn. See image below

          - True: Draws the largest arc
          - False: Draws the smallest arc (Default)

        :type parent: inkscape element object
        :type Pstart: list
        :type Pend: list
        :type radius: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type flagRightOf: bool
        :type arcType: string
        :type largeArc: bool

        :returns: the new arc object
        :rtype: line Object

        **Arc options**

        .. image:: ../imagesDocs/arc_startEndRadius_flags.png
          :width: 800px

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> 
        >>> P1=[10.0,0.0]
        >>> P2=[20.0,10.0]
        >>> R=15.0
        >>> myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> #draws an open arc
        >>> inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[25,0], label='arc1',  lineStyle=myLineStyle, arcType='open')
        >>>
        >>> #draws a closed (slice) arc
        >>> inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[25,20], label='arc2',  lineStyle=myLineStyle, arcType='slice')
        >>>
        >>> #draws an open arc to the right
        >>> inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[0,0], label='arc',  lineStyle=myLineStyle, flagRightOf=True, largeArc=True)
        """

        # finds the center point using some linear algebra
        StartVector = np.array(Pstart)
        EndVector = np.array(Pend)

        DistVector = EndVector - StartVector
        Dist = np.linalg.norm(DistVector)  # distance between start and end
        if Dist > 2.0 * radius:
            return None

        if (flagRightOf and largeArc) or (not flagRightOf and not largeArc):
            RadiusDirection = np.array([-DistVector[1], DistVector[0]])  # perpendicular to DistVector
        else:
            RadiusDirection = np.array([DistVector[1], -DistVector[0]])  # perpendicular to DistVector

        RadiusDirection = RadiusDirection / np.linalg.norm(RadiusDirection)  # normalize RadiusDirection
        CenterPoint = StartVector + DistVector / 2.0 + RadiusDirection * math.sqrt(radius ** 2.0 - (Dist / 2.0) ** 2.0)

        # computes the starting angle and ending angle
        temp = StartVector - CenterPoint
        AngStart = math.atan2(temp[1], temp[0])
        temp = EndVector - CenterPoint
        AngEnd = math.atan2(temp[1], temp[0])

        if flagRightOf:  # inkscape does not follow svg path format to create arcs. It uses sodipodi which is weird  =S
            sodipodiAngleStart = str(AngEnd)
            sodipodiAngleEnd = str(AngStart)
        else:
            sodipodiAngleStart = str(AngStart)
            sodipodiAngleEnd = str(AngEnd)

        # arc instructions
        if largeArc:
            largeArcFlag = 1
        else:
            largeArcFlag = 0
        if flagRightOf:
            sweepFlag = 0
        else:
            sweepFlag = 1
        arcString = ' a %f,%f 0 %d %d %f,%f' % (radius, radius, largeArcFlag, sweepFlag, EndVector[0] - StartVector[0], EndVector[1] - StartVector[1])
        if arcType.lower() == 'slice':
            arcString = arcString + ' L ' + str(CenterPoint[0] + offset[0]) + ' ' + str(CenterPoint[1] + offset[1]) + ' z'
        if arcType.lower() == 'chord':
            arcString = arcString + ' z'

        # M = moveto,L = lineto,H = horizontal lineto,V = vertical lineto,C = curveto,S = smooth curveto,Q = quadratic Bezier curve,T = smooth quadratic Bezier curveto,A = elliptical Arc,Z = closepath
        Attribs = {inkex.addNS('label', 'inkscape'): label, 'style': str(inkex.Style(lineStyle)), inkex.addNS('type', 'sodipodi'): 'arc',
                   inkex.addNS('rx', 'sodipodi'): str(radius), inkex.addNS('ry', 'sodipodi'): str(radius),
                   inkex.addNS('cx', 'sodipodi'): str(CenterPoint[0] + offset[0]), inkex.addNS('cy', 'sodipodi'): str(CenterPoint[1] + offset[1]),
                   inkex.addNS('start', 'sodipodi'): sodipodiAngleStart, inkex.addNS('end', 'sodipodi'): sodipodiAngleEnd,
                   'd': 'M ' + str(offset[0] + StartVector[0]) + ' ' + str(offset[1] + StartVector[1]) + arcString}
        if arcType.lower() == 'open':
            Attribs[inkex.addNS('arc-type', 'sodipodi')] = 'arc'
        else:
            Attribs[inkex.addNS('arc-type', 'sodipodi')] = arcType.lower()

        return etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)

    # ---------------------------------------------
    @staticmethod
    def centerAngStartAngEnd(parent, centerPoint, radius, angStart, angEnd, offset=[0, 0], label='arc', lineStyle=lineStyle.setSimpleBlack(),
                             arcType='open', largeArc=False):
        """Draw a circle arc given its center and start and end angles

        .. image:: ../imagesDocs/arc_centerAngStartAngEnd.png
          :width: 200px


        :param parent: parent object
        :param centerPoint: center coordinate [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param radius: Arc radius
        :param angStart: Start angle in degrees
        :param angEnd: End angle in degrees
        :param offset: Extra offset coords [x,y]
        :param label: Label of the line. Default 'arc'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()
        :param arcType: Type of arc. Valid values: 'open', 'slice', 'chord'. See image below. Default: 'open'
        :param largeArc: Sets the largest arc to be drawn. See image below

          - True: Draws the largest arc
          - False: Draws the smallest arc (Default)

        :type parent: inkscape element object
        :type centerPoint: list
        :type radius: float
        :type angStart: float
        :type angEnd: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type arcType: string
        :type largeArc: bool

        :returns: the new arc object
        :rtype: line Object

        **Arc options**

        .. image:: ../imagesDocs/arc_centerAngStartAngEnd_flags.png
          :width: 700px

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle = inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> #draws the shortest arc
        >>> inkDraw.arc.centerAngStartAngEnd(parent=root_layer, centerPoint=[0,0], radius=15.0, angStart=-10, angEnd=90,
        >>>                                  offset=[0,0], label='arc1',  lineStyle=myLineStyle, arcType='open',largeArc=False)
        >>> #draws the longest arc
        >>> inkDraw.arc.centerAngStartAngEnd(parent=root_layer, centerPoint=[0,0], radius=15.0, angStart=-10, angEnd=90,
        >>>                                  offset=[30,0], label='arc1',  lineStyle=myLineStyle, arcType='open',largeArc=True)
        """

        Pstart = [radius * math.cos(math.radians(angStart)), radius * math.sin(math.radians(angStart))]
        Pend = [radius * math.cos(math.radians(angEnd)), radius * math.sin(math.radians(angEnd))]

        pos = [centerPoint[0] + offset[0], centerPoint[1] + offset[1]]

        if abs(angEnd - angStart) <= 180:
            flagRight = largeArc
        else:
            flagRight = not largeArc

        return arc.startEndRadius(parent, Pstart, Pend, radius, pos, label, lineStyle, flagRight, arcType, largeArc)

    # ---------------------------------------------
    @staticmethod
    def threePoints(parent, Pstart, Pmid, Pend, offset=[0, 0], label='arc', lineStyle=lineStyle.setSimpleBlack(), arcType='open'):
        """Draw a circle arc given 3 points

        .. image:: ../imagesDocs/arc_3points.png
          :width: 120px


        :param parent: parent object
        :param Pstart: Start coordinate [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param Pmid: Mid coordinate [x,y]
        :param Pend: End coordinate [x,y]
        :param offset: Extra offset coords [x,y]
        :param label: Label of the line. Default 'arc'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()
        :param arcType: Type of arc. Valid values: 'open', 'slice', 'chord'. See image below. Default: 'open'

        :type parent: inkscape element object
        :type Pstart: list
        :type Pmid: list
        :type Pend: list
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type arcType: string

        :returns: the new arc object
        :rtype: line Object

        **Arc options**

        .. image:: ../imagesDocs/arc_type_flags.png
          :width: 400px

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle = inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> P1=[10.0,0.0]
        >>> P2=[20.0,10.0]
        >>> P3=[50.0,30.0]
        >>>
        >>> #draws an open arc
        >>> inkDraw.arc.threePoints(parent=root_layer, Pstart=P1, Pmid=P3, Pend=P3, offset=[25,0], label='arc1',  lineStyle=myLineStyle, arcType='open')
        """

        [center,radius] = circle3Points(Pstart, Pmid, Pend)

        if center is None:
            return
        vStart=np.array(Pstart)
        vEnd=np.array(Pend)
        vMid=np.array(Pmid)

        # find side
        DistVector = vEnd-vStart
        NormalLeftVector = np.array([DistVector[1],-DistVector[0]])
        MidVector = vMid - vStart
        CenterVector = center - vStart

        # check if  MidVector and CenterVector are pointing to the same side of DistVector
        if np.dot(CenterVector,NormalLeftVector)*np.dot(MidVector,NormalLeftVector)>0:
            largeArc = True
        else:
            largeArc = False

        angStart = math.atan2(Pstart[1]-center[1], Pstart[0]-center[0])
        angEnd = math.atan2(Pend[1]-center[1], Pend[0]-center[0])

        angles = np.unwrap([angStart, angEnd])*180/np.pi
        angStart=angles[0]
        angEnd=angles[1]

        if angEnd - angStart>0:
            return arc.centerAngStartAngEnd(parent, center, radius, angStart, angEnd, offset, label,lineStyle,arcType,largeArc)
        else:
            return arc.centerAngStartAngEnd(parent, center, radius, angEnd, angStart, offset, label,lineStyle,arcType,largeArc)


class circle():
    """ Class with methods for drawing circles.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.
    """

    @staticmethod
    def centerRadius(parent, centerPoint, radius, offset=[0, 0], label='circle', lineStyle=lineStyle.setSimpleBlack()):
        """Draw a circle given its center point and radius

        :param parent: Parent object
        :param centerPoint: Center coordinate [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param radius: Circle's radius
        :param offset: Extra offset coords [x,y]
        :param label: Label of the line. Default 'circle'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscape element object
        :type centerPoint: list
        :type radius: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new circle object
        :rtype: line Object

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle = inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> inkDraw.circle.centerRadius(parent=root_layer, centerPoint=[0,0], radius=15.0, offset=[5,1], label='circle1', lineStyle=myLineStyle)
        """

        # arc instructions
        arcStringA = ' a %f,%f 0 1 1 %f,%f' % (radius, radius, -2 * radius, 0)
        arcStringB = ' a %f,%f 0 1 1 %f,%f' % (radius, radius, 2 * radius, 0)

        # M = moveto,L = lineto,H = horizontal lineto,V = vertical lineto,C = curveto,S = smooth curveto,Q = quadratic Bezier curve,T = smooth quadratic Bezier curveto,A = elliptical Arc,Z = closepath
        Attribs = {inkex.addNS('label', 'inkscape'): label, 'style': str(inkex.Style(lineStyle)), inkex.addNS('type', 'sodipodi'): 'arc',
                   inkex.addNS('rx', 'sodipodi'): str(radius), inkex.addNS('ry', 'sodipodi'): str(radius),
                   inkex.addNS('cx', 'sodipodi'): str(centerPoint[0] + offset[0]), inkex.addNS('cy', 'sodipodi'): str(centerPoint[1] + offset[1]),
                   inkex.addNS('start', 'sodipodi'): '0', inkex.addNS('end', 'sodipodi'): str(2 * math.pi),
                   'd': 'M ' + str(centerPoint[0] + offset[0] + radius) + ' ' + str(
                       centerPoint[1] + offset[1]) + arcStringA + ' ' + arcStringB + ' z'}

        return etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)

    # ---------------------------------------------
    @staticmethod
    def threePoints(parent, P1, P2, P3, offset=[0, 0], label='circle', lineStyle=lineStyle.setSimpleBlack()):
        """Draw a circle given 3 poins on the circle.

        The function checks if the 3 points are aligned. In this case, no circle is drawn.

        :param parent: parent object
        :param P1: point coordinates [x,y]
        :param P2: point coordinates [x,y]
        :param P3: point coordinates [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param offset: Extra offset coords [x,y]
        :param label: Label of the line. Default 'arc'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscape element object
        :type P1: list
        :type P2: list
        :type P3: list
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new circle object
        :rtype: line Object

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle = inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> inkDraw.circle.threePoints(parent=root_layer, P1=[0,0], P2=[30,40], P3=[-20,20], offset=[0,0], label='circle1', lineStyle=myLineStyle)

        .. image:: ../imagesDocs/circle_3P.png
          :width: 200px

        """

        [center,radius] = circle3Points(P1, P2, P3)

        return circle.centerRadius(parent, center, radius, offset, label, lineStyle)

class rectangle():
    """ Class with methods for drawing rectangles.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.
    """

    @staticmethod
    def widthHeightCenter(parent, centerPoint, width, height, radiusX=None, radiusY=None, offset=[0, 0], label='rectangle',
                          lineStyle=lineStyle.setSimpleBlack()):
        """Draw a rectangle given its center point and dimensions

        :param parent: Parent object
        :param centerPoint: Center coordinate [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param width: Dimension in X direction
        :param height: Dimension in Y direction
        :param radiusX: Rounding radius in X direction. If this value is ``None``, the rectangle will have sharp corners. Default: None
        :param radiusY: Rounding radius in Y direction.
                - If ``None``, then radiusX will also be used in Y direction.
                - If ``None`` and radiusX is also ``None``, then the rectangle will have sharp corners. Default: None
        :param offset: Extra offset coords [x,y]
        :param label: Label of the line. Default 'circle'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscape element object
        :type centerPoint: list
        :type width: float
        :type height: float
        :type radiusX: float
        :type radiusY: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new rectangle object
        :rtype: rectangle Object

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> #draws a 50x60 rectangle with radiusX=2.0 and radiusY=3.0
        >>> inkDraw.rectangle.widthHeightCenter(parent=root_layer, centerPoint=[0,0], width=50, height=60, radiusX=2.0,radiusY=3.0, offset=[0,0], label='rect1', lineStyle=myLineStyle)
        """
        x = centerPoint[0] - width / 2.0 + offset[0]
        y = centerPoint[1] - height / 2.0 + offset[1]

        Attribs = {inkex.addNS('label', 'inkscape'): label, 'style': str(inkex.Style(lineStyle)), 'width': str(width), 'height': str(height),
                   'x': str(x), 'y': str(y), 'rx': str(radiusX), 'ry': str(radiusY)}

        if radiusX and radiusX > 0.0:
            Attribs['rx'] = str(radiusX)
            if radiusY is None:
                Attribs['ry'] = str(radiusX)
            else:
                if radiusY > 0.0:
                    Attribs['ry'] = str(radiusY)

        return etree.SubElement(parent, inkex.addNS('rect', 'svg'), Attribs)

    @staticmethod
    def corners(parent, corner1, corner2, radiusX=None, radiusY=None, offset=[0, 0], label='rectangle', lineStyle=lineStyle.setSimpleBlack()):
        """Draw a rectangle given the coordinates of two oposite corners

        :param parent: Parent object
        :param corner1: Coordinates of corner 1 [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param corner2: Coordinates of corner 2 [x,y]
        :param radiusX: Rounding radius in X direction. If this value is ``None``, the rectangle will have sharp corners. Default: None
        :param radiusY: Rounding radius in Y direction. If this value is ``None``, then radiusX will also be used in Y direction. If radiusX is also ``None``, then the rectangle will have sharp corners. Default: None
        :param offset: Extra offset coords [x,y]
        :param label: Label of the line. Default 'circle'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscape element object
        :type corner1: list
        :type corner2: list
        :type radiusX: float
        :type radiusY: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new rectangle object
        :rtype: rectangle Object

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> #draws a rectangle with corners C1=[1,5] and C2=[6,10], with radiusX=2.0 and radiusY=3.0
        >>> inkDraw.rectangle.corners(parent=root_layer, corner1=[1,5], corner2=[6,10], radiusX=2.0,radiusY=3.0, offset=[0,0], label='rect1',  lineStyle=myLineStyle)
        """
        x = (corner1[0] + corner2[0]) / 2.0
        y = (corner1[1] + corner2[1]) / 2.0

        width = abs(corner1[0] - corner2[0])
        height = abs(corner1[1] - corner2[1])

        return rectangle.widthHeightCenter(parent, [x, y], width, height, radiusX, radiusY, offset, label, lineStyle)


class ellipse():
    """ Class with methods for drawing ellipses.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.
    """

    @staticmethod
    def centerRadius(parent, centerPoint, radiusX, radiusY, offset=[0, 0], label='circle', lineStyle=lineStyle.setSimpleBlack()):
        """Draw an ellipse given its center point and radii

        :param parent: Parent object
        :param centerPoint: Center coordinate [x,y]

            .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param radiusX: Ellipse's radius in x direction
        :param radiusY: Ellipse's radius in y direction
        :param offset: Extra offset coords [x,y]
        :param label: Label of the line. Default 'circle'
        :param lineStyle: Line style to be used. See :class:`lineStyle` class. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscape element object
        :type centerPoint: list
        :type radiusX: float
        :type radiusY: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new ellipse object
        :rtype: line Object

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>
        >>> #draws the shortest arc
        >>> inkDraw.ellipse.centerRadius(parent=root_layer, centerPoint=[0,0], radiusX=15.0, radiusY=25.0, offset=[5,1], label='circle1',  lineStyle=myLineStyle)
        """

        # arc instructions
        arcStringA = ' a %f,%f 0 1 1 %f,%f' % (radiusX, radiusY, -2 * radiusX, 0)
        arcStringB = ' a %f,%f 0 1 1 %f,%f' % (radiusX, radiusY, 2 * radiusX, 0)

        # M = moveto,L = lineto,H = horizontal lineto,V = vertical lineto,C = curveto,S = smooth curveto,Q = quadratic Bezier curve,T = smooth quadratic Bezier curveto,A = elliptical Arc,Z = closepath
        Attribs = {inkex.addNS('label', 'inkscape'): label, 'style': str(inkex.Style(lineStyle)), inkex.addNS('type', 'sodipodi'): 'arc',
                   inkex.addNS('rx', 'sodipodi'): str(radiusX), inkex.addNS('ry', 'sodipodi'): str(radiusY),
                   inkex.addNS('cx', 'sodipodi'): str(centerPoint[0] + offset[0]), inkex.addNS('cy', 'sodipodi'): str(centerPoint[1] + offset[1]),
                   inkex.addNS('start', 'sodipodi'): '0', inkex.addNS('end', 'sodipodi'): str(2 * math.pi),
                   'd': 'M ' + str(centerPoint[0] + offset[0] + radiusX) + ' ' + str(
                       centerPoint[1] + offset[1]) + arcStringA + ' ' + arcStringB + ' z'}

        return etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)
