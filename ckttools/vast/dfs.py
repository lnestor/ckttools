from .search import get_ilists_from_input, get_ilist_output, try_get_ilist_from_output, get_ilist_inputs

# TODO: implement one DFS function that takes in arguments to go
# forwards/backwards, count # of hops, and run conditions

def dfs(moddef, start, forward=False):
    visited = {}

    if forward:
        _dfs_forwards(moddef, start, visited, 0)
    else:
        _dfs_backwards(moddef, start, visited, 0)

    return list(visited.keys()), visited

def dfs_condition(moddef, start, cond):
    visited = {}
    return _dfs_backwards_cond(moddef, start, visited, cond)

def _dfs_backwards_cond(moddef, net, visited, cond):
    ilist = try_get_ilist_from_output(moddef, net)

    if ilist is None:
        return None
    elif cond(ilist):
        return net

    inputs = get_ilist_inputs(ilist)

    for i in inputs:
        if i in visited and visited[i] < hops + 1:
            continue
        else:
            rslt = _dfs_backwards_cond(moddef, i, visited, cond)

            if rslt:
                return rslt

    return None

def _dfs_forwards(moddef, net, visited, hops):
    ilists = get_ilists_from_input(moddef, net)
    outputs = set([get_ilist_output(i) for i in ilists])

    if len(outputs) == 0:
        return

    for output in outputs:
        if output in visited and visited[output] < hops:
            continue
        else:
            visited[output] = hops
            _dfs_forwards(moddef, output, visited, hops + 1)

def _dfs_backwards(moddef, net, visited, hops):
    ilist = try_get_ilist_from_output(moddef, net)
    visited[net] = hops

    if ilist is None:
        return

    inputs = get_ilist_inputs(ilist)

    for i in inputs:
        if i in visited and visited[i] < hops + 1:
            continue
        else:
            _dfs_backwards(moddef, i, visited, hops + 1)
