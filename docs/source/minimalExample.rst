General Gist
============

The general gist of inkscapeMadeEasy is:

1) ``inkscapeMadeEasy_Base.inkscapeMadeEasy`` inherits ``inkex.Effect``, therefore has access to all ``inkex.Effect`` member functions plus all methods defined in ``inkscapeMadeEasy_Base.py``

2) Your extension is a class that inherits ``inkscapeMadeEasy_Base.inkscapeMadeEasy``. Therefore you will have access to all member functions of ``inkscapeMadeEasy_Base.inkscapeMadeEasy`` plus the methods you define in your extension.

3) If you need anything from ``inkscapeMadeEasy_Draw`` or ``inkscapeMadeEasy_Plot``, you can import them into your project.

The basic structure of your plugin should be the following:

.. code-block:: python
   :linenos:

    import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
    import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
    import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot

    class MinimalExample(inkBase.inkscapeMadeEasy):

        def __init__(self):
            inkBase.inkscapeMadeEasy.__init__(self)
            ...
            initialization procedure, argument parser
            ...

        def effect(self):
            ...
            The method 'effect()' is is the only method called directly by inkscape.
            Consider this function to be the main function of your plugin.
            ...

        def fooBar(self):
            ...
            You can create other methods if you want. These can be called by other
            methods inside your plugin but inkscape will NEVER call these directly.
            ...


    if __name__ == '__main__':
        myPlugin = MinimalExample()
        myPlugin.run()


.. note:: The best way of learning how to use it is by looking at real life examples. Check my other `repositories <https://github.com/fsmMLK>`_.


.. _minimalExample:

Minimal example
===============

The following is a minimal inkscape example using inkscapeMadeEasy.


The structure of inkscape extensions directory should be as follows:

.. code-block:: none
    
   inkscape
    ┣━━ extensions
    ┋    ┣━━ inkscapeMadeEasy   <-- folder with inkscapeMadeEasy files
         ┃    ┣━━ inkscapeMadeEasy_Base.py
         ┃    ┣━━ inkscapeMadeEasy_Draw.py
         ┃    ┣━━ inkscapeMadeEasy_Plot.py
         ┃    ┗━━ basicLatexPackages.tex
         ┃
         ┣━━ minimalExample   <-- folder with minimal example files
         ┃    ┣━━ minimalExample.py
         ┃    ┗━━ minimalExample.inx
         ┋


minimalExample.inx
------------------

.. literalinclude:: ../../examples/minimalExample.inx
   :language: xml
   :linenos:
   
minimalExample.py
-----------------

.. literalinclude:: ../../examples/minimalExample.py
   :language: python
   :linenos:
 
testingMinimalExample.py
------------------------

You can even run the plugin without inkscape! Create a .py file in the ``minimalExample`` directory with the contents bellow and run python from the console. 

.. code-block:: python

    python3 path/to/minimalExample/testingMinimalExample.py
    
.. tip:: Why would you want to do this? Debugging your code! Inkscape neither have a stdout for you to dump stuff and inspect nor allow break points. Running independently from inkscape allow you to run via PyCharm or other python IDEs. Use it now and thank me later. =)


.. literalinclude:: ../../examples/testingMinimalExample.py
   :language: python
   :linenos:
   

.. note:: Remember to change the paths of the svg files. ``existing_file.svg`` is one existing file that will be modified by the example. ``new_file.svg`` will be created with the result of the example.
