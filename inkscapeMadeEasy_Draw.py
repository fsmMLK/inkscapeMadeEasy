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
#useLatex=False


try:
  useLatex
except NameError:
  useLatex=True
else:
  useLatex=False
  
import inkex
import math
import simplestyle
import numpy as np
from lxml.etree import tostring
if useLatex:
  import textextLib.textext as textext
  
import sys
import tempfile
"""
This module contains a set of classes and some functions to help dealing with drawings.

This module requires the following modules: inkex, math, simplestyle (from inkex module), numpy, lxml and sys

"""



def displayMsg(msg):
    """Displays a message to the user.

    :returns: nothing
    :rtype: -
    
    .. note:: Identical function has been also defined inside inkscapeMadeEasy class   
    
    """
    sys.stderr.write(msg + '\n')
    
def Dump(obj, file='./dump_file.txt', mode='w'):
    """Function to easily output the result of ``str(obj)`` to a file

    This function was created to help debugging the code while it is running under inkscape. Since inkscape does not possess a terminal as today (2016), this function overcomes partially the issue of sending things to stdout by dumping result of the function ``str()`` in a text file.


    :param obj: object to sent to the file. Any type that can be used in ``str()``
    :param file: file path. Default: ``./dump_file.txt``
    :param mode: writing mode of the file. Default: ``w`` (write)
    :type obj: any, as long as ``str(obj``) is implemented (see ``__str__()`` metaclass definition )
    :type arg2: string
    :type mode: string
    :returns: nothing
    :rtype: -

    .. note:: Identical function has been also defined inside inkscapeMadeEasy class   

    **Example**

    >>> vector1=[1,2,3,4,5,6]
    >>> Dump(vector,file='~/temporary.txt',mode='w')   % writes the list to a file
    >>> vector2=[7,8,9,10]
    >>> Dump(vector2,file='~/temporary.txt',mode='a')   % append the list to a file

    """
    file = open(file, mode)
    file.write(str(obj) + '\n')
    file.close()


class color():
    """
    Class to manipulate colors.

    This class manipulates color information, generating a string in inkscape's expected format ``#RRGGBB``

    This class contains only static methods so that you don't have to inherit this in your class

    .. note:: alpha channel is not implemented yet. Assume alpha=1.0

    """
    @staticmethod
    def defined(colorName):
        """ Returns the color string representing a predefined color name

        :param colorName: color name
        :type colorName: string
        :returns:  string representing the color in inkscape's expected format ``#RRGGBB``
        :rtype: string

        **Available pre defined colors**

        .. image:: ../imagesDocs/Default_colors.png
          :width: 400px

        **Example**

        >>> colorString = color.defined('red')                   # returns #ff0000 representing red color

        """
        if colorName not in ['Dred', 'red', 'Lred',
                             'Dblue', 'blue', 'Lblue',
                             'Dgreen', 'green', 'Lgreen',
                             'Dyellow', 'yellow', 'Lyellow',
                             'Dmagen', 'magen', 'Lmagen',
                             'black', 'white']:
            sys.exit("InkscapeDraw.color.defined() :  Error. color -->" + colorName + "<-- not defined")

        if colorName == 'Dred':
            return '#800000'
        if colorName == 'red':
            return '#FF0000'
        if colorName == 'Lred':
            return '#FF8181'

        if colorName == 'Dblue':
            return '#000080'
        if colorName == 'blue':
            return '#0000FF'
        if colorName == 'Lblue':
            return '#8181FF'

        if colorName == 'Dgreen':
            return '#008000'
        if colorName == 'green':
            return '#00FF00'
        if colorName == 'Lgreen':
            return '#81FF81'

        if colorName == 'black':
            return '#000000'
        if colorName == 'white':
            return '#FFFFFF'

        if colorName == 'Dyellow':
            return '#808000'
        if colorName == 'yellow':
            return '#FFFF00'
        if colorName == 'Lyellow':
            return '#FFFF81'

        if colorName == 'Dmagen':
            return '#800080'
        if colorName == 'magen':
            return '#FF00FF'
        if colorName == 'Lmagen':
            return '#FF81FF'

    @staticmethod
    def RGB(RGBlist):
        """ returns a string representing a color specified by RGB level in the range 0-255

        :param RGBlist: list containing RGB levels in the range 0-225 each
        :type RGBlist: list
        :returns:  string representing the color in inkscape's expected format ``#RRGGBB``
        :rtype: string

        **Example**

        >>> colorString = color.RGB([120,80,0])                   # returns a string representing the color R=120, G=80, B=0

        """
        RGBhex = [''] * 3
        for i in range(3):
            if RGBlist[i] > 255:
                RGBlist[i] = 255

            if RGBlist[i] < 0:
                RGBlist[i] = 0

            if RGBlist[i] < 16:
                RGBhex[i] = '0' + hex(int(RGBlist[i]))[2:].upper()

            else:
                RGBhex[i] = hex(int(RGBlist[i]))[2:].upper()

        return '#' + '%s%s%s' % (RGBhex[0], RGBhex[1], RGBhex[2])

    #---------------------------------------------
    @staticmethod
    def gray(percentage):
        """ returns a gray level compatible string based on white percentage between 0.0 and 1.0

        if percentage is higher than 1.0, percentage is truncated to 1.0 (white)
        if percentage is lower than 0.0, percentage is truncated to 0.0 (black)

        :param percentage: value between 0.0 (black) and 1.0 (white)
        :type percentage: float
        :returns:  string representing the color in inkscape's expected format ``#RRGGBB``
        :rtype: string

        **Example**

        >>> colorString = color.gray(0.6)                   # returns a string representing the gray level with 60% of white

        """
        RGBLevel = 255 * percentage

        if percentage > 1.0:
            RGBLevel = 255
        if percentage < 0.0:
            RGBLevel = 0

        return color.RGB([RGBLevel] * 3)

    #---------------------------------------------
    @staticmethod
    def colorPickerToRGBalpha(colorPickerString):
        """ Function that converts the string returned by  the widget 'color' in the .inx file into 2 strings, one representing the color in format ``#RRGGBB`` and the other representing the alpha channel ``AA``

        :param colorPickerString: string returned by 'color' widget
        :type colorPickerString: string
        :returns: a list of strings: [color,alpha]
                    - color: string in ``#RRGGBB`` format
                    - alpha: string in ``AA`` format
        :rtype: list

        .. note:: For more information on this widget, see <http://wiki.inkscape.org/wiki/index.php/INX_Parameters> 

        .. Warning:: you probably don't need to use this function. Consider using the method ``color.parseColorPicker()``

        **usage**

        1- in your inx file you must have one attribute of the type 'color'::

          <param name="myColorPicker" type="color"></param>

        2- in your .py file, you must parse it as a string:
          >>>   self.OptionParser.add_option("--myColorPicker", action="store", type="string", dest="myColorPickerVar", default='0') 

        3- call this function to convert so.myColorPickerVar to two strings
                 - #RRGGBB   with RGB values in hex
                 - AA       with alpha value in hex

        **Example**

        Let your .inx file contains a widget of type 'color' with the name myColorPicker::

        <param name="myColorPicker" type="color"></param>

        Then in the .py file

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     inkex.Effect.__init__(self) 
        >>>     self.OptionParser.add_option("--myColorPicker", action="store", type="string", dest="myColorPickerVar", default='#000000')  # parses the input parameter
        >>> 
        >>>   def effect(self):
        >>>     color,alpha = inkDraw.color.colorPickerToRGBalpha(self.options.myColorPickerVar)       # returns the string representing the selected color and alpha channel

        """
        colorHex = hex(int(colorPickerString) & 0xffffffff)[2:].zfill(8).upper()  # [2:] removes the 0x ,  zfill adds the leading zeros, upper: uppercase
        RGB = '#' + colorHex[0:6]
        alpha = colorHex[6:]
        return [RGB, alpha]

    #---------------------------------------------
    @staticmethod
    def parseColorPicker(stringColorOption, stringColorPicker):
        """ Function that converts the string returned by  the widgets 'color' and 'optiongroup' in the .inx file into 2 strings, one representing the color in format ``#RRGGBB`` and the other representing the alpha channel ``AA``

        You must have in your .inx both 'optiongroup' and 'color' widgets as defined below. You don't have to have all the color options presented in the example. That is the most complete example, considering the default colors in color.defined method.   


        :param stringColorOption: string returned by 'optiongroup' widget
        :type stringColorOption: string
        :param stringColorPicker: string returned by 'color' widget
        :type stringColorPicker: string
        :returns: a list of strings: [color,alpha]
                    - color: string in ``#RRGGBB`` format
                    - alpha: string in ``AA`` format
        :rtype: list

        .. note:: For more information on this widget, see <http://wiki.inkscape.org/wiki/index.php/INX_Parameters> 

        **Example**

        It works in the following manner: The user select in the optiongroup list the desired color. All pre defined colors are listed there. There is also a 'my default color' where you can set your preferred default color and a 'use color picker' to select from the color picker widget. Keep in mind that the selected color in this widget will be considered ONLY if 'use color picker' option is selected. 

        Let your .inx file contains a widget of type 'color' with the name 'myColorPicker' and another 'optiongroup' with the name 'myColorOption'::

         <param name="myColorOption" type="optiongroup" appearance="minimal" _gui-text="some text here">
             <_option value="#FF0022">my default color</_option>    <--you can set your pre define color in the form #RRGGBB
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

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     inkex.Effect.__init__(self) 
        >>>     self.OptionParser.add_option("--myColorPicker", action="store", type="string", dest="myColorPickerVar", default='0')       # parses the input parameters
        >>>     self.OptionParser.add_option("--myColorOption", action="store", type="string", dest="myColorOptionVar", default='black')   # parses the input parameter
        >>> 
        >>>   def effect(self):
        >>>     so = self.options
        >>>     [RGBstring,alpha] = inkDraw.color.parseColorPicker(so.myColorOptionVar,so.myColorPickerVar)

        """
        alphaString = 'FF'
        if stringColorOption.startswith("#"):
            return [stringColorOption, alphaString]
        else:
            if stringColorOption == 'none':
                colorString = 'none'
            else:
                if stringColorOption == 'picker':
                    [colorString, alphaString] = color.colorPickerToRGBalpha(stringColorPicker)
                else:
                    colorString = color.defined(stringColorOption)
        return [colorString, alphaString]


