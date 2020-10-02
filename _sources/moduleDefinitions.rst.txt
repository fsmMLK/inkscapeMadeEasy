inkscapeMadeEasy_Base
=====================

Base class for extensions.

This class extends the inkex.Effect class by adding several basic functions to help manipulating inkscape elements. All extensions should inherit this class.

.. Important:: Unless explicitly mentioned, all the code snippet  presented in this section assume you are using inkscapeMadeEasy as presented in the :ref:`minimalExample` section and your are within the scope of your extension class and, therefore, can use ``self.[SOME_FUNCTION]``.

.. note:: in all examples, assume inkscapeMadeEasy modules are imported with the following aliases

    .. code-block:: python
        :linenos:
        
        import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
        import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
        import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot

.. automodule:: inkscapeMadeEasy_Base
    :members:
    :undoc-members:
    :show-inheritance:


inkscapeMadeEasy_Draw
=====================

This module contains classes and functions to help dealing with drawings.

.. Important:: Unless explicitly mentioned, all the code snippet presented in this section assume you are using inkscapeMadeEasy as presented in the :ref:`minimalExample` section and your are within the scope of your extension class and, therefore, can use ``self.[SOME_FUNCTION]``.

.. note:: in all examples, assume inkscapeMadeEasy modules are imported with the following aliases

    .. code-block:: python
        :linenos:

        import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
        import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
        import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot

.. automodule:: inkscapeMadeEasy_Draw
    :members:
    :undoc-members:
    :show-inheritance:

inkscapeMadeEasy_Plot
=====================

This module contains classes and functions to create plots

.. Important:: Unless explicitly mentioned, all the code snippet presented in this section assume you are using inkscapeMadeEasy as presented in the :ref:`minimalExample` section and your are within the scope of your extension class and, therefore, can use ``self.[SOME_FUNCTION]``.

.. note:: in all examples, assume inkscapeMadeEasy modules are imported with the following aliases

    .. code-block:: python
        :linenos:

        import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
        import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
        import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot

.. automodule:: inkscapeMadeEasy_Plot
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: generateListOfTicksLinear,generateListOfTicksLog10,findOrigin,getPositionAndText
