#!/usr/bin/python

# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------

import math
import os
import re
import sys
from copy import deepcopy

import numpy as np
import inkex

"""
Base helper module that extends Aaron Spike's inkex.py module, adding basic manipulation functions

This module requires the following modules: inkex, re, lxml, numpy and os.
"""


# ---------------------------------------------
class inkscapeMadeEasy(inkex.Effect):
    """
    Base class for extensions.

    This class extends the inkex.Effect class by adding several basic functions to help
    manipulating inkscape elements. All extensions should inherit this class.

    """

    def __init__(self):
        inkex.Effect.__init__(self)
        self.inkscapeResolution_dpi = 96.0  # number of pixels per inch

        resolution_in = self.inkscapeResolution_dpi
        resolution_mm = self.inkscapeResolution_dpi / 25.4

        self.unitsDict = {'mm': resolution_mm,  # 25.4mm per inch
                          'cm': resolution_mm * 10.0,  # 1cm = 10mm
                          'm': resolution_mm * 1.0e3,  # 1m = 1000mm
                          'km': resolution_mm * 1.0e6,  # 1km = 1e6mm
                          'in': resolution_in,  # 1in = 96px
                          'ft': resolution_in * 12.0,  # foot = 12*in
                          'yd': resolution_in * 12.0 * 3.0,  # yard = 3*ft
                          'pt': resolution_in / 72.0,  # point 1pt = 1/72th of an inch
                          'px': 1.0, 'pc': resolution_in / 6.0}  # picas	1pc = 1/6th of and inch

    # coordinates o the origin of the grid. unfortunately the grid does not fit
    # x0=0
    # y0=-7.637817382813

    def displayMsg(self, msg):
        """Displays a message to the user.

        :param msg: message
        :type msg: string
        
        :returns: nothing
        :rtype: -

        """
        sys.stderr.write(msg + '\n')

    def getBasicLatexPackagesFile(self):
        """Returns the full path  of the ``basicLatexPackages.tex`` file with commonly used Latex packages 

        The default packages are::

        \\usepackage{amsmath,amsthm,amsbsy,amsfonts,amssymb}
        \\usepackage[per=slash]{siunitx}
        \\usepackage{steinmetz}

        You can add other packages to the file ``basicLatexPackages.tex``, located in the extension directory.

        :returns:  Full path  of the file with commonly used Latex packages 
        :rtype: string

        """
        directory = os.getcwd()
        return directory + '/textextLib/basicLatexPackages.tex'

    def Dump(self, obj, file='./dump_file.txt', mode='w'):
        """Function to easily output the result of ``str(obj)`` to a file

        This function was created to help debugging the code while it is running under inkscape.
        Since inkscape does not possess a terminal as today (2016), this function overcomes partially the
        issue of sending things to stdout by dumping result of the function ``str()`` in a text file.


        :param obj: object to sent to a file. Any type that can be used in ``str()``
        :param file: file path. Default: ``./dump_file.txt``
        :param mode: writing mode of the file Default: ``w`` (write)
        :type obj: any, as long as ``str(obj)`` is implemented (see ``__str__()`` metaclass definition )
        :type file: string
        :type mode: string
        :returns:  nothing
        :rtype: -

        **Example**

        >>> from inkscapeMadeEasy_Base import inkscapeMadeEasy 
        >>> x=inkscapeMadeEasy
        >>> vector1=[1,2,3,4,5,6]
        >>> x.Dump(vector1,file='~/temporary.txt',mode='w')   # writes the list to a file
        >>> vector2=[7,8,9,10]
        >>> x.Dump(vector2,file='~/temporary.txt',mode='a')   # append the list to a file


        """
        file = open(file, mode)
        file.write(str(obj) + '\n')
        file.close()

    def removeElement(self, element):
        """Function to remove one element or group. If the parent of the element is a group
        and has no other children, then the parent is also removed.

        :param element: element object
        :type element: element object
        :returns:  nothing
        :rtype: -

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(groupA, [[5,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkscapeMadeEasy_Draw.line.relCoords(rootLayer, [[5,0]],[0,0])    # creates a line in rootLayer
        >>> line3 = inkscapeMadeEasy_Draw.line.relCoords(groupA, [[15,0]],[10,0])    # creates a line in groupA
        >>> self.removeElement(line1)                              # removes line 1
        >>> self.removeElement(line2)                              # removes line 2
        >>> self.removeElement(line3)                              # removes line 3. Also removes groupA since this group has no other children
        >>> groupB = self.createGroup(rootLayer,label='temp1')                # creates a group inside rootLayer
        >>> line4 = inkscapeMadeEasy_Draw.line.relCoords(groupB, [[5,0]],[0,0])       # creates a line in groupB
        >>> self.removeElement(groupB)                              # removes group B and all its children

        """

        parent = element.getparent()

        parent.remove(element)

        if parent.tag == 'g' and len(parent.getchildren()) == 0:  # if object's parent is a group and has no other children, remove parent as well
            temp = parent.getparent()
            if temp is not None:
                temp.remove(parent)

    def exportSVG(self, element, fileOut):
        """ Export the elements in a new svgfile

        This function will export the element in a new SVG file. If a list of elements is passed as argument. All elements in the list will be exported to the same file.

        :param element: element or list of elements to be exported
        :param fileOut: file path, including the extension.
        :type element: element or list of elements
        :type file: string
        :returns:  nothing
        :rtype: -

        .. note:: All the defs of the original file will be copied to the new file. Therefore you might want to run te vacuum tool to cleanup the new SVG file

        **Example**

        >>> from inkscapeMadeEasy_Base import inkscapeMadeEasy
        >>> import inkscapeMadeEasy_Draw as inkDraw
        >>> x=inkscapeMadeEasy
        >>> rootLayer = x.document.getroot()                             # retrieves the root layer of the file
        >>> groupA = x.createGroup(rootLayer,label='temp')               # creates a group inside rootLayer
        >>> groupB = x.createGroup(rootLayer,label='child')              # creates a group inside groupA
        >>> line1 = inkDraw.line.relCoords(groupA, [[10,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(groupB, [[20,0]],[0,0])       # creates a line in groupB
        >>> self.exportSVG(line1,'file1.svg')                            # exports only line1
        >>> self.exportSVG(groupA,'file2.svg')                           # exports groupA (and all elements contained in it)
        >>> self.exportSVG([groupA,groupB],'file3.svg')                  # exports groupA and groupB (and all elements contained in it) to the same file

        """
        document = inkex.etree.fromstring(blankSVG)

        elem_tmp = deepcopy(element)
        # add definitions
        defs_tmp = deepcopy(self.getDefinitions())
        document.append(defs_tmp)

        # add elements
        if isinstance(elem_tmp, list):
            for e in elem_tmp:
                document.append(e)
        else:
            document.append(elem_tmp)

        et = inkex.etree.ElementTree(document)
        et.write(fileOut, pretty_print=True)

    def uniqueIdNumber(self, prefix_id):
        """ Generates a unique ID with a given prefix ID by adding a numeric suffix

        This function is used to generate a valid unique ID by concatenating a given prefix with a
        numeric suffix. The overall format is ``prefix-%05d``.

        This function makes sure the ID is unique by checking in ``doc_ids`` member.
        This function is specially useful for creating an unique ID for markers and other elements in defs.


        :param prefix_id: prefix of the ID
        :type prefix_id: string
        :returns: the unique ID
        :rtype: string

        .. note:: This function has been adapted from Aaron Spike's inkex.py  https://github.com/hacktoon/ink2canvas/blob/master/ink2canvas/lib/inkex.py

        **Example**

        >>> from inkscapeMadeEasy_Base import inkscapeMadeEasy 
        >>> x=inkscapeMadeEasy
        >>> a=x.uniqueIdNumber('myName')   # a=myName-00001
        >>> b=x.uniqueIdNumber('myName')   # b=myName-00002
        >>> c=x.uniqueIdNumber('myName')   # c=myName-00003


        """
        numberID = 1
        new_id = prefix_id + '-%05d' % numberID
        while new_id in self.doc_ids:
            numberID += 1
            new_id = prefix_id + '-%05d' % numberID
        self.doc_ids[new_id] = 1

        return new_id

    # ---------------------------------------------
    def getDefinitions(self):
        """ retrieves the Defs element of the svg file.

        This function returns the element Defs of the current svg file. This elements stores the definition (e.g. marker definition)

        if no Defs can be found, a new empty Defs is created

        :returns: the defs element
        :rtype: etree element

        """
        defs = self.getElemFromXpath('/svg:svg//svg:defs')
        if defs is None:
            defs = inkex.etree.SubElement(self.document.getroot(), inkex.addNS('defs', 'svg'))

        return defs

    # ---------------------------------------------
    def unifyDefs(self):
        """Unify all <defs> nodes in a single <defs> node.

        :returns: None
        :rtype: -

        .. note:: This function does not check whether the ids are unique
        """
        root = self.getElemFromXpath('/svg:svg')
        mainDef = self.getDefinitions()

        for d in root.findall('.//svg:defs', namespaces=inkex.NSS):
            if d != mainDef:
                for child in d:
                    mainDef.append(child)
                    if child.tag == inkex.addNS('g', 'svg') or child.tag == 'g':
                        self.ungroup(child)
                d.getparent().remove(d)

    # ---------------------------------------------
    def getDefsByTag(self, tag='marker'):
        """ retrieves the Defs elements of the svg file of a given a tag.

        :returns: a list with the def elements
        :rtype: list of etree element

        """

        return self.getDefinitions().findall('.//svg:%s' % tag, namespaces=inkex.NSS)

    # ---------------------------------------------
    def getDefsById(self,id):
        """ return a list of elements in the defs node, given (part of) the id

        :returns: a list with the def elements
        :rtype: list of etree element

        """

        return self.getDefinitions().xpath('./*[contains(@id,"%s")]' % id)

    # ---------------------------------------------
    def getElemFromXpath(self, xpath):
        """ returns the element from the xml, given its xpath

        :param xpath: tag of the element to be searched
        :type xpath: string
        :returns: element
        :rtype: element

        **Example**

        >>> from inkscapeMadeEasy_Base import inkscapeMadeEasy
        >>> x=inkscapeMadeEasy
        >>> name = x.getElemFromXpath('/svg:svg//svg:defs')   # returns the list of definitions of the document

        """
        elem = self.xpathSingle(xpath)
        return elem

    # ---------------------------------------------
    def getElemAttrib(self, elem, attribName):
        """ Returns the atribute of one element, given the atribute name


        :param elem: elem under consideration
        :param attribName: attribute to be searched. Format:  namespace:attrName
        :type elem: element
        :type attribName: string
        :returns: attribute
        :rtype: string

        >>> from inkscapeMadeEasy_Base import inkscapeMadeEasy
        >>> x=inkscapeMadeEasy
        >>> elem= x.getElemFromXpath('/svg:svg')
        >>> docNAme = x.getElemAttrib(elem,'sodipodi:docname')
        """
        # splits namespace and attrib name
        atribList = attribName.split(':')

        if len(atribList) == 1:  # if has no namespace
            attrib = attribName
        else:  # if has namespace
            namespace = inkex.NSS[atribList[0]]
            attrib = '{%s}' % namespace + atribList[1]

        return elem.attrib[attrib]

    # ---------------------------------------------
    def getDocumentScale(self):
        """returns the scale of the document

        **Example**

        >>> scale = x.getDocumentScale()

        """

        try:
            elem = self.getElemFromXpath('/svg:svg')
            width = float(self.getElemAttrib(elem, 'width').replace(self.documentUnit, ''))

            viewBox = self.getElemFromXpath('/svg:svg')
            viewBox_width = float(self.getElemAttrib(viewBox, 'viewBox').split(' ')[2])

            doc_scale = viewBox_width / width
        except:
            doc_scale = 1.0

        return doc_scale

    # ---------------------------------------------
    def getDocumentName(self):
        """returns the name of the document
        
        :returns: fileName
        :rtype: string
        
        **Example**

        >>> from inkscapeMadeEasy_Base import inkscapeMadeEasy
        >>> x=inkscapeMadeEasy
        >>> name = x.getDocumentName()
        
        """
        elem = self.getElemFromXpath('/svg:svg')
        try:
            fileName = self.getElemAttrib(elem, 'sodipodi:docname')
        except:
            fileName = None
        return fileName

    # ---------------------------------------------
    def getDocumentUnit(self):
        """returns the unit of the document
        
        :returns: unit string code. See table below
        :rtype: string
        
        **Units**
        
        The list of available units are:
        
        ==================   ============   =============
        Name                 string code    relation
        ==================   ============   =============
        millimetre           mm             1in = 25.4mm
        centimetre           cm             1cm = 10mm
        metre                m              1m = 100cm
        kilometre            km             1km = 1000m
        inch                 in             1in = 96px
        foot                 ft             1ft = 12in
        yard                 yd             1yd = 3ft
        point                pt             1in = 72pt
        pixel                px             
        pica                 pc             1in = 6pc
        ==================   ============   =============
        
        **Example**
        
        >>> docunit = self.getDocumentUnit()    #returns 'cm', 'mm', etc.
        
        
        """
        elem = self.getElemFromXpath('/svg:svg/sodipodi:namedview')
        try:
            unit = self.getElemAttrib(elem, 'inkscape:document-units')
        except:
            unit = 'px'
        return unit

    # ---------------------------------------------
    def getcurrentLayer(self):
        """returns the current layer of the document
        
        :returns: name of the current layer
        :rtype: string
        
        **Example**
        
        >>> from inkscapeMadeEasy_Base import inkscapeMadeEasy 
        >>> x=inkscapeMadeEasy
        >>> name = x.getDocumentName()
        
        """
        return self.current_layer

    # ---------------------------------------------
    def removeAbsPath(self, element):
        abspath = self.getElemAttrib(element, 'sodipodi:absref')
        fileName = os.path.basename(abspath)
        dirName = os.path.dirname(abspath)

        # removes sodipodi:absref attribute
        namespace = inkex.NSS['sodipodi']
        attrib = '{%s}' % namespace + 'absref'

        element.attrib.pop(attrib, None)

        # adds sodipodi:relref
        attrib = '{%s}' % namespace + 'relref'
        element.set(attrib, fileName)

    # ---------------------------------------------
    def unit2userUnit(self, value, unit_in):
        """Converts a value from given unit to inkscape's default unit (px)

        :param value: value to be converted
        :param unit_in: input unit string code. See table below
        :type value: float
        :type unit_in: string
        :returns: converted value
        :rtype: float
        
        **Units**
        
        The list of available units are:
        
        ==================   ============   =============
        Name                 string code    relation
        ==================   ============   =============
        millimetre           mm             1in = 25.4mm
        centimetre           cm             1cm = 10mm
        metre                m              1m = 100cm
        kilometre            km             1km = 1000m
        inch                 in             1in = 96px
        foot                 ft             1ft = 12in
        yard                 yd             1yd = 3ft
        point                pt             1in = 72pt
        pixel                px             
        pica                 pc             1in = 6pc
        ==================   ============   =============

        **Example**
        
        >>> x_cm = 5.0
        >>> x_px = self.unit2userUnit(x_cm,'cm')       # converts  5.0cm -> 188.97px
        """

        return value * self.unitsDict[unit_in.lower()]

    # ---------------------------------------------
    def userUnit2unit(self, value, unit_out):
        """Converts a value from inkscape's default unit (px) to specified unit
        
        :param value: value to be converted
        :param unit_out: output unit string code. See table below
        :type value: float
        :type unit_out: string
        :returns: converted value
        :rtype: float
        
        **Units**
        
        The list of available units are:
        
        ==================   ============   =============
        Name                 string code    relation
        ==================   ============   =============
        millimetre           mm             1in = 25.4mm
        centimetre           cm             1cm = 10mm
        metre                m              1m = 100cm
        kilometre            km             1km = 1000m
        inch                 in             1in = 96px
        foot                 ft             1ft = 12in
        yard                 yd             1yd = 3ft
        point                pt             1in = 72pt
        pixel                px             
        pica                 pc             1in = 6pc
        ==================   ============   =============

        **Example**

        >>> x_px = 5.0
        >>> x_cm = self.userUnit2unit(x_px,'cm')       # converts  5.0px -> 0.1322cm
        """
        return value / float(self.unitsDict[unit_out.lower()])

    # ---------------------------------------------
    def unit2unit(self, value, unit_in, unit_out):
        """Converts a value from one provided unit to another unit
        
        :param value: value to be converted
        :param unit_in: input unit string code. See table below
        :param unit_out: output unit string code. See table below
        :type value: float
        :type unit_in: string
        :type unit_out: string
        :returns: converted value
        :rtype: float
        
        **Units**
        
        The list of available units are:
        
        ==================   ============   =============
        Name                 string code    relation
        ==================   ============   =============
        millimetre           mm             1in = 25.4mm
        centimetre           cm             1cm = 10mm
        metre                m              1m = 100cm
        kilometre            km             1km = 1000m
        inch                 in             1in = 96px
        foot                 ft             1ft = 12in
        yard                 yd             1yd = 3ft
        point                pt             1in = 72pt
        pixel                px             
        pica                 pc             1in = 6pc
        ==================   ============   =============

        **Example**

        >>> x_in = 5.0
        >>> x_cm = self.unit2unit(x_in,'in','cm')       # converts  5.0in -> 12.7cm
        """
        return value * self.unitsDict[unit_in.lower()] / float(self.unitsDict[unit_out.lower()])

    # ---------------------------------------------
    def createGroup(self, parent, label='none'):
        """Creates a new empty group of elements.

        This function creates a new empty group of elements. In order to create new elements inside
        this groups you must create them informing the group as the parent element.


        :param parent: parent object of the group. It can be another group or the root element
        :param label: label of the group. Default: 'none'
        :type parent: element object
        :type label: string
        :returns: the group object
        :rtype: group element


        .. note:: The label does not have to be unique

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> groupB = self.createGroup(groupA,label='child')                  # creates a group inside groupA
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(groupA, [[10,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkscapeMadeEasy_Draw.line.relCoords(groupB, [[20,0]],[0,0])       # creates a line in groupB
        """
        if label != 'none':
            g_attribs = {inkex.addNS('label', 'inkscape'): label}
            group = inkex.etree.SubElement(parent, 'g', g_attribs)
        else:
            group = inkex.etree.SubElement(parent, 'g')

        return group

    # ---------------------------------------------
    def ungroup(self, group):
        """Ungroup elements

        The new parent element of the ungrouped elements will be the parent of the removed group. See example below

        :param group: group to be removed
        :type group: group element
        :returns: none
        :rtype: -

        **Example**


        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> groupB = self.createGroup(groupA,label='temp')                # creates a group inside groupA
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(groupA, [[10,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkscapeMadeEasy_Draw.line.relCoords(groupB, [[20,0]],[0,0])       # creates a line in groupB
        >>> line3 = inkscapeMadeEasy_Draw.line.relCoords(groupB, [[30,0]],[0,0])       # creates a line in groupB
        >>>  # at this point, the file struct is:   groupA[ line1, groupB[ line2, line3 ] ]
        >>> self.ungroup(groupB)                                                       # ungroup line2 and line3.
        >>>  # now the file struct is:   groupA[ line1, line2, line3 ]
        """

        if group.tag == 'g' or group.tag == inkex.addNS('g', 'svg'):  # if object is a group
            parent = group.getparent()

            if parent is not None:
                for child in group:
                    parent.append(child)

                self.removeElement(group)

        return

    # ---------------------------------------------
    def getTransformMatrix(self, element):
        """Returns the transformation attribute of the given element and the resulting transformation matrix (numpy Array)

        This function is used to extract the transformation operator of a given element.

        :param element: element object
        :type element: element object
        :returns: [transfAttrib, transfMatrix]

          - transfAttrib: string containing all transformations as it is in the file
          - transfMatrix: numpy array with the resulting transformation matrix
        :rtype: tuple

        If the element does not have any transformation attribute, this function returns:
           - transfAttrib=''
           - transfMatrix=identity matrix
        """

        transfAttrib = ''
        transfMatrix = np.eye(3)

        if 'transform' in element.attrib:
            transfAttrib = element.attrib['transform']

        if not transfAttrib:
            return transfAttrib, transfMatrix

        # split operation into several strings
        listOperations = [e + ')' for e in transfAttrib.replace(',', ' ').split(')') if e != ""]

        for operation in listOperations:
            if 'translate' in operation:
                data = re.compile("translate\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                x = float(data[0])
                y = float(data[1])
                mat = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'scale' in operation:
                data = re.compile("scale\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                scalex = float(data[0])
                if len(data) == 2:
                    scaley = float(data[1])
                else:
                    scaley = scalex
                mat = np.diag([scalex, scaley, 1])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'rotate' in operation:
                data = re.compile("rotate\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                angleRad = -float(data[0]) * np.pi / 180.0  # negative angle because inkscape is upside down =(
                matRot = np.array([[np.cos(angleRad), np.sin(angleRad), 0], [-np.sin(angleRad), np.cos(angleRad), 0], [0, 0, 1]])
                if len(data) == 3:  # must translate before and after rotation
                    x = float(data[1])
                    y = float(data[2])
                    matBefore = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])  # translation before rotation
                    matAfter = np.array([[1, 0, -x], [0, 1, -y], [0, 0, 1]])  # translation after rotation
                    matRot = np.dot(matBefore, matRot)
                    matRot = np.dot(matRot, matAfter)

                transfMatrix = np.dot(transfMatrix, matRot)

            if 'skewX' in operation:
                data = re.compile("skewX\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                angleRad = float(data[0]) * np.pi / 180.0
                mat = np.array([[1, np.tan(angleRad), 0], [0, 1, 0], [0, 0, 1]])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'skewY' in operation:
                data = re.compile("skewY\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                angleRad = float(data[0]) * np.pi / 180.0
                mat = np.array([[1, 0, 0], [np.tan(angleRad), 1, 0], [0, 0, 1]])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'matrix' in operation:
                data = re.compile("matrix\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                a = float(data[0])
                b = float(data[1])
                c = float(data[2])
                d = float(data[3])
                e = float(data[4])
                f = float(data[5])
                mat = np.array([[a, c, e], [b, d, f], [0, 0, 1]])
                transfMatrix = np.dot(transfMatrix, mat)

        return transfAttrib, transfMatrix

    # ---------------------------------------------
    def rotateElement(self, element, center, angleDeg):
        """Rotates the element using the transformation attribute.

        It is possible to rotate elements isolated or entire groups.

        :param element: element object to be rotated
        :param center: tuple with center point of rotation
        :param angleDeg: angle of rotation in degrees, counter-clockwise direction
        :type element: element object
        :type center: tuple
        :type angleDeg: float
        :returns:  nothing
        :rtype: -

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(groupA, [[5,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkscapeMadeEasy_Draw.line.relCoords(rootLayer, [[5,0]],[0,0])    # creates a line in rootLayer
        >>> self.rotateElement(line2,[0,0],120)                              # rotates line2 120 degrees around center x=0,y=0
        >>> self.rotateElement(groupA,[1,1],-90)                             # rotates groupA -90 degrees around center x=1,y=1
        """
        transfString = ''

        if angleDeg == 0:
            return

        if 'transform' in element.attrib:
            transfString = element.attrib['transform']

        # if transform attribute is present, we must add the new rotation
        if transfString:
            newTransform = 'rotate(%f %f %f) %s' % (-angleDeg, center[0], center[1], transfString)  # negative angle bc inkscape is upside down
        else:  # if no transform attribute was found
            newTransform = 'rotate(%f %f %f)' % (-angleDeg, center[0], center[1])  # negative angle bc inkscape is upside down

        element.attrib['transform'] = newTransform

    def copyElement(self, element, newParent, distance=None, angleDeg=None):
        """Copies one element to the same or other parent Element.

        It is possible to copy elements isolated or entire groups.

        :param element: element object to be copied
        :param newParent: New parent object. It can be another group or the group
        :param distance: tuple with the distance to move the object. If None, then the copy is placed at the same position
        :param angleDeg: angle of rotation in degrees, counter-clockwise direction
        :type element: element object
        :type newParent: element object
        :type distance: tuple
        :type angleDeg: float
        :returns:  newElement
        :rtype: element object

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(groupA, [[5,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkscapeMadeEasy_Draw.line.relCoords(rootLayer, [[5,0]],[0,0])    # creates a line in rootLayer
        >>> self.copyElement(line2,groupA)                                  # create a copy of line2 in groupA
        >>> self.moveElement(groupA,[10,-10])                                # moves line2  DeltaX=10, DdeltaY=-10
        """
        newElem = deepcopy(element)
        newParent.append(newElem)

        if distance is not None:
            self.moveElement(newElem, distance)

        if angleDeg is not None:
            self.rotateElement(newElem, self.getCenter(newElem), angleDeg)

        return newElem

    # ---------------------------------------------
    def moveElement(self, element, distance):
        """Moves the element using the transformation attribute.

        It is possible to move elements isolated or entire groups.

        :param element: element object to be rotated
        :param distance: tuple with the distance to move the object
        :type element: element object
        :type distance: tuple
        :returns:  nothing
        :rtype: -

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(groupA, [[5,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkscapeMadeEasy_Draw.line.relCoords(rootLayer, [[5,0]],[0,0])    # creates a line in rootLayer
        >>> self.moveElement(line2,[10,10])                                  # moves line2  DeltaX=10, DdeltaY=10
        >>> self.moveElement(groupA,[10,-10])                                # moves line2  DeltaX=10, DdeltaY=-10
        """

        if distance == 0:
            return

        transfString = ''

        if 'transform' in element.attrib:
            transfString = element.attrib['transform']

        # if transform attribute is present, we must add the new translation
        if transfString:
            newTransform = 'translate(%f %f) %s ' % (distance[0], distance[1], transfString)
        else:  # if no transform attribute was found
            newTransform = 'translate(%f %f)' % (distance[0], distance[1])

        element.attrib['transform'] = newTransform

    # ---------------------------------------------
    def scaleElement(self, element, scaleX=1.0, scaleY=0.0, center=None):
        """Scales the element using the transformation attribute.

        It is possible to scale elements isolated or entire groups.

        :param element: element object to be rotated
        :param scaleX: scaling factor in X direction. Default=1.0
        :param scaleY: scaling factor in Y direction. Default=0.0
        :param center: center point considered as the origin for the scaling. Default=None. If None, the origin is adopted
        :type element: element object
        :type scaleX: float
        :type scaleX: float
        :type center: tuple
        :returns:  nothing
        :rtype: -


        .. note:: If scaleY==0, then scaleY=scaleX is assumed (default behavior)

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> circ1 = centerRadius(groupA,centerPoint=[0,0],radius=1.0)        # creates a line in groupA
        >>> circ2 = centerRadius(rootLayer,centerPoint=[0,0],radius=1.0)     # creates a line in rootLayer
        >>> self.scaleElement(circ1,2.0)                                     # scales x2 in both X and Y directions
        >>> self.scaleElement(circ1,2.0,3.0)                                 # scales x2 in X and x3 in Y
        >>> self.scaleElement(groupA,0.5)                                    # scales x0.5 the group in both X and Y directions
        """
        if center is not None:
            self.moveElement(element, [-center[0], -center[1]])

        transfString = ''

        if 'transform' in element.attrib:
            transfString = element.attrib['transform']

        # if transform attribute is present, we must add the new translation
        if transfString:
            if scaleY != 0.0:
                newTransform = 'scale(%f %f) %s ' % (scaleX, scaleY, transfString)
            else:
                newTransform = 'scale(%f) %s' % (scaleX, transfString)
        else:  # if no transform attribute was found
            if scaleY != 0.0:
                newTransform = 'scale(%f %f)' % (scaleX, scaleY)
            else:
                newTransform = 'scale(%f)' % scaleX

        element.attrib['transform'] = newTransform

        if center is not None:
            self.moveElement(element, [center[0], center[1]])

    # ---------------------------------------------
    def findMarker(self, markerName):
        """Search for markerName in the document.

        :param markerName: marker name
        :type markerName: string

        :returns: True if markerName was found
        :rtype: bool
        """

        for m in self.getDefsByTag(tag='marker'):
            if m.get('id') == markerName:
                return True

        return False

    # ---------------------------------------------
    def getPoints(self, element):
        """Retrieves the list of points of the element.

        This function works on paths, texts or groups. In the case of a group, the function will include recursively all its components

        :param element: element object
        :type element: element object
        :returns: list of points
        :rtype: list of list

        .. note:: This function will consider any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                                   # retrieves the root layer of the file
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(rootLayer, [[5,0],[0,6]],[0,0])   # creates a line in groupA
        >>> list = self.getPoints(line1)                                          # gets list = [[0.0, 0.0], [5.0, 0.0], [5.0, 6.0]]

        """

        # stores the list of coordinates
        listCoords = []

        # check if element is valid. 'path', 'text' and 'g' are valid
        accepted_strings = set([inkex.addNS('path', 'svg'), inkex.addNS('text', 'svg'), 'g', 'path', 'use', inkex.addNS('use', 'svg')])
        if element.tag not in accepted_strings:
            return listCoords

        if element.tag == inkex.addNS('path', 'svg') or element.tag == 'path':  # if object is path

            # adds special character between letters and splits. the first regular expression excludes e and E bc they are used to represent scientific notation  =S
            dString = re.sub('([a-df-zA-DF-Z])+?', r'#\1#', element.attrib['d']).replace('z', '').replace('Z', '').replace(',', ' ').split('#')

            dString = [i.lstrip() for i in dString]  # removes leading spaces from strings
            dString = filter(None, dString)  # removes empty elements
            Xcurrent = 0
            Ycurrent = 0

            while len(dString) > 0:
                commandType = dString[0]
                argument = [float(x) for x in dString[1].split()]  # extracts arguments from M command and converts to float
                del dString[0]
                del dString[0]

                if commandType in 'mMlLtT':  # extracts points from command 'move to' M/m or 'line to' l/L or 'smooth quadratic Bezier curveto't/T
                    X = argument[0::2]  # 2 parameters per segment, x is 1st
                    Y = argument[1::2]  # 2 parameters per segment, y is 2nd

                if commandType in 'hH':  # extracts points from command 'horizontal line' h/H
                    X = argument
                    Y = [Ycurrent] * len(X)

                if commandType in 'vV':  # extracts points from command 'vertical line' v/V
                    Y = argument
                    X = [Xcurrent] * len(Y)

                if commandType in 'cC':  # extracts points from command 'Bezier Curve' c/C
                    X = argument[4::6]  # 6 parameters per segment, x is 5th
                    Y = argument[5::6]  # 6 parameters per segment, y is 6th

                if commandType in 'sSqQ':  # extracts points from command 'quadratic Bezier Curve' q/Q or 'smooth curveto' s/S
                    X = argument[2::4]  # 4 parameters per segment, x is 3rd
                    Y = argument[3::4]  # 4 parameters per segment, y is 4th

                if commandType in 'aA':  # extracts points from command 'arc' a/A
                    X = argument[5::7]  # 7 parameters per segment, x is 6th
                    Y = argument[6::7]  # 7 parameters per segment, y is 7th

                if commandType in 'h':  # if h
                    for i in range(0, len(X)):  # convert to abs coordinates
                        if i == 0:
                            X[i] = X[i] + Xcurrent
                        else:
                            X[i] = X[i] + X[i - 1]

                if commandType in 'v':  # if v
                    for i in range(0, len(Y)):  # convert to abs coordinates
                        if i == 0:
                            Y[i] = Y[i] + Ycurrent
                        else:
                            Y[i] = Y[i] + Y[i - 1]

                if commandType in 'mltcsqa':  # if m or l
                    for i in range(0, len(X)):  # convert to abs coordinates
                        if i == 0:
                            X[i] = X[i] + Xcurrent
                            Y[i] = Y[i] + Ycurrent
                        else:
                            X[i] = X[i] + X[i - 1]
                            Y[i] = Y[i] + Y[i - 1]

                coords = zip(X, Y)
                listCoords.extend(coords)
                Xcurrent = X[-1]
                Ycurrent = Y[-1]

        if element.tag == inkex.addNS('text', 'svg'):  # if object is a text
            x = float(element.attrib['x'])
            y = float(element.attrib['y'])
            coords = [[x, y]]
            listCoords.extend(coords)

        if element.tag == 'g':  # if object is a group
            for obj in element.iterchildren("*"):
                if obj != element and obj.tag != 'defs':
                    listPoints = self.getPoints(obj)
                    listCoords.extend(listPoints)

        if element.tag == 'use' or element.tag == inkex.addNS('use', 'svg'):  # if object is a use
            listCoordsTemp = []
            x = float(element.attrib['x'])
            y = float(element.attrib['y'])
            link = self.getElemAttrib(element, 'xlink:href').replace('#','')
            elemLink = self.getElementById(link)
            for obj in elemLink.iter():
                if obj != elemLink:
                    listPoints = self.getPoints(obj)
                    listCoordsTemp.extend(listPoints)

            #apply translation
            listCoords=[[coord[0]+x,coord[1]+y] for coord in listCoordsTemp]


        # apply transformation
        if len(listCoords)>0:

            # creates numpy array with the points to be transformed
            transfMat = self.getTransformMatrix(element)[1]

            coordsNP = np.hstack((np.array(listCoords), np.ones([len(listCoords), 1]))).transpose()

            coordsTransformed = np.dot(transfMat, coordsNP)
            coordsTransformed = np.delete(coordsTransformed, 2, 0).transpose().tolist()  # remove last line, transposes and converts to list of lists

        else:
            coordsTransformed = []

        return coordsTransformed

    # ---------------------------------------------
    def getBoundingBox(self, element):
        """Retrieves the bounding Box of the element.

        This function works on paths, texts or groups. In the case of a group, the function will consider recursively all its components

        :param element: element object
        :type element: element object
        :returns: two lists: [xMin,yMin] and [xMax,yMax]
        :rtype: list

        .. note:: This function will consider any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                                   # retrieves the root layer of the file
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(rootLayer, [[5,0],[0,6]],[0,0])   # creates a line in groupA
        >>> BboxMin,BboxMax = self.getBoundingBox(line1)                          # gets BboxMin = [0.0, 0.0] and BboxMax = [5.0, 6.0]

        """
        coords = self.getPoints(element)
        coordsNP = np.array(coords)

        bboxMax = np.max(coordsNP, 0)
        bboxMin = np.min(coordsNP, 0)
        return bboxMin.tolist(), bboxMax.tolist()

    # ---------------------------------------------
    def getCenter(self, element):
        """Retrieves the center coordinates of the bounding Box of the element.

        This function works on paths, texts or groups. In the case of a group, the function will consider recursively all its components

        :param element: element object
        :type element: element object
        :returns: two lists: [xCenter,yCenter]
        :rtype: list

        .. note:: This function will consider any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                                   # retrieves the root layer of the file
        >>> line1 = inkscapeMadeEasy_Draw.line.relCoords(rootLayer, [[5,0],[0,6]],[0,0])   # creates a line in groupA
        >>> Center = self.getCenter(line1)                                        # gets Center = [2.5, 3.0]

        """

        bboxMin, bboxMax = self.getBoundingBox(element)

        bboxCenter = [(bboxMax[0] + bboxMin[0]) / 2, (bboxMax[1] + bboxMin[1]) / 2]

        return bboxCenter

    def getSegmentFromPoints(self, pointList, normalDirection='R'):
        """given two points of a straight line segment, returns the parameters of that segment:
        
        length, angle (in radians), tangent unitary vector and normal unitary vector

        :param pointList: start and end coordinates [ Pstart, Pend ]
        :param normalDirection:
        
          - 'R': normal vector points to the right of the tangent vector (Default)
          - 'L': normal vector points to the left of the tangent vector (Default)
          
        :type pointList: list of points
        :type normalDirection: string
    
        :returns: list: [length, theta, t_versor,n_versor]
        :rtype: list
        
        **Example**

        >>> segmentParam = getSegmentFromPoints([[1,1],[2,2]],'R')                               # returns [1.4142, 0.78540, [0.7071,0.7071], [0.7071,-0.7071] ]
        >>> segmentParam = getSegmentFromPoints([[1,1],[2,2]],'L')                               # returns [1.4142, 0.78540, [0.7071,0.7071], [-0.7071,0.7071] ]


        """

        # tangent versor (pointing P2)
        P1 = np.array(pointList[0])
        P2 = np.array(pointList[1])

        t_vector = P2 - P1
        length = np.linalg.norm(t_vector)
        t_versor = t_vector / length

        # normal vector: counter-clockwise with respect to tangent vector
        if normalDirection in 'rR':
            n_versor = np.array([t_versor[1], -t_versor[0]])
        if normalDirection in 'lL':
            n_versor = np.array([-t_versor[1], t_versor[0]])

        # angle
        theta = math.atan2(t_versor[1], t_versor[0])

        return [length, theta, t_versor, n_versor]

    def getSegmentParameters(self, element, normalDirection='R'):
        """given a path segment composed by only two points, returns the parameters of that segment:
        
        length, angle (in radians), start point, end point, tangent unitary vector and normal unitary vector

        This function works with paths only.

        :param element: path element object
        :param normalDirection:
        
          - 'R': normal vector points to the right of the tangent vector (Default)
          - 'L': normal vector points to the left of the tangent vector (Default)
          
        :type element: element object
        :type normalDirection: string
        
        :returns: list: [Pstart,Pend,length, theta, t_versor,n_versor]
        :rtype: list

        If the element is not a path, the function returns an empty list
        If the path element has more than two points, the function returns an empty list
        
           
        .. note:: This function will consider any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                                      # retrieves the root layer of the file
        >>> line1 = inkscapeMadeEasy_Draw.line.absCoords(rootLayer, [[1,1],[2,2]])   # creates a line in groupA
        >>> segementList = getSegmentParameters(line1,'R')                               # returns [[1,1], [2,2],1.4142, 0.78540,  [0.7071,0.7071], [0.7071,-0.7071] ]

        """

        # check if element is valid. 'path'
        accepted_strings = set([inkex.addNS('path', 'svg'), 'path'])
        if element.tag not in accepted_strings:
            return []

        listPoints = self.getPoints(element)
        if len(listPoints) > 2:  # if the path has more than two points
            return []

        data = self.getSegmentFromPoints(listPoints, normalDirection)

        return listPoints + data


blankSVG = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="210mm"
   height="297mm"
   viewBox="0 0 793.7008056641 1122.51965332"
   version="1.1"
   id="svg1406"
   inkscape:version="0.92.3 (2405546, 2018-03-11)"
   sodipodi:docname="blank.svg">
  <metadata
     id="metadata1412">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="1920"
     inkscape:window-height="1056"
     id="namedview1408"
     showgrid="true"
     inkscape:snap-text-baseline="true"
     inkscape:zoom="0.7296085858586"
     inkscape:cx="396.8503937008"
     inkscape:cy="561.2598425197"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="svg1406">
    <inkscape:grid
       type="xygrid"
       id="grid1957" />
  </sodipodi:namedview>
</svg>

"""