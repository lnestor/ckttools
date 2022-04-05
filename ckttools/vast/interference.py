from .search import get_output_names, get_net_names
from .dfs import dfs

def find_interfering_nets(moddef, type_, nets, hops=-1):
    if type_ == "none":
        return _none(moddef, nets)
    elif type_ == "indirect":
        return _indirect(moddef, nets, hops)
    else:
        raise

def _indirect(moddef, nets, specified_hops):
    all_outputs = get_output_names(moddef)
    nets_ahead = set()
    nets_behind = set()
    interfering_outputs = set()

    for interfering_net in nets:
        _nets_ahead, _ = dfs(moddef, interfering_net, forward=True)
        _nets_behind, _ = dfs(moddef, interfering_net)

        nets_ahead.update(_nets_ahead)
        nets_behind.update(_nets_behind)

        interfering_outputs.update([net for net in nets_ahead if net in all_outputs])

    interfering_nets = set()
    for output in interfering_outputs:
        dfs_nets, hops = dfs(moddef, output)
        interfering_nets.update(dfs_nets)

    indirect_nets = interfering_nets
    indirect_nets = [net for net in indirect_nets if net not in nets_ahead]
    indirect_nets = [net for net in indirect_nets if net not in nets_behind]

    if specified_hops == -1:
        return indirect_nets
    else:
        indirect_nets = [net for net in indirect_nets if abs(hops[net] - hops[nets[0]]) == specified_hops]
        return indirect_nets

def _none(moddef, nets):
    all_outputs = get_output_names(moddef)
    interfering_outputs = set()

    for interfering_net in nets:
        nets_ahead, _ = dfs(moddef, interfering_net, forward=True)
        interfering_outputs.update([net for net in nets_ahead if net in all_outputs])

    interfering_nets = set()
    for output in interfering_outputs:
        dfs_nets, _ = dfs(moddef, output)
        interfering_nets.update(dfs_nets)

    all_nets = get_net_names(moddef)
    return [n for n in all_nets if n not in interfering_nets]
