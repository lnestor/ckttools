import pyverilog.vparser.ast as vast
from .search import get_key_input_names, get_ilists_from_input, get_ilist_input_nodes

def change_ilist_input_name(ilist, old_name, new_name):
    input_objs = get_ilist_input_nodes(ilist)

    for input_obj in input_objs:
        if isinstance(input_obj, vast.Identifier) and input_obj.name == old_name:
            input_obj.name = new_name

def rename_ilist_output(ilist, name):
    ilist.children()[0].children()[0].children()[0].name = name
