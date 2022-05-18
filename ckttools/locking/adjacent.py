from vast.dfs import dfs_condition
from vast.search import get_ilist_inputs, get_output_names, get_ilist_output, get_ilist_from_output

def find_adjacent(moddef, allow_unary=True, inputs=False):
    if allow_unary:
        raise NotImplemented

    outputs = moddef.outputs
    cond = lambda ilist: len(get_ilist_inputs(ilist)) >= 2 and get_ilist_output(ilist) not in outputs

    valid_nets = [dfs_condition(moddef, output, cond) for output in outputs]
    valid_nets = [net for net in valid_nets if net is not None]

    if inputs:
        valid_net_inputs = [get_ilist_inputs(moddef.get_ilist(net)) for net in valid_nets]
        valid_nets = [net for net_inputs in valid_net_inputs for net in net_inputs]

    return valid_nets
