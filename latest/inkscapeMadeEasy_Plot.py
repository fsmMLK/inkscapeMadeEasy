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

import math
import sys

import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


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
    :returns:  nothing
    :rtype: -

    .. note:: Identical function has been also defined inside :meth:`inkscapeMadeEasy_Base.inkscapeMadeEasy` class

    This function was created to help debugging the code while it is running under inkscape. Since inkscape does not possess a terminal as today (2016),
    this function overcomes partially the issue of sending things to stdout by dumping result of the function ``str()`` in a text file.

    **Example**

    >>> vector1=[1,2,3,4,5,6]
    >>> inkPlot.Dump(vector1,file='~/temporary.txt',mode='w')   # writes the list to a file
    >>> vector2=[7,8,9,10]
    >>> inkPlot.Dump(vector2,file='~/temporary.txt',mode='a')   # append the list to a file
    """

    with open(file, mode) as file:
        file.write(str(obj) + '\n')


def generateListOfTicksLinear(axisLimits, axisOrigin, tickStep):
    """Defines list of ticks in a linear plot

    .. note:: Internal function.
    """

    # make the list of ticks, symmetrically to the origin
    listTicksPositive = [axisOrigin]
    while listTicksPositive[-1] < axisLimits[1]:
        listTicksPositive.append(listTicksPositive[-1] + tickStep)

    listTicksNegative = [axisOrigin]

    while listTicksNegative[-1] > axisLimits[0]:
        listTicksNegative.append(listTicksNegative[-1] - tickStep)

    listTicks = listTicksPositive + listTicksNegative[1:]
    return listTicks


def generateListOfTicksLog10(axisLimits):
    """Defines list of ticks in a log10 plot

    .. note:: Internal function.
    """

    # make the list of ticks, symmetrically to the origin
    listTicks = [axisLimits[0]]
    while listTicks[-1] < axisLimits[1]:
        listTicks.append(listTicks[-1] * 10)
    return listTicks


def findOrigin(axisLimits, flagLog10, scale):
    """ retrieves the position of the origin. In case of logarithmic scale, it will be axisLimits[0]

    .. note:: Internal function.
    """
    if flagLog10:
        axisOrigin = math.log10(axisLimits[0]) * scale
    else:
        if axisLimits[0] <= 0.0 and axisLimits[1] >= 0.0:
            axisOrigin = 0.0
        else:
            if axisLimits[1] < 0:
                axisOrigin = axisLimits[1] * scale
            else:
                axisOrigin = axisLimits[0] * scale

    return axisOrigin


def getPositionAndText(value, scale, flagLog10, axisUnitFactor):
    """given a value, its scale, and some flags, finds it position in the diagram and the text to be shown

    .. note:: Internal function."""
    if flagLog10:
        pos = math.log10(value) * scale
    else:
        pos = value * scale
    # try to simplify number
    if int(value) - value == 0:
        valStr = str(int(round(value, 3)))
    else:
        valStr = str(round(value, 3))

    # option to add extra factor to the axis ticks
    if flagLog10:
        exponent = str(int(math.log10(value)))
        if axisUnitFactor:
            if inkDraw.useLatex:
                Text = '10^{' + exponent + '}' + axisUnitFactor + ''
            else:
                Text = '10^' + exponent + '' + axisUnitFactor + ''
        else:
            if inkDraw.useLatex:
                Text = '10^{' + exponent + '}'
            else:
                Text = '10^' + exponent + ''
    else:
        if axisUnitFactor:
            if value == 0:
                Text = '0'
            if value == 1:
                Text = axisUnitFactor
            if value == -1:
                Text = '-' + axisUnitFactor
            if value != 0 and value != 1 and value != -1:
                Text = valStr + axisUnitFactor
        else:
            Text = valStr

    if inkDraw.useLatex:
        Text = '$' + Text + '$'

    return [pos, Text]


class axis():
    """ This class has member functions to create customizable plot axes.
    
    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.

    .. note:: This class can use LaTeX to render text if LaTeX support is enabled. LaTeX support is an optional feature that requires a few extra packages to be installed outside inkscape. **It is enabled by default**.
            Please refer to :ref:`disableLatexSupport` on how to disable it. If disabled, this function will still work, internally calling the :meth:`inkscapeMadeEasy_Draw.text.write` to generate text.
    """

    @staticmethod
    def cartesian(ExtensionBaseObj, parent, xLim, yLim, position=[0, 0], xLabel='', yLabel='', xlog10scale=False, ylog10scale=False, xTicks=True,
                  yTicks=True, xTickStep=1.0, yTickStep=1.0, xScale=20, yScale=20, xAxisUnitFactor='', yAxisUnitFactor='', xGrid=False, yGrid=False,
                  forceTextSize=0, forceLineWidth=0, drawAxis=True, ExtraLengthAxisX=0.0, ExtraLengthAxisY=0.0):
        """Creates the axes of a cartesian plot

        .. note:: This method uses LaTeX in labels and tick marks if LaTeX support is enabled. This is an optional feature, **enabled by default**. Please refer to :ref:`disableLatexSupport` on how to disable it.
    
        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param parent: Parent object
        :param xLim: Limits of the X axis [x_min,x_max]. If the axis is in log10 scale, then the limits will be rounded to complete one decade.
        :param yLim: Limits of the Y axis [y_min,y_max]. If the axis is in log10 scale, then the limits will be rounded to complete one decade.
        :param position: Position of the plot. It is defined at the point where x and y axis cross [x0,y0]. The point where the axis cross depend on the limits.

              - If xLimits comprises the origin x=0, then the  Y axis crosses the X axis at x=0.
              - If xLimits contains only negative numbers, then the Y axis crosses the X axis at x_max.
              - If xLimits contains only positive numbers, then the Y axis crosses the X axis at x_min.

              - The same rule applies to y direction.
        :param xLabel: Label of the X axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param yLabel: Label of the Y axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param xlog10scale: Sets X axis to log10 scale if True. Default: False
        :param ylog10scale: Sets Y axis to log10 scale if True. Default: False
        :param xTicks: Adds axis ticks to the X axis if True. Default: True
        :param yTicks: Adds axis ticks to the Y axis if True. Default: True
        :param xTickStep: Value interval between two consecutive ticks on X axis. (Not used if X axis is in log10 scale). Default:1.0
        :param yTickStep: Value interval between two consecutive ticks on Y axis. (Not used if Y axis is in log10 scale). Default:1.0
        :param xScale: Distance between each xTickStep in svg units. Default: 20

               - If axis is linear, then xScale is the size in svg units of each tick
               - If axis is log10, the xScale is the size in svg units of one decade

        :param yScale: Distance between each yTickStep in svg units. Default: 20

               - If axis is linear, then yScale is the size in svg units of each tick
               - If axis is log10, the yScale is the size in svg units of one decade

        :param xAxisUnitFactor: Extra text to be added to the ticks in X axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.
        :param yAxisUnitFactor: Extra text to be added to the ticks in Y axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.

        :param xGrid: Adds grid lines to X axis if True. Default: False
        :param yGrid: Adds grid lines to Y axis if True. Default: False
        :param forceTextSize: Size of the text. If this parameter is 0.0 then the method will compute an appropriate size. Default: 0.0
        :param forceLineWidth: Width of the lines. If this parameter is 0.0 then the method will compute an appropriate size. Default: 0.0

        :param drawAxis: Control flag of the axis method

               - True: draws axis normally
               - False: returns the limits and origin position without drawing the axis itself

        :param ExtraLengthAxisX: Extra length near the arrow pointer of X axis. Default 0.0
        :param ExtraLengthAxisY: Extra length near the arrow pointer of Y axis. Default 0.0

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type parent: inkscape element object
        :type xLim: list
        :type yLim: list
        :type position: list
        :type xLabel: string
        :type yLabel: string
        :type xlog10scale: bool
        :type ylog10scale: bool
        :type xTicks: bool
        :type yTicks: bool
        :type xTickStep: float
        :type yTickStep: float
        :type xScale: float
        :type yScale: float
        :type xAxisUnitFactor: string
        :type yAxisUnitFactor: string
        :type xGrid: bool
        :type yGrid: bool
        :type forceTextSize: float
        :type forceLineWidth: float
        :type drawAxis: bool
        :type ExtraLengthAxisX: float
        :type ExtraLengthAxisY: float

        :returns: [GroupPlot, outputLimits, axisOrigin]

            - GroupPlot:  the axis area object (if drawAxis=False, this output is ``None``)
            - outputLimits: a list with tuples:[(x_min,xPos_min),(x_max,xPos_max),(y_min,yPos_min),(y_max,yPos_max)]

                  - x_min, x_max, y_min, y_max:               The limits of the axis object
                  - xPos_min, xPos_max, yPos_min, yPos_max:   The positions of the limits of the axis object, considering the scaling and units
            - axisOrigin [X0,Y0]:                      A list with the coordinates of the point where the axes cross.
        :rtype: list

        **Examples**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>
        >>> inkPlot.axis.cartesian(ExtensionBaseObj, parent=root_layer, xLim=[0,3], yLim=[0,2], position=[0, 0],
        >>>                        xLabel='my label $x$', yLabel='my label $y$', xlog10scale=False, ylog10scale=False,
        >>>                        xTicks=True, yTicks=True, xTickStep=0.5, yTickStep=1.0, xScale=50, yScale=60,
        >>>                        xAxisUnitFactor='', yAxisUnitFactor='', xGrid=True, yGrid=True, forceTextSize=0, forceLineWidth=0,
        >>>                        drawAxis=True, ExtraLengthAxisX=20.0, ExtraLengthAxisY=10.0)

        The images below show the cartesian plane of the example above, together with other variations.

        .. image:: ../imagesDocs/plot_axisCartesianParameters_01.png
          :width: 800px

        """
        if drawAxis:
            GroupPlot = ExtensionBaseObj.createGroup(parent, 'Plot')

        # sets the scale  scaleX and scaleY stores the size of one unit in both axis (linear axis) or the size of a decade in log plots
        if xlog10scale:
            scaleX = xScale
        else:
            scaleX = xScale / float(xTickStep)

        if ylog10scale:
            scaleY = -yScale
        else:
            scaleY = -yScale / float(yTickStep)  # negative bc inkscape is upside down

        # font size and other text parameters
        if forceTextSize == 0:
            textSize = 0.25 * min(xScale, yScale)
        else:
            textSize = forceTextSize

        textSizeSmall = 0.8 * textSize  # font size for axis ticks

        text_offset = textSize  # base space for text positioning
        ExtraSpaceArrowX = (2.0 + ExtraLengthAxisX) * text_offset  # extra space for drawing arrow on axis
        ExtraSpaceArrowY = (3.0 + ExtraLengthAxisY) * text_offset  # extra space for drawing arrow on axis
        lenghtTicks = textSize / 2.0  # length of the ticks

        # create styles
        if forceLineWidth == 0:
            lineWidth = min(xScale, yScale) / 35.0
        else:
            lineWidth = forceLineWidth

        lineWidthGrid = 0.7 * lineWidth
        lineWidthGridFine = lineWidthGrid / 2.0

        nameMarkerArrowAxis = inkDraw.marker.createArrow1Marker(ExtensionBaseObj, 'ArrowAxis', RenameMode=1, scale=0.4)
        lineStyleAxis = inkDraw.lineStyle.set(lineWidth, lineColor=inkDraw.color.gray(0.3), markerEnd=nameMarkerArrowAxis[1])
        lineStyleTicks = inkDraw.lineStyle.set(lineWidth, lineColor=inkDraw.color.gray(0.3))
        lineStyleGrid = inkDraw.lineStyle.set(lineWidthGrid, lineColor=inkDraw.color.gray(0.7))
        lineStyleGridFine = inkDraw.lineStyle.set(lineWidthGridFine, lineColor=inkDraw.color.gray(0.7))

        textStyleLarge = inkDraw.textStyle.setSimpleBlack(textSize)
        textStyleSmall = inkDraw.textStyle.setSimpleBlack(textSizeSmall, 'center')

        # check if limits are valid
        if xLim[0] >= xLim[1]:
            sys.stderr.write('Error: xLim is invalid.')
            return 0
        if yLim[0] >= yLim[1]:
            sys.stderr.write('Error: yLim is invalid.')
            return 0
        # check if the limits are valid for logarithmic scales.
        if xlog10scale:
            if xLim[0] <= 0 or xLim[1] <= 0:
                sys.stderr.write('Error: xLim is invalid in logarithmic scale')
                return 0
            else:
                xmin = pow(10, math.floor(math.log10(xLim[0])))
                xmax = pow(10, math.ceil(math.log10(xLim[1])))
                xLimits = [xmin, xmax]
        else:
            xLimits = xLim

        if ylog10scale:
            if yLim[0] <= 0 or yLim[1] <= 0:
                sys.stderr.write('Error: yLim is invalid in logarithmic scale')
                return 0
            else:
                ymin = pow(10, math.floor(math.log10(yLim[0])))
                ymax = pow(10, math.ceil(math.log10(yLim[1])))
                yLimits = [ymin, ymax]
        else:
            yLimits = yLim

        # finds the position of the Origin of axis
        axisOrigin = [0.0, 0.0]

        axisOrigin[0] = findOrigin(xLimits, xlog10scale, scaleX)
        axisOrigin[1] = findOrigin(yLimits, ylog10scale, scaleY)

        # computes the positions of the limits on svg, considering the scale

        if xlog10scale:  # convert limits to position in diagram, including scaling factor
            xLimitsPos = [math.log10(x) * scaleX for x in xLimits]
        else:
            xLimitsPos = [x * scaleX for x in xLimits]

        if ylog10scale:  # convert limits to position in diagram, including scaling factor
            yLimitsPos = [math.log10(y) * scaleY for y in yLimits]
        else:
            yLimitsPos = [y * scaleY for y in yLimits]

        # build the list of tuples with the limits of the plotting area
        outputLimits = list(zip([xLimits[0], xLimits[1], yLimits[0], yLimits[1]],
                           [xLimitsPos[0] - axisOrigin[0] + position[0], xLimitsPos[1] - axisOrigin[0] + position[0],
                            yLimitsPos[0] - axisOrigin[1] + position[1], yLimitsPos[1] - axisOrigin[1] + position[1]]))
        if not drawAxis:
            return [None, outputLimits, axisOrigin]

        # axis ticks
        groupTicks = ExtensionBaseObj.createGroup(GroupPlot, 'Ticks')

        if xTicks or xGrid:

            if xlog10scale:
                listTicks = generateListOfTicksLog10(xLimits)
            else:
                listTicks = generateListOfTicksLinear(xLimits, axisOrigin[0] / scaleX, xTickStep)
            for x in listTicks:

                if x <= xLimits[1] and x >= xLimits[0]:

                    # get position, considering the scale and its text
                    [posX, xText] = getPositionAndText(x, scaleX, xlog10scale, xAxisUnitFactor)

                    if xGrid and posX != axisOrigin[0]:  # grid lines. Do not draw if grid line is over the axis
                        inkDraw.line.absCoords(groupTicks, [[posX, yLimitsPos[0]], [posX, yLimitsPos[1]]], [0, 0], lineStyle=lineStyleGrid)

                    # intermediate grid lines in case of logarithmic scale
                    if xGrid and xlog10scale and x < xLimits[1]:
                        for i in range(2, 10):
                            aditionalStep = math.log10(i) * scaleX
                            inkDraw.line.absCoords(groupTicks, [[posX + aditionalStep, yLimitsPos[0]], [posX + aditionalStep, yLimitsPos[1]]], [0, 0],
                                                   lineStyle=lineStyleGridFine)

                    # tick
                    if xTicks:
                        if posX != axisOrigin[0]:  # don't draw if in the origin
                            inkDraw.line.relCoords(groupTicks, [[0, lenghtTicks]], [posX, axisOrigin[1] - lenghtTicks / 2.0],
                                                   lineStyle=lineStyleTicks)

                    # sets justification
                    # inkDraw.text.write(ExtensionBaseObj,'orig='+str(axisOrigin),[axisOrigin[0]+10,axisOrigin[1]-30],groupTicks,fontSize=7)
                    # inkDraw.text.write(ExtensionBaseObj,'xlim='+str(xLimitsPos),[axisOrigin[0]+10,axisOrigin[1]-20],groupTicks,fontSize=7)
                    # inkDraw.text.write(ExtensionBaseObj,'ylim='+str(yLimitsPos),[axisOrigin[0]+10,axisOrigin[1]-10],groupTicks,fontSize=7)

                    if axisOrigin[1] == yLimitsPos[0]:
                        justif = 'tc'
                        offsetX = 0
                        offsetY = text_offset / 2.0  # inkDraw.circle.centerRadius(groupTicks, axisOrigin, 10, [0,0])

                    if axisOrigin[1] != yLimitsPos[0] and axisOrigin[1] != yLimitsPos[1]:
                        justif = 'tr'
                        offsetX = -text_offset / 4.0
                        offsetY = text_offset / 2.0
                        # inkDraw.circle.centerRadius(groupTicks, axisOrigin, 10, [0,0])
                        # inkDraw.text.write(ExtensionBaseObj,str(axisOrigin[1]),[axisOrigin[0]+10,axisOrigin[1]+10],groupTicks,fontSize=7)
                        # inkDraw.text.write(ExtensionBaseObj,str(yLimitsPos[0]),[axisOrigin[0]+10,axisOrigin[1]+20],groupTicks,fontSize=7)
                        if posX == axisOrigin[0]:
                            if posX == xLimitsPos[1]:
                                justif = 'tr'
                                offsetX = -text_offset / 4.0
                            else:
                                justif = 'tl'
                                offsetX = +text_offset / 4.0

                    if axisOrigin[1] == yLimitsPos[1]:
                        justif = 'bc'
                        offsetX = 0
                        offsetY = -text_offset / 2.0
                        # inkDraw.circle.centerRadius(groupTicks,axisOrigin, 10, [0,0])
                        if posX == axisOrigin[0]:
                            if posX == xLimitsPos[1]:
                                justif = 'br'
                                offsetX = -text_offset / 4.0
                            else:
                                justif = 'bl'
                                offsetX = +text_offset / 4.0

                    # value
                    if xTicks:
                        inkDraw.text.latex(ExtensionBaseObj, groupTicks, xText, [posX + offsetX, axisOrigin[1] + offsetY], textSizeSmall,
                                           refPoint=justif)

        if yTicks or yGrid:
            # approximate limits to multiples of 10
            if ylog10scale:
                listTicks = generateListOfTicksLog10(yLimits)
            else:
                listTicks = generateListOfTicksLinear(yLimits, axisOrigin[1] / scaleY, yTickStep)

            for y in listTicks:
                if y <= yLimits[1] and y >= yLimits[0]:

                    # get position, considering the scale and its text
                    [posY, yText] = getPositionAndText(y, abs(scaleY), ylog10scale, yAxisUnitFactor)
                    posY = -posY

                    if yGrid and posY != axisOrigin[1]:  # grid lines. Do not draw if grid line is over the axis
                        inkDraw.line.absCoords(groupTicks, [[xLimitsPos[0], posY], [xLimitsPos[1], posY]], [0, 0], lineStyle=lineStyleGrid)

                    # intermediate grid lines in case of logarithmic scale
                    if yGrid and ylog10scale and y < yLimits[1]:
                        for i in range(2, 10):
                            aditionalStep = math.log10(i) * scaleY
                            inkDraw.line.absCoords(groupTicks, [[xLimitsPos[0], posY + aditionalStep], [xLimitsPos[1], posY + aditionalStep]], [0, 0],
                                                   lineStyle=lineStyleGridFine)

                    # tick
                    if yTicks:
                        if posY != axisOrigin[1]:  # don't draw if in the origin
                            inkDraw.line.relCoords(groupTicks, [[lenghtTicks, 0]], [axisOrigin[0] - lenghtTicks / 2.0, posY],
                                                   lineStyle=lineStyleTicks)

                    # sets justification
                    # inkDraw.text.write(ExtensionBaseObj,'orig='+str(axisOrigin),[axisOrigin[0]+10,axisOrigin[1]-30],groupTicks,fontSize=7)
                    # inkDraw.text.write(ExtensionBaseObj,'xlim='+str(xLimitsPos),[axisOrigin[0]+10,axisOrigin[1]-20],groupTicks,fontSize=7)
                    # inkDraw.text.write(ExtensionBaseObj,'ylim='+str(yLimitsPos),[axisOrigin[0]+10,axisOrigin[1]-10],groupTicks,fontSize=7)

                    if axisOrigin[0] == xLimitsPos[0]:
                        justif = 'cr'
                        offsetX = -text_offset / 2.0
                        offsetY = 0  # inkDraw.circle.centerRadius(groupTicks,axisOrigin, 10, [0,0],'trash')

                    if axisOrigin[0] != xLimitsPos[0] and axisOrigin[0] != xLimitsPos[1]:
                        justif = 'tr'
                        offsetX = -text_offset / 2.0
                        offsetY = text_offset / 4.0
                        # inkDraw.circle.centerRadius(groupTicks,axisOrigin, 10, [0,0])
                        # inkDraw.text.write(ExtensionBaseObj,str(axisOrigin[0]),[axisOrigin[0]+10,axisOrigin[1]+10],groupTicks,fontSize=7)
                        # inkDraw.text.write(ExtensionBaseObj,str(yLimitsPos[0]*scaleX),[axisOrigin[0]+10,axisOrigin[1]+20],groupTicks,fontSize=7)
                        if posY == axisOrigin[1]:
                            if posY == yLimitsPos[1]:
                                justif = 'tr'
                                offsetY = text_offset / 4.0
                            else:
                                justif = 'br'
                                offsetY = -text_offset / 4.0

                    if axisOrigin[0] == xLimitsPos[1]:
                        justif = 'cl'
                        offsetX = text_offset / 2.0
                        offsetY = 0
                        # inkDraw.circle.centerRadius(groupTicks,axisOrigin, 10, [0,0])
                        if posY == axisOrigin[1]:
                            if posY == yLimitsPos[1]:
                                justif = 'tl'
                                offsetY = text_offset / 4.0
                            else:
                                justif = 'bl'
                                offsetY = -text_offset / 4.0

                    # value
                    if yTicks:
                        inkDraw.text.latex(ExtensionBaseObj, groupTicks, yText, [axisOrigin[0] + offsetX, (posY + offsetY)], textSizeSmall,
                                           refPoint=justif)

        ExtensionBaseObj.moveElement(GroupPlot, [position[0] - axisOrigin[0], position[1] - axisOrigin[1]])

        # draw axis in the end so it stays on top of other objects
        GroupAxis = ExtensionBaseObj.createGroup(GroupPlot, 'Axis')

        inkDraw.line.absCoords(GroupAxis, [[xLimitsPos[0], 0], [xLimitsPos[1] + ExtraSpaceArrowX, 0]], [0, axisOrigin[1]], 'Xaxis',
                               lineStyle=lineStyleAxis)
        if xLabel:  # axis labels
            inkDraw.text.latex(ExtensionBaseObj, GroupAxis, xLabel,
                               [xLimitsPos[1] + ExtraSpaceArrowX - text_offset / 3, axisOrigin[1] + text_offset / 2.0], textSize, refPoint='tl')

        inkDraw.line.absCoords(GroupAxis, [[0, yLimitsPos[0]], [0, yLimitsPos[1] - ExtraSpaceArrowY]], [axisOrigin[0], 0], 'Yaxis',
                               lineStyle=lineStyleAxis)
        if yLabel:  # axis labels
            inkDraw.text.latex(ExtensionBaseObj, GroupAxis, yLabel, [axisOrigin[0] + text_offset / 2.0, (yLimitsPos[1] - ExtraSpaceArrowY)], textSize,
                               refPoint='tl')

        return [GroupPlot, outputLimits, axisOrigin]

    @staticmethod
    def polar(ExtensionBaseObj, parent, rLim, tLim=[0.0, 360.0], position=[0.0, 0.0], rLabel='', rlog10scale=False, rTicks=True, tTicks=True,
              rTickStep=1.0, tTickStep=45.0, rScale=20, rAxisUnitFactor='', rGrid=False, tGrid=False, forceTextSize=0, forceLineWidth=0,
              drawAxis=True, ExtraLengthAxisR=0.0):
        """Creates the axes of a polar plot

        .. note:: This method uses LaTeX in labels and tick marks if LaTeX support is enabled. This is an optional feature, **enabled by default**.
            Please refer to :ref:`disableLatexSupport` on how to disable it.
        
        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param parent: Parent object
        :param rLim: Limits of the R axis [r_min,r_max]. If the axis is in log10 scale, then the limits will be rounded to complete one decade.
        :param tLim: Limits of the theta axis [t_min,t_max]. Values in degrees. Default: [0,360]
        :param position: Position of the center [x0,y0].

        :param rLabel: Label of the R axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param rlog10scale: Sets R axis to log10 scale if True. Default: False

            - If rlog10scale=True, then the lower limit of rLim must be >=1

        :param rTicks: Adds axis ticks to the R axis if True. Default: True
        :param tTicks: Adds axis ticks to the theta axis if True. Default: True
        :param rTickStep: Value interval between two consecutive ticks on R axis. (Not used if R axis is in log10 scale). Default:1.0
        :param tTickStep: Value interval between two consecutive ticks on theta axis. Default:45.0
        :param rScale:  Distance between each rTickStep in svg units. Default: 20

               - If axis is linear, then rScale is the size in svg units of each tick
               - If axis is log10, the rScale is the size in svg units of one decade

        :param rAxisUnitFactor: Extra text to be added to the ticks in R axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.

        :param rGrid: Adds grid lines to R axis if true. Default: False
        :param tGrid: Adds grid lines to theta axis if true. Default: False
        :param forceTextSize: Size of the text. If this parameter is 0.0 then the method will compute an appropriate size. Default: 0.0
        :param forceLineWidth: Width of the lines. If this parameter is 0.0 then the method will compute an appropriate size. Default: 0.0

        :param drawAxis: Control flag of the axis method

               - True: draws axis normally
               - False: returns the limits and origin position without drawing the axis itself

        :param ExtraLengthAxisR: Extra length between the R axis and its label. Default 0.0

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type parent: inkscape element object
        :type rLim: list
        :type tLim: list
        :type position: list
        :type rLabel: string
        :type rlog10scale: bool
        :type rTicks: bool
        :type tTicks: bool
        :type rTickStep: float
        :type tTickStep: float
        :type rScale: float
        :type rAxisUnitFactor: string
        :type rGrid: bool
        :type tGrid: bool
        :type forceTextSize: float
        :type forceLineWidth: float
        :type drawAxis: bool
        :type ExtraLengthAxisR: float

        :returns: [GroupPlot, outputRLimits, axisOrigin]

            - GroupPlot:  the axis area object (if drawAxis=False, this output is ``None``)
            - outputRLimits: a list with tuples:[(r_min,rPos_min),(r_max,rPos_max)]

                  - r_min, r_max       :   The limits of the axis object
                  - rPos_min, rPos_max :   The positions of the limits of the axis object, considering the scaling and units
            - axisOrigin [X0,Y0] :   A list with the coordinates of the point where the axes cross.
        :rtype: list

        **Examples**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>>
        >>> inkPlot.axis.cartesian(self, parent=root_layer, rLim=[0, 3], tLim=[0, 150], position=[0.0, 0.0], rLabel='my radius',
        >>>                        rlog10scale=False, rTicks=True, tTicks=True, rTickStep=1.0, tTickStep=30.0, rScale=50,
        >>>                        rAxisUnitFactor='', rGrid=True, tGrid=True, forceTextSize=0, forceLineWidth=0,
        >>>                        drawAxis=True, ExtraLengthAxisR=10.0)

        The images below show the cartesian plane of the example above, together with other variations.

        .. image:: ../imagesDocs/plot_axisPolarParameters_01.png
          :width: 800px
        """

        if drawAxis:
            GroupPlot = ExtensionBaseObj.createGroup(parent, 'Plot')

        # sets the scale  scaleX and scaleY stores the size of one unit in both axis (linear axis) or the size of a decade in log plots
        if rlog10scale:
            scaleR = rScale
        else:
            scaleR = rScale / float(rTickStep)

        # font size and other text parameters
        if forceTextSize == 0:
            textSize = 0.2 * rScale
        else:
            textSize = forceTextSize

        textSizeSmall = 0.8 * textSize  # font size for axis ticks

        text_offset = textSize  # base space for text positioning
        ExtraSpaceArrowR = (2.0 + ExtraLengthAxisR) * text_offset  # extra space for drawing arrow on axis
        lenghtTicks = textSize / 2.0  # length of the ticks

        # create styles
        if forceLineWidth == 0:
            lineWidth = rScale / 30.0
        else:
            lineWidth = forceLineWidth

        lineWidthGrid = 0.7 * lineWidth
        lineWidthGridFine = lineWidthGrid / 2.0

        # nameTickerArrowAxis = inkDraw.marker.createArrow1Marker(ExtensionBaseObj, 'ArrowAxis', RenameMode=1, scale=0.4)
        lineStyleAxis = inkDraw.lineStyle.set(lineWidth, lineColor=inkDraw.color.gray(0.3))
        lineStyleTicks = inkDraw.lineStyle.set(lineWidth, lineColor=inkDraw.color.gray(0.3))
        lineStyleGrid = inkDraw.lineStyle.set(lineWidthGrid, lineColor=inkDraw.color.gray(0.7))
        lineStyleGridFine = inkDraw.lineStyle.set(lineWidthGridFine, lineColor=inkDraw.color.gray(0.7))

        textStyleLarge = inkDraw.textStyle.setSimpleBlack(textSize)
        textStyleSmall = inkDraw.textStyle.setSimpleBlack(textSizeSmall, 'center')

        # check if limits are valid
        if rLim[0] < 0.0 or rLim[0] >= rLim[1]:
            sys.stderr.write('Error: rLim is invalid')
            return 0
        if tLim[0] >= tLim[1]:
            sys.stderr.write('Error: tLim is invalid')
            return 0
        # check if the limits are valid for logarithmic scales.
        if rlog10scale:
            if rLim[0] < 1 or rLim[1] < 1:
                sys.stderr.write('Error: rLim is invalid in logarithmic scale')
                return 0
            else:
                rmin = pow(10, math.floor(math.log10(rLim[0])))
                rmax = pow(10, math.ceil(math.log10(rLim[1])))
                rLimits = [rmin, rmax]
        else:
            rLimits = rLim

        tLimits = tLim

        if abs(tLimits[1] - tLimits[0]) > 360:
            tLimits = [0, 360]

        if abs(tLimits[1] - tLimits[0]) > 180:
            largeArc = True
        else:
            largeArc = False

        # finds the position of the Origin of axis
        axisOrigin = [0.0, 0.0]
        axisOrigin[0] = findOrigin(rLimits, rlog10scale, scaleR)
        axisOrigin[1] = findOrigin(tLimits, False, 1.0)

        # computes the positions of the limits on svg, considering the scale

        if rlog10scale:  # convert limits to position in diagram, including scaling factor
            rLimitsPos = [math.log10(x) * scaleR for x in rLimits]
        else:
            rLimitsPos = [x * scaleR for x in rLimits]

        # build the list of tuples with the limits of the plotting area
        outputLimits = list(zip([rLimits[0], rLimits[1]], [rLimitsPos[0] - axisOrigin[0] + position[0], rLimitsPos[1] - axisOrigin[0] + position[0]]))

        if not drawAxis:
            return [None, outputLimits, [0, 0]]

        # axis ticks
        groupTicks = ExtensionBaseObj.createGroup(GroupPlot, 'Ticks')

        if rTicks or rGrid:

            if rlog10scale:
                listTicks = generateListOfTicksLog10(rLimits)
            else:
                listTicks = generateListOfTicksLinear(rLimits, axisOrigin[0] / scaleR, rTickStep)
            for r in listTicks:

                if r <= rLimits[1] and r >= rLimits[0]:

                    # get position, considering the scale and its text
                    [posR, rText] = getPositionAndText(r, scaleR, rlog10scale, rAxisUnitFactor)

                    if rGrid and posR > 0.0 and r > rLimits[0] and r < rLimits[1]:  # grid lines.
                        if tLimits[1] - tLimits[0] < 360:
                            inkDraw.arc.centerAngStartAngEnd(groupTicks, [0, 0], posR, -tLimits[1], -tLimits[0], [0, 0], lineStyle=lineStyleGrid,
                                                             largeArc=largeArc)  # negative angles bc inkscape is upside down
                        else:
                            inkDraw.circle.centerRadius(groupTicks, [0, 0], posR, offset=[0, 0], lineStyle=lineStyleGrid)

                    # intermediate grid lines in case of logarithmic scale
                    if rGrid and rlog10scale and r < rLimits[1]:
                        for i in range(2, 10):
                            aditionalStep = math.log10(i) * scaleR
                            if tLimits[1] - tLimits[0] < 360:
                                inkDraw.arc.centerAngStartAngEnd(groupTicks, [0, 0], posR + aditionalStep, -tLimits[1], -tLimits[0], [0, 0],
                                                                 lineStyle=lineStyleGridFine,
                                                                 largeArc=largeArc)  # negative angles bc inkscape is upside down
                            else:
                                inkDraw.circle.centerRadius(groupTicks, [0, 0], posR + aditionalStep, offset=[0, 0], lineStyle=lineStyleGridFine)

                    # tick
                    if rTicks and posR > 0.0:
                        inkDraw.arc.centerAngStartAngEnd(groupTicks, [0, 0], posR, -tLimits[0] - math.degrees(lenghtTicks / float(posR * 2)),
                                                         -tLimits[0] + math.degrees(lenghtTicks / float(posR * 2)), [0, 0], lineStyle=lineStyleTicks,
                                                         largeArc=False)
                    if rTicks and posR == 0.0:
                        inkDraw.line.relCoords(groupTicks, [[0, lenghtTicks]], [0, - lenghtTicks / 2.0], lineStyle=lineStyleTicks)

                    # sets justification
                    # inkDraw.text.write(ExtensionBaseObj,'orig='+str(axisOrigin),[axisOrigin[0]+10,axisOrigin[1]-30],groupTicks,fontSize=7)
                    # inkDraw.text.write(ExtensionBaseObj,'xlim='+str(xLimitsPos),[axisOrigin[0]+10,axisOrigin[1]-20],groupTicks,fontSize=7)
                    # inkDraw.text.write(ExtensionBaseObj,'ylim='+str(yLimitsPos),[axisOrigin[0]+10,axisOrigin[1]-10],groupTicks,fontSize=7)

                    if posR == 0:
                        justif = 'cc'
                        offsetX = 0
                        offsetY = text_offset * 1.2
                        posX = posR * math.cos(math.radians(-tLimits[0])) + offsetX
                        posY = posR * math.sin(math.radians(-tLimits[0])) + offsetY
                    else:
                        offsetT = text_offset * 1.2
                        if tLimits[1] - tLimits[0] > 340:
                            offsetR = text_offset / 2.0
                        else:
                            offsetR = 0
                        justif = 'cc'
                        posX = (posR + offsetR) * math.cos(math.radians(-tLimits[0])) + offsetT * math.sin(math.radians(tLimits[0]))
                        posY = (posR + offsetR) * math.sin(math.radians(-tLimits[0])) + offsetT * math.cos(math.radians(-tLimits[0]))
                    # value
                    # inkDraw.circle.centerRadius(groupTicks,[posX,posY], 1)
                    if rTicks:
                        inkDraw.text.latex(ExtensionBaseObj, groupTicks, rText, [posX, posY], textSizeSmall, refPoint=justif)

        if tTicks or tGrid:

            listTicks = generateListOfTicksLinear(tLimits, axisOrigin[1], tTickStep)
            for t in listTicks:
                if t <= tLimits[1] and t >= tLimits[0]:
                    c = math.cos(math.radians(-t))  # negative angles bc inkscape is upside down
                    s = math.sin(math.radians(-t))  # negative angles bc inkscape is upside down
                    # get position, considering the scale and its text
                    if inkDraw.useLatex:
                        tText = '$' + str(t) + '$'
                    else:
                        tText = str(t)

                    if (tGrid and t > tLimits[0] and t < tLimits[1]) or (tGrid and t == tLimits[0] and tLimits[1] - tLimits[0] >= 360):
                        if rLimitsPos[0] == 0:  # if rmin is zero, then make the lines to reach the center
                            if not rlog10scale:
                                P1 = [(rLimitsPos[0] + scaleR * rTickStep / 2) * c, (rLimitsPos[0] + scaleR * rTickStep / 2) * s]
                            else:
                                P1 = [(rLimitsPos[0] + 0.3 * scaleR) * c, (rLimitsPos[0] + 0.3 * scaleR) * s]
                        else:
                            P1 = [rLimitsPos[0] * c, rLimitsPos[0] * s]
                        P2 = [rLimitsPos[1] * c, rLimitsPos[1] * s]
                        inkDraw.line.absCoords(groupTicks, [P1, P2], [0, 0], lineStyle=lineStyleGrid)

                    # tick
                    if (tTicks and t != tLimits[1]) or (tTicks and t == tLimits[1] and tLimits[1] - tLimits[0] < 360):
                        P1 = [(rLimitsPos[1] - lenghtTicks / 2.0) * c, (rLimitsPos[1] - lenghtTicks / 2.0) * s]
                        inkDraw.line.relCoords(groupTicks, [[lenghtTicks * c, lenghtTicks * s]], P1, lineStyle=lineStyleTicks)

                    if c > 1.0e-4:
                        justif = 'cl'
                    else:
                        if c < -1.0e-4:
                            justif = 'cr'
                        else:
                            justif = 'cc'

                    offsetR = text_offset
                    posX = (rLimitsPos[1] + offsetR) * c
                    posY = (rLimitsPos[1] + offsetR) * s
                    # value
                    if (tTicks and t != tLimits[1]) or (tTicks and t == tLimits[1] and tLimits[1] - tLimits[0] < 360):
                        inkDraw.text.latex(ExtensionBaseObj, groupTicks, tText, [posX, posY], textSizeSmall, refPoint=justif)

        ExtensionBaseObj.moveElement(GroupPlot, position)

        # draw axis in the end so it stays on top of other objects
        GroupAxis = ExtensionBaseObj.createGroup(GroupPlot, 'Axis')

        c0 = math.cos(math.radians(-tLimits[0]))  # negative angles bc inkscape is upside down
        s0 = math.sin(math.radians(-tLimits[0]))  # negative angles bc inkscape is upside down
        c1 = math.cos(math.radians(-tLimits[1]))  # negative angles bc inkscape is upside down
        s1 = math.sin(math.radians(-tLimits[1]))  # negative angles bc inkscape is upside down
        P1 = [rLimitsPos[0] * c0, rLimitsPos[0] * s0]
        P2 = [rLimitsPos[1] * c0, rLimitsPos[1] * s0]
        P3 = [rLimitsPos[1] * c1, rLimitsPos[1] * s1]
        P4 = [rLimitsPos[0] * c1, rLimitsPos[0] * s1]
        if tLimits[1] - tLimits[0] < 360:
            inkDraw.line.absCoords(GroupAxis, [P1, P2], [0, 0], lineStyle=lineStyleAxis)
            inkDraw.line.absCoords(GroupAxis, [P3, P4], [0, 0], lineStyle=lineStyleAxis)
        else:
            if rTicks:
                inkDraw.line.absCoords(GroupAxis, [P1, P2], [0, 0], lineStyle=lineStyleAxis)

        if tLimits[1] - tLimits[0] < 360:
            if rLimitsPos[0] > 0:
                inkDraw.arc.startEndRadius(GroupAxis, P1, P4, rLimitsPos[0], offset=[0, 0], lineStyle=lineStyleAxis, flagRightOf=True, arcType='open',
                                           largeArc=largeArc)
            inkDraw.arc.startEndRadius(GroupAxis, P2, P3, rLimitsPos[1], offset=[0, 0], lineStyle=lineStyleAxis, flagRightOf=True, arcType='open',
                                       largeArc=largeArc)
        else:
            if rLimitsPos[0] > 0:
                inkDraw.circle.centerRadius(GroupAxis, [0, 0], rLimitsPos[0], offset=[0, 0], lineStyle=lineStyleAxis)
            inkDraw.circle.centerRadius(GroupAxis, [0, 0], rLimitsPos[1], offset=[0, 0], lineStyle=lineStyleAxis)

        if rLabel:  # axis labels
            c0 = math.cos(math.radians(-tLimits[0]) + text_offset / rLimitsPos[1])  # negative angles bc inkscape is upside down
            s0 = math.sin(math.radians(-tLimits[0]) + text_offset / rLimitsPos[1])  # negative angles bc inkscape is upside down
            posText = [(rLimitsPos[1] + ExtraSpaceArrowR) * c0, (rLimitsPos[1] + ExtraSpaceArrowR) * s0]
            inkDraw.text.latex(ExtensionBaseObj, GroupAxis, rLabel, posText, textSize, refPoint='cl')

        return [GroupPlot, outputLimits, [0, 0]]


class plot():
    """ This class has member functions to create plots.

    .. note:: This class contains only static methods so that your plugin class don't have to inherit it.

    .. note:: This class uses LaTeX in labels and tick marks if LaTeX support is enabled. This is an optional feature, **enabled by default**.
            Please refer to :ref:`disableLatexSupport` on how to disable it. If disabled, this function will still work, internally calling the :meth:`inkscapeMadeEasy_Draw.text.write` to generate text.
    """

    @staticmethod
    def cartesian(ExtensionBaseObj, parent, xData, yData, position=[0, 0], xLabel='', yLabel='', xlog10scale=False, ylog10scale=False, xTicks=True,
                  yTicks=True, xTickStep=1.0, yTickStep=1.0, xScale=20, yScale=20, xExtraText='', yExtraText='', xGrid=False, yGrid=False,
                  generalAspectFactorAxis=1.0, lineStylePlot=inkDraw.lineStyle.setSimpleBlack(), forceXlim=None, forceYlim=None, drawAxis=True,
                  ExtraLengthAxisX=0.0, ExtraLengthAxisY=0.0):
        """Create a cartesian Plot

        .. note:: This method uses LaTeX in labels and tick marks if LaTeX support is enabled. This is an optional feature, **enabled by default**. Please refer to :ref:`disableLatexSupport` on how to disable it.

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param parent: Parent object
        :param xData: List of x data
        :param yData: List of y data
        :param position: Position of the plot. It is defined at the point where x and y axis cross [x0,y0]. The point where the axis cross depend on the limits.

              - If xLimits comprises the origin x=0, then the  Y axis crosses the X axis at x=0.
              - If xLimits contains only negative numbers, then the Y axis crosses the X axis at x_max.
              - If xLimits contains only positive numbers, then the Y axis crosses the X axis at x_min.

              - The same rule applies to y direction.
        :param xLabel: Label of the X axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param yLabel: Label of the Y axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param xlog10scale: Sets X axis to log10 scale if True. Default: False
        :param ylog10scale: Sets Y axis to log10 scale if True. Default: False
        :param xTicks: Adds axis ticks to the X axis if True. Default: True
        :param yTicks: Adds axis ticks to the Y axis if True. Default: True
        :param xTickStep: Value interval between two consecutive ticks on X axis. (Not used if X axis is in log10 scale). Default:1.0
        :param yTickStep: Value interval between two consecutive ticks on Y axis. (Not used if Y axis is in log10 scale). Default:1.0
        :param xScale:  Distance between each xTickStep in svg units. Default: 20

               - If axis is linear, then xScale is the size in svg units of each tick
               - If axis is log10, the xScale is the size in svg units of one decade

        :param yScale: Distance between each yTickStep in svg units. Default: 20

               - If axis is linear, then yScale is the size in svg units of each tick
               - If axis is log10, the yScale is the size in svg units of one decade

        :param xExtraText: Extra text to be added to the ticks in X axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.
        :param yExtraText: Extra text to be added to the ticks in Y axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.

        :param xGrid: Adds grid lines to X axis if True. Default: False
        :param yGrid: Adds grid lines to Y axis if True. Default: False
        :param generalAspectFactorAxis: Regulates the general aspect ratio between grid lines, text and Ticks separations. Default: 1.0

        :param lineStylePlot: Line style to be used to plot the data. See class ``inkscapeMadeEasy_Draw.lineStyle``. Default: lineStylePlot=inkDraw.lineStyle.setSimpleBlack()
        :param forceXlim: Forces limits of X axis to these limits. These limits affect the axis only, that is, all xData is plotted despite of these limits.

            - if forceXlim=None Limits will be defined by the limits of xData (Default)
            - if forceXlim=[xMin,xMax] then these limits will be used.

            .. note:: for logarithmic scale, the limits are always adjusted to complete the decade. Usually you don't need this for logarithmic scale

        :param forceYlim: Forces limits of Y axis to these limits. These limits affect the axis only, that is, all yData is plotted despite of these limits.

            - if forceYlim=None Limits will be defined by the limits of yData (Default)
            - if forceYlim=[yMin,yMax] then these limits will be used.

            .. note:: for logarithmic scale, the limits are always adjusted to complete the decade. Usually you don't need this for logarithmic scale

        :param drawAxis: Control flag of the axis method

               - True: draws axis normally
               - False: returns the limits and origin position without drawing the axis itself

        :param ExtraLengthAxisX: Extra length near the arrow pointer of X axis. Default 0.0
        :param ExtraLengthAxisY: Extra length near the arrow pointer of Y axis. Default 0.0

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type parent: inkscape element object
        :type xData: list
        :type yData: list
        :type position: list
        :type xLabel: string
        :type yLabel: string
        :type xlog10scale: bool
        :type ylog10scale: bool
        :type xTicks: bool
        :type yTicks: bool
        :type xTickStep: float
        :type yTickStep: float
        :type xScale: float
        :type yScale: float
        :type xExtraText: string
        :type yExtraText: string
        :type xGrid: bool
        :type yGrid: bool
        :type generalAspectFactorAxis: float
        :type lineStylePlot: lineStyle object
        :type forceXlim: list
        :type forceYlim: list
        :type drawAxis: bool
        :type ExtraLengthAxisX: float
        :type ExtraLengthAxisY: float

        :returns: [GroupPlot, outputLimits, axisOrigin]

            - GroupPlot:  the plot object
            - outputLimits: a list with tuples:[(x_min,xPos_min),(x_max,xPos_max),(y_min,yPos_min),(y_max,yPos_max)]

                  - x_min, x_max, y_min, y_max:               The limits of the axis object
                  - xPos_min, xPos_max, yPos_min, yPos_max:   The positions of the limits of the axis object, considering the scaling and units
            - axisOrigin [X0,Y0]:                      A list with the coordinates of the point where the axes cross.
        :rtype: list

        .. important:: If any of the axis are log10, then the method ignores any pairs of (x,y) data with invalid coordinates, that is, if xData and/or yData is less than or equal to 0.0 (they would result in complex log10... =P ). The method will create a text object alongside your plot warning this.

        .. note:: If any of the axis are linear, the method will ignore any value greater than 10.000 (in absolute value). This avoids plotting very large numbers. The method will create a text object alongside your plot warning this.

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> xData=[-1,-0.5,0,0.5,1.0,1.5,2]
        >>> yData=[x*x for x in xData]    # computes y=x*x
        >>> #create a lineStyle for the plot
        >>> myMarkerDot=inkDraw.marker.createDotMarker(self,'DotM',RenameMode=2,scale=0.3,
        >>>                                            strokeColor=inkDraw.color.defined('black'),fillColor=inkDraw.color.defined('black'))
        >>> lineStyleDiscrete = inkDraw.lineStyle.set(lineWidth=1.0, markerStart=myMarkerDot,markerMid=myMarkerDot,markerEnd=myMarkerDot)
        >>>
        >>> inkPlot.plot.cartesian(self,root_layer,xData,yData,position=[0,0],
        >>>                        xLabel='my $x$ data',yLabel='$y(x)$',xlog10scale=False,ylog10scale=False,
        >>>                        xTicks=True,yTicks=True,xTickStep=0.5,yTickStep=2.0,
        >>>                        xScale=20,yScale=10,xExtraText='a',yExtraText='',
        >>>                        xGrid=True,yGrid=True,generalAspectFactorAxis=1.0,lineStylePlot=lineStyleDiscrete,
        >>>                        forceXlim=None,forceYlim=None,drawAxis=True)

        The image below present the plot above with a few argument variations.

        .. image:: ../imagesDocs/plot_plotCartesianParameters_01.png
          :width: 800px

        """

        textSize = generalAspectFactorAxis * 0.25 * min(xScale, yScale)
        lineWidthAxis = generalAspectFactorAxis * min(xScale, yScale) / 35.0

        yDataTemp = []
        xDataTemp = []
        flagShowedError = False
        if xlog10scale:  # remove invalid pairs of coordinates for log plot (less than or equal to 0.0)
            for i in range(len(xData)):
                if xData[i] > 0.0:
                    yDataTemp.append(yData[i])
                    xDataTemp.append(xData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj,
                                           'Error: The point (%f,%f)\n is invalid in logarithmic scale. Ignoring it...' % (xData[i], yData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True
        else:  # remove invalid pairs of coordinates for linear plot (larger than +-10k )
            for i in range(len(xData)):
                if abs(xData[i]) <= 1.0e4:
                    yDataTemp.append(yData[i])
                    xDataTemp.append(xData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj, 'Error: The point (%f,%f)\n is too large. Ignoring it...' % (xData[i], yData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True

        yData = yDataTemp
        xData = xDataTemp

        yDataTemp = []
        xDataTemp = []
        flagShowedError = False
        if ylog10scale:  # remove invalid pairs of coordinates for log plot (less than or equal to 0.0)
            for i in range(len(yData)):
                if yData[i] > 0.0:
                    yDataTemp.append(yData[i])
                    xDataTemp.append(xData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj,
                                           'Error: The point (%f,%f)\n is invalid in logarithmic scale. Ignoring it...' % (xData[i], yData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True
        else:  # remove invalid pairs of coordinates for linear plot (larger than +-10k )
            for i in range(len(yData)):
                if abs(yData[i]) <= 1.0e4:
                    yDataTemp.append(yData[i])
                    xDataTemp.append(xData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj, 'Error: The point (%f,%f)\n is too large. Ignoring it...' % (xData[i], yData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True

        yData = yDataTemp
        xData = xDataTemp

        if forceXlim is not None:
            Xlimits = forceXlim
        else:
            Xlimits = [min(xData), max(xData)]
        if forceYlim is not None:
            Ylimits = forceYlim
        else:
            Ylimits = [min(yData), max(yData)]  # min<->max inverted  bc inkscape is upside down

        if Ylimits[0] == Ylimits[1]:
            if Ylimits[0] > 0:
                Ylimits[0] = 0
            if Ylimits[0] == 0:
                Ylimits[1] = 1
            if Ylimits[0] < 0:
                Ylimits[1] = 0

        if Xlimits[0] == Xlimits[1]:
            if Xlimits[0] > 0:
                Xlimits[0] = 0
            if Xlimits[0] == 0:
                Xlimits[1] = 1
            if Xlimits[0] < 0:
                Xlimits[1] = 0

        # draw axis
        axisGroup = ExtensionBaseObj.createGroup(parent, 'PlotData')

        [axisObj, limits, origin] = axis.cartesian(ExtensionBaseObj, axisGroup, Xlimits, Ylimits, position, xLabel=xLabel, yLabel=yLabel,
                                                   xlog10scale=xlog10scale, ylog10scale=ylog10scale, xTicks=xTicks, yTicks=yTicks,
                                                   xTickStep=xTickStep, yTickStep=yTickStep, xScale=xScale, yScale=yScale, xAxisUnitFactor=xExtraText,
                                                   yAxisUnitFactor=yExtraText, xGrid=xGrid, yGrid=yGrid, forceTextSize=textSize,
                                                   forceLineWidth=lineWidthAxis, drawAxis=drawAxis, ExtraLengthAxisX=ExtraLengthAxisX,
                                                   ExtraLengthAxisY=ExtraLengthAxisY)

        # scales data and convert to logarithmic scale if needed. Also subtracts the origin point of the axis to move the plot to the correct position
        if xlog10scale:
            xData = [math.log10(x) * xScale - origin[0] for x in xData]
        else:
            xData = [x * (xScale / xTickStep) - origin[0] for x in xData]

        if ylog10scale:
            yData = [-math.log10(y) * yScale - origin[1] for y in yData]
        else:
            yData = [-y * (yScale / yTickStep) - origin[1] for y in yData]  # negative bc inkscape is upside down

        coords = zip(xData, yData)

        inkDraw.line.absCoords(axisGroup, coords, position, lineStyle=lineStylePlot)

        return [axisGroup, limits, origin]

    @staticmethod
    def polar(ExtensionBaseObj, parent, rData, tData, position=[0, 0], rLabel='', rlog10scale=False, rTicks=True, tTicks=True, rTickStep=1.0,
              tTickStep=45.0, rScale=20, rExtraText='', rGrid=False, tGrid=False, generalAspectFactorAxis=1.0,
              lineStylePlot=inkDraw.lineStyle.setSimpleBlack(), forceRlim=None, forceTlim=None, drawAxis=True, ExtraLengthAxisR=0.0):
        """Create a polar Plot

        .. note:: This method uses LaTeX in labels and tick marks if LaTeX support is enabled. This is an optional feature, **enabled by default**. Please refer to :ref:`disableLatexSupport` on how to disable it.

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param parent: Parent object
        :param rData: List of R data
        :param tData: List of Theta data
        :param position: Position of the plot [x0,y0]. It is defined at the center point

        :param rLabel: Label of the R axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param rlog10scale: Sets R axis to log10 scale if True. Default: False
        :param rTicks: Adds axis ticks to the R axis if True. Default: True
        :param tTicks: Adds axis ticks to the Theta axis if True. Default: True
        :param rTickStep: Value interval between two consecutive ticks on R axis. (Not used if R axis is in log10 scale). Default:1.0
        :param tTickStep: Value interval between two consecutive ticks on Theta axis.
        :param rScale:  Distance between each rTickStep in svg units. Default: 20

               - If axis is linear, then rScale is the size in svg units of each tick
               - If axis is log10, the rScale is the size in svg units of one decade

        :param rExtraText: Extra text to be added to the ticks in R axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.

        :param rGrid: Adds grid lines to R axis if True. Default: False
        :param tGrid: Adds grid lines to Theta axis if True. Default: False
        :param generalAspectFactorAxis: Regulates the general aspect ratio between grid lines, text and Ticks separations. Default: 1.0

        :param lineStylePlot: Line style to be used to plot the data. See class ``inkscapeMadeEasy_Draw.lineStyle``. Default: lineStylePlot=inkDraw.lineStyle.setSimpleBlack()
        :param forceRlim: Forces limits of R axis to these limits. These limits affect the axis only, that is, all rData is plotted despite of these limits.

                - if forceRlim=None Limits will be defined by the limits of rData (Default)
                - if forceRlim=[rMin,rMax] then these limits will be used.

            .. note:: for logarithmic scale, the limits are always adjusted to complete the decade. Usually you don't need this for logarithmic scale

        :param forceTlim: Forces limits of Theta axis to these limits. These limits affect the axis only, that is, all tData is plotted despite of these limits.

                - if forceTlim=None Limits will be defined by min and max of tData (Default)
                - if forceTlim=[tMin,tMax] then these limits will be used.

        :param drawAxis: Control flag of the axis method

               - True: draws axis normally
               - False: returns the limits and origin position without drawing the axis itself

        :param ExtraLengthAxisR: Extra length near the arrow pointer of R axis. Default 0.0

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type parent: inkscape element object
        :type rData: list
        :type tData: list
        :type position: list
        :type rLabel: string
        :type rlog10scale: bool
        :type rTicks: bool
        :type tTicks: bool
        :type rTickStep: float
        :type tTickStep: float
        :type rScale: float
        :type rExtraText: string
        :type rGrid: bool
        :type tGrid: bool
        :type generalAspectFactorAxis: float
        :type lineStylePlot: lineStyle object
        :type forceRlim: list
        :type forceTlim: list
        :type drawAxis: bool
        :type ExtraLengthAxisR: float

        :returns: [GroupPlot, outputLimits, axisOrigin]

            - GroupPlot:  the plot object
            - outputLimits: a list with tuples:[(x_min,xPos_min),(x_max,xPos_max),(y_min,yPos_min),(y_max,yPos_max)]

                  - x_min, x_max, y_min, y_max:               The limits of the axis object
                  - xPos_min, xPos_max, yPos_min, yPos_max:   The positions of the limits of the axis object, considering the scaling and units
                  - axisOrigin [X0,Y0]:                      A list with the coordinates of the point where the axes cross.
        :rtype: list

        .. important:: If any of the axis are log10, then the method ignores any pairs of (x,y) data with invalid coordinates, that is, if rData and/or tData is less than or equal to 0.0 (they would result in complex log10... =P ). The method will create a text object alongside your plot warning this.

        .. note:: If any of the axis are linear, the method will ignore any value greater than 10.000 (in absolute value). This avoids plotting very large numbers. The method will create a text object alongside your plot warning this.

        **Example**

        >>> root_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> rData=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12]
        >>> tData=[30*x for x in range(12)]
        >>>
        >>> myMarkerDot=inkDraw.marker.createDotMarker(self,'DotM',RenameMode=2,scale=0.3,
        >>>                                            strokeColor=inkDraw.color.defined('black'),fillColor=inkDraw.color.defined('black'))
        >>> lineStyleDiscrete = inkDraw.lineStyle.set(lineWidth=1.0,linecolor=inkDraw.color.defined('red'),
        >>>                                           markerStart=myMarkerDot,markerMid=myMarkerDot,markerEnd=myMarkerDot)
        >>>
        >>> inkPlot.plot.polar(self,root_layer,rData,tData,position=[0,0],
        >>>                    rLabel='my $R$ data',rlog10scale=False,
        >>>                    rTicks=True,tTicks=True,rTickStep=2,tTickStep=30,
        >>>                    rScale=20,rExtraText='a',
        >>>                    rGrid=True,tGrid=True,generalAspectFactorAxis=1.0,lineStylePlot=lineStyleDiscrete,
        >>>                    forceRlim=None,forceTlim=None,drawAxis=True)
        >>>
        >>> # another spiral, comprising two turns
        >>> tData=[2*x for x in range(360)]
        >>> rData=[x/180.0 for x in tData]
        >>>
        >>> inkPlot.plot.polar(self,root_layer,rData,tData,position=[0,0],
        >>>                    rLabel='my $R$ data',rlog10scale=False,
        >>>                    rTicks=True,tTicks=True,rTickStep=2,tTickStep=30,
        >>>                    rScale=20,rExtraText='',
        >>>                    rGrid=True,tGrid=True,generalAspectFactorAxis=1.0,
        >>>                    forceRlim=None,forceTlim=None,drawAxis=True)

        The image below present the plot above with a few argument variations.

        .. image:: ../imagesDocs/plot_plotPolarParameters_01.png
          :width: 900px

        """

        textSize = generalAspectFactorAxis * 0.25 * rScale
        lineWidthAxis = generalAspectFactorAxis * rScale / 35.0

        tDataTemp = []
        rDataTemp = []
        flagShowedError = False
        if rlog10scale:  # remove invalid pairs of coordinates for log plot (less than or equal to 0.0)
            for i in range(len(rData)):
                if rData[i] >= 1.0:
                    tDataTemp.append(tData[i])
                    rDataTemp.append(rData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj,
                                           'Error: The point (%f,%f)\n is invalid in logarithmic scale. Ignoring it...' % (rData[i], tData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True
        else:  # remove invalid pairs of coordinates for linear plot (larger than +-10k )
            for i in range(len(rData)):
                if abs(rData[i]) <= 1.0e4:
                    tDataTemp.append(tData[i])
                    rDataTemp.append(rData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj, 'Error: The point (%f,%f)\n is too large. Ignoring it...' % (rData[i], tData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True

        tData = tDataTemp
        rData = rDataTemp

        if forceRlim is not None:
            Rlimits = forceRlim
        else:
            Rlimits = [min(rData), max(rData)]
        if forceTlim is not None:
            Tlimits = forceTlim
        else:
            Tlimits = [min(tData), max(tData)]  # min<->max inverted  bc inkscape is upside down

        if Tlimits[0] == Tlimits[1]:
            if Tlimits[0] > 0:
                Tlimits[0] = 0
            if Tlimits[0] == 0:
                Tlimits[1] = 360
            if Tlimits[0] < 0:
                Tlimits[1] = 0

        if Rlimits[0] == Rlimits[1]:
            if Rlimits[0] > 0:
                Rlimits[0] = 0
            if Rlimits[0] == 0:
                Rlimits[1] = 1
            if Rlimits[0] < 0:
                Rlimits[1] = 0

        # draw axis
        axisGroup = ExtensionBaseObj.createGroup(parent, 'PlotData')

        [axisObj, limits, origin] = axis.polar(ExtensionBaseObj, axisGroup, Rlimits, Tlimits, position, rLabel=rLabel, rlog10scale=rlog10scale,
                                               rTicks=rTicks, tTicks=tTicks, rTickStep=rTickStep, tTickStep=tTickStep, rScale=rScale,
                                               rAxisUnitFactor=rExtraText, rGrid=rGrid, tGrid=tGrid, forceTextSize=textSize,
                                               forceLineWidth=lineWidthAxis, drawAxis=drawAxis, ExtraLengthAxisR=ExtraLengthAxisR)

        # scales data and convert to logarithmic scale if needed. Also subtracts the origin point of the axis to move the plot to the correct position
        nPoints = min(len(rData), len(tData))
        xData = []
        yData = []
        if rlog10scale:
            for i in range(nPoints):
                xData.append(math.log10(rData[i]) * math.cos(math.radians(-tData[i])) * rScale)  # negative theta bc inkscape is upside down
                yData.append(math.log10(rData[i]) * math.sin(math.radians(-tData[i])) * rScale)  # negative theta bc inkscape is upside down
        else:
            for i in range(nPoints):
                xData.append(rData[i] * math.cos(math.radians(-tData[i])) * (rScale / rTickStep))  # negative theta bc inkscape is upside down
                yData.append(rData[i] * math.sin(math.radians(-tData[i])) * (rScale / rTickStep))  # negative theta bc inkscape is upside down

        coords = zip(xData, yData)

        inkDraw.line.absCoords(axisGroup, coords, position, lineStyle=lineStylePlot)

        return [axisGroup, limits, origin]

    @staticmethod
    def stem(ExtensionBaseObj, parent, xData, yData, position=[0, 0], xLabel='', yLabel='', ylog10scale=False, xTicks=True, yTicks=True,
             xTickStep=1.0, yTickStep=1.0, xScale=20, yScale=20, xExtraText='', yExtraText='', xGrid=False, yGrid=False, generalAspectFactorAxis=1.0,
             lineStylePlot=inkDraw.lineStyle.setSimpleBlack(), forceXlim=None, forceYlim=None, drawAxis=True, ExtraLengthAxisX=0.0,
             ExtraLengthAxisY=0.0):
        """Create a cartesian stem plot

        .. note:: This method uses LaTeX in labels and tick marks if LaTeX support is enabled. This is an optional feature, **enabled by default**. Please refer to :ref:`disableLatexSupport` on how to disable it.

        :param ExtensionBaseObj: Most of the times you have to pass 'self' when calling from inside your plugin class. See example below
        :param parent: Parent object
        :param xData: List of x data
        :param yData: List of y data
        :param position: Position of the plot. It is defined at the point where x and y axis cross [x0,y0]. The point where the axis cross depend on the limits.

              - If xLimits comprises the origin x=0, then the  Y axis crosses the X axis at x=0.
              - If xLimits contains only negative numbers, then the Y axis crosses the X axis at x_max.
              - If xLimits contains only positive numbers, then the Y axis crosses the X axis at x_min.

              - The same rule applies to y direction.
        :param xLabel: Label of the X axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param yLabel: Label of the Y axis. Default: ''

              The text can contain any LaTeX command. If you want to write mathematical text, you can enclose it between dollar signs $...$. If LaTeX support is disabled, do not use $.

        :param ylog10scale: Sets Y axis to log10 scale if True. Default: False
        :param xTicks: Adds axis ticks to the X axis if True. Default: True
        :param yTicks: Adds axis ticks to the Y axis if True. Default: True
        :param xTickStep: Value interval between two consecutive ticks on X axis. (Not used if X axis is in log10 scale). Default:1.0
        :param yTickStep: Value interval between two consecutive ticks on Y axis. (Not used if Y axis is in log10 scale). Default:1.0
        :param xScale:  Distance between each xTickStep in svg units. Default: 20

               - If axis is linear, then xScale is the size in svg units of each tick
               - If axis is log10, the xScale is the size in svg units of one decade

        :param yScale: Distance between each yTickStep in svg units. Default: 20

               - If axis is linear, then yScale is the size in svg units of each tick
               - If axis is log10, the yScale is the size in svg units of one decade

        :param xExtraText: Extra text to be added to the ticks in X axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.
        :param yExtraText: Extra text to be added to the ticks in Y axis. Default: ''

              This is useful when we want to represent interval with different units. example pi, 2pi 3pi, etc.
              The text can be any LaTeX text. Keep in mind that this text will be inserted within a mathematical environment $...$, therefore no $ is needed here.

        :param xGrid: Adds grid lines to X axis if True. Default: False
        :param yGrid: Adds grid lines to Y axis if True. Default: False
        :param generalAspectFactorAxis: Regulates the general aspect ratio between grid lines, text and Ticks separations. Default: 1.0

        :param lineStylePlot: Line style to be used to plot the data. See class ``inkscapeMadeEasy_Draw.lineStyle``. Default: lineStylePlot=inkDraw.lineStyle.setSimpleBlack()
        :param forceXlim: Forces limits of X axis to these limits. These limits affect the axis only, that is, all xData is plotted despite of these limits.

            - if forceXlim=None Limits will be defined by the limits of xData (Default)
                - if forceXlim=[xMin,xMax] then these limits will be used.

            .. note:: for logarithmic scale, the limits are always adjusted to complete the decade. Usually you don't need this for logarithmic scale

        :param forceYlim: Forces limits of Y axis to these limits. These limits affect the axis only, that is, all yData is plotted despite of these limits.

            - if forceYlim=None Limits will be defined by the limits of yData (Default)
                - if forceYlim=[yMin,yMax] then these limits will be used.

            .. note:: for logarithmic scale, the limits are always adjusted to complete the decade. Usually you don't need this for logarithmic scale

        :param drawAxis: Control flag of the axis method

               - True: draws axis normally
               - False: returns the limits and origin position without drawing the axis itself

        :param ExtraLengthAxisX: Extra length near the arrow pointer of X axis. Default 0.0
        :param ExtraLengthAxisY: Extra length near the arrow pointer of Y axis. Default 0.0

        :type ExtensionBaseObj: inkscapeMadeEasy object
        :type parent: inkscape element object
        :type xData: list
        :type yData: list
        :type position: list
        :type xLabel: string
        :type yLabel: string
        :type ylog10scale: bool
        :type xTicks: bool
        :type yTicks: bool
        :type xTickStep: float
        :type yTickStep: float
        :type xScale: float
        :type yScale: float
        :type xExtraText: string
        :type yExtraText: string
        :type xGrid: bool
        :type yGrid: bool
        :type generalAspectFactorAxis: float
        :type lineStylePlot: lineStyle object
        :type forceXlim: list
        :type forceYlim: list
        :type drawAxis: bool
        :type ExtraLengthAxisX: float
        :type ExtraLengthAxisY: float

        :returns: [GroupPlot, outputLimits, axisOrigin]

            - GroupPlot:  the plot object
            - outputLimits: a list with tuples:[(x_min,xPos_min),(x_max,xPos_max),(y_min,yPos_min),(y_max,yPos_max)]

                  - x_min, x_max, y_min, y_max:               The limits of the axis object
                  - xPos_min, xPos_max, yPos_min, yPos_max:   The positions of the limits of the axis object, considering the scaling and units
                  - axisOrigin [X0,Y0]:                      A list with the coordinates of the point where the axes cross.
        :rtype: list

        .. important:: If any of the axis are log10, then the method ignores any pairs of (x,y) data with invalid coordinates, that is, if xData and/or yData is less than or equal to 0.0 (they would result in complex log10... =P ). The method will create a text object alongside your plot warning this.

        .. note:: If any of the axis are linear, the method will ignore any value greater than 10.000 (in absolute value). This avoids plotting very large numbers. The method will create a text object alongside your plot warning this.

        **Example**

        >>> oot_layer = self.document.getroot()     # retrieves the root layer of the document
        >>> xData=[-1,-0.5,0,0.5,1.0,1.5,2]
        >>> yData=[x*x for x in xData]    # computes y=x*x
        >>>
        >>> # creates a line style with a dot marker for the stem plot
        >>> myMarkerDot=inkDraw.marker.createDotMarker(self,'DotMDiscreteTime',RenameMode=2,scale=0.3,
        >>>                                            strokeColor=inkDraw.color.defined('black'),fillColor=inkDraw.color.defined('red'))
        >>> lineStyleDiscrete = inkDraw.lineStyle.set(lineWidth=1.0, markerEnd=myMarkerDot)
        >>>
        >>> inkPlot.plot.stem(self,root_layer,xData,yData,position=[0,0],
        >>>                   xLabel='my $x$ data',yLabel='$y(x)$',ylog10scale=False,
        >>>                   xTicks=True,yTicks=True,xTickStep=0.5,yTickStep=2.0,
        >>>                   xScale=20,yScale=20,xExtraText='a',yExtraText='',
        >>>                   xGrid=True,yGrid=True,generalAspectFactorAxis=1.0,lineStylePlot=lineStyleDiscrete,
        >>>                   forceXlim=None,forceYlim=None,drawAxis=True)

        The image below present the plot above.

        .. image:: ../imagesDocs/plot_plotStemParameters_01.png
          :width: 400px

        """

        textSize = generalAspectFactorAxis * 0.25 * min(xScale, yScale)
        lineWidthAxis = generalAspectFactorAxis * min(xScale, yScale) / 35.0

        yDataTemp = []
        xDataTemp = []
        flagShowedError = False

        # remove invalid pairs of coordinates for linear plot (larger than +-10k )
        for i in range(len(xData)):
            if abs(xData[i]) <= 1.0e4:
                yDataTemp.append(yData[i])
                xDataTemp.append(xData[i])
            else:
                if not flagShowedError:
                    inkDraw.text.write(ExtensionBaseObj, 'Error: The point (%f,%f)\n is too large. Ignoring it...' % (xData[i], yData[i]),
                                       [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                    inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                       fontSize=textSize / 2.0)
                    flagShowedError = True

        yData = yDataTemp
        xData = xDataTemp

        yDataTemp = []
        xDataTemp = []
        flagShowedError = False
        if ylog10scale:  # remove invalid pairs of coordinates for log plot (less than or equal to 0.0)
            for i in range(len(yData)):
                if yData[i] > 0.0:
                    yDataTemp.append(yData[i])
                    xDataTemp.append(xData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj,
                                           'Error: The point (%f,%f)\n is invalid in logarithmic scale. Ignoring it...' % (xData[i], yData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True
        else:  # remove invalid pairs of coordinates for linear plot (larger than +-10k )
            for i in range(len(yData)):
                if abs(yData[i]) <= 1.0e4:
                    yDataTemp.append(yData[i])
                    xDataTemp.append(xData[i])
                else:
                    if not flagShowedError:
                        inkDraw.text.write(ExtensionBaseObj, 'Error: The point (%f,%f)\n is too large. Ignoring it...' % (xData[i], yData[i]),
                                           [position[0], position[1] + 2 * textSize], parent, fontSize=textSize / 2.0)
                        inkDraw.text.write(ExtensionBaseObj, '       Please check your graph', [position[0], position[1] + 2.5 * textSize], parent,
                                           fontSize=textSize / 2.0)
                        flagShowedError = True

        yData = yDataTemp
        xData = xDataTemp

        if forceXlim:
            Xlimits = forceXlim
        else:
            Xlimits = [min(xData), max(xData)]
        if forceYlim:
            Ylimits = forceYlim
        else:
            Ylimits = [min(yData), max(yData)]  # min<->max inverted  bc inkscape is upside down

        if Ylimits[0] == Ylimits[1]:
            if Ylimits[0] > 0:
                Ylimits[0] = 0
            if Ylimits[0] == 0:
                Ylimits[1] = 1
            if Ylimits[0] < 0:
                Ylimits[1] = 0

        if Xlimits[0] == Xlimits[1]:
            if Xlimits[0] > 0:
                Xlimits[0] = 0
            if Xlimits[0] == 0:
                Xlimits[1] = 1
            if Xlimits[0] < 0:
                Xlimits[1] = 0

        # draw axis
        axisGroup = ExtensionBaseObj.createGroup(parent, 'PlotData')

        [axisObj, limits, origin] = axis.cartesian(ExtensionBaseObj, axisGroup, Xlimits, Ylimits, position, xLabel=xLabel, yLabel=yLabel,
                                                   xlog10scale=False, ylog10scale=ylog10scale, xTicks=xTicks, yTicks=yTicks, xTickStep=xTickStep,
                                                   yTickStep=yTickStep, xScale=xScale, yScale=yScale, xAxisUnitFactor=xExtraText,
                                                   yAxisUnitFactor=yExtraText, xGrid=xGrid, yGrid=yGrid, forceTextSize=textSize,
                                                   forceLineWidth=lineWidthAxis, drawAxis=drawAxis, ExtraLengthAxisX=ExtraLengthAxisX,
                                                   ExtraLengthAxisY=ExtraLengthAxisY)

        # scales data and convert to logarithmic scale if needed. Also subtracts the origin point of the axis to move the plot to the correct position
        xData = [x * (xScale / xTickStep) - origin[0] for x in xData]

        if ylog10scale:
            yData = [-math.log10(y) * yScale - origin[1] for y in yData]
        else:
            yData = [-y * (yScale / yTickStep) - origin[1] for y in yData]  # negative bc inkscape is upside down

        stemGroup = ExtensionBaseObj.createGroup(axisGroup, 'StemGroup')

        for i in range(len(xData)):
            inkDraw.line.relCoords(stemGroup, [[0, yData[i]]], [xData[i] + position[0], 0 + position[1]], lineStyle=lineStylePlot)

        return [axisGroup, limits, origin]
