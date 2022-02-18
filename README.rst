====================
inheritance_explorer
====================


.. image:: https://img.shields.io/pypi/v/inheritance_explorer.svg
        :target: https://pypi.python.org/pypi/inheritance_explorer

.. image:: https://img.shields.io/travis/chrishavlin/inheritance_explorer.svg
        :target: https://travis-ci.com/chrishavlin/inheritance_explorer

.. image:: https://readthedocs.org/projects/inheritance-explorer/badge/?version=latest
        :target: https://inheritance-explorer.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


A tool for exploring complex inheritance patters in python code. 

Installation
------------

not released (yet?), so install from source (fork/clone locally, `pip install .`). 

Usage
-----

From a jupyter notebook:

.. code-block:: python

    import yt  # or another package
    from inheritance_explorer import ClassGraphTree

    base_class = yt.data_objects.static_output.Dataset # the starting class to map from
    fname = "_parse_parameter_file"  # the method to observe along the way

    cgt = ClassGraphTree(base_class, funcname=fname) # traces an inheritance tree
    graph = cgt.build_interactive_graph(width="1200px", 
                                        height="1200px", 
                                        bgcolor='#222222', 
                                        font_color='white') # constructs a pyvis interactive graph
    graph.show('_tmp.html')  # render the pyvis interactive graph here!



Example notebook `here
<https://github.com/chrishavlin/yt_scratch/blob/master/notebooks/inheritance_explorer_yt.ipynb/>`_



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
