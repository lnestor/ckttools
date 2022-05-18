def pp(bits, key=None):
    bitstr = ""

    for name in sorted(bits, key=key):
        if bits[name] == True:
            bitstr += "1"
        elif bits[name] == False:
            bitstr += "0"
        else:
            bitstr += "X"

    return bitstr
