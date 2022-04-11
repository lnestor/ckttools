import pyverilog.vparser.ast as vast
from vast.search import find_last_input, find_last_wire, find_last_output

def create_ilist(moddef, gate_type, gate_name, output, inputs, add_output_wire=True):
    out_port = vast.PortArg(None, vast.Identifier(output))
    # TODO: These should be int constants instead of identifiers sometimes
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
    last_input_index = find_last_input(moddef)
    # moddef.items != moddef.children(), all indices are 2 off
    return _create_input(moddef, name, last_input_index - 1)

def create_inputs(moddef, names):
    last_input_index = find_last_input(moddef)
    # moddef.items != moddef.children(), all indices are 2 off
    return [_create_input(moddef, n, last_input_index - 1 + i) for i, n in enumerate(names)]

def _create_input(moddef, name, index):
    portlist = moddef.children()[1]
    ports = list(portlist.ports)
    items = list(moddef.items)

    port = vast.Port(name, None, None, None)
    ports.append(port)

    decl = vast.Decl([vast.Input(name)])
    items.insert(index, decl)

    portlist.ports = tuple(ports)
    moddef.items = tuple(items)
    return decl

def create_wire(moddef, name):
    last_wire_index = find_last_wire(moddef)
    # moddef.items != moddef.children(), all indices are 2 off
    return _create_wire(moddef, name, last_wire_index - 1)

def create_wires(moddef, names):
    last_wire_index = find_last_wire(moddef)
    # moddef.items != moddef.children(), all indices are 2 off
    return [_create_wire(moddef, n, last_wire_index - 1 + i) for i, n in enumerate(names)]

def _create_wire(moddef, name, index):
    items = list(moddef.items)

    decl = vast.Decl([vast.Wire(name)])
    items.insert(index, decl)

    moddef.items = tuple(items)
    return decl

def create_output(moddef, name):
    last_output_index = find_last_output(moddef)
    # moddef.items != moddef.children(), all indices are 2 off
    return _create_output(moddef, name, last_output_index - 1)

def create_outputs(moddef, names):
    last_output_index = find_last_output(moddef)
    # moddef.items != moddef.children(), all indices are 2 off
    return [_create_output(moddef, n, last_output_index - 1 + i) for i, n in enumerate(names)]

def _create_output(moddef, name, index):
    portlist = moddef.children()[1]
    ports = list(portlist.ports)
    items = list(moddef.items)

    port = vast.Port(name, None, None, None)
    ports.append(port)

    decl = vast.Decl([vast.Output(name)])
    items.insert(index, decl)

    portlist.ports = tuple(ports)
    moddef.items = tuple(items)
    return decl

def create_moddef(name):
    return vast.ModuleDef(name, vast.Paramlist([]), vast.Portlist([]), [])
