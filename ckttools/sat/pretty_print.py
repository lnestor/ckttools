import re

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_) if s]

def pp(bits, key=natural_key):
    bitstr = ""

    for name in sorted(bits, key=key):
        if bits[name] == True:
            bitstr += "1"
        elif bits[name] == False:
            bitstr += "0"
        else:
            bitstr += "X"

    return bitstr
