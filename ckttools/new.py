DIPS = [
    "00 00 00 00",
    "01 01 01 01",
    "10 10 10 10",
    "11 11 11 11",
    "00 01 10 11",
    "11 00 01 10",
    "10 11 00 01",
    "01 10 11 00",
]

EXTRAS = [
    "00 10 01 11",
    "11 01 01 11",
    "10 01 01 00",
    "11 11 01 00",
    "11 11 01 11"
]

DIPS = [
    "00 00 00",
    "01 01 01",
    "10 10 10",
    "11 11 11"
]

EXTRAS = [
    "11 01 00",
    "10 01 10",
    "10 11 00",
    "01 10 00",
    "10 00 00"
]

def neg(pattern):
    if pattern[0] == "00":
        return ["01", "10", "11"]
    elif pattern[0] == "01":
        return ["00", "10", "11"]
    elif pattern[0] == "10":
        return ["00", "01", "11"]
    elif pattern[0] == "11":
        return ["00", "01", "10"]

def ex(pattern):
    return [pattern]

def find_hidden_keys(pattern):
    keys = []
    keys.extend((i, j, k) for i in ex(pattern[0]) for j in ex(pattern[1]) for k in neg(ex(pattern[2])))
    keys.extend((i, j, k) for i in ex(pattern[0]) for j in neg(ex(pattern[1])) for k in ex(pattern[2]))
    keys.extend((i, j, k) for i in neg(ex(pattern[0])) for j in ex(pattern[1]) for k in ex(pattern[2]))
    keys.extend((i, j, k) for k in neg(ex(pattern[2])) for i in neg(ex(pattern[0])) for j in neg(ex(pattern[1])))
    return keys

def find_eliminated_keys(pattern):
    keys = []
    keys.extend((i, j, k) for i in ex(pattern[0]) for j in neg(ex(pattern[1])) for k in neg(ex(pattern[2])))
    keys.extend((i, j, k) for i in neg(ex(pattern[0])) for j in ex(pattern[1]) for k in neg(ex(pattern[2])))
    keys.extend((i, j, k) for i in neg(ex(pattern[0])) for j in neg(ex(pattern[1])) for k in ex(pattern[2]))
    keys.extend((i, j, k) for i in ex(pattern[0]) for j in ex(pattern[1]) for k in ex(pattern[2]))
    return keys

def main():
    patterns = [d.split(" ") for d in DIPS]
    extras = [e.split(" ") for e in EXTRAS]

    hidden = [find_hidden_keys(p) for p in patterns]
    hidden_set = set(e for sub in hidden for e in sub)

    eliminated = [find_eliminated_keys(p) for p in patterns]
    eliminated_set = set(e for sub in eliminated for e in sub)

    extras_eliminated = [find_eliminated_keys(e) for e in extras]
    remaining = [list(set(e) - eliminated_set) for e in extras_eliminated]
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    main()
