"""Main module."""
from typing import Any, Optional
import collections
import inspect
from graphviz import Digraph
from typing import Optional, Any
import textwrap
from inheritance_explorer.similarity import PycodeSimilarity
import numpy as np
from matplotlib.colors import rgb2hex

class ChildNode:
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
    def __init__(
        self,
        baseclass: Any,
        funcname: Optional[str] = None,
        default_color: Optional[str] = "#000000",
        func_override_color: Optional[str] = "#ff0000",
        similarity_cutoff: Optional[float] = 0.75,
    ):
        """
        baseclass:
            the starting base class to begin mapping from
        funcname:
            the name of a function to watch for overrides
        default_color: t
            he default outline color of nodes, in any graphviz string
        func_override_color:
            the outline color of nodes that override funcname, in any graphviz string
        """
        self.baseclass = baseclass
        self.basename: str = baseclass.__name__
        self.funcname = funcname

        self._nodenum: int = 0
        self._node_list = []  # a list of unique ChildNodes
        self._override_src = collections.OrderedDict()
        self._override_src_files = {}
        self._current_node = 1  # the current global node, must start at 1
        self._default_color = default_color
        self._override_color = func_override_color
        self.similarity_container = None
        self.similarity_results = None
        self.similarity_cutoff = similarity_cutoff
        self.build()

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

    def check_subclasses(self, parent, parent_id: int, node_i: int) -> int:
        for child in parent.__subclasses__():
            color = self._get_new_node_color(child, parent)
            new_node = ChildNode(
                child, node_i, parent=parent, parent_id=parent_id, color=color
            )
            self._node_list.append(new_node)
            if self.funcname and self._node_overrides_func(child, parent):
                self._store_node_func_source(child, node_i)
            node_i += 1
            node_i = self.check_subclasses(child, node_i - 1, node_i)
        return node_i

    def _store_node_func_source(self, clss, current_node: int):
        # store the source code of funcname for the current class and node
        #    clss:  a class
        #    current_node: the
        f = getattr(clss, self.funcname)
        if isinstance(f, collections.abc.Callable):
            src = textwrap.dedent(inspect.getsource(f))
            self._override_src_files[current_node] = f"{inspect.getsourcefile(f)}:{inspect.getsourcelines(f)[1]}"
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

    def build(self):

        # construct the first node
        color = self._get_baseclass_color()
        self._node_list.append(
            ChildNode(self.baseclass, self._current_node, parent=None, color=color)
        )
        self._store_node_func_source(self.baseclass, self._current_node)

        # now check all the children
        self._current_node += 1
        _ = self.check_subclasses(
            self.baseclass, self._current_node - 1, self._current_node
        )

        # construct the full similarity matrix
        s_c = PycodeSimilarity(method="permute")
        _, sim_matrix, sim_axis = s_c.run(self._override_src)
        sim_axis = np.array(sim_axis)
        sim_axis_names = np.array([c.child_name for c in self._node_list])
        self.similarity_results = {'matrix': sim_matrix,
                                   'axis': sim_axis,
                                   'axis_names': sim_axis_names}


        cutoff_sim = self.similarity_cutoff
        similarity_sets = {}  # a dict that points to other similar nodes
        M = sim_matrix
        for irow in range(M.shape[0]):
            rowvals = M[irow, :]
            indxs = np.where(rowvals >= cutoff_sim)[0]
            indxs = indxs[indxs != irow] # these are matrix indeces
            node_ids = sim_axis[indxs]
            if len(node_ids) > 0:
                this_child = sim_axis[irow]
                similarity_sets[this_child] = set(node_ids.tolist())
        self.similarity_sets = similarity_sets


    def digraph(self, include_similarity=False, **kwargs):
        """
        build a graphviz Digraph from the current node list

        **kwargs:
            any additional keyword arguments are passed to graphviz.Digraph(**kwargs)
        """
        dot = Digraph(**kwargs)
        # finally build the graph
        iset = 0
        Nsets = len(self.similarity_sets)
        for node in self._node_list:
            dot.node(
                node.child_id,
                label=node.child_name,
                color=node.color,
                comment=node._extra_info,
            )
            if node.parent:
                dot.edge(node.child_id, node.parent_id)
            if include_similarity:
                if int(node.child_id) in self.similarity_sets:
                    R = (iset+1.0) / Nsets * 0.5 + 0.5
                    G = 0.5
                    B = 0.5
                    hexcolor = rgb2hex((R, G, B))
                    iset += 1
                    for similar_node_id in self.similarity_sets[int(node.child_id)]:
                        dot.edge(node.child_id, str(similar_node_id), color=hexcolor)
        return dot
