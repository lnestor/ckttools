from vast.dfs import dfs_condition
from vast.search import get_ilist_inputs, get_output_names, get_ilist_output

def find_adjacent(moddef, allow_unary=True):
    if allow_unary:
        raise NotImplemented

    outputs = get_output_names(moddef)
    cond = lambda ilist: len(get_ilist_inputs(ilist)) >= 2 and get_ilist_output(ilist) not in outputs

    valid_nets = [dfs_condition(moddef, output, cond) for output in outputs]
    valid_nets = [net for net in valid_nets if net is not None]
    return valid_nets
