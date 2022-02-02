import pyverilog.vparser.ast as vast

def create_ilist(gate_type, gate_name, output, inputs):
    out_port = vast.PortArg(None, vast.Identifier(output))
    in_ports = [vast.PortArg(None, vast.Identifier(name)) for name in inputs]

    portlist = (out_port, *in_ports)
    parameterlist = ()
    instance = vast.Instance(gate_type, gate_name, portlist, parameterlist)
    ilist = vast.InstanceList(gate_type, (), (instance,))

    return ilist
