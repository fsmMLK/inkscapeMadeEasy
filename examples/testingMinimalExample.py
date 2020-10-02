#!/usr/bin/python
import os

import minimalExample as myExtension

#loads the extension
myExt = myExtension.MinimalExample()

#runs
myExt.run([r'--drawCircle=True', r'--drawPlot=True', r'/path/to/existing_file.svg'], output=os.devnull)

#save the result
myExt.document.write('/path/to/new_file.svg')
