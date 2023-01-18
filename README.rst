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


A tool for exploring complex inheritance patters in python code. 

.. image:: https://raw.githubusercontent.com/chrishavlin/inheritance_explorer/main/docs/resources/tree_shot.png
        

Installation
------------

not released (yet?), so install from source (fork/clone locally, `pip install .`). 

For some functionality, the `graphviz <https://graphviz.org/>`_ package needs to be installed separately. TO DO: add install instructions, note which parts of the code require it. 


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
