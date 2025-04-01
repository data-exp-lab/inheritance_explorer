import pytest

from inheritance_explorer._testing import ClassForTesting
from inheritance_explorer._widget_support import _display_code_compare, _get_class_names
from inheritance_explorer.inheritance_explorer import ClassGraphTree


@pytest.fixture()
def cgt():
    return ClassGraphTree(ClassForTesting, funcname="use_this_func")


def test_code_comparison_widget_from_cgt(cgt):
    cgt.display_code_comparison()


def test_secret_code_comparison_widget(cgt):
    _display_code_compare(cgt, class_1_name="ClassForTesting4")
    _display_code_compare(
        cgt, class_2_name="ClassForTesting3", include_overrides_only=False
    )


def test_get_class_names(cgt):

    cnames_all = _get_class_names(cgt, include_overrides_only=False)
    assert len(cnames_all) == len(cgt._node_list)

    cnames_override = _get_class_names(cgt, include_overrides_only=True)
    assert len(cnames_override) < len(cgt._node_list)
    assert len(cnames_override) == len(cgt._override_src)
