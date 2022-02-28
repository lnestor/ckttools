import copy
from vast.modify import add_suffix_to_keys

def build_miter(moddef):
    miter_half1 = copy.deepcopy(moddef)
    miter_half2 = copy.deepcopy(moddef)

    add_suffix_to_keys(miter_half1, "half1")
    add_suffix_to_keys(miter_half2, "half2")