class marker():
    """
    Class to manipulate markers.

    This class is used to create new custom markers. Markers can be used with the lineStyle class to define line types that include start, mid and end markers

    This class contains only static methods so that you don't have to inherit this in your class

    """
    #---------------------------------------------
    @staticmethod
    def createMarker(ExtensionBaseObj, nameID, markerPath, RenameMode=0, strokeColor=color.defined('black'), fillColor=color.defined('black'), lineWidth=1.0, markerTransform=None):
        """Creates a custom line marker

        :param ExtensionBaseObj: Most of the times you have to use 'self' from inkscapeMadeEasy related objects
        :param nameID: nameID of the marker
        :param markerPath: path definition. Must follow 'd' attribute format. See <https://www.w3.org/TR/SVG/paths.html#PathElement> for further information
        :param RenameMode: Renaming behavior mode

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified.
             - 1: overwrite marker definition if nameID is already taken
             - 2: Create a new unique nameID, adding a suffix number (Please refer to inkscapeMadeEasy.uniqueIdNumber(prefix_id) ).

        :param strokeColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fillColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param lineWidth: line width of the marker. Default: 1.0
        :param markerTransform: custom transform applied to marker's path. Default: ``None`` 

           the transform must follow 'transform' attribute format. See <https://www.w3.org/TR/SVG/coords.html#TransformAttribute> for further information

        :type ExtensionBaseObj: inkscapeMadeEasy object (see example below)
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

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     nameID='myMarker'
        >>>     markerPath='M 3,0 L 0,1 L 0,-1 z'   # defines a path forming an triangle with vertices (3,0) (0,1) (0,-1)
        >>>     strokeColor=inkDraw.color.defined('red')
        >>>     fillColor=None
        >>>     RenameMode=1
        >>>     width=1
        >>>     markerTransform=None
        >>>     markerID=inkDraw.marker.createMarker(self,nameID,markerPath,RenameMode,strokeColor,fillColor,width,markerTransform)
        >>>     myLineStyle = inkDraw.lineStyle.set(1.0, markerEnd=markerID,lineColor=inkDraw.color.defined('black'))  # see lineStyle class for further information on this function
        >>> 
        >>>     #tries to make another marker with the same nameID, changing RenameMode
        >>>     strokeColor=inkDraw.color.defined('blue')
        >>>     RenameMode=0
        >>>     markerID=inkDraw.marker.createMarker(self,nameID,RenameMode,scale,strokeColor,fillColor) # this will not modify the marker
        >>>     RenameMode=1
        >>>     markerID=inkDraw.marker.createMarker(self,nameID,RenameMode,scale,strokeColor,fillColor) # modifies the marker 'myMarker'
        >>>     RenameMode=2
        >>>     markerID=inkDraw.marker.createMarker(self,nameID,RenameMode,scale,strokeColor,fillColor) # creates a new marker with nameID='myMarker-0001'

        .. note:: In next versions, path definition and transformation will be modified to make it easier. =)
        """

        # print tostring(ExtensionBaseObj.getDefinitions())

        if RenameMode == 0 and ExtensionBaseObj.findMarker(nameID):
            return nameID

        if RenameMode == 2:
            numberID = 1
            new_id = nameID + '_n%05d' % (numberID)
            while new_id in ExtensionBaseObj.doc_ids:
                numberID += 1

                new_id = nameID + '_n%05d' % (numberID)
            ExtensionBaseObj.doc_ids[new_id] = 1
            nameID = new_id

        if RenameMode == 1 and ExtensionBaseObj.findMarker(nameID):
            defs = ExtensionBaseObj.getDefinitions()
            for obj in defs.iter():
                if obj.get('id') == nameID:
                    defs.remove(obj)

        # creates a new marker
        marker_attribs = {inkex.addNS('stockid', 'inkscape'): nameID,
                          'orient': 'auto', 'refY': '0.0', 'refX': '0.0',
                          'id': nameID,
                          'style': 'overflow:visible'}

        newMarker = inkex.etree.SubElement(ExtensionBaseObj.getDefinitions(), inkex.addNS('marker', 'defs'), marker_attribs)

        if not fillColor:
            fillColor = 'none'
        if not strokeColor:
            strokeColor = 'none'

        marker_style = {'fill-rule': 'evenodd', 'fill': fillColor,
                        'stroke': strokeColor, 'stroke-width': str(lineWidth)}

        marker_lineline_attribs = {'d': markerPath, 'style': simplestyle.formatStyle(marker_style)}

        if markerTransform:
            marker_lineline_attribs['transform'] = markerTransform

        inkex.etree.SubElement(newMarker, inkex.addNS('path', 'defs'), marker_lineline_attribs)

        ExtensionBaseObj.doc_ids[nameID] = 1

        # print tostring(ExtensionBaseObj.getDefinitions())
        return nameID

    #---------------------------------------------
    @staticmethod
    def createDotMarker(ExtensionBaseObj, nameID, RenameMode=0, scale=0.4, strokeColor=color.defined('black'), fillColor=color.defined('black')):
        """Creates a dotS/M/L marker, exactly like inkscape default markers

        :param ExtensionBaseObj: Most of the times you have to use 'self' from inkscapeMadeEasy related objects
        :param nameID: nameID of the marker
        :param RenameMode: Renaming behavior mode. For more information, see documentation of marker.createMarker(...) method.

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified
             - 1: overwrite marker if nameID is already taken
             - 2: Create a new unique nameID, adding a suffix number (Please refer to inkscapeMadeEasy.uniqueIdNumber(prefix_id) ).

        :param scale: scale of the marker. To copy exactly inkscape sizes dotS/M/L, use 0.2, 0.4 and 0.8 respectively. Default: 0.4
        :param strokeColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fillColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :type ExtensionBaseObj: inkscapeMadeEasy object (see example below)
        :type nameID: string
        :type RenameMode: int
        :type scale: float
        :type strokeColor: string
        :type fillColor: string    

        :returns: NameID of the new marker
        :rtype: string

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     myMarker=inkDraw.marker.createDotMarker(self,nameID='myDotMarkerA',RenameMode=1,scale=0.5,strokeColor=inkDraw.color.defined('red'),fillColor=None)
        >>>     myLineStyle = inkDraw.lineStyle.set(1.0, markerEnd=myMarker,lineColor=inkDraw.color.defined('black'))  # see lineStyle class for further information on this function
        """

        markerPath = 'M -2.5,-1.0 C -2.5,1.7600000 -4.7400000,4.0 -7.5,4.0 C -10.260000,4.0 -12.5,1.7600000 -12.5,-1.0 C -12.5,-3.7600000 -10.260000,-6.0 -7.5,-6.0 C -4.7400000,-6.0 -2.5,-3.7600000 -2.5,-1.0 z '
        width = 1.0
        markerTransform = 'scale(' + str(scale) + ') translate(7.4, 1)'
        return marker.createMarker(ExtensionBaseObj, nameID, markerPath, RenameMode, strokeColor, fillColor, width, markerTransform)

    #---------------------------------------------
    @staticmethod
    def createCrossMarker(ExtensionBaseObj, nameID, RenameMode=0, scale=0.4, strokeColor=color.defined('black'), fillColor=color.defined('black')):
        """Creates a cross marker

        :param ExtensionBaseObj: Most of the times you have to use 'self' from inkscapeMadeEasy related objects
        :param nameID: nameID of the marker
        :param RenameMode: Renaming behavior mode. For more information, see documentation of marker.createMarker(...) method.

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified
             - 1: overwrite marker if nameID is already taken
             - 2: Create a new unique nameID, adding a suffix number (Please refer to inkscapeMadeEasy.uniqueIdNumber(prefix_id) ).

        :param scale: scale of the marker. Default: 0.4
        :param strokeColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fillColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :type ExtensionBaseObj: inkscapeMadeEasy object (see example below)
        :type nameID: string
        :type RenameMode: int
        :type scale: float
        :type strokeColor: string
        :type fillColor: string    

        :returns: NameID of the new marker
        :rtype: string

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     myMarker=inkDraw.marker.createCrossMarker(self,nameID='myDotMarkerA',RenameMode=1,scale=0.5,strokeColor=inkDraw.color.defined('red'),fillColor=None)
        >>>     myLineStyle = inkDraw.lineStyle.set(1.0, markerEnd=myMarker,lineColor=inkDraw.color.defined('black'))  # see lineStyle class for further information on this function
        """

        markerPath = 'M -5,5 L 5,-5 M 5,5 L -5,-5'
        markerTransform = 'scale(' + str(scale) + ')'
        width = 1.0
        return marker.createMarker(ExtensionBaseObj, nameID, markerPath, RenameMode, strokeColor, fillColor, width, markerTransform)

    #---------------------------------------------
    @staticmethod
    def createArrow1Marker(ExtensionBaseObj, nameID, RenameMode=0, scale=0.4, strokeColor=color.defined('black'), fillColor=color.defined('black')):
        """Creates a arrowS/M/L arrow markers (both start and end markers), exactly like inkscape

        :param ExtensionBaseObj: Most of the times you have to use 'self' from inkscapeMadeEasy related objects
        :param nameID: nameID of the marker. Start and End markers will have 'Start' and 'End' suffix respectively
        :param RenameMode: Renaming behavior mode. For more information, see documentation of marker.createMarker(...) method.

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified
             - 1: overwrite marker if nameID is already taken
             - 2: Create a new unique nameID, adding a suffix number (Please refer to inkscapeMadeEasy.uniqueIdNumber(prefix_id) ).

        :param scale: scale of the marker. Default: 0.4
        :param strokeColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fillColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :type ExtensionBaseObj: inkscapeMadeEasy object (see example below)
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

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     StartArrowMarker,EndArrowMarker=inkDraw.marker.createArrow1Marker(self,nameID='myArrow',RenameMode=1,scale=0.5,strokeColor=inkDraw.color.defined('red'),fillColor=None)
        >>>     myLineStyle = inkDraw.lineStyle.set(1.0, markerStart=StartArrowMarker,markerEnd=EndArrowMarker,lineColor='#000000')  # see lineStyle class for further information on this function
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

    #---------------------------------------------
    @staticmethod
    def createInfLineMarker(ExtensionBaseObj, nameID, RenameMode=0, scale=1.0, strokeColor=None, fillColor=color.defined('black')):
        """Creates ellipsis markers, both start and end markers.

        These markers differ from inkscape's default ellipsis since these markers are made such that the diameter of the dots are equal to the line width.

        :param ExtensionBaseObj: Most of the times you have to use 'self' from inkscapeMadeEasy related objects
        :param nameID: nameID of the marker. Start and End markers will have 'Start' and 'End' suffix respectively
        :param RenameMode: Renaming behavior mode. For more information, see documentation of marker.createMarker(...) method.

             - 0: (default) do not rename the marker. If nameID is already taken, the marker will not be modified
             - 1: overwrite marker if nameID is already taken
             - 2: Create a new unique nameID, adding a suffix number (Please refer to inkscapeMadeEasy.uniqueIdNumber(prefix_id) ).

        :param scale: scale of the marker. Default 1.0
        :param strokeColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: ``None``
        :param fillColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :type ExtensionBaseObj: inkscapeMadeEasy object (see example below)
        :type nameID: string
        :type RenameMode: int
        :type scale: float
        :type strokeColor: string
        :type fillColor: string    

        :returns: a list of strings: [startInfMarker,endInfMarker]
                    - startInfMarker: nameID of start marker
                    - endInfMarker: nameID of end marker
        :rtype: list

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     startInfMarker,endInfMarker=inkDraw.marker.createInfLineMarker(self,nameID='myInfMarker',RenameMode=1,scale=1.0,strokeColor=None,fillColor='#00FF00')
        >>>     myLineStyle = inkDraw.lineStyle.set(1.0, markerStart=startInfMarker,markerEnd=endInfMarker,lineColor='#000000')  # see lineStyle class for further information on this function
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

        nameStart = marker.createMarker(ExtensionBaseObj, nameID + 'Start', markerPath, RenameMode, strokeColor, fillColor, width, markerTransform)

        if scale != 1.0:
            markerTransform = 'translate(' + str(2.0 * scale) + ', 0) scale(' + str(scale) + ')'
        else:
            markerTransform = 'translate(' + str(2.0 * scale) + ', 0)'

        nameEnd = marker.createMarker(ExtensionBaseObj, nameID + 'End', markerPath, RenameMode, strokeColor, fillColor, width, markerTransform)

        return [nameStart, nameEnd]


