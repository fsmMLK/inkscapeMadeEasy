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
from lxml import etree

import inkex


class inkscapeMadeEasy(inkex.Effect):

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

        self.blankSVG = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
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
       viewBox="0 0 793.70081 1122.5197"
       version="1.1"
       id="svg878"
       inkscape:version="1.0.1 (1.0.1+r73)"
       sodipodi:docname="blank.svg">
      <defs
         id="defs872" />
      <sodipodi:namedview
         id="base"
         pagecolor="#ffffff"
         bordercolor="#666666"
         borderopacity="1.0"
         inkscape:pageopacity="0.0"
         inkscape:pageshadow="2"
         inkscape:zoom="0.35"
         inkscape:cx="400"
         inkscape:cy="560"
         inkscape:document-units="px"
         inkscape:current-layer="layer1"
         inkscape:document-rotation="0"
         showgrid="false"
         units="px"
         inkscape:window-width="1347"
         inkscape:window-height="850"
         inkscape:window-x="569"
         inkscape:window-y="202"
         inkscape:window-maximized="0" />
      <metadata
         id="metadata875">
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
      <g
         inkscape:label="Layer 1"
         inkscape:groupmode="layer"
         id="layer1" />
    </svg>
        """
    # ---------------------------------------------
    def bool(self,valueStr):
        """
        ArgParser function to turn a boolean string into a python boolean

        :param valueStr: string representing a boolean. Valid values: 'true','false' with any letter capitalization
        :type valueStr: string

        :returns: boolean value
        :rtype: bool

        .. note:: This function was copied from inkex.utils.py to avoid having to import inkex.py in your project just to use inkex.Boolean in ``arg_parser.add_argument``. You can pass this function in ``arg_parser.add_argument`` method when dealing with boolean values. See :ref:`minimalExample` section for a good example.

        **Example**

        In your ``__init__`` function, ``arg_parser.add_argument`` requires a callable to convert string to bool when dealing with bool variables. See :ref:`minimalExample` section for a good example.

        >>> self.arg_parser.add_argument("--boolVariable", type=self.bool, dest="boolVariable", default=False)

        """
        if valueStr.upper() == 'TRUE':
            return True
        elif valueStr.upper() == 'FALSE':
            return False
        return None

    # ---------------------------------------------
    def displayMsg(self, msg):
        """Display a message to the user.

        :param msg: message
        :type msg: string
        
        :returns: nothing
        :rtype: -

        """
        sys.stderr.write(msg + '\n')

    # ---------------------------------------------
    def getBasicLatexPackagesFile(self):
        """Return the full path  of the ``basicLatexPackages.tex`` file with commonly used Latex packages

        The default contents of the ``basicLatexPackages.tex`` is::

        \\usepackage{amsmath,amsthm,amsbsy,amsfonts,amssymb}
        \\usepackage[per=slash]{siunitx}
        \\usepackage{steinmetz}

        :returns:  Full path  of the file with commonly used Latex packages 
        :rtype: string

        .. note:: You can add other packages to the file ``basicLatexPackages.tex``.

        """
        directory = os.getcwd()
        return os.path.abspath(directory + '/../inkscapeMadeEasy/basicLatexPackages.tex')

    # ---------------------------------------------
    def Dump(self, obj, file='./dump_file.txt', mode='w'):
        """Function to easily output the result of ``str(obj)`` to a file

        :param obj: python object to sent to a file. Any object can be used, as long as ``str(obj)`` is implemented (see ``__str__()`` metaclass definition of your object)
        :param file: file path. Default: ``./dump_file.txt``
        :param mode: writing mode of the file Default: ``w`` (write)
        :type obj: any
        :type file: string
        :type mode: string
        :returns:  nothing
        :rtype: -

        .. note:: This function was created to help debugging the code while it is running under inkscape. Since inkscape does not possess a terminal as today (2016), this function overcomes partially the issue of sending things to stdout by dumping result of the function ``str(obj)`` in a text file.

        **Example**

        >>> vector1=[1,2,3,4,5,6]
        >>> self.Dump(vector1,file='~/temporary.txt',mode='w')   # writes the list to a file
        >>> vector2=[7,8,9,10]
        >>> self.Dump(vector2,file='~/temporary.txt',mode='a')   # append the list to a file
        """
        with open(file, mode) as file:
            file.write(str(obj) + '\n')

    # ---------------------------------------------
    def removeElement(self, element):
        """Remove one element (can be a gropu) of the document.

        If the parent of the removed element is a group and has no other children, then the parent group is also removed.

        :param element: inkscape element object to be removed. If the element is a group, then all its chidren are also removed.
        :type element: inkscape element object
        :returns:  nothing
        :rtype: -

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkDraw.line.relCoords(groupA, [[5,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(rootLayer, [[5,0]],[0,0])    # creates a line in rootLayer
        >>> line3 = inkDraw.line.relCoords(groupA, [[15,0]],[10,0])     # creates a line in groupA
        >>> self.removeElement(line1)                                         # removes line 1
        >>> self.removeElement(line2)                                         # removes line 2
        >>> self.removeElement(line3)                                         # removes line 3. Also removes groupA since this group has no other children
        >>> groupB = self.createGroup(rootLayer,label='temp1')                # creates a group inside rootLayer
        >>> line4 = inkDraw.line.relCoords(groupB, [[5,0]],[0,0])       # creates a line in groupB
        >>> self.removeElement(groupB)                                        # removes group B and all its children
        """

        parent = element.getparent()

        parent.remove(element)

        if parent.tag == 'g' and len(parent.getchildren()) == 0:  # if object's parent is a group and has no other children, remove parent too
            temp = parent.getparent()
            if temp is not None:
                temp.remove(parent)

    # ---------------------------------------------
    def importSVG(self, parent, fileIn, createGroup=True):
        """ Import SVG file into the current document

        This function will all unify the defs node via :meth:`unifyDefs`

        :param parent: parent element where all contents will be placed
        :param fileIn: SVG file path
        :param createGroup: create a group containing all imported elements. (Default: True)
        :type parent: inkscape element object
        :type fileIn: string
        :type createGroup: bool
        :returns:  imported element objects. If createGroup==True, returns the group. Otherwise returns a list with all imported elements
        :rtype: inkscape element object or list of objects

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> imported1 = self.importSVG(rootLayer,'/path/to/file1.svg',True)  # import contents of the file and group them. imported1 is the group element
        >>> imported2 = self.importSVG(rootLayer,'/path/to/file2.svg',False) # import contents of the file. imported2 is a list of the imported elements

        """
        documentIn = etree.parse(fileIn, parser=etree.XMLParser(huge_tree=True)).getroot()

        if createGroup:
            group = self.createGroup(parent, label='importedSVG')
            for elem in documentIn:
                if elem.tag != inkex.addNS('namedview', 'sodipodi') and elem.tag != inkex.addNS('metadata', 'svg'):
                    group.append(elem)
            self.unifyDefs()
            return group
        else:
            listElements=[]
            for elem in documentIn:
                if elem.tag != inkex.addNS('namedview', 'sodipodi') and elem.tag != inkex.addNS('metadata', 'svg'):
                    parent.append(elem)
                    if elem.tag != inkex.addNS('defs', 'svg'):
                        listElements.append(elem)
            self.unifyDefs()
            return listElements

    # ---------------------------------------------
    def exportSVG(self, element, fileOut):
        """ Export the element (or list of elements) in a new svgfile.

        This function will export the element (or list of elements) to a new SVG file. If a list of elements is passed as argument, all elements in the list will be exported to the same file.

        :param element: element or list of elements to be exported
        :param fileOut: file path, including the extension.
        :type element: inkscape element object or list of inkscape element objects
        :type file: string
        :returns:  nothing
        :rtype: -

        .. note:: Currently (2020), all the defs of the original file will be copied to the new file. Therefore you might want to run the vacuum tool to cleanup the new SVG file ``File > Clean um document``

        **Example**

        >>> rootLayer = self.document.getroot()                          # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')            # creates a group inside rootLayer
        >>> groupB = self.createGroup(rootLayer,label='child')           # creates a group inside groupA
        >>> line1 = inkDraw.line.relCoords(groupA, [[10,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(groupB, [[20,0]],[0,0])       # creates a line in groupB
        >>> self.exportSVG(line1,'path/to/file1.svg')                    # exports only line1
        >>> self.exportSVG(groupA,'path/to/file2.svg')                   # exports groupA (and all elements it contais)
        >>> self.exportSVG([groupA,groupB],'path/to/file3.svg')          # exports groupA and groupB (and all elements they contain) to the same file

        """
        document = etree.fromstring(self.blankSVG.encode('ascii'))

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

        et = etree.ElementTree(document)
        et.write(fileOut, pretty_print=True)

    # ---------------------------------------------
    def uniqueIdNumber(self, prefix_id):
        """ Generate an unique element ID number with a given prefix ID by adding a numeric suffix

        This function is used to generate a valid unique ID by concatenating a given prefix with a numeric suffix. The overall format is ``prefix-%05d``.

        This function makes sure the ID is unique by checking in ``doc_ids`` member. This function is specially useful for creating an unique ID for markers and other elements in defs.

        :param prefix_id: prefix of the ID
        :type prefix_id: string
        :returns: the unique ID
        :rtype: string

        .. note:: This function has been adapted from inkex.py. However it uses an incremental number method

        **Example**

        >>> a=self.uniqueIdNumber('myName')    # a=myName-00001
        >>> b=self.uniqueIdNumber('myName')    # b=myName-00002, because myName-00001 is already in use
        >>> c=self.uniqueIdNumber('myName')    # c=myName-00003, because myName-00001 and myName-00002 are already in use
        >>> d=self.uniqueIdNumber('myNameX')   # d=myNameX-00001


        """
        numberID = 1
        new_id = prefix_id + '-%05d' % numberID
        while new_id in self.get_ids():
            numberID += 1
            new_id = prefix_id + '-%05d' % numberID
        self.svg.get_ids().add(new_id)

        return new_id

    # ---------------------------------------------
    def getDefinitions(self):
        """ Return the <defs> element of the svg file.

        This function returns the principal <defs> element of the current svg file.

        if no <defs> can be found, a new empty <defs> is created

        :returns: the defs element
        :rtype: inkscape element object

        """
        defs = self.getElemFromXpath('/svg:svg//svg:defs')
        if defs is None:
            defs = etree.SubElement(self.document.getroot(), inkex.addNS('defs', 'svg'))

        return defs

    # ---------------------------------------------
    def unifyDefs(self):
        """Unify all <defs> nodes in a single <defs> node.

        :returns: None
        :rtype: -

        .. warning:: This function does not check whether the ids are unique!
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
        """ Return a list of elements in <defs> of a given a tag.

        :param tag: tag of the element
        :type tag: string

        :returns: a list with the def elements
        :rtype: list of inkscape elements

        """

        return self.getDefinitions().findall('.//svg:%s' % tag, namespaces=inkex.NSS)

    # ---------------------------------------------
    def getDefsById(self,id):
        """ Return a list of elements in <defs> of a given (part of) the id

        :param id: (part of the id of the element)
        :type tag: string

        :returns: a list with the def elements
        :rtype: list of inkscape elements

        """

        return self.getDefinitions().xpath('./*[contains(@id,"%s")]' % id)

    # ---------------------------------------------
    def getElemFromXpath(self, xpath):
        """ Return the element from the xml, given its xpath

        :param xpath: xpath of the element to be searched
        :type xpath: string
        :returns: inkscape element object
        :rtype: inkscape element object

        **Example**

        >>> name = self.getElemFromXpath('/svg:svg//svg:defs')   # returns the list of definitions of the document

        """
        return self.svg.getElement(xpath)

    # ---------------------------------------------
    def getElemAttrib(self, elem, attribName):
        """ Return the atribute of one element, given the atribute name

        :param elem: element under consideration
        :param attribName: attribute to be searched. Format:  namespace:attrName
        :type elem: inkscape element object
        :type attribName: string
        :returns: attribute
        :rtype: string

        **Example**

        >>> elem= self.getElemFromXpath('/svg:svg')               # first get the element. In this example, the entire document
        >>> docNAme = self.getElemAttrib(elem,'sodipodi:docname') # now get the name of the document, an attribute of svg:svg
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
    def getDocumentScaleFactor(self):
        """Return the scale factor of the document.

        The scale factor is defined as

        .. math:: S=\\frac{\\text{document width}}{\\text{viewbox width}}

        **Example**

        >>> scale = self.getDocumentScaleFactor()
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
        """Return the name of the document
        
        :returns: fileName
        :rtype: string
        
        **Example**

        >>> name = self.getDocumentName()
        
        """
        elem = self.getElemFromXpath('/svg:svg')
        try:
            fileName = self.getElemAttrib(elem, 'sodipodi:docname')
        except:
            fileName = None
        return fileName

    # ---------------------------------------------
    def getDocumentUnit(self):
        """Return the unit of the document
        
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
        """Return the current layer of the document
        
        :returns: Name of the current layer
        :rtype: string
        
        **Example**
        
        >>> name = self.getcurrentLayer()
        """
        return self.svg.get_current_layer()

    # ---------------------------------------------
    def abs2relPath(self, element):
        abspath = self.getElemAttrib(element, 'sodipodi:absref')
        fileName = os.path.basename(abspath)

        # removes sodipodi:absref attribute
        namespace = inkex.NSS['sodipodi']
        attrib = '{%s}' % namespace + 'absref'

        element.attrib.pop(attrib, None)

        # adds sodipodi:relref
        attrib = '{%s}' % namespace + 'relref'
        element.set(attrib, fileName)

    # ---------------------------------------------
    def unit2userUnit(self, value, unit_in):
        """Convert a value from given unit to inkscape's default unit (px)

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
        """Convert a value from inkscape's default unit (px) to specified unit
        
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
        """Convert a value from one unit to another unit
        
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
    def createGroup(self, parent, label=None):
        """Create a new empty group of elements.

        This function creates a new empty group of elements. To create new elements inside this groups you must create them informing the group as the parent element.

        :param parent: parent object of the group. It can be another group or the root element
        :param label: label of the group. Default:  ``None``.
                      The label does not have to be unique
        :type parent: inkscape element object
        :type label: string
        :returns: the group object
        :rtype: group element

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> groupB = self.createGroup(groupA,label='child')                  # creates a group inside groupA
        >>> line1 = inkDraw.line.relCoords(groupA, [[10,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(groupB, [[20,0]],[0,0])       # creates a line in groupB

        """
        if label is not None:
            g_attribs = {inkex.addNS('label', 'inkscape'): label}
            group = etree.SubElement(parent, 'g', g_attribs)
        else:
            group = etree.SubElement(parent, 'g')

        return group

    # ---------------------------------------------
    def ungroup(self, group):
        """Ungroup elements

        The new parent element of the ungrouped elements will be the parent of the removed group. See example below

        :param group: group to be removed
        :type group: group element
        :returns: list of the elements previously contained in the group
        :rtype: list of inkscape object elements

        **Example**


        >>> rootLayer = self.document.getroot()                          # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')            # creates a group inside rootLayer
        >>> groupB = self.createGroup(groupA,label='temp')               # creates a group inside groupA
        >>> line1 = inkDraw.line.relCoords(groupA, [[10,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(groupB, [[20,0]],[0,0])       # creates a line in groupB
        >>> line3 = inkDraw.line.relCoords(groupB, [[30,0]],[0,0])       # creates a line in groupB
        >>>  # at this point, the file struct is:   rootLayer[groupA[ line1, groupB[ line2, line3 ] ]]
        >>> elemList = self.ungroup(groupB)                              # ungroup line2 and line3. elemList is a list containing line2 and line3 elements.
        >>>  # now the file struct is:   rootLayer[groupA[ line1, line2, line3 ]]
        """

        if group.tag == 'g' or group.tag == inkex.addNS('g', 'svg'):  # if object is a group
            parent = group.getparent()

            listElem=[]
            if parent is not None:
                for child in group:
                    parent.append(child)
                    listElem.append(child)

                self.removeElement(group)

        return listElem

    # ---------------------------------------------
    def getTransformMatrix(self, element):
        """Return the transformation attribute of the given element and the resulting 3x3 transformation matrix (numpy Array)

        This function is used to extract the transformation operator of a given element.

        :param element: element object with the transformation matrix
        :type element: inkscape element object
        :returns: list [transfAttrib, transfMatrix]

          - transfAttrib: string containing all transformations as it is in the file
          - transfMatrix: numpy array with the resulting 3x3 transformation matrix
        :rtype: tuple

        .. note :: If the element does not have any transformation attribute, this function returns:
           - transfAttrib=''  (empty string)
           - transfMatrix= 3x3 identity matrix
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
                data = re.compile(r"translate\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                x = float(data[0])
                y = float(data[1])
                mat = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'scale' in operation:
                data = re.compile(r"scale\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                scalex = float(data[0])
                if len(data) == 2:
                    scaley = float(data[1])
                else:
                    scaley = scalex
                mat = np.diag([scalex, scaley, 1])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'rotate' in operation:
                data = re.compile(r"rotate\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
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
                data = re.compile(r"skewX\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                angleRad = float(data[0]) * np.pi / 180.0
                mat = np.array([[1, np.tan(angleRad), 0], [0, 1, 0], [0, 0, 1]])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'skewY' in operation:
                data = re.compile(r"skewY\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
                angleRad = float(data[0]) * np.pi / 180.0
                mat = np.array([[1, 0, 0], [np.tan(angleRad), 1, 0], [0, 0, 1]])
                transfMatrix = np.dot(transfMatrix, mat)

            if 'matrix' in operation:
                data = re.compile(r"matrix\((.*?\S)\)").match(operation.lstrip()).group(1).split()  # retrieves x and y values
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
        """apply a rotation to the element using the transformation matrix attribute.

        It is possible to rotate isolated elements or groups.

        :param element: element object to be rotated
        :param center: center point of rotation
        :param angleDeg: angle of rotation in degrees, counter-clockwise direction
        :type element: inkscape element object
        :type center: list
        :type angleDeg: float
        :returns:  nothing
        :rtype: -

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkDraw.line.relCoords(groupA, [[5,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(rootLayer, [[5,0]],[0,0])    # creates a line in rootLayer
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
        """Copy one element to the same parent or other parent group.

        It is possible to copy elements isolated or entire groups.

        :param element: element object to be copied
        :param newParent: New parent object. Can be another group or the same group
        :param distance: moving distance of the new copy. The coordinates are relative to the original position. If ``None``, then the copy is placed at the same position
        :param angleDeg: angle of rotation in degrees, counter-clockwise direction
        :type element: inkscape element object
        :type newParent: inkscape element object
        :type distance: list
        :type angleDeg: float
        :returns:  new element
        :rtype: inkscape element object

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkDraw.line.relCoords(groupA, [[5,0]],[0,0])            # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(rootLayer, [[5,0]],[0,0])         # creates a line in rootLayer
        >>> self.copyElement(line2,groupA)                                   # create a copy of line2 in groupA
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
        """Move the element using the transformation attribute.

        It is possible to move elements isolated or entire groups.

        :param element: element object to be moved
        :param distance: moving distance. The coordinates are relative to the original position.
        :type element: inkscape element object
        :type distance: tuple
        :returns:  nothing
        :rtype: -

        **Example**

        >>> rootLayer = self.document.getroot()                              # retrieves the root layer of the file
        >>> groupA = self.createGroup(rootLayer,label='temp')                # creates a group inside rootLayer
        >>> line1 = inkDraw.line.relCoords(groupA, [[5,0]],[0,0])       # creates a line in groupA
        >>> line2 = inkDraw.line.relCoords(rootLayer, [[5,0]],[0,0])    # creates a line in rootLayer
        >>> self.moveElement(line2,[10,10])                                  # moves line2  DeltaX=10, DdeltaY=10
        >>> self.moveElement(groupA,[10,-10])                                # moves line2  DeltaX=10, DdeltaY=-10
        """

        if distance[0] == 0 and distance[1] == 0:
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
    def scaleElement(self, element, scaleX=1.0, scaleY=None, center=None):
        """Scale the element using the transformation attribute.

        It is possible to scale elements isolated or entire groups.

        :param element: element object to be scaled
        :param scaleX: scaling factor in X direction. Default=1.0
        :param scaleY: scaling factor in Y direction. Default=``None``. If scaleY=``None``, then scaleY=scaleX is assumed (default behavior)
        :param center: center point considered as the origin for the scaling. Default=``None``. If ``None``, the origin is adopted
        :type element: inkscape element object
        :type scaleX: float
        :type scaleX: float
        :type center: list
        :returns:  nothing
        :rtype: -

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
            if scaleY is not None:
                newTransform = 'scale(%f %f) %s ' % (scaleX, scaleY, transfString)
            else:
                newTransform = 'scale(%f) %s' % (scaleX, transfString)
        else:  # if no transform attribute was found
            if scaleY is not None:
                newTransform = 'scale(%f %f)' % (scaleX, scaleY)
            else:
                newTransform = 'scale(%f)' % scaleX

        element.attrib['transform'] = newTransform

        if center is not None:
            self.moveElement(element, [center[0], center[1]])

    # ---------------------------------------------
    def findMarker(self, markerName):
        """Search for markerName definition in the document.

        :param markerName: name of the marker
        :type markerName: string
        :returns: True if markerName is in the document. False otherwise
        :rtype: bool
        """
        list  = self.getDefsByTag(tag='marker')
        for m in list:
            if m.get('id') == markerName:
                return True

        return False

    # ---------------------------------------------
    def getPoints(self, element):
        """Returns a list of points of the element.

        This function works on paths, texts or groups. In the case of a group, the function will include recursively all its components.

        :param element: element object
        :type element: inkscape element object
        :returns: array of points
        :rtype: numpy array

        .. note:: This function will apply any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                                   # retrieves the root layer of the file
        >>> line1 = inkDraw.line.relCoords(rootLayer, [[5,0],[0,6]],[0,0])        # creates a line in groupA, using relative coordinates
        >>> list = self.getPoints(line1)                                          # list = [[0.0, 0.0], [5.0, 0.0], [5.0, 6.0]]

        """

        # stores the list of coordinates
        listCoords = []

        # check if element is valid. 'path', 'text' and 'g' are valid
        accepted_strings = set([inkex.addNS('path', 'svg'), inkex.addNS('text', 'svg'), 'g', inkex.addNS('g', 'svg'), 'path', 'use', inkex.addNS('use', 'svg')])
        if element.tag not in accepted_strings:
            return listCoords

        if element.tag in [inkex.addNS('path', 'svg'), 'path']:  # if object is path

            # adds special character between letters and splits. the first regular expression excludes e and E bc they are used to represent scientific notation  =S
            dString = re.sub('([a-df-zA-DF-Z])+?', r'#\1#', element.attrib['d']).replace('z', '').replace('Z', '').replace(',', ' ').split('#')

            dString = [i.lstrip() for i in dString]  # removes leading spaces from strings
            dString = list(filter(None, dString))  # removes empty elements
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

        if element.tag in ['text', inkex.addNS('text', 'svg')]:  # if object is a text
            x = float(element.attrib['x'])
            y = float(element.attrib['y'])
            coords = [[x, y]]
            listCoords.extend(coords)

        if element.tag in ['g', inkex.addNS('g', 'svg')]:  # if object is a group
            for obj in element.iterchildren("*"):
                if obj != element and obj.tag not in [ 'defs', inkex.addNS('defs', 'svg')]:
                    listPoints = self.getPoints(obj)
                    listCoords.extend(listPoints)

        if element.tag in ['use', inkex.addNS('use', 'svg')]:  # if object is a use
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
            coordsTransformed = np.delete(coordsTransformed, 2, 0).transpose()  # remove last line, transposes and converts to list of lists

        else:
            coordsTransformed = np.array([])

        return coordsTransformed

    # ---------------------------------------------
    def getBoundingBox(self, element):
        """Return the bounding Box of the element.

        This function works on paths, texts or groups. In the case of a group, the function will consider recursively all its components

        :param element: element object
        :type element: inkscape element object
        :returns: two lists: [xMin,yMin] and [xMax,yMax]
        :rtype: list

        .. note:: This function will appply any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                                   # retrieves the root layer of the file
        >>> line1 = inkDraw.line.relCoords(rootLayer, [[5,0],[0,6]],[0,0])        # creates a line in groupA
        >>> BboxMin,BboxMax = self.getBoundingBox(line1)                          # gets BboxMin = [0.0, 0.0] and BboxMax = [5.0, 6.0]

        """
        coords = self.getPoints(element)
        coordsNP = np.array(coords)

        bboxMax = np.max(coordsNP, 0)
        bboxMin = np.min(coordsNP, 0)
        return bboxMin.tolist(), bboxMax.tolist()

    # ---------------------------------------------
    def getCenter(self, element):
        """Return the center coordinates of the bounding Box of the element.

        This function works on paths, texts or groups. In the case of a group, the function will consider recursively all its components

        :param element: element object
        :type element: inkscape element object
        :returns: list: [xCenter, yCenter]
        :rtype: list

        .. note:: This function will apply any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                                   # retrieves the root layer of the file
        >>> line1 = inkDraw.line.relCoords(rootLayer, [[5,0],[0,6]],[0,0])   # creates a line in groupA
        >>> Center = self.getCenter(line1)                                        # gets Center = [2.5, 3.0]

        """

        bboxMin, bboxMax = self.getBoundingBox(element)

        bboxCenter = np.array([(bboxMax[0] + bboxMin[0]) / 2, (bboxMax[1] + bboxMin[1]) / 2])

        return bboxCenter

    def getSegmentFromPoints(self, pointList, normalDirection='R'):
        """Given two points of a straight line segment, returns the parameters of that segment:
        
        length, angle (in radians), tangent unitary vector and normal unitary vector

        :param pointList: start and end coordinates [ Pstart, Pend ]
        :param normalDirection:
        
          - 'R': normal vector points to the right of the tangent vector (Default)
          - 'L': normal vector points to the left of the tangent vector
          
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
        """Given a path segment composed by only two points, returns the parameters of that segment:
        
        length, angle (in radians), start point, end point, tangent unitary vector and normal unitary vector

        This function works with paths only.

         - If the element is not a path, the function returns an empty list
         - If the path element has more than two points, the function returns an empty list

        :param element: path element object
        :param normalDirection:
        
          - 'R': normal vector points to the right of the tangent vector (Default)
          - 'L': normal vector points to the left of the tangent vector
          
        :type element: inkscape element object
        :type normalDirection: string
        
        :returns: list: [Pstart,Pend,length, theta, t_versor,n_versor]
        :rtype: list

        .. note:: This function will apply any transformation stored in transform attribute,
            that is, it will compute the resulting coordinates of each object

        **Example**

        >>> rootLayer = self.document.getroot()                        # retrieves the root layer of the file
        >>> line1 = inkDraw.line.absCoords(rootLayer, [[1,1],[2,2]])   # creates a line in groupA
        >>> segementList = getSegmentParameters(line1,'R')             # returns [[1,1], [2,2],1.4142, 0.78540,  [0.7071,0.7071], [0.7071,-0.7071] ]

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



