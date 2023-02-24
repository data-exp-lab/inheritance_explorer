Code Comparison Widget
======================

The ``inheritance_explorer.ClassGraphTree`` includes a code comparison widget for
displaying code of the function that is tracked during the recursive class tracking
from within a Jupyter notebook.

To use it, simply construct a ``ClassGraphTree`` with a function to track then
call ``display_code_comparison()``.

For example, the following maps the child classes of the primary ``Dataset``
class in ``yt`` and tracks the ``_is_valid`` function, which is a required function
for all children classes::

    from inheritance_explorer import ClassGraphTree
    import yt
    base_class = yt.data_objects.static_output.Dataset
    cgt = ClassGraphTree(base_class, funcname="_is_valid")

The following screenshot shows the code comparison widget in a Jupyter notebook:

.. image:: /resources/inherit_code_widget.gif
    :width: 800

