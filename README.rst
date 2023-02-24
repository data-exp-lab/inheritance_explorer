====================
inheritance_explorer
====================


.. image:: https://img.shields.io/pypi/v/inheritance_explorer.svg
        :target: https://pypi.python.org/pypi/inheritance_explorer

.. image:: https://github.com/data-exp-lab/inheritance_explorer/actions/workflows/run-tests.yml/badge.svg
        :target: https://github.com/data-exp-lab/inheritance_explorer/actions/workflows/run-tests.yml
        :alt: Testing Status

.. image:: https://readthedocs.org/projects/inheritance-explorer/badge/?version=latest
        :target: https://inheritance-explorer.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/data-exp-lab/inheritance_explorer/branch/main/graph/badge.svg?token=EvmlPg5X1O
        :target: https://codecov.io/gh/data-exp-lab/inheritance_explorer
        :alt: Current Coverage



The ``inheritance_explorer`` is an open source python package for inspecting
other packages. In particular, it focuses on class inheritance structures, allowing
you to produce graphs that recursively map out child classes from a given
starting class. There are a number of useful applications: from learning structures
of unfamiliar code bases to identifying duplicate code.

.. image:: https://github.com/data-exp-lab/inheritance_explorer/raw/main/docs/resources/interactive_yt_ds_parse_param.gif

Useful links: `github repository <https://github.com/data-exp-lab/inheritance_explorer>`_, `full documentation <https://inheritance-explorer.readthedocs.io/en/latest/>`_

Installation
------------

To install the latest release into your current active environment:

.. code-block:: bash

    $ pip install inheritance_explorer

If you want to produce static images of any graphs, you'll also need to
install ``graphviz`` following the instructions at
`https://graphviz.org/download/ <https://graphviz.org/download/>`_. ``graphviz``
is not needed for the interactive plotting and similarity calculations (see
Quick Start below).

Quick Start
-----------

Basic class mapping
+++++++++++++++++++

The primary function of the ``inheritance_explorer`` is to trace out the class
inheritance starting from a single parent class and recursively traversing all
child classes. To get started, initialize a `ClassGraphTree` with the starting
class:

.. code-block:: python

    from matplotlib.axes import Axes
    from inheritance_explorer import ClassGraphTree

    base_class = Axes # the starting class to map from
    cgt = ClassGraphTree(base_class) # traces an inheritance tree

From here, there are a number of ways to visualize the inheritance graph.

From a jupyter notebook, you can construct a ``pyvis`` interactive network graph
 with:

.. code-block:: python

    graph = cgt.build_interactive_graph(width="1200px",
                                        height="1200px",
                                        bgcolor='#222222',
                                        font_color='white')
    graph.show('_tmp.html') # render the pyvis interactive graph

If you have ``graphviz`` installed, you can also render a static graph either to
 display in a jupyter notebook or save to file. To display in a notebook:

.. code-block:: python

    cgt.show_graph()

To save a file, you can access the underlying `graph` object directly:

.. code-block:: python

    cgt.graph.write('matplotlib_Axes.png')

Function tracking
+++++++++++++++++

The ``ClassGraphTree`` can also track a selected function of a class during traversal.
When a child class overrides the function, the source code is stored. To use this
functionality, use the ``funcname`` keyword argument to provide the function name
as a string:

.. code-block:: python

    from matplotlib.axes import Axes
    from inheritance_explorer import ClassGraphTree

    base_class = Axes # the starting class to map from
    cgt = ClassGraphTree(base_class, funcname='clear')

By default, after the traversal completes, the different versions of the function
that is tracked will be run through a code-similarity calculation. Cases where the
similarity fraction is above a cutoff value (default of .75), the two nodes will be
connected on the resulting graph:

.. image:: https://github.com/data-exp-lab/inheritance_explorer/raw/main/docs/resources/mpl_axesclear.png

Additionally, you can inspect the source code itself for any of the classes that
define it using ``cgt.get_source_code(class_name)``. If in a jupyter notebook,
you can view it with syntax highlighting with

.. code-block:: python

    from IPython.display import Code
    Code(cgt.get_source_code('PolarAxes'), language="python")

For a complete description of the code similarity calculation and how to
modify it, check out the full documentation.

Command line usage
++++++++++++++++++

``inheritance_explorer`` provides some command line functionality, check the
`full documentation <https://inheritance-explorer.readthedocs.io/en/latest/>`_ for details.
