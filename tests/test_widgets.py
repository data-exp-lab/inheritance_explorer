import pytest

from inheritance_explorer._testing import ClassForTesting
from inheritance_explorer.inheritance_explorer import ClassGraphTree


@pytest.fixture()
def cgt():
    return ClassGraphTree(ClassForTesting, funcname="use_this_func")


def test_code_comparison_widget(cgt):
    cgt.display_code_comparison()
