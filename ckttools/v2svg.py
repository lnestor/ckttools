import argparse
import os
from pyverilog.vparser.parser import parse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Convert a verilog file to an image")
    parser.add_argument("verilog_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    ast, _ = parse([args.verilog_file], debug=False)
    module_name = ast.children()[0].children()[0].name

    subprocess.run(["yosys", "-p", 'prep -top %s; write_json output.json' % module_name, args.verilog_file])
    subprocess.run(["netlistsvg", "output.json", "-o", args.output_file])
    subprocess.run(["rm", "output.json"])

if __name__ == "__main__":
    main()
