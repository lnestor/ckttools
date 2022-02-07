from functools import reduce
from itertools import combinations
import numpy as np
from vast.search import get_ilist_output, get_ilist_type, get_ilist_inputs

def _calculate_or_probability(input_probs):
    parity = 1
    prob = 0

    for i in range(len(input_probs)):
        combos = list(combinations(input_probs, i + 1))
        inter_prob = [np.prod(combo) for combo in combos]
        prob += parity * sum(inter_prob)
        parity *= -1

    return prob

def _calculate_xor_probability(input_probs):
    if len(input_probs) == 1:
        return input_probs[0]
    else:
        rest = _calculate_xor_probability(input_probs[1:])
        return _calculate_or_probability([input_probs[0], rest]) - input_probs[0] * rest

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
        return _calculate_or_probability(input_probs)
    elif type_ == "nor":
        return 1 - _calculate_or_probability(input_probs)
    elif type_ == "xor":
        return _calculate_xor_probability(input_probs)
    elif type_ == "xnor":
        return 1 - _calculate_xor_probability(input_probs)
    elif type_ == "not":
        return 1 - input_probs[0]
    else:
        raise RuntimeError("p(flip) calculation: unknown gate type " + type_)

def calculate_flip_probability(ilists, net):
    ilist_map = {get_ilist_output(ilist): ilist for ilist in ilists}
    return _calculate(ilist_map, net)
