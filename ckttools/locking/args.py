import random
from locking.filters import get_filter
from vast.search import get_net_names

def get_insertion_net(moddef, pass_config, prev_pass_data):
    if "insertion" not in pass_config:
        print("ERROR: pass %i does not have insertion data" % pass_config["index"])
        exit(-1)

    filters = [get_filter(name, value, pass_config) for name, value in pass_config["insertion"].items()]
    nets = get_net_names(moddef)

    for filter_ in filters:
        nets = filter_.filter(moddef, nets, prev_pass_data)

    return random.choice(nets)

def get_start_input_index(config, prev_pass_data):
    if "primary-input-start" not in config:
        return 0
    elif config["primary-input-start"] == "continuous":
        index = config["index"]
        return prev_pass_data[index - 1]["last_input_index"] + 1
    else:
        return int(config["primary-input-start"])

def default_pass_args(moddef, pass_config, prev_pass_data):
    args = {}
    args["insertion_net"] = get_insertion_net(moddef, pass_config, prev_pass_data)
    args["start_input_index"] = get_start_input_index(pass_config, prev_pass_data)
    return args
