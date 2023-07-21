import textwrap
from typing import Optional

import ipywidgets
from IPython.display import Markdown, display

from inheritance_explorer import ClassGraphTree


def find_closest_source(cgt: ClassGraphTree, node_id: int):
    # recursive backwards walk to find a node that overrides the source
    if node_id in cgt._override_src:
        # it overrides, get the source
        return node_id, cgt.get_source_code(node_id)
    else:
        # check parent
        current_node = cgt._node_list[node_id - 1]
        if current_node.parent_id is None:
            return None, None
        else:
            return find_closest_source(cgt, int(current_node.parent_id))


# it does not, get base class source


def display_code_compare(cgt: ClassGraphTree):
    _display_code_compare(cgt)


def _display_code_compare(
    cgt: ClassGraphTree,
    class_1_name: Optional[str] = None,
    class_2_name: Optional[str] = None,
):
    names_classes = [i.child_name for i in cgt._node_list]
    names_classes.sort()

    class_dropdown_1 = ipywidgets.Dropdown(options=names_classes.copy())
    class_dropdown_2 = ipywidgets.Dropdown(options=names_classes.copy())

    defined_at = ipywidgets.HTML()
    source_1 = ipywidgets.Output(layout=ipywidgets.Layout(width="100%", height="50em"))
    source_2 = ipywidgets.Output(layout=ipywidgets.Layout(width="100%", height="50em"))

    def _get_source(class_i) -> str:
        node_id = cgt._node_map_r[class_i]
        src_id, rawsrc = find_closest_source(cgt, node_id)

        this_src = f"\n\n## {class_i}.{cgt.funcname}"
        if src_id is None:
            this_src += ": could not find source code."
        elif src_id != node_id:
            definining_class = cgt._node_map[src_id]
            this_src += f" defined in {definining_class}:"

        this_src = this_src + "\n\n```python\n" + textwrap.dedent(rawsrc) + "\n\n```"
        return this_src

    def update_source_1(event):
        class_1 = class_dropdown_1.value
        this_src = _get_source(class_1)
        source_1.clear_output()
        with source_1:
            display(Markdown(data=this_src))

    def update_source_2(event):
        class_2 = class_dropdown_2.value
        this_src = _get_source(class_2)
        source_2.clear_output()
        with source_2:
            display(Markdown(data=this_src))

    class_dropdown_1.observe(update_source_1, ["value"])
    class_dropdown_2.observe(update_source_2, ["value"])
    update_source_1(None)
    update_source_2(None)

    if class_1_name is not None:
        class_dropdown_1.value = class_1_name

    if class_2_name is not None:
        class_dropdown_1.value = class_2_name

    display(
        ipywidgets.HBox(
            [
                ipywidgets.VBox([class_dropdown_1, source_1]),
                ipywidgets.VBox([class_dropdown_2, source_2]),
                defined_at,
            ]
        )
    )
