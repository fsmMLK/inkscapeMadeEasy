#!/usr/bin/python
import os

import minimalExample as myExtension

#loads the extension
myExt = myExtension.MinimalExample()

#runs the plugin. Remember to change the paths of the svg files.
# ``existing_file.svg`` is one existing file that will be modified by the example.
# ``new_file.svg`` will be created with the result of the example.
myExt.run([r'--drawCircle=True', r'--drawPlot=True', r'/path/to/existing_file.svg'], output=os.devnull)

#save the result
myExt.document.write('/path/to/new_file.svg')
