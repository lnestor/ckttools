from vast.search import get_output_names
from vast import interference

def get_filter(filter_name, filter_arg, index):
    if filter_name == "net-type":
        return Filter(net_type_filter(filter_arg, index))
    elif filter_name == "net-name":
        return Filter(net_name_filter(filter_arg))
    elif filter_name == "interference":
        return Filter(interference_filter(filter_arg))
    else:
        print("WARNING: unknown insertion filter %s" % filter_name)
        return Filter(null_filter())

class Filter:
    def __init__(self, filter_fn):
        self.fn = filter_fn

    def filter(self, moddef, nets, prev_pass_data):
        filtered_nets = self.fn(moddef, nets, prev_pass_data)

        if len(filtered_nets) == 0:
            print("ERROR: pass has no valid insertion net")
            exit(-1)
        else:
            return filtered_nets

def filt(nets, allowed):
    return [n for n in nets if n in allowed]

def null_filter():
    return lambda moddef, nets, prev_pass_data: nets

def net_type_filter(net_type, index):
    if net_type == "output":
        return lambda moddef, nets, prev_pass_data: filt(nets, get_output_names(moddef))
    elif net_type == "previous":
        return lambda moddef, nets, prev_pass_data: filt(nets, prev_pass_data[index - 1]["insertion_net"])
    else:
        print("ERROR: unknown net type %s in insertion filter" % net_type)
        exit(-1)

def net_name_filter(net_name):
    return lambda moddef, nets, prev_pass_data: filt(nets, [net_name])

def find_interfering_nets(moddef, args, prev_pass_data):
    nets = [prev_pass_data[idx]["insertion_net"] for idx in args["passes"]]
    return interference.find_interfering_nets(moddef, args["type"], nets, args["hops"] if "hops" in args else -1)

def interference_filter(args):
    return lambda moddef, nets, prev_pass_data: filt(nets, find_interfering_nets(moddef, args, prev_pass_data))
