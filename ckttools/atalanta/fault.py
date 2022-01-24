def create_fault_file(fname, net_names):
    with open(fname, "w") as f:
        for net_name in net_names:
            f.write("%s /0\n" % net_name)
            f.write("%s /1\n" % net_name)
