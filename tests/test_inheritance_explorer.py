from inheritance_explorer.inheritance_explorer import ChildNode, ClassGraphTree
from inheritance_explorer._testing import ClassForTesting
import collections
import pydot

def test_child():
    child_class = ChildNode
    node = ChildNode(child_class, 1)
    assert(type(node.child_id) == str)


def test_class_graph():

    # map out the structure of SimilarityContainer, track the run method
    cgt = ClassGraphTree(ClassForTesting, "use_this_func")
    assert(cgt._node_list[1].parent_id == "1")
    c = cgt.check_source_similarity()
    assert(isinstance(c, collections.OrderedDict))
    assert(c[3].similarity_fraction < 1.0)

    # make sure the graph builds
    for in_sim in [True, False]:
        cgt = ClassGraphTree(ClassForTesting, "use_this_func")
        cgt.build_graph(include_similarity=in_sim)
        assert isinstance(cgt.graph, pydot.Dot)
    cgt = ClassGraphTree(ClassForTesting, "use_this_func")
    cgt.build_graph(graph_type="graph")
    assert isinstance(cgt.graph, pydot.Dot)


def test_class_graph_no_function():
    cgt = ClassGraphTree(ClassForTesting)
    assert (cgt._node_list[1].parent_id == "1")
