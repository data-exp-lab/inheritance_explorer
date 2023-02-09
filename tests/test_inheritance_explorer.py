import collections

import pydot
import pytest

from inheritance_explorer._testing import ClassForTesting
from inheritance_explorer.inheritance_explorer import ClassGraphTree, _ChildNode


@pytest.fixture()
def cgt():
    return ClassGraphTree(ClassForTesting, "use_this_func")


def test_child():
    child_class = _ChildNode
    node = _ChildNode(child_class, 1)
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
        cgraph = cgt.graph(include_similarity=in_sim)
        assert isinstance(cgraph, pydot.Dot)
    cgt = ClassGraphTree(ClassForTesting, "use_this_func")
    assert isinstance(cgt.graph(graph_type="graph"), pydot.Dot)

    # try some graphviz keywords, just make sure they dont error:
    _ = cgt.graph(ratio="fill", size="16,10!")


def test_class_graph_no_function():
    cgt = ClassGraphTree(ClassForTesting)
    assert cgt._node_list[1].parent_id == "1"


def test_source_code_return():
    cgt = ClassGraphTree(ClassForTesting, funcname="use_this_func")

    for node in ["ClassForTesting", "ClassForTesting2", "ClassForTesting4"]:
        assert isinstance(cgt.get_source_code(node), str)

        node_id = cgt._node_map_r[node]
        assert isinstance(cgt.get_source_code(node_id), str)

    with pytest.raises(ValueError, match="does not override the chosen"):
        _ = cgt.get_source_code("ClassForTesting3")
        _ = cgt.get_source_code(cgt._node_map_r["ClassForTesting3"])

    with pytest.raises(KeyError, match="Could not find node"):
        _ = cgt.get_source_code(10)


def test_multi_source_code():
    cgt = ClassGraphTree(ClassForTesting, funcname="use_this_func")

    test_classes = ["ClassForTesting", "ClassForTesting2", "ClassForTesting4"]
    src_dict = cgt.get_multiple_source_code(
        test_classes[0], test_classes[1], test_classes[2]
    )
    assert len(src_dict) == len(test_classes)
    for src_key in test_classes:
        assert src_key in src_dict

    src_dict_nodes = [cgt._node_map_r[c] for c in test_classes]
    src_dict = cgt.get_multiple_source_code(src_dict_nodes[0], *src_dict_nodes[1:])
    assert len(src_dict) == len(test_classes)

    with pytest.raises(ValueError, match="does not override the chosen"):
        _ = cgt.get_multiple_source_code("ClassForTesting", "ClassForTesting3")

    with pytest.raises(KeyError, match="Could not find node"):
        _ = cgt.get_multiple_source_code("ClassForTesting", 10)


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


@pytest.mark.parametrize("max_recursion_level", (0, 1))
def test_recursion_level(max_recursion_level):
    cgt = ClassGraphTree(
        ClassForTesting, "use_this_func", max_recursion_level=max_recursion_level
    )
    n_nodes = len(cgt._node_list)
    assert n_nodes == 3 + max_recursion_level


def test_class_exclusion():
    cgt = ClassGraphTree(
        ClassForTesting,
        "use_this_func",
        classes_to_exclude=["ClassForTesting2"],
    )
    for node in cgt._node_list:
        assert node.child_name != "ClassForTesting2"
