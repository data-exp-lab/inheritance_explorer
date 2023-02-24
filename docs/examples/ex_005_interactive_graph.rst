Interactive Class Graph
=======================

The ``inheritance_explorer`` relies on ``pyvis`` to construct interactive
graphs. Given an existing ``ClassGraphTree``::

    from yt.data_objects.static_output import Dataset
    from inheritance_explorer import ClassGraphTree

    cgt = ClassGraphTree(Dataset, funcname='_parse_parameter_file')

You can construct an interactive graph by first building it, then calling ``show``
with a filename to use for the temporary ``.html`` required for rendering::

    graph = cgt.build_interactive_graph(width="500px",
                                    height="500px",
                                    bgcolor='#222222',
                                    font_color='white') # constructs a pyvis interactive graph
    graph.show('_tmp.html')

The following screen capture shows the interactive graph in action:

.. image:: /resources/interactive_yt_ds_parse_param.gif
    :width: 500

Note that in this image, the purple nodes are classes that override the function
that was passed in for tracking (``funcname='_parse_parameter_file'``) while blue
lines connect nodes for which the source code of the overriding function is similar.
