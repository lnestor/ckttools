import numpy as np
import probability as prob
from vast.search import get_ilist_output, get_ilist_type, get_ilist_inputs, try_get_ilist_from_output

def _calculate(moddef, net):
    if not moddef.is_ilist(net):
        return 0.5

    ilist = moddef.get_ilist(net)
    type_ = get_ilist_type(ilist)
    input_probs = [_calculate(moddef, input_) for input_ in get_ilist_inputs(ilist)]

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

def calculate_flip_probability(moddef, net):
    return _calculate(moddef, net)
