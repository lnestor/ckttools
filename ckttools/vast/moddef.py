from pyverilog.vparser.parser import parse
from util.lazyprop import lazyprop
from vast.create import create_input, create_ilist, create_wire
from vast.modify import rename_ilist_output
from vast.search import get_output_names, get_key_input_names, get_primary_input_names, get_wire_names, get_ilists, get_ilist_output, get_input_names, get_net_names, get_ilists_from_input, get_ilist_inputs

def get_ast(verilog):
    ast, _ = parse([verilog], debug=False)
    return ast

def get_moddef_no_wrapper(ast):
    return ast.children()[0].children()[0]

def get_moddef(ast):
    return ModuleDefWrapper(get_moddef_no_wrapper(ast))

def get_moddef_from_verilog(verilog):
    ast, _ = parse([verilog], debug=False)
    return get_moddef(ast)

class ModuleDefWrapper:
    def __init__(self, moddef):
        self.moddef = moddef
        self.ilist_map = {get_ilist_output(ilist): ilist for ilist in self.ilists}

    @lazyprop
    def outputs(self):
        return get_output_names(self.moddef)

    @lazyprop
    def inputs(self):
        return get_input_names(self.moddef)

    @lazyprop
    def primary_inputs(self):
        return get_primary_input_names(self.moddef)

    @lazyprop
    def key_inputs(self):
        return get_key_input_names(self.moddef)

    @lazyprop
    def wires(self):
        return get_wire_names(self.moddef)

    @lazyprop
    def ilists(self):
        return get_ilists(self.moddef)

    @lazyprop
    def keygates(self):
        return [ilist for ilist in get_ilists(self.moddef) if self.is_key_gate(ilist)]

    @lazyprop
    def net_names(self):
        return get_net_names(self.moddef)

    def get_ilist(self, output):
        return self.ilist_map[output]

    def get_ilists_from_input(self, input_):
        return get_ilists_from_input(self.moddef, input_)

    def is_ilist(self, output):
        return output in self.ilist_map

    def is_input(self, name):
        return name in self.inputs

    def is_key_gate_output(self, net_name):
        ilist = self.get_ilist(net_name)
        inputs = get_ilist_inputs(ilist)
        return any([i in self.key_inputs for i in inputs])

    def is_key_gate(self, ilist):
        inputs = get_ilist_inputs(ilist)
        return any(["signal_from_circuit" in i for i in inputs])

    def name(self):
        return self.moddef.name

    def create_input(self, name):
        del self.inputs
        del self.key_inputs
        del self.primary_inputs
        del self.net_names
        return create_input(self.moddef, name)

    def create_wire(self, name):
        del self.wires
        del self.net_names
        return create_wire(self.moddef, name)

    def create_ilist(self, gate_type, gate_name, output, inputs, add_output_wire=True):
        del self.wires
        del self.ilists
        del self.net_names
        ilist = create_ilist(self.moddef, gate_type, gate_name, output, inputs, add_output_wire)
        self.ilist_map[output] = ilist
        return ilist

    def rename_ilist_output(self, original_name, changed_name):
        # This could cause issues if this is called after an ilist is added
        # At that point, 2 ilists with the same output exist. This method
        # does not guarentee which one is refreshed in the ilist map.
        # This method also deletes from the ilist map which could cause
        # issues if trying to access that later. In general, this should
        # be followed with a create_ilist call to recreate the ilist in the
        # ilist map
        del self.ilists
        ilist = self.get_ilist(original_name)
        rename_ilist_output(ilist, changed_name)
        del self.ilist_map[original_name]
        self.ilist_map[changed_name] = ilist
