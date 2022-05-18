from .bench import Bench
from pyverilog.vparser.parser import parse
from vast.search import (
    get_input_names,
    get_output_names,
    get_ilists,
    get_ilist_output,
    get_ilist_inputs,
    get_ilist_type
)
from vast.moddef import get_moddef_from_verilog

def parse_from_verilog(filename):
    return parse_from_moddef(get_moddef_from_verilog(filename))

def parse_from_moddef(moddef):
    bench = Bench(moddef.name())

    for input_name in moddef.inputs:
        bench.add_input(input_name)

    for output_name in moddef.outputs:
        bench.add_output(output_name)

    for ilist in moddef.ilists:
        output = get_ilist_output(ilist)
        inputs = get_ilist_inputs(ilist)
        type_ = get_ilist_type(ilist)

        bench.add_gate(output, type_, inputs)

    return bench


def parse_from_bench(filename):
    raise
