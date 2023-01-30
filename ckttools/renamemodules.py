import argparse
import os
import re

def get_args():
    args = argparse.ArgumentParser(description="Rename Verilog modules")
    args.add_argument("path")

    return args.parse_args()

def main():
    args = get_args()

    filenames = os.listdir(args.path)
    for filename in filenames:
        full_path = args.path + "/" + filename
        print("Renaming %s" % full_path)

        with open(full_path, "r") as f:
            contents = f.read()

        new_contents = re.sub("module (.*) \(", "module %s(" % filename[0:-2], contents)
        with open(full_path, "w") as f:
            f.write(new_contents)

if __name__ == "__main__":
    main()
