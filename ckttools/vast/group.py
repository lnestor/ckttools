from .search import get_ilist_inputs, get_ilist_name

def find_interference_groups(moddef):
    visited = set()
    current_group = set()
    keys_still_in_search = set()
    groups = []

    for output in moddef.outputs:
        _run_dfs(moddef, output, visited, current_group, keys_still_in_search, groups)

    return groups

def _run_dfs(moddef, net_name, visited, current_group, keys_still_in_search, groups):
    visited.add(net_name)
    ilist = moddef.get_ilist(net_name)
    is_key = moddef.is_key_gate_output(net_name)

    if is_key:
        current_group.add(get_ilist_name(ilist))
        keys_still_in_search.add(net_name)


    for child in get_ilist_inputs(ilist):
        if child not in visited and child not in moddef.inputs:
            _run_dfs(moddef, child, visited, current_group, keys_still_in_search, groups)

    if is_key:
        keys_still_in_search.remove(net_name)
        if len(keys_still_in_search) == 0:
            groups.append(list(current_group))
            current_group.clear()


