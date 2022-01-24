import argparse
from bench.parse import parse_from_verilog

def main():
    parser = argparse.ArgumentParser(description="Convert a verilog file to a .bench file")
    parser.add_argument("verilog", help="The verilog file")
    parser.add_argument("-o", "--output", help="The output .bench file. Otherwise it will print to the screen.")
    args = parser.parse_args()

    bench = parse_from_verilog(args.verilog)

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(bench)
    else:
        print(bench)

if __name__ == "__main__":
    main()
