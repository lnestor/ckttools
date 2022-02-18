import numpy as np
import probability as prob
from vast.search import get_ilist_output, get_ilist_type, get_ilist_inputs

def _calculate(ilist_map, net):
    if net not in ilist_map:
        return 0.5

    ilist = ilist_map[net]
    type_ = get_ilist_type(ilist)
    input_probs = [_calculate(ilist_map, input_) for input_ in get_ilist_inputs(ilist)]

    if type_ == "and":
        return np.prod(input_probs)
    elif type_ == "nand":
        return 1 - np.prod(input_probs)
    elif type_ == "or":
        return prob.or_(input_probs)
    elif type_ == "nor":
        return 1 - prob.or_(input_probs)
    elif type_ == "xor":
        return prob.xor(input_probs)
    elif type_ == "xnor":
        return 1 - prob.xor(input_probs)
    elif type_ == "not":
        return 1 - input_probs[0]
    else:
        raise RuntimeError("p(flip) calculation: unknown gate type " + type_)

def calculate_flip_probability(ilists, net):
    ilist_map = {get_ilist_output(ilist): ilist for ilist in ilists}
    return _calculate(ilist_map, net)
