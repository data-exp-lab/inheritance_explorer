import pytest

from inheritance_explorer._testing import ClassForTesting
from inheritance_explorer._widget_support import _display_code_compare
from inheritance_explorer.inheritance_explorer import ClassGraphTree


@pytest.fixture()
def cgt():
    return ClassGraphTree(ClassForTesting, funcname="use_this_func")


def test_code_comparison_widget_from_cgt(cgt):
    cgt.display_code_comparison()


def test_secret_code_comparison_widget(cgt):
    _display_code_compare(cgt, class_1_name="ClassForTesting4")
    _display_code_compare(cgt, class_2_name="ClassForTesting3")
