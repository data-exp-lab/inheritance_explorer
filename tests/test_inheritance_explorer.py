from inheritance_explorer.inheritance_explorer import ChildNode, ClassGraphTree
from inheritance_explorer.similarity import PycodeSimilarity
from inheritance_explorer._testing import ClassForTesting


def test_child():
    child_class = ChildNode
    node = ChildNode(child_class, 1)
    assert(type(node.child_id) == str)


def test_class_graph():

    # map out the structure of SimilarityContainer, track the run method
    cgt = ClassGraphTree(ClassForTesting, "use_this_func")
    assert(cgt._node_list[1].parent_id == "1")
    c = cgt.check_source_similarity()
    assert(isinstance(c, PycodeSimilarity))
    assert(c.results._3.similarity_fraction < 1.0)
