Code Comparison Widget
======================

The ``inheritance_explorer.ClassGraphTree`` includes a code comparison widget for
displaying code of the function that is tracked during the recursive class tracking
from within a Jupyter notebook.

To use it, simply construct a ``ClassGraphTree`` with a function to track then
call ``display_code_comparison()``.

For example, the following maps the child classes of the ``BaseParticleIOHandler``
class in ``yt`` and tracks the ``_read_particle_fields`` function, which is implemented across
a large number of subclasses::

    from inheritance_explorer import ClassGraphTree
    import yt
    base_class = yt.utilities.io_handler.BaseParticleIOHandler
    cgt = ClassGraphTree(base_class, funcname="_read_particle_fields")
    cgt.display_code_comparison()

The following screenshot shows the code comparison widget in a Jupyter notebook:

.. image:: /resources/inherit_code_widget.gif
    :width: 800

