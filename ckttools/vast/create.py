import pyverilog.vparser.ast as vast
from vast.search import find_last_input, find_last_wire

def create_ilist(moddef, gate_type, gate_name, output, inputs, add_output_wire=True):
    out_port = vast.PortArg(None, vast.Identifier(output))
    in_ports = [vast.PortArg(None, vast.Identifier(name)) for name in inputs]

    portlist = (out_port, *in_ports)
    parameterlist = ()
    instance = vast.Instance(gate_type, gate_name, portlist, parameterlist)
    ilist = vast.InstanceList(gate_type, (), (instance,))

    if add_output_wire:
        create_wire(moddef, output)

    items = list(moddef.items)
    items.append(ilist)
    moddef.items = tuple(items)

    return output

def create_input(moddef, name):
    portlist = moddef.children()[1]
    ports = list(portlist.ports)
    items = list(moddef.items)

    port = vast.Port(name, None, None, None)
    ports.append(port)

    last_input_index = find_last_input(moddef)
    decl = vast.Decl([vast.Input(name)])
    # moddef.items != moddef.children(), all indices are 2 off
    items.insert(last_input_index - 1, decl)

    portlist.ports = tuple(ports)
    moddef.items = tuple(items)

    return decl

def create_wire(moddef, name):
    items = list(moddef.items)

    last_wire_index = find_last_wire(moddef)
    decl = vast.Decl([vast.Wire(name)])
    # moddef.items != moddef.children(), all indices are 2 off
    items.insert(last_wire_index - 1, decl)

    moddef.items = tuple(items)
    return decl

