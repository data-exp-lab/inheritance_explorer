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
    source = ipywidgets.Output(layout=ipywidgets.Layout(width="100%", height="50em"))

    def update_source(event):
        class_1 = class_dropdown_1.value
        class_2 = class_dropdown_2.value
        funcsource_string = ""

        for class_i in (class_1, class_2):
            node_id = cgt._node_map_r[class_i]
            src_id, rawsrc = find_closest_source(cgt, node_id)

            this_src = f"\n\n## {class_i}.{cgt.funcname}"
            if src_id is None:
                this_src += ": could not find source code."
            elif src_id != node_id:
                definining_class = cgt._node_map[src_id]
                this_src += f" defined in {definining_class}:"

            this_src = (
                this_src + "\n\n```python\n" + textwrap.dedent(rawsrc) + "\n\n```"
            )
            funcsource_string += this_src

        source.clear_output()
        with source:
            display(Markdown(data=funcsource_string))

    class_dropdown_1.observe(update_source, ["value"])
    class_dropdown_2.observe(update_source, ["value"])
    update_source(None)

    if class_1_name is not None:
        class_dropdown_1.value = class_1_name

    if class_2_name is not None:
        class_dropdown_1.value = class_2_name

    display(ipywidgets.VBox([class_dropdown_1, class_dropdown_2, defined_at, source]))
