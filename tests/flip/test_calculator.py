from ckttools.flip.calculator import calculate_flip_probability
from ckttools.vast.create import create_ilist

def test_calculate_flip_probability_input():
    ilists = [create_ilist("and", "AND0", "output", ["input1", "input2"])]
    prob = calculate_flip_probability(ilists, "input")
    assert prob == 0.5

def test_calculate_flip_probability_and():
    ilists = [create_ilist("and", "AND0", "output", ["input1", "input2"])]
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.25

def test_calculate_flip_probability_nand():
    ilists = [create_ilist("nand", "NAND0", "output", ["input1", "input2"])]
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.75

def test_calculate_flip_probability_or_two_inputs():
    ilists = [create_ilist("or", "OR0", "output", ["input1", "input2"])]
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.75

def test_calculate_flip_probability_nor_two_inputs():
    ilists = [create_ilist("nor", "NOR0", "output", ["input1", "input2"])]
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.25

def test_calculate_flip_probability_or_three_inputs():
    ilists = [create_ilist("or", "OR0", "output", ["input1", "input2", "input3"])]
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.875

def test_calculate_flip_probability_nor_three_inputs():
    ilists = [create_ilist("nor", "NOR0", "output", ["input1", "input2", "input3"])]
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.125

def test_calculate_flip_probability_or_four_inputs():
    ilists = [create_ilist("or", "OR0", "output", ["input1", "input2", "input3", "input4"])]
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.9375

def test_calculate_flip_probability_xor():
    ilist1 = create_ilist("and", "AND0", "middle1", ["input1", "input2"])
    ilist2 = create_ilist("and", "AND1", "middle2", ["input3", "input4"])
    ilist3 = create_ilist("xor", "XOR0", "output", ["middle1", "middle2"])
    prob = calculate_flip_probability([ilist1, ilist2, ilist3], "output")
    assert prob == .375

def test_calculate_flip_probability_xnor():
    ilist1 = create_ilist("and", "AND0", "middle1", ["input1", "input2"])
    ilist2 = create_ilist("and", "AND1", "middle2", ["input3", "input4"])
    ilist3 = create_ilist("xnor", "XNOR0", "output", ["middle1", "middle2"])
    prob = calculate_flip_probability([ilist1, ilist2, ilist3], "output")
    assert prob == 0.625

def test_calculate_flip_probability_not():
    ilists = []
    ilists.append(create_ilist("and", "AND0", "mid", ["input1", "input2"]))
    ilists.append(create_ilist("not", "NOT0", "output", ["mid"]))
    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.75

def test_calculate_flip_probability_complx():
    ilists = []
    ilists.append(create_ilist("not", "NOT0", "output", ["mid1"])) # not(.6875) = .3125
    ilists.append(create_ilist("xor", "XOR0", "mid1", ["mid2", "mid3"])) # xor(.25, .875) = .6875
    ilists.append(create_ilist("or", "OR0", "mid2", ["mid4", "input1"])) # or(.75, .5) = .875
    ilists.append(create_ilist("and", "AND1", "mid3", ["input2", "input3"])) # .25
    ilists.append(create_ilist("or", "OR1", "mid4", ["input4", "input5"])) # .75

    prob = calculate_flip_probability(ilists, "output")
    assert prob == 0.3125
