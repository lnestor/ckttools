import argparse
from logic.key_correctness import check_key_correctness
import os
from vast.moddef import get_moddef_from_verilog

def get_args():
    parser = argparse.ArgumentParser(description="Checks if a key is correct")
    parser.add_argument("locked", help="The locked verilog file")
    parser.add_argument("unlocked", help="The oracle verilog file")
    parser.add_argument("--key", required=True, help="The key to test")
    return parser.parse_args()

def map_keybits(moddef, key):
    if(len(moddef.key_inputs) != len(key)):
        print("Error: provided key is not correct length")
        print("       Expected %i bits, got %i" % (len(moddef.key_inputs), len(key)))
        exit(-1)

    return {input_: int(value) for input_, value in zip(moddef.key_inputs, key)}

def keystr(string):
    if os.path.isfile(string):
        with open(string) as f:
            return f.read().strip()
    else:
        return string

def main():
    args = get_args()

    locked_moddef = get_moddef_from_verilog(args.locked)
    unlocked_moddef = get_moddef_from_verilog(args.unlocked)

    primary_inputs = locked_moddef.primary_inputs
    keys = map_keybits(locked_moddef, keystr(args.key))

    check_key_correctness(locked_moddef, unlocked_moddef, keys)

if __name__ == "__main__":
    main()
