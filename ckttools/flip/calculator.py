import numpy as np
import sympy
from vast.search import get_ilist_type, get_ilist_inputs

def _get_terms(expr):
    if isinstance(expr, sympy.Mul):
        return [expr]
    elif isinstance(expr, sympy.Add):
        return expr._args
    else:
        return expr

def _truncate(term):
    if isinstance(term, sympy.Mul):
        new_factors = []

        for factor in term._args:
            if len(factor._args) == 2:
                new_factors.append(factor._args[0])
            else:
                new_factors.append(factor)

        return sympy.Mul(*new_factors)

    return term


def _or(input_exprs):
    return 1 - sympy.Mul(*[1 - i for i in input_exprs])

def _xor(input_exprs):
    if len(input_exprs) == 1:
        return input_exprs[0]
    else:
        rest = _xor(input_exprs[1:])
        return _or([input_exprs[0], rest]) - input_exprs[0] * rest

def _get_expr(moddef, net, exprs, inputs):
    if isinstance(net, int):
        exprs[net] = 1 if net == 1 else 0
    elif net in exprs:
        pass
    elif not moddef.is_ilist(net):
        exprs[net] = sympy.symbols(net)
        inputs.append(exprs[net])
    else:
        ilist = moddef.get_ilist(net)
        type_ = get_ilist_type(ilist)
        input_exprs = [_get_expr(moddef, input_, exprs, inputs) for input_ in get_ilist_inputs(ilist)]

        expr = None
        if type_ == "and":
            expr = sympy.Mul(*input_exprs)
        elif type_ == "nand":
            expr = 1 - sympy.Mul(*input_exprs)
        elif type_ == "or":
            expr = _or(input_exprs)
        elif type_ == "nor":
            expr = 1 - _or(input_exprs)
        elif type_ == "xor":
            expr = _xor(input_exprs)
        elif type_ == "xnor":
            expr = 1 - _xor(input_exprs)
        elif type_ == "not":
            expr = 1 - input_exprs[0]
        elif type_ == "buf":
            expr = input_exprs[0]
        else:
            raise RuntimeError("p(flip) calculation: unknown gate type " + type_)

        expanded = sympy.expand(expr)
        terms = _get_terms(expanded)
        truncated_terms = [_truncate(term) for term in terms]
        new_expr = sympy.expand(sympy.Add(*truncated_terms))

        exprs[net] = new_expr

    return exprs[net]

def calculate_flip_probability(moddef, net):
    exprs = {}
    inputs = []
    _get_expr(moddef, net, exprs, inputs)
    subs = [(i, 0.5) for i in inputs]

    return exprs[net].subs(subs)