class lineStyle():
    """
    Class to create line styles.

    This class is used to define line styles. It is capable of setting stroke and filling colors, line width, linejoin and linecap, markers (start, mid, and end) and stroke dash array

    This class contains only static methods so that you don't have to inherit this in your class

    """

    #---------------------------------------------
    @staticmethod
    def set(lineWidth=1.0, lineColor=color.defined('black'), fillColor=None, lineJoin='round',
            lineCap='round', markerStart=None, markerMid=None, markerEnd=None, strokeDashArray=None):
        """ Creates a new line style

        :param lineWidth: line width. Default: 1.0
        :param lineColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fillColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: ``None``
        :param lineJoin: shape of the lines at the joints. Valid values 'miter', 'round', 'bevel'. Default: round
        :param lineCap: shape of the lines at the ends. Valid values 'butt', 'square', 'round'. Default: round
        :param markerStart: marker at the start node. Default: ``None``
        :param markerMid: marker at the mid nodes. Default: ``None``
        :param markerEnd: marker at the end node. Default: ``None``
        :param strokeDashArray: dashed line pattern definition. Default: ``None`` See <http://www.w3schools.com/svg/svg_stroking.asp> for further information

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

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>> 
        >>>     # creates a line style using a dot marker at its end node
        >>>     myMarker=inkDraw.marker.createDotMarker(self,nameID='myMarker',RenameMode=1,scale=0.5,strokeColor=color.defined('red'),fillColor=None)   # see marker class for further information on this function
        >>>     myLineStyle = inkDraw.lineStyle.set(lineWidth=1.0, markerEnd=myMarker,lineColor=inkDraw.color.defined('black'),fillColor=inkDraw.color('red'))
        >>> 
        >>>     # creates a line style with dashed line (5 units dash , 10 units space
        >>>     myDashedStyle = inkDraw.lineStyle.set(lineWidth=1.0,lineColor=inkDraw.color.defined('black'),fillColor=inkDraw.color,strokeDashArray='5,10') 
        >>>     # creates a line style with a more complex pattern (5 units dash , 10 units space, 2 units dash, 3 units space
        >>>     myDashedStyle = inkDraw.lineStyle.set(lineWidth=1.0,lineColor=inkDraw.color.defined('black'),fillColor=inkDraw.color,strokeDashArray='5,10,2,3') 
        """

        if not fillColor:
            fillColor = 'none'
        if not lineColor:
            lineColor = 'none'
        if not strokeDashArray:
            strokeDashArray = 'none'

        # dictionary with the styles
        lineStyle = {'stroke': lineColor,
                     'stroke-width': str(lineWidth),
                     'stroke-dasharray': strokeDashArray,
                     'fill': fillColor}

        #Endpoint and junctions
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

    #---------------------------------------------
    @staticmethod
    def setSimpleBlack(lineWidth=1.0):
        """Defines a standard black line style.

        The only adjustable parameter is its width. The fixed parameters are: lineColor=black, fillColor=None, lineJoin='round', lineCap='round', no markers, no dash pattern

        :param lineWidth: line width. Default: 1.0
        :type lineWidth: float     

        :returns: line definition following the provided specifications
        :rtype: string

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>> 
        >>>     mySimpleStyle = inkDraw.lineStyle.setSimpleBlack(lineWidth=2.0) 

        """
        return lineStyle.set(lineWidth)


