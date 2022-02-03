import itertools
from .search import get_ilist_map, get_ilist_inputs

def _get_key_inputs_from_subcircuit(ilist_map, net):
    if net not in ilist_map:
        return [net]
    else:
        ilist = ilist_map[net]
        keys_on_input_nets = [_get_key_inputs_from_subcircuit(ilist_map, input_) for input_ in get_ilist_inputs(ilist)]
        return list(itertools.chain.from_iterable(keys_on_input_nets))


def get_key_inputs_from_subcircuit(moddef, net):
    ilist_map = get_ilist_map(moddef)
    return _get_key_inputs_from_subcircuit(ilist_map, net)
