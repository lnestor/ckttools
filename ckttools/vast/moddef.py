from pyverilog.vparser.parser import parse
from util.lazyprop import lazyprop
from vast.search import get_output_names, get_key_input_names, get_primary_input_names, get_wire_names, get_ilists, get_ilist_output, get_input_names

def get_ast(verilog):
    ast, _ = parse([verilog], debug=False)
    return ast

def get_moddef(ast):
    return ModuleDefWrapper(ast.children()[0].children()[0])

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

    def get_ilist(self, output):
        return self.ilist_map[output]

    def is_ilist(self, output):
        return output in self.ilist_map

    def is_input(self, name):
        return name in self.inputs

    def name(self):
        return self.moddef.name