class textStyle():
    """
    Class to create text styles.

    This class is used to define text styles. It is capable of setting font size, justification, text color, font family, font style, font weight, line spacing, letter spacing and word spacing

    This class contains only static methods so that you don't have to inherit this in your class

    """
    #---------------------------------------------
    @staticmethod
    def set(fontSize=10, justification='left', textColor=color.defined('black'), fontFamily='Sans', fontStyle='normal', fontWeight='normal', lineSpacing='100%', letterSpacing='0px', wordSpacing='0px'):
        """Defines a new text style

        :param fontSize: size of the font in px. Default: 10
        :param justification: text justification. ``left``, ``right``, ``center``. Default: ``left``
        :param textColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param fontFamily: font family name. Default ``Sans``
        :param fontStyle: ``normal``  or ``italic``. Default: ``normal``
        :param fontWeight: ``normal``  or ``bold``. Default: ``normal``
        :param lineSpacing: spacing between lines in percentage. Default: ``100%``
        :param letterSpacing: extra space between letters. Format: ``_px``. Default: ``0px``
        :param wordSpacing: extra space between words. Format: ``_px``. Default: ``0px``

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

        .. Warning: This method does NOT verify whether the font family is installed in your machine or not.

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>> 
        >>>     myTextStyle=inkDraw.textStyle.set(fontSize=10, justification='left', textColor=color.defined('black'), fontFamily='Sans', fontStyle='normal', fontWeight='normal', lineSpacing='100%', letterSpacing='0px', wordSpacing='0px')
        """

        if not textColor:
            textColor = 'none'

        if justification == 'left':
            justification = 'start'
            anchor = 'start'
        if justification == 'right':
            justification = 'end'
            anchor = 'end'
        if justification == 'center':
            anchor = 'middle'

        textStyle = {'font-size': str(fontSize) + 'px',
                     'font-style': fontStyle,
                     'font-weight': fontWeight,
                     'text-align': justification,   # start, center, end
                     'line-height': lineSpacing,
                     'letter-spacing': letterSpacing,
                     'word-spacing': wordSpacing,
                     'text-anchor': anchor,   # start, middle, end
                     'fill': textColor,
                     'fill-opacity': '1',
                     'stroke': 'none',
                     'font-family': fontFamily}

        return textStyle

    #---------------------------------------------
    @staticmethod
    def setSimpleBlack(fontSize=10, justification='left'):
        """Defines a standard black text style

        The only adjustable parameter are font size and justification. The fixed parameters are: textColor=color.defined('black'), fontFamily='Sans', fontStyle='normal', fontWeight='normal', lineSpacing='100%', letterSpacing='0px', wordSpacing='0px.

        :param fontSize: size of the font in px. Default: 10
        :param justification: text justification. ``left``, ``right``, ``center``. Default: ``left``

        :type fontSize: float     
        :type justification: string

        :returns: line definition following the provided specifications
        :rtype: string

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>> 
        >>>     mySimpleStyle = inkDraw.textStyle.setSimpleBlack(fontSize=20,justification='center') 

        """
        return textStyle.set(fontSize, justification)

    #---------------------------------------------
    @staticmethod
    def setSimpleColor(fontSize=10, justification='left', textColor=color.defined('black')):
        """Defines a standard colored text style

        The only adjustable parameter are font size justification and textColor. The fixed parameters are: fontFamily='Sans', fontStyle='normal', fontWeight='normal', lineSpacing='100%', letterSpacing='0px', wordSpacing='0px.

        :param fontSize: size of the font in px. Default: 10
        :param justification: text justification. ``left``, ``right``, ``center``. Default: ``left``
        :param textColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')

        :type fontSize: float     
        :type justification: string
        :type textColor: string

        :returns: line definition following the provided specifications
        :rtype: string

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>> 
        >>>     mySimpleStyle = inkDraw.textStyle.setSimpleColor(fontSize=20,justification='center',textColor=inkDraw.color.gray(0.5)) 
        """
        return textStyle.set(fontSize, justification, textColor)


