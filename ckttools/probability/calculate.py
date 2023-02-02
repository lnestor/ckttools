from itertools import combinations
import numpy as np

def or_(probs):
    prob = 1 - np.prod([(1 - p) for p in probs])
    return prob

def xor(probs):
    if len(probs) == 1:
        return probs[0]
    else:
        rest = xor(probs[1:])
        return or_([probs[0], rest]) - probs[0] * rest
