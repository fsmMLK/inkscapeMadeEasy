#!/usr/bin/python

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
# in this example I am going to use both inkscapeMadeEasy_Draw.py and inkscapeMadeEasy_Plot functions, so I have to load them.
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot


# your plugin must inherit inkBase.inkscapeMadeEasy
class MinimalExample(inkBase.inkscapeMadeEasy):
    # the __init__ must initiate inkBase.inkscapeMadeEasy and build your argument parser
    def __init__(self):
        # initiate inkBase.inkscapeMadeEasy
        inkBase.inkscapeMadeEasy.__init__(self)

        # argument parser
        self.arg_parser.add_argument("--drawCircle", type=self.bool, dest="drawCircle", default=False)
        self.arg_parser.add_argument("--drawPlot", type=self.bool, dest="drawPlot", default=False)

    # the effect function will be the main function of your plugin. This function will 'do the stuff'
    def effect(self):
        # parse the arguments.
        so = self.options

        # get the coords of the center of the view. In this case I am calling a function inside inkex.
        position = [self.svg.namedview.center[0], self.svg.namedview.center[1]]

        # parent of all elements
        root_layer = self.document.getroot()

        # creates a group. Note 'createGroup' is an inkscapeMadeEasy_Base.inkscapeMadeEasy method.
        # However, MinimalExample inherits all the methods and properties from inkBase.inkscapeMadeEasy so you can call it with ``self.[SOME_METHOD]``
        group = self.createGroup(root_layer, 'myGroup')

        # the next elements will be created inside the group
        if so.drawCircle:
            # draw a circle, showing how to use inkscapeMadeEasy_Draw.py
            center = [0, 0]
            radius = 2
            # creates a line style for the circle
            self.lineStyle = inkDraw.lineStyle.setSimpleBlack(1.5)
            inkDraw.circle.centerRadius(group, center, radius, offset=position, lineStyle=self.lineStyle)

        if so.drawPlot:
            # draw a cartesian plane, showing how to use inkscapeMadeEasy_Plot.py
            inkPlot.axis.cartesian(self, group, xLim=[0.0, 2.0], yLim=[0.0, 2.0], position=position, xLabel='x axis', yLabel='y axis')


if __name__ == '__main__':
    myPlugin = MinimalExample()
    myPlugin.run()
