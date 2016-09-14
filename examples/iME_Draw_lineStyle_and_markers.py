#!/usr/bin/python

import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import math

class myExtension(inkBase.inkscapeMadeEasy):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--myColorPicker", action="store", type="string", dest="lineColorPickerVar", default='0')
        self.OptionParser.add_option("--myColorOption", action="store", type="string", dest="lineColorOptionVar", default='0')

    def effect(self):
        # sets the position to the viewport center, round to next 10.
        position=[self.view_center[0],self.view_center[1]]
        position[0]=int(math.ceil(position[0] / 10.0)) * 10
        position[1]=int(math.ceil(position[1] / 10.0)) * 10
        
        
        # creates a dot marker, with red stroke color and gray (40%) filling color 
        myDotMarker = inkDraw.marker.createDotMarker(self,
                                                     nameID='myDot' ,
                                                     RenameMode=1,             # overwrite an eventual markers with the same name
                                                     scale=0.2,
                                                     strokeColor=inkDraw.color.defined('red'),
                                                     fillColor=inkDraw.color.gray(0.4))
        
        # parses the input options to get the color of the line
        lineColor, alpha = inkDraw.color.parseColorPicker(self.options.lineColorOptionVar, self.options.lineColorPickerVar)
        
        # create a new line style with a 2.0 pt line and the marker just defined at both ends
        myLineStyleDot = inkDraw.lineStyle.set(lineWidth=2.0,
                                               lineColor=lineColor,
                                               fillColor=inkDraw.color.defined('blue'),
                                               lineJoin='round',
                                               lineCap='round',
                                               markerStart=myDotMarker,
                                               markerMid=myDotMarker,
                                               markerEnd=myDotMarker,
                                               strokeDashArray=None)
        #root_layer = self.current_layer
        root_layer = self.document.getroot()    
    
        # draws a line using the new line style. (see inkscapeMadeEasy_Draw.line class for further info on this function
        inkDraw.line.relCoords(root_layer,coordsList= [[0,100],[100,0]],offset=position,lineStyle=myLineStyleDot)


        # -- Creates a second line style with ellipsis and 
        
        # creates a ellipsis marker with default values
        infMarkerStart,infMarkerEnd = inkDraw.marker.createInfLineMarker(self,
                                                                        nameID='myEllipsis' ,
                                                                        RenameMode=1)             # overwrite an eventual markers with the same name
        
        # create a new line style
        myStyleInf = inkDraw.lineStyle.set(lineWidth=1.0,
                                           lineColor=lineColor,
                                           fillColor=None,
                                           lineJoin='round',
                                           lineCap='round',
                                           markerStart=infMarkerStart,
                                           markerMid=None,
                                           markerEnd=infMarkerEnd,
                                           strokeDashArray=None)
        
        # draws a line using the new line style. (see inkscapeMadeEasy_Draw.line class for further info on this function
        inkDraw.line.relCoords(root_layer,coordsList= [[0,100],[100,0]],offset=[position[0]+300,position[1]],lineStyle=myStyleInf)
        
if __name__ == '__main__':
    x = myExtension()
    x.affect()
