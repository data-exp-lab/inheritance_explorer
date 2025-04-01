import collections

import pydot
import pytest

from inheritance_explorer._testing import ClassForTesting
from inheritance_explorer.inheritance_explorer import (
    ClassGraphTree,
    _ChildNode,
    _validate_color,
)


@pytest.fixture()
def cgt():
    return ClassGraphTree(ClassForTesting, "use_this_func")


def test_child():
    child_class = _ChildNode
    node = _ChildNode(child_class, 1)
    assert isinstance(node.child_id, str)
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

    with pytest.raises(ValueError, match="does not override the chosen"):
        _ = cgt.get_source_code(cgt._node_map_r["ClassForTesting3"])

    with pytest.raises(ValueError, match="Could not find node"):
        _ = cgt.get_source_code(10)

    with pytest.raises(ValueError, match="Could not find node"):
        _ = cgt.get_source_code("does_not_exist")


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
    src_dict_2 = cgt.get_multiple_source_code(src_dict_nodes[0], *src_dict_nodes[1:])
    assert len(src_dict_2) == len(test_classes)

    with pytest.raises(ValueError, match="does not override the chosen"):
        _ = cgt.get_multiple_source_code("ClassForTesting", "ClassForTesting3")

    with pytest.raises(ValueError, match="Could not find node"):
        _ = cgt.get_multiple_source_code(0, 10)


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


def test_interactive_styles(cgt):
    node_style = {"size": 20.0, "color": "magenta"}
    edge_style = {"weight": 5}
    sim_style = {"color": (0.5, 1.0, 1.0), "weight": 5}
    _ = cgt.build_interactive_graph(
        width="500px",
        height="500px",
        bgcolor=(0.98, 0.98, 0.98),
        font_color="black",
        node_style=node_style,
        edge_style=edge_style,
        similarity_edge_style=sim_style,
        override_node_color="black",
        cdn_resources="in_line",
    )


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


def test_errors_no_source_override():
    # _get_source_info
    cgt = ClassGraphTree(ClassForTesting)
    with pytest.raises(
        RuntimeError, match="this functionality requires function tracking."
    ):
        _ = cgt._get_source_info(ClassForTesting)

    with pytest.raises(
        RuntimeError, match="this functionality requires function tracking."
    ):
        cgt._store_node_func_source(ClassForTesting, 0)

    cgt = ClassGraphTree(ClassForTesting, funcname="use_this_func")
    # monkey patch the funcname to make the callable fail
    cgt.funcname = "misc_attr"
    result = cgt._get_source_info(ClassForTesting)
    assert result is None


def test_missing_source_node(cgt):
    with pytest.raises(ValueError, match="Could not find node for not_a_node"):
        cgt.get_source_code("not_a_node")


def test_class_graph_special_cases(cgt):

    # map out the structure of SimilarityContainer, track the run method
    assert cgt._node_list[1].parent_id == "1"
    with pytest.raises(
        ValueError, match="unexpected value, similarity_container_class"
    ):
        _ = cgt.check_source_similarity(similarity_container_class="not_a_thing")

    cgt.check_source_similarity(reference=1)


def test_set_graphviz_args(cgt):

    cgt.set_graphviz_args_kwargs(1, 2, 3, other_arg="hello", another=True)

    d = cgt._graphviz_args_kwargs
    assert all([val in d["args"] for val in (1, 2, 3)])
    assert "other_arg" in d["kwargs"]
    assert d["kwargs"]["other_arg"] == "hello"
    assert "another" in d["kwargs"]
    assert d["kwargs"]["another"] is True


@pytest.mark.parametrize(
    "input_clr,expected",
    [((0.0, 0.0, 0.0), "#000000"), (None, "#ffffff"), ("#000000", "#000000")],
)
def test_validate_color(input_clr, expected):
    default_clr = (1.0, 1.0, 1.0)

    assert _validate_color(input_clr, default_rgb_tuple=default_clr) == expected


def test_validate_color_invalid():
    with pytest.raises(TypeError, match="clr has unexpected type"):
        _validate_color(100, (1.0, 1.0, 1.0))