class text():
    """ Class for writing texts. It is possible to add regular inkscape's text elements or LaTeX text. For the later, the excellent 'textext' extension from Pauli Virtanen's <https://pav.iki.fi/software/textext/> is incorporated here. Please refer to `Main Features`_ section for further instructions


    This class contains only static methods so that you don't have to inherit this in your class
    
    .. note:: LaTeX support is an optional feature, **enabled by default**. Please refer to :ref:`latexSupport` on how to disable it.
    
    """
    @staticmethod
    def write(ExtensionBaseObj, text, coords, parent, textStyle=textStyle.setSimpleBlack(fontSize=10, justification='left'), fontSize=None, justification=None, angleDeg=0.0):
        """Adds a text line to the document

        :param ExtensionBaseObj: Most of the times you have to use 'self' from inkscapeMadeEasy related objects
        :param text: text to be drawn. Use \\\\n in the string to start a new line
        :param coords: position [x,y]
        :param parent: parent object
        :param textStyle: text style to be used. See class ``textStyle``. Default: textStyle.setSimpleBlack(fontSize=10,justification='left')
        :param fontSize: size of the font in px.
                - ``None``: Uses fontSize of textStyle argument (Default)
                - number: takes precedence over the size on textStyle
        :param justification: text justification. ``left``, ``right``, ``center``
                - ``None``: Uses justification of textStyle argument (Default)
                - ``left``, ``right``, ``center``: takes precedence over the justification set on textStyle
        :param angleDeg: angle of the text, counterclockwise, in degrees. Default: 0

        :type ExtensionBaseObj: inkscapeMadeEasy object (see example below)
        :type text: string
        :type coords: list
        :type parent: element object
        :type textStyle: textStyle object
        :type fontSize: float
        :type justification: string
        :type angleDeg: float

        :returns: the new text object
        :rtype: text Object

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     mySimpleStyle = inkDraw.textStyle.setSimpleBlack(fontSize=20,justification='center')  # creates a simple text style.
        >>>     
        >>>     #adds a two-line text, at the point x=5.0,y=6.0
        >>>     #               L1: 'foo bar who-hoo!'
        >>>     #               L2: 'second line!'
        >>>     myText='foo bar who-hoo!\\ntwo lines!'
        >>>     inkDraw.text.write(self, text=myText, coords=[5.0,6.0], parent=root_layer, textStyle=mySimpleStyle, fontSize=None, justification=None, angleDeg=0.0)
        >>> 
        >>>     # creates a group in root-layer and add text to it
        >>>     myGroup = self.createGroup(parent=root_layer,'textGroup')
        >>>     #adds a text 'foo bar', rotated 45 degrees, at the point x=0,y=0, overriding justification of mySimpleStyle
        >>>     inkDraw.text.write(self, text='foo bar', coords=[0.0,0.0], parent=myGroup, textStyle=mySimpleStyle, fontSize=None, justification='left', angleDeg=45.0)

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

        AttribsText = {inkex.addNS('space', 'xml'): "preserve",
                       'style': simplestyle.formatStyle(textStyle),
                       'x': str(coords[0]),
                       'y': str(coords[1]),
                       inkex.addNS('linespacing', 'sodipodi'): textStyle['line-height']}

        #textObj = inkex.etree.SubElement(parent, inkex.addNS('text','svg'), AttribsText )

        textObj = inkex.etree.Element(inkex.addNS('text', 'svg'), AttribsText)
        parent.append(textObj)

        AttribsLineText = {inkex.addNS('role', 'sodipodi'): "line",
                           'x': str(coords[0]),
                           'y': str(coords[1])}

        textLines=text.split('\\n')
        
        for n in range(len(textLines)):
          myTspan = inkex.etree.SubElement(textObj, inkex.addNS('tspan', 'svg'), AttribsLineText)
          myTspan.text = textLines[n].decode('utf-8')   
          
        if angleDeg != 0:
            ExtensionBaseObj.rotateElement(textObj, center=coords, angleDeg=angleDeg)  # negative angle bc inkscape is upside down

        return textObj

    #---------------------------------------------
    @staticmethod
    def latex(ExtensionBaseObj, parent, LaTeXtext, position, fontSize=10, refPoint='cc', textColor=color.defined('black'), LatexCommands=' ', angleDeg=0, preambleFile=None):
        """Draws a text line using LaTeX. You can use any LaTeX contents here.

        .. note:: Employs the excellent 'textext' extension from Pauli Virtanen's <https://pav.iki.fi/software/textext/> is incorporated here. Please refer to `Main Features`_ section for further instructions
        
        .. note:: LaTeX support is an optional feature that requires a few extra packages to be installed outside inkscape. **It is enabled by default**. Please refer to :ref:`latexSupport` on how to disable it. If disabled, this function will still work, internally calling the method text.write().

        :param ExtensionBaseObj: Most of the times you have to use 'self' from inkscapeMadeEasy related objects
        :param parent: parent object        
        :param LaTeXtext: text to be drawn. Can contain any latex command
        :param position: position of the reference point [x,y]  
        :param fontSize: size of the font. Assume any text of ``\\normalsize`` will have this size. Default: 10 
        :param refPoint: text reference Point. See figure below for options. Default: ``cc``
        :param textColor: color in the format ``#RRGGBB`` (hexadecimal), or ``None`` for no color. Default: color.defined('black')
        :param LatexCommands: commands to be included before LaTeXtext (default: ' '). If LaTeX support is disabled, this parameter has no effect.
        :param angleDeg: angle of the text, counterclockwise, in degrees. Default: 0
        :param preambleFile: optional preamble file to be included. Default: None. If LaTeX support is disabled, this parameter has no effect.

        :type ExtensionBaseObj: inkscapeMadeEasy object (see example below)
        :type parent: element object 
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

        .. note:: This function does not use ``textStyle`` class.

        **Reference point options**

        .. image:: ../imagesDocs/LaTeX_reference_Point.png
          :width: 400px

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

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     customCommand = r'\\newcommand{\\fooBar}{\\textbf{Foo Bar Function! WhooHoo!}}'   # do not forget the r to avoid backslash escape.
        >>>     inkDraw.text.latex(self, root_layer,r'This is one equation \\begin{align} x=y^2\\end{align} And this is my \\fooBar{}', position=[0.0,0.0], fontSize=10, refPoint='cc', textColor=inkDraw.color.defined('black'), LatexCommands=customCommand, angleDeg=0, preambleFile=None)
        """

        # write an empty svg file.

        if not LaTeXtext:  # check whether text is empty
            return 0

        tempDir=tempfile.gettempdir()
        tempFilePath = tempDir + '/temp_svg_inkscapeMadeEasy_Draw.txt'   
        
        if useLatex:  # set useLatex=False to replace latex by an standard text (much faster for debugging =)  )
          
            Dump(r'<?xml version="1.0" encoding="UTF-8" standalone="no"?><!-- Created with Inkscape (http://www.inkscape.org/) --><svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="744.09448819" height="1052.3622047" id="svg19803" version="1.1" inkscape:version="0.48.3.1 r9886" sodipodi:docname="New document 45"> <defs id="defs19805" /> <sodipodi:namedview id="base" pagecolor="#ffffff" bordercolor="#666666" borderopacity="1.0" inkscape:pageopacity="0.0" inkscape:pageshadow="2" inkscape:zoom="0.35" inkscape:cx="375" inkscape:cy="520" inkscape:document-units="px" inkscape:current-layer="layer1" showgrid="false" inkscape:window-width="500" inkscape:window-height="445" inkscape:window-x="932" inkscape:window-y="0" inkscape:window-maximized="0" /> <metadata id="metadata19808"> <rdf:RDF> <cc:Work rdf:about=""> <dc:format>image/svg+xml</dc:format> <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /> <dc:title></dc:title> </cc:Work> </rdf:RDF> </metadata> <g inkscape:label="Layer 1" inkscape:groupmode="layer" id="layer1" /></svg>',tempFilePath, 'w')

            # temp instance for determining font height. Draws a F letter just to find the height of the font
            if 2 == 1:  # turning off this part of the code.
                texTemp = textext.TexText()  # start textText (awesome extension! =] )
                texTemp.affect([r'--text=' + 'F', '--scale-factor=1', tempFilePath], output=False)
                groupLatex = texTemp.current_layer.find('g')
                BboxMin, BboxMax = ExtensionBaseObj.getBoundingBox(groupLatex)
                Height0 = BboxMax[1] - BboxMin[1]

            Height0 = 6.76  # running the code above, we get a 'F' with height of 6.76, with scale 1.0 from textext. This will be used to scale the text accordingly to fit user specification 'fontSize'

            scale = fontSize / Height0
        
            tex = textext.TexText()  # start textText (awesome extension! =] )
            if preambleFile:
                tex.affect([r'--text=' + LatexCommands + LaTeXtext, '--scale-factor=1', '--preamble-file=' + preambleFile, tempFilePath], output=False)
            else:
                tex.affect([r'--text=' + LatexCommands + LaTeXtext, '--scale-factor=1', '--preamble-file=' + ExtensionBaseObj.getBasicLatexPackagesFile(), tempFilePath], output=False)

            groupLatex = tex.current_layer.find('g')

            # change color
            for obj in groupLatex.iter():
                if obj.tag == inkex.addNS('path', 'svg') or obj.tag == 'path' or obj.tag == 'polygon':
                    obj.set('style', 'fill:' + textColor + ';stroke-width:0')

            # remove transforms
            del groupLatex.attrib["transform"]

            ExtensionBaseObj.scaleElement(groupLatex, scaleX=scale, scaleY=-scale)     # scale to fit font size
        else:
            if refPoint[1] == 'l':
                justification='left'

            if refPoint[1] == 'c':
                justification='center'

            if refPoint[1] == 'r':
                justification='right'
            
            mytextStyle = textStyle.setSimpleColor(fontSize=fontSize/0.76, justification='left', textColor=textColor)
            groupLatex = text.write(ExtensionBaseObj, LaTeXtext, [0, 0], parent,textStyle=mytextStyle, fontSize=fontSize/0.76,justification=justification, angleDeg=0.0) # attention! keep angleDeg=0.0 here bc it will be rotated below


        BboxMin, BboxMax = ExtensionBaseObj.getBoundingBox(groupLatex)
        
        if useLatex:  # set useLatex=False to replace latex by an standard text (much faster for debugging =)  )
            if refPoint[0] == 't':
                refPointY = BboxMin[1]     # BboxMin bc inkscape is upside down

            if refPoint[0] == 'c':
                refPointY = (BboxMax[1] + BboxMin[1]) / 2.0

            if refPoint[0] == 'b':
                refPointY = BboxMax[1]     # BboxMax bc inkscape is upside down

            if refPoint[1] == 'l':
                refPointX = BboxMin[0]

            if refPoint[1] == 'c':
                refPointX = (BboxMax[0] + BboxMin[0]) / 2.0

            if refPoint[1] == 'r':
                refPointX = BboxMax[0]
        else:
            refPointX = BboxMin[0]
            if refPoint[0] == 't':
                refPointY = BboxMin[1]-fontSize     # BboxMin bc inkscape is upside down

            if refPoint[0] == 'c':
                refPointY = BboxMin[1]-(fontSize)/2.0     # BboxMin bc inkscape is upside down

            if refPoint[0] == 'b':
                refPointY = BboxMax[1]     # BboxMax bc inkscape is upside down

        ExtensionBaseObj.moveElement(groupLatex, [-refPointX, -refPointY])  # move to origin
        ExtensionBaseObj.moveElement(groupLatex, [position[0], position[1]])
        if angleDeg != 0:
            ExtensionBaseObj.rotateElement(groupLatex, center=[position[0], position[1]], angleDeg=angleDeg)

        y = parent.append(groupLatex)

        return groupLatex


class line():
    """ This is a class with different methods for drawing lines.

    This class contains only static methods so that you don't have to inherit this in your class
    """
    @staticmethod
    def absCoords(parent, coordsList, offset=[0, 0], label='none', lineStyle=lineStyle.setSimpleBlack()):
        """Draws a (poly)line based on a list of absolute coordinates

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param parent: parent object
        :param coordsList: list with coords x and y.  ex  [[x1,y1], ..., [xN,yN]]
        :param offset: offset coords. Default [0,0]
        :param label: label of the line. Default 'none'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscapeMadeEasy object (see example below)
        :type coordsList: list of list
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new line object
        :rtype: line Object

        **Example**

        .. image:: ../imagesDocs/lineExample.png
          :width: 250px

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     myLineStyle = set(lineWidth=1.0, lineColor=color.defined('red'))
        >>>     
        >>> 
        >>>     # creates a polyline passing by points (0,0) (0,1) (1,1) (1,2) (2,2) using absolute coordinates
        >>>     coords=[ [0,0], [0,1], [1,1], [1,2], [2,2] ]
        >>>     inkDraw.line.absCoords(root_layer, coordsList=coords, offset=[0, 0], label='fooBarLine', lineStyle=myLineStyle)
        >>>
        >>>     # creates the same polyline translated to point (5,6). Note we just have to change the offset
        >>>     inkDraw.line.absCoords(root_layer, coordsList=coords, offset=[5, 6], label='fooBarLine', lineStyle=myLineStyle)
        """

        # string with coordinates
        string_coords = ''

        for point in coordsList:
            string_coords = string_coords + ' ' + str(point[0] + offset[0]) + ' ' + str(point[1] + offset[1])

        Attribs = {inkex.addNS('label', 'inkscape'): label,
                   'style': simplestyle.formatStyle(lineStyle),
                   # M = move, L = line, H = horizontal line, V = vertical line, C = curve, S = smooth curve, Q = quadratic Bezier curve, T = smooth quadratic Bezier curve, A = elliptical Arc,Z = closepath
                   'd': 'M ' + string_coords}

        return inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)

    #---------------------------------------------
    @staticmethod
    def relCoords(parent, coordsList, offset=[0, 0], label='none', lineStyle=lineStyle.setSimpleBlack()):
        """Draws a (poly)line based on a list of relative coordinates

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param parent: parent object
        :param coordsList: list with distances dx and dy for all points.  ex  [[dx1,dy1], ..., [dxN,dyN]]
        :param offset: offset coords. Default [0,0]
        :param label: label of the line. Default 'none'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscapeMadeEasy object (see example below)
        :type coordsList: list of list
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new line object
        :rtype: line Object

        **Example**

        .. image:: ../imagesDocs/lineExample.png
          :width: 250px

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     myLineStyle = setSimpleBlack(lineWidth=1.0)
        >>>     
        >>> 
        >>>     # creates a polyline passing by points (0,0) (0,1) (1,1) (1,2) (2,2) using relative coordinates
        >>>     coords=[ [0,1], [1,0], [0,1], [1,0] ]
        >>>     inkDraw.line.relCoords(root_layer, coordsList=coords, offset=[0, 0], label='fooBarLine', lineStyle=myLineStyle)
        >>>
        >>>     # creates the same polyline translated to point (5,6)
        >>>     inkDraw.line.relCoords(root_layer, coordsList=coords, offset=[5, 6], label='fooBarLine', lineStyle=myLineStyle)
        """

        # string with coordinates
        string_coords = ''
        for dist in coordsList:
            string_coords = string_coords + ' ' + str(dist[0]) + ' ' + str(dist[1])

        Attribs = {inkex.addNS('label', 'inkscape'): label,
                   'style': simplestyle.formatStyle(lineStyle),
                   # M = move, L = line, H = horizontal line, V = vertical line, C = curve, S = smooth curve, Q = quadratic Bezier curve, T = smooth quadratic Bezier curve, A = elliptical Arc,Z = closepath
                   'd': 'm ' + str(offset[0]) + ' ' + str(offset[1]) + string_coords}

        return inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)


class arc():
    """ This is a class with different methods for drawing arcs.

    This class contains only static methods so that you don't have to inherit this in your class
    """
    @staticmethod
    def startEndRadius(parent, Pstart, Pend, radius, offset=[0, 0], label='arc',  lineStyle=lineStyle.setSimpleBlack(), flagRightOf=True, flagOpen=True, largeArc=False):
        """Draws a circle arc from ``Pstart`` to ``Pend`` with a given radius

        .. image:: ../imagesDocs/arc_startEndRadius.png
          :width: 80px

        :param parent: parent object
        :param Pstart: start coordinate [x,y]
        :param Pend: end coordinate [x,y]
        :param radius: arc radius
        :param offset: extra offset coords [x,y]. Default [0,0]
        :param label: label of the line. Default 'arc'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()
        :param flagRightOf: sets the side of the vector Pend-Pstart which the arc must be drawn. See image below

          - True: Draws the arc to the right (Default)
          - False: Draws the arc to the left

        :param flagOpen: closes the arc. See image below. Default: True
        :param largeArc: Sets the largest arc to be drawn. See image below

          - True: Draws the largest arc
          - False: Draws the smallest arc (Default)

        :type parent: inkscapeMadeEasy object (see example below)
        :type Pstart: list
        :type Pend: list
        :type radius: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type flagRightOf: bool
        :type flagOpen: bool
        :type largeArc: bool

        :returns: the new arc object
        :rtype: line Object

        **Arc options**

        .. image:: ../imagesDocs/arc_startEndRadius_flags.png
          :width: 800px

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> 
        >>>     P1=[10.0,0.0]
        >>>     P2=[20.0,10.0]
        >>>     R=15.0
        >>>     myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>     
        >>>     #draws an opened arc
        >>>     inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[25,0], label='arc1',  lineStyle=myLineStyle, flagOpen=True)
        >>> 
        >>>     #draws a closed arc
        >>>     inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[25,20], label='arc2',  lineStyle=myLineStyle, flagOpen=False)
        >>>     
        >>>     #draws arcs with all combinations of flagRightOf and largeArc parameters
        >>>     inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[0,0], label='arc',  lineStyle=myLineStyle, flagRightOf=True, largeArc=True)
        >>>     inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[25,0], label='arc4',  lineStyle=myLineStyle, flagRightOf=False, largeArc=True)
        >>>     inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[0,40], label='arc5',  lineStyle=myLineStyle, flagRightOf=True, largeArc=False)
        >>>     inkDraw.arc.startEndRadius(parent=root_layer, Pstart=P1, Pend=P2, radius=R, offset=[25,40], label='arc6',  lineStyle=myLineStyle, flagRightOf=False, largeArc=False)
        """

        # finds the center point using some linear algebra
        StartVector = np.array(Pstart)
        EndVector = np.array(Pend)

        DistVector = EndVector - StartVector
        Dist = np.linalg.norm(DistVector)  # distance between start and end
        if Dist > 2.0 * radius:
            exit

        if (flagRightOf and largeArc) or (not flagRightOf and not largeArc):
            RadiusDirection = np.array([-DistVector[1], DistVector[0]])  # perpendicular to DistVector
        else:
            RadiusDirection = np.array([DistVector[1], -DistVector[0]])  # perpendicular to DistVector

        RadiusDirection = RadiusDirection / np.linalg.norm(RadiusDirection)  # normalize RadiusDirection
        CenterPoint = StartVector + DistVector / 2.0 + RadiusDirection * math.sqrt(radius**2.0 - (Dist / 2.0)**2.0)

        # computes the starting angle and ending angle
        temp = StartVector - CenterPoint
        AngStart = math.atan2(temp[1], temp[0])
        temp = EndVector - CenterPoint
        AngEnd = math.atan2(temp[1], temp[0])

        if flagRightOf:   # inkscape does not follow svg path format to create arcs. It uses sodipodi which is weird  =S
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
        if flagOpen == False:  # option to close arc
            arcString = arcString + ' L ' + str(CenterPoint[0] + offset[0]) + ' ' + str(CenterPoint[1] + offset[1]) + ' z'

        Attribs = {inkex.addNS('label', 'inkscape'): label,
                   'style': simplestyle.formatStyle(lineStyle),
                   inkex.addNS('type', 'sodipodi'): 'arc',
                   inkex.addNS('rx', 'sodipodi'): str(radius),
                   inkex.addNS('ry', 'sodipodi'): str(radius),
                   inkex.addNS('cx', 'sodipodi'): str(CenterPoint[0] + offset[0]),
                   inkex.addNS('cy', 'sodipodi'): str(CenterPoint[1] + offset[1]),
                   inkex.addNS('start', 'sodipodi'): sodipodiAngleStart,
                   inkex.addNS('end', 'sodipodi'): sodipodiAngleEnd,
                   # M = moveto,L = lineto,H = horizontal lineto,V = vertical lineto,C = curveto,S = smooth curveto,Q = quadratic Bezier curve,T = smooth quadratic Bezier curveto,A = elliptical Arc,Z = closepath
                   'd': 'M ' + str(offset[0] + StartVector[0]) + ' ' + str(offset[1] + StartVector[1]) + arcString}
        if flagOpen:
            Attribs[inkex.addNS('open', 'sodipodi')] = 'true'

        return inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)

    #---------------------------------------------
    @staticmethod
    def centerAngStartAngEnd(parent, centerPoint, radius, angStart, angEnd, offset=[0, 0], label='arc', lineStyle=lineStyle.setSimpleBlack(), flagOpen=True, largeArc=False):
        """Draws a circle arc given its center and start and end angles

        .. image:: ../imagesDocs/arc_centerAngStartAngEnd.png
          :width: 200px

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param parent: parent object
        :param centerPoint: center coordinate [x,y]
        :param radius: arc radius
        :param angStart: start angle in degrees
        :param angEnd: end angle in degrees
        :param offset: extra offset coords [x,y]
        :param label: label of the line. Default 'arc'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()
        :param flagOpen: closes the arc. See image below. Default: True
        :param largeArc: Sets the largest arc to be drawn. See image below

          - True: Draws the largest arc
          - False: Draws the smallest arc (Default)

        :type parent: inkscapeMadeEasy object (see example below)
        :type centerPoint: list
        :type radius: float
        :type angStart: float
        :type angEnd: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object
        :type flagOpen: bool
        :type largeArc: bool

        :returns: the new arc object
        :rtype: line Object

        **Arc options**

        .. image:: ../imagesDocs/arc_centerAngStartAngEnd_flags.png
          :width: 700px

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>     
        >>>     #draws the shortest arc
        >>>     inkDraw.arc.centerAngStartAngEnd(parent=root_layer, centerPoint=[0,0], radius=15.0, angStart=-10, angEnd=90, offset=[0,0], label='arc1',  lineStyle=myLineStyle, flagOpen=True,largeArc=False)
        >>>     #draws the longest arc
        >>>     inkDraw.arc.centerAngStartAngEnd(parent=root_layer, centerPoint=[0,0], radius=15.0, angStart=-10, angEnd=90, offset=[30,0], label='arc1',  lineStyle=myLineStyle, flagOpen=True,largeArc=True)
        """

        Pstart = [radius * math.cos(math.radians(angStart)), radius * math.sin(math.radians(angStart))]
        Pend = [radius * math.cos(math.radians(angEnd)), radius * math.sin(math.radians(angEnd))]

        pos = [centerPoint[0] + offset[0], centerPoint[1] + offset[1]]

        if abs(angEnd - angStart) <= 180:
            flagRight = largeArc
        else:
            flagRight = not largeArc

        return arc.startEndRadius(parent, Pstart, Pend, radius, pos, label, lineStyle, flagRight, flagOpen, largeArc)


class circle():
    """ This is a class with different methods for drawing circles.

    This class contains only static methods so that you don't have to inherit this in your class
    """
    @staticmethod
    def centerRadius(parent, centerPoint, radius, offset=[0, 0], label='circle', lineStyle=lineStyle.setSimpleBlack()):
        """draws a circle given its center point and radius

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param parent: parent object
        :param centerPoint: center coordinate [x,y]
        :param radius: circle's radius
        :param offset: extra offset coords [x,y]
        :param label: label of the line. Default 'circle'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscapeMadeEasy object (see example below)
        :type centerPoint: list
        :type radius: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new circle object
        :rtype: line Object

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>     
        >>>     #draws the shortest arc
        >>>     inkDraw.circle.centerRadius(parent=root_layer, centerPoint=[0,0], radius=15.0, offset=[5,1], label='circle1',  lineStyle=myLineStyle)
        """

        # arc instructions
        arcStringA = ' a %f,%f 0 1 1 %f,%f' % (radius, radius, -2 * radius, 0)
        arcStringB = ' a %f,%f 0 1 1 %f,%f' % (radius, radius, 2 * radius, 0)

        Attribs = {inkex.addNS('label', 'inkscape'): label,
                   'style': simplestyle.formatStyle(lineStyle),
                   inkex.addNS('type', 'sodipodi'): 'arc',
                   inkex.addNS('rx', 'sodipodi'): str(radius),
                   inkex.addNS('ry', 'sodipodi'): str(radius),
                   inkex.addNS('cx', 'sodipodi'): str(centerPoint[0] + offset[0]),
                   inkex.addNS('cy', 'sodipodi'): str(centerPoint[1] + offset[1]),
                   inkex.addNS('start', 'sodipodi'): '0',
                   inkex.addNS('end', 'sodipodi'): str(2 * math.pi),
                   # M = moveto,L = lineto,H = horizontal lineto,V = vertical lineto,C = curveto,S = smooth curveto,Q = quadratic Bezier curve,T = smooth quadratic Bezier curveto,A = elliptical Arc,Z = closepath
                   'd': 'M ' + str(centerPoint[0] + offset[0] + radius) + ' ' + str(centerPoint[1] + offset[1]) + arcStringA + ' ' + arcStringB + ' z'}

        return inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)

class rectangle():
    """ This is a class with different methods for drawing rectangles.

    This class contains only static methods so that you don't have to inherit this in your class
    """
    @staticmethod
    def widthHeightCenter(parent, centerPoint, width, height,radiusX=None,radiusY=None, offset=[0, 0], label='rectangle', lineStyle=lineStyle.setSimpleBlack()):
        """draws a rectangle given its center point and dimensions

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param parent: parent object
        :param centerPoint: center coordinate [x,y]
        :param width: dimension in X direction
        :param height: dimension in Y direction
        :param radiusX: rounding radius in X direction. If this value is ``None``, the rectangle will have sharp corners. Default: None
        :param radiusY: rounding radius in Y direction. If this value is ``None``, then radiusX will also be used in Y direction. If radiusX is also ``None``, then the rectangle will have sharp corners. Default: None
        :param offset: extra offset coords [x,y]
        :param label: label of the line. Default 'circle'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscapeMadeEasy object (see example below)
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

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>     
        >>>     #draws a 50x60 rectangle with radiusX=2.0 and radiusY=3.0
        >>>     inkDraw.rectangle.widthHeightCenter(parent=root_layer, centerPoint=[0,0], width=50, height=60, radiusX=2.0,radiusY=3.0, offset=[0,0], label='rect1',  lineStyle=myLineStyle)
        """
        x= centerPoint[0]-width/2.0 + offset[0]
        y= centerPoint[1]-height/2.0 + offset[1]
        
        Attribs = {inkex.addNS('label', 'inkscape'): label,
                      'style': simplestyle.formatStyle(lineStyle),
                      'width': str(width),
                      'height': str(height),
                      'x': str(x),
                      'y': str(y),
                      'rx': str(radiusX),
                      'ry': str(radiusY)}
        
        if radiusX and radiusX>0.0:
          Attribs['rx'] = str(radiusX)
          if radiusY == None:
            Attribs['ry'] = str(radiusX)
          else:
            if radiusY > 0.0:
              Attribs['ry'] = str(radiusY)

        return inkex.etree.SubElement(parent, inkex.addNS('rect', 'svg'), Attribs)

    @staticmethod
    def corners(parent, corner1, corner2, radiusX=None,radiusY=None, offset=[0, 0], label='rectangle', lineStyle=lineStyle.setSimpleBlack()):
        """draws a rectangle given the coordinates of two oposite corners

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param parent: parent object
        :param corner1: coordinates of corner 1 [x,y]
        :param corner2: coordinates of corner 1 [x,y]
        :param radiusX: rounding radius in X direction. If this value is ``None``, the rectangle will have sharp corners. Default: None
        :param radiusY: rounding radius in Y direction. If this value is ``None``, then radiusX will also be used in Y direction. If radiusX is also ``None``, then the rectangle will have sharp corners. Default: None
        :param offset: extra offset coords [x,y]
        :param label: label of the line. Default 'circle'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscapeMadeEasy object (see example below)
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

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>     
        >>>     #draws a rectangle with corners C1=[1,5] and C2=[6,10], with radiusX=2.0 and radiusY=3.0
        >>>     inkDraw.rectangle.corners(parent=root_layer, corner1=[1,5], corner2=[6,10], radiusX=2.0,radiusY=3.0, offset=[0,0], label='rect1',  lineStyle=myLineStyle)
        """
        x= (corner1[0]+corner2[0])/2.0
        y= (corner1[1]+corner2[1])/2.0
        
        width = abs(corner1[0]-corner2[0])
        height = abs(corner1[1]-corner2[1])

        return rectangle.widthHeightCenter(parent, [x,y], width, height, radiusX, radiusY, offset, label, lineStyle)    
     
class ellipse():
    """ This is a class with different methods for drawing ellipses.

    This class contains only static methods so that you don't have to inherit this in your class
    """
    @staticmethod
    def centerRadius(parent, centerPoint, radiusX, radiusY, offset=[0, 0], label='circle', lineStyle=lineStyle.setSimpleBlack()):
        """draws an ellipse given its center point and radius

        .. warning:: Keep in mind  that Inkscape's y axis is upside down!

        :param parent: parent object
        :param centerPoint: center coordinate [x,y]
        :param radiusX: circle's radius in x direction
        :param radiusY: circle's radius in y direction
        :param offset: extra offset coords [x,y]
        :param label: label of the line. Default 'circle'
        :param lineStyle: line style to be used. See class ``lineStyle``. Default: lineStyle=lineStyle.setSimpleBlack()

        :type parent: inkscapeMadeEasy object (see example below)
        :type centerPoint: list
        :type radiusX: float
        :type radiusY: float
        :type offset: list
        :type label: string
        :type lineStyle: lineStyle object

        :returns: the new ellipse object
        :rtype: line Object

        **Example**

        >>> import inkex
        >>> import inkscapeMadeEasy_Base as inkBase
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> 
        >>> class myExtension(inkBase.inkscapeMadeEasy):
        >>>   def __init__(self):
        >>>     ...
        >>>     ...
        >>> 
        >>>   def effect(self):
        >>>     root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>     myLineStyle=inkDraw.lineStyle.setSimpleBlack()
        >>>     
        >>>     #draws the shortest arc
        >>>     inkDraw.ellipse.centerRadius(parent=root_layer, centerPoint=[0,0], radiusX=15.0, radiusY=25.0, offset=[5,1], label='circle1',  lineStyle=myLineStyle)
        """

        # arc instructions
        arcStringA = ' a %f,%f 0 1 1 %f,%f' % (radiusX, radiusY, -2 * radiusX, 0)
        arcStringB = ' a %f,%f 0 1 1 %f,%f' % (radiusX, radiusY, 2 * radiusX, 0)

        Attribs = {inkex.addNS('label', 'inkscape'): label,
                   'style': simplestyle.formatStyle(lineStyle),
                   inkex.addNS('type', 'sodipodi'): 'arc',
                   inkex.addNS('rx', 'sodipodi'): str(radiusX),
                   inkex.addNS('ry', 'sodipodi'): str(radiusY),
                   inkex.addNS('cx', 'sodipodi'): str(centerPoint[0] + offset[0]),
                   inkex.addNS('cy', 'sodipodi'): str(centerPoint[1] + offset[1]),
                   inkex.addNS('start', 'sodipodi'): '0',
                   inkex.addNS('end', 'sodipodi'): str(2 * math.pi),
                   # M = moveto,L = lineto,H = horizontal lineto,V = vertical lineto,C = curveto,S = smooth curveto,Q = quadratic Bezier curve,T = smooth quadratic Bezier curveto,A = elliptical Arc,Z = closepath
                   'd': 'M ' + str(centerPoint[0] + offset[0] + radiusX) + ' ' + str(centerPoint[1] + offset[1]) + arcStringA + ' ' + arcStringB + ' z'}

        return inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), Attribs)
