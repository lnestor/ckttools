from itertools import combinations
import numpy as np

def or_(probs):
    parity = 1
    prob = 0

    for i in range(len(probs)):
        combos = list(combinations(probs, i + 1))
        inter_prob = [np.prod(combo) for combo in combos]
        prob += parity * sum(inter_prob)
        parity *= -1

    return prob

def xor(probs):
    if len(probs) == 1:
        return probs[0]
    else:
        rest = xor(probs[1:])
        return or_([probs[0], rest]) - probs[0] * rest
