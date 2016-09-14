#!/usr/bin/python

import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw


class myExtension(inkBase.inkscapeMadeEasy):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--tab", action="store", type="string", dest="tab", default="object")
        self.OptionParser.add_option("--myColorPicker", action="store", type="string", dest="myColorPickerVar", default='0')
        self.OptionParser.add_option("--myColorOption", action="store", type="string", dest="myColorOptionVar", default='0')

    def effect(self):
        color, alpha = inkDraw.color.colorPickerToRGBalpha(self.options.myColorPickerVar)

        # do the same thing, but first verify whether myColorOptionVar is providing a pre defined color or asking to get it from the picker.
        color, alpha = inkDraw.color.parseColorPicker(self.options.myColorOptionVar, self.options.myColorPickerVar)


if __name__ == '__main__':
    x = myExtension()
    x.affect()
