import textwrap

import ipywidgets
from IPython.display import Markdown, display


def display_code_compare(cgt):
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
            rawsrc = cgt.get_source_code(node_id)

            this_src = (
                f"\n\n## {class_i}.{cgt.funcname}\n\n```python\n"
                + textwrap.dedent(rawsrc)
                + "\n\n```"
            )
            funcsource_string += this_src

        source.clear_output()
        with source:
            display(Markdown(data=funcsource_string))

    class_dropdown_1.observe(update_source, ["value"])
    class_dropdown_2.observe(update_source, ["value"])
    update_source(None)
    display(ipywidgets.VBox([class_dropdown_1, class_dropdown_2, defined_at, source]))
