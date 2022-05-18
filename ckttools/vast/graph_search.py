import itertools
from .search import get_ilist_map, get_ilist_inputs, get_key_input_names

def _get_inputs_from_subcircuit(moddef, net):
    if not moddef.is_ilist(net):
        return [net]
    else:
        ilist = moddef.get_ilist(net)
        keys_on_input_nets = [_get_inputs_from_subcircuit(moddef, input_) for input_ in get_ilist_inputs(ilist)]
        return list(itertools.chain.from_iterable(keys_on_input_nets))

def get_key_inputs_from_subcircuit(moddef, net):
    inputs = _get_inputs_from_subcircuit(moddef, net)
    key_inputs = moddef.key_inputs

    return set([input_ for input_ in inputs if input_ in key_inputs])
