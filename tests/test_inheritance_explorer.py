import collections

import pydot
import pytest

from inheritance_explorer._testing import ClassForTesting
from inheritance_explorer.inheritance_explorer import ChildNode, ClassGraphTree


@pytest.fixture()
def cgt():
    return ClassGraphTree(ClassForTesting, "use_this_func")


def test_child():
    child_class = ChildNode
    node = ChildNode(child_class, 1)
    assert type(node.child_id) == str
    assert node.parent_id is None


def test_class_graph(cgt):

    # map out the structure of SimilarityContainer, track the run method
    assert cgt._node_list[1].parent_id == "1"
    c = cgt.check_source_similarity()
    assert isinstance(c, collections.OrderedDict)
    assert c[3].similarity_fraction < 1.0

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
    assert cgt._node_list[1].parent_id == "1"


@pytest.mark.parametrize(
    ("kwarg_name", "kwarg_values"),
    [
        ("above_cutoff", (True, False)),
        (
            "colorbar",
            (True, False),
        ),
        ("cmap", ("magma",)),
    ],
)
def test_similarity(cgt, kwarg_name, kwarg_values):

    kwargs = {}
    for value in kwarg_values:
        kwargs[kwarg_name] = value
    _ = cgt.plot_similarity(**kwargs)


def test_interactive(cgt):
    _ = cgt.build_interactive_graph()
    _ = cgt.build_interactive_graph(include_similarity=False)
    _ = cgt.show_graph()
    _ = cgt.show_graph(env=None)
