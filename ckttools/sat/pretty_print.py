def pp(bits, key=None):
    bitstr = ""

    for name in sorted(bits, key=key):
        if bits[name] == True:
            bitstr += "1"
        else:
            bitstr += "0"

    return bitstr
