import collections
import inspect
import textwrap
from typing import Any, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pydot
from matplotlib.axes import Axes
from matplotlib.colors import rgb2hex
from pyvis.network import Network

from inheritance_explorer.similarity import PycodeSimilarity


class _ChildNode:
    def __init__(
        self,
        child: Any,
        child_id: int,
        parent: Optional[Any] = None,
        parent_id: Optional[int] = None,
        color: Optional[str] = "#000000",
    ):
        self.child = child
        self.child_name = child.__name__
        self._child_id = child_id
        self.parent = parent

        self._parent_id = parent_id
        self.parent_name = None
        if parent:
            self.parent_name = parent.__name__

        self.color = color
        self._extra_info = "comment string"

    @property
    def child_id(self) -> str:
        return str(self._child_id)

    @property
    def parent_id(self) -> str:
        if self._parent_id:
            return str(self._parent_id)
        return


class ClassGraphTree:
    """
    A hierarchical class graph container.

    Parameters
    ----------

    baseclass
        the starting base class to begin mapping from
    funcname: str
        (optional) the name of a function to watch for overrides
    default_color: str
        (optional) the default outline color of nodes, in any graphviz string
    func_override_color: str
        (optional) the outline color of nodes that override funcname, in any
        graphviz string
    max_recursion_level: int
        (optional) the max number of recrusion levels to map to. A value of 0
        will show only the immediate children of the provided class. Default is
        set to 500.
    classes_to_exclude : List[str]
        (optional) a list of class names to exclude from the mapping.

    """

    def __init__(
        self,
        baseclass: Any,
        funcname: Optional[str] = None,
        default_color: Optional[str] = "#000000",
        func_override_color: Optional[str] = "#ff0000",
        similarity_cutoff: Optional[float] = 0.75,
        max_recursion_level: Optional[int] = 500,
        classes_to_exclude: Optional[List[str]] = None,
    ):

        self.baseclass = baseclass
        self.basename: str = baseclass.__name__
        self.funcname = funcname
        self.max_recursion_level = max_recursion_level
        self._nodenum: int = 0
        self._node_list = []  # a list of unique ChildNodes
        self._node_map = {}  # map of global node index to node name
        self._override_src = collections.OrderedDict()
        self._override_src_files = {}
        self._current_node = 1  # the current global node, must start at 1
        self._default_color = default_color
        self._override_color = func_override_color
        self._graphviz_args_kwargs = {}
        self.similarity_container = None
        self.similarity_results = None
        self.similarity_cutoff = similarity_cutoff
        if classes_to_exclude is None:
            classes_to_exclude = []
        self.classes_to_exclude = classes_to_exclude
        self._build()
        self._node_map_r = {v: k for k, v in self._node_map.items()}  # name to index

    def _get_source_info(self, obj) -> Optional[str]:
        f = getattr(obj, self.funcname)
        if isinstance(f, collections.abc.Callable):
            return f"{inspect.getsourcefile(f)}:{inspect.getsourcelines(f)[1]}"
        return None

    def _node_overrides_func(self, child, parent) -> bool:
        childsrc = self._get_source_info(child)
        parentsrc = self._get_source_info(parent)
        if childsrc != parentsrc:
            return True  # it overrides!
        return False

    def _get_new_node_color(self, child, parent) -> str:
        if self.funcname and self._node_overrides_func(child, parent):
            return self._override_color
        return self._default_color

    def _get_baseclass_color(self) -> str:
        color = self._default_color
        if self.funcname:
            f = getattr(self.baseclass, self.funcname)
            class_where_its_defined = f.__qualname__.split(".")[0]
            if self.basename == class_where_its_defined:
                # then its defined here, use the override color
                color = self._override_color
        return color

    def check_subclasses(
        self, parent, parent_id: int, node_i: int, current_recursion_level: int
    ) -> int:
        if current_recursion_level <= self.max_recursion_level:
            for child in parent.__subclasses__():
                if child.__name__ not in self.classes_to_exclude:
                    color = self._get_new_node_color(child, parent)
                    new_node = _ChildNode(
                        child, node_i, parent=parent, parent_id=parent_id, color=color
                    )
                    self._node_list.append(new_node)
                    self._node_map[node_i] = new_node.child_name
                    if self.funcname and self._node_overrides_func(child, parent):
                        self._store_node_func_source(child, node_i)
                    node_i += 1
                    node_i = self.check_subclasses(
                        child, node_i - 1, node_i, current_recursion_level + 1
                    )
        return node_i

    def _store_node_func_source(self, clss, current_node: int):
        # store the source code of funcname for the current class and node
        #    clss:  a class
        #    current_node: the
        f = getattr(clss, self.funcname)
        if isinstance(f, collections.abc.Callable):
            src = textwrap.dedent(inspect.getsource(f))
            self._override_src_files[
                current_node
            ] = f"{inspect.getsourcefile(f)}:{inspect.getsourcelines(f)[1]}"
            self._override_src[current_node] = src

    def check_source_similarity(
        self,
        SimilarityContainer=PycodeSimilarity,
        method="reference",
        reference: Optional[int] = None,
    ):
        # compares all the source code of the child methods that have
        # over-ridden funcname

        if reference is None:
            reference = 1  # use whatever the basenode is

        self.similarity_container = SimilarityContainer(method=method)
        sim = self.similarity_container.run(self._override_src, reference=reference)
        return sim

    def _build(self):

        # construct the first node
        color = self._get_baseclass_color()
        self._node_list.append(
            _ChildNode(self.baseclass, self._current_node, parent=None, color=color)
        )
        self._node_map[self._current_node] = self._node_list[-1].child_name
        if self.funcname:
            self._store_node_func_source(self.baseclass, self._current_node)

        # now check all the children
        self._current_node += 1
        _ = self.check_subclasses(
            self.baseclass, self._current_node - 1, self._current_node, 0
        )

        # construct the full similarity matrix
        s_c = PycodeSimilarity(method="permute")
        _, sim_matrix, sim_axis = s_c.run(self._override_src)
        sim_axis = np.array(sim_axis)
        sim_axis_names = np.array([c.child_name for c in self._node_list])
        self.similarity_results = {
            "matrix": sim_matrix,
            "axis": sim_axis,
            "axis_names": sim_axis_names,
        }

        cutoff_sim = self.similarity_cutoff
        similarity_sets = {}  # a dict that points to other similar nodes
        M = sim_matrix
        for irow in range(M.shape[0]):
            rowvals = M[irow, :]
            indxs = np.where(rowvals >= cutoff_sim)[0]
            indxs = indxs[indxs != irow]  # these are matrix indeces
            node_ids = sim_axis[indxs]
            if len(node_ids) > 0:
                this_child = sim_axis[irow]
                similarity_sets[this_child] = set(node_ids.tolist())
        self.similarity_sets = similarity_sets

    def _build_graph(
        self, *args, include_similarity: bool = True, **kwargs
    ) -> pydot.Dot:
        """
        build a digraph from the current node list

        Parameters
        ----------
        *args:
            any arg accepted by pydot.Dot
        include_similarity: bool
            include edges for similar code (default True)
        **kwargs:
            any additional keyword arguments are passed to graphviz.Digraph(**kwargs)
        """

        gtype = "digraph"
        if "graph_type" in kwargs:
            gtype = kwargs.pop("graph_type")

        dot = pydot.Dot("test_graph", *args, graph_type=gtype, **kwargs)

        iset = 0
        Nsets = len(self.similarity_sets)
        for node in self._node_list:
            new_node = pydot.Node(
                node.child_id, label=node.child_name, color=node.color
            )
            dot.add_node(new_node)
            if node.parent:
                dot.add_edge(pydot.Edge(node.child_id, node.parent_id))
            if include_similarity:
                if int(node.child_id) in self.similarity_sets:
                    R = (iset + 1.0) / Nsets * 0.5 + 0.5
                    G = 0.5
                    B = 0.5
                    hexcolor = rgb2hex((R, G, B))
                    iset += 1
                    for similar_node_id in self.similarity_sets[int(node.child_id)]:
                        new_edge = pydot.Edge(
                            node.child_id, str(similar_node_id), color=hexcolor
                        )
                        dot.add_edge(new_edge)

        return dot

    _graph = None

    # @property
    def graph(self, *args, include_similarity: bool = True, **kwargs) -> pydot.Dot:
        """a GraphViz dot graph of the class hierarchy using pydot"""
        # if self._graph is None:
        self._graph = self._build_graph(
            *args, include_similarity=include_similarity, **kwargs
        )
        return self._graph

    def set_graphviz_args_kwargs(self, *args, **kwargs):
        self._graphviz_args_kwargs = {"args": args, "kwargs": kwargs}

    def show_graph(self, *args, env: str = "notebook", format: str = "png", **kwargs):
        """display a static GraphViz graph"""
        return _show_graph(self.graph(*args, **kwargs), env=env, format=format)

    def plot_similarity(
        self,
        above_cutoff: Optional[bool] = False,
        ax: Optional[Axes] = None,
        colorbar: Optional[bool] = True,
        **kwargs,
    ) -> Tuple[dict, Axes]:
        """
        add the similarity plot to a matplotlib axis (or create a new one)

        Parameters
        ----------
        above_cutoff: bool
            if True (default False), plots where similarity > cutoff
        ax: Axes
            matplotlib axis to add the plot to. A new axis handle will be
            created and returned if this is not set.
        colorbar: bool
            adds a colorbar to ax if True (default)

        kwargs
            any keyword argument accepted by plt.imshow()

        Returns
        -------
        (sim_labels, ax)
            sim_labels: dictionary mapping the matrix indices to label
            ax: the modified (or new) axis handle


        """
        if ax is None:
            _, ax = plt.subplots(1)

        if above_cutoff:
            M = self.similarity_results["matrix"] > self.similarity_cutoff
        else:
            M = self.similarity_results["matrix"]

        if "cmap" not in kwargs:
            if above_cutoff:
                kwargs["cmap"] = "gray"
            else:
                kwargs["cmap"] = "magma"

        im = ax.imshow(M, **kwargs)
        _ = ax.set_xticks(range(M.shape[0]))
        _ = ax.set_yticks(range(M.shape[0]))
        if colorbar:
            plt.colorbar(im, ax=ax)

        sim_labels = [
            self._node_list[cid - 1].child_name for cid in self._override_src.keys()
        ]
        sim_labels = {lid: label for lid, label in enumerate(sim_labels)}
        return sim_labels, ax

    def build_interactive_graph(
        self, include_similarity: bool = True, **kwargs
    ) -> Network:

        """
        build an interactive Network graph from the current node list

        Parameters
        ----------
        *args:
            any arg accepted by pydot.Dot
        include_similarity: bool
            include edges for similar code (default True)
        **kwargs:
            any additional keyword arguments are passed to graphviz.Digraph(**kwargs)

        Returns
        -------
        Network
            the pyvis.Network representation of the class hierarchy.
        """

        grph = nx.Graph(directed=True)

        iset = 0
        for node in self._node_list:
            if node.color == "#000000":
                # no override. show improve this...
                hexcolor = rgb2hex((0.7, 0.7, 0.7))
            else:
                hexcolor = rgb2hex((0.5, 0.5, 1.0))

            if node.parent:
                parent_info = f"({node.parent.__name__})"
            else:
                parent_info = ""
            grph.add_node(
                node.child_id,
                title=f"{node.child_name}{parent_info}",
                color=hexcolor,
            )

            if include_similarity:
                if int(node.child_id) in self.similarity_sets:
                    hexcolor = rgb2hex((0, 0.5, 1.0))
                    iset += 1
                    for similar_node_id in self.similarity_sets[int(node.child_id)]:
                        grph.add_edge(
                            node.child_id,
                            str(similar_node_id),
                            color=hexcolor,
                            physics=False,
                        )

            arrowsop = {"from": {"enabled": True}}
            if node.parent:
                grph.add_edge(
                    node.child_id,
                    node.parent_id,
                    color=rgb2hex((0.7, 0.7, 0.7)),
                    physics=True,
                    arrows=arrowsop,
                )

        # return the interactive pyvis Network graph
        network_wrapper = Network(notebook=True, **kwargs)
        network_wrapper.from_nx(grph)
        return network_wrapper

    def get_source_code(self, node: Union[str, int]) -> str:
        """
        retrieve the source code of the comparison function for a
        specified node

        Parameters
        ----------
        node: Union[str, int]
        the node to fetch the source code for

        Returns
        -------
        str
        a string containing the source code for the node.
        """
        if node in self._override_src:
            return self._override_src[node]
        elif isinstance(node, str) and node in self._node_map_r:
            node_id = self._node_map_r[node]
            if node_id in self._override_src:
                return self._override_src[node_id]
            else:
                raise ValueError(
                    f"node {node} does not override the " f"chosen function."
                )
        raise KeyError(f"Could not find node for {node}")

    def get_multiple_source_code(self, node_1: Union[str, int], *args) -> dict:
        """
        Retrieve the source code for multiple nodes

        Parameters
        ----------
        node_1: Union[str, int]
        the first node to fetch
        *args: Union[str, int]
        any additional nodes to fetch

        Returns
        -------
        dict
        dictionary where the node is the key and the source code the value.
        """
        src_dict = {}
        src_dict[node_1] = self.get_source_code(node_1)
        for src_key in args:
            src_dict[src_key] = self.get_source_code(src_key)
        return src_dict

    def display_code_comparison(self):
        """
        show the code comparison widget
        """

        # add a check that we are running from a notebook?
        if self.funcname is not None:
            from inheritance_explorer._widget_support import display_code_compare

            display_code_compare(self)


def _show_graph(dot_graph: pydot.Dot, format: str = "svg", env: str = "notebook"):
    # return a GraphViz dot graph in a jupyter-friendly format.
    create_func = getattr(dot_graph, f"create_{format}")
    graph = create_func()

    if env == "notebook":
        if format == "svg":
            from IPython.core.display import SVG

            return SVG(graph)
        else:
            from IPython.core.display import Image

            return Image(graph, unconfined=True)

    return graph
