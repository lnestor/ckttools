import os
from .parse import parse_from_verilog

def create_bench_file(output_filename, input_filename):
    _, extension = os.path.splitext(input_filename)

    if extension == ".v":
        create_from_verilog(output_filename, input_filename)
    else:
        raise

def create_from_verilog(output_filename, verilog_filename):
    bench = parse_from_verilog(verilog_filename)

    with open(output_filename, "w") as f:
        f.write(str(bench))
