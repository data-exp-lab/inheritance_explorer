"""Console script for inheritance_explorer. Run $ inheritance_explorer --help
for instructions and options.
"""
import importlib
import os

import click

from inheritance_explorer.inheritance_explorer import ClassGraphTree


@click.command()
@click.argument("module_class", type=str)
@click.argument("output_file", type=str)
@click.option(
    "--output_format",
    default=None,
    help="output format string (default is svg, or the file extension of output_file)",
)
@click.option(
    "--import_list", default=None, help="comma-separated list of modules to import"
)
@click.option("--funcname", default=None, help="function name to track")
def map_class(module_class, output_file, output_format, import_list, funcname):
    """
    map a class and save the graph to a file. requires graphviz installation.

    MODULE_CLASS : the starting class to map from, must be of the form Module.Class
    Multiple modules may be specified, it is assumed the last entry is the class.
    For example, matplotlib.axes.Axes with map from Axes, which can
    be imported from matplotlib.axes

    OUTPUT_FILE : the output file for saving the graph
    """

    # import the class of interest
    mod_cls = module_class.split(".")
    if len(mod_cls) > 2:
        mod_name = ".".join(mod_cls[0:-1])
    elif len(mod_cls) < 2:
        raise ValueError(f"module_class be of the form module.class, found {mod_cls}")
    else:
        mod_name = mod_cls[0]

    mod = importlib.import_module(mod_name)
    cls = getattr(mod, mod_cls[-1])

    # import any other modules that we want in scope
    if import_list is not None:
        import_list = [m.strip() for m in import_list.split(",")]
        modules = [importlib.import_module(mod) for mod in import_list]  # noqa: F841

    if funcname is not None:
        if hasattr(cls, funcname) is False:
            raise AttributeError(f"{funcname} is not an attribute of {cls}")

    # now build the graph
    cgt = ClassGraphTree(cls, funcname=funcname)

    # and save it
    _, file_extension = os.path.splitext(output_file)
    fmt = file_extension.replace(".", "")
    if output_format is None and file_extension == "":
        fmt = "svg"

    cgt.graph().write(output_file, format=fmt)

    return 0
