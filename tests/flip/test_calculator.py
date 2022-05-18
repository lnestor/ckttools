from ckttools.flip.calculator import calculate_flip_probability
from ckttools.vast.create import create_ilist
from ckttools.vast.moddef import ModuleDefWrapper
import pytest
import pyverilog.vparser.ast as vast

@pytest.fixture
def moddef():
    return vast.ModuleDef("Example", vast.Paramlist([]), vast.Portlist([]), [])

def test_calculate_flip_probability_input(moddef):
    create_ilist(moddef, "and", "AND0", "output", ["input1", "input2"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "input")
    assert prob == 0.5

def test_calculate_flip_probability_and(moddef):
    create_ilist(moddef, "and", "AND0", "output", ["input1", "input2"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.25

def test_calculate_flip_probability_nand(moddef):
    create_ilist(moddef, "nand", "NAND0", "output", ["input1", "input2"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.75

def test_calculate_flip_probability_or_two_inputs(moddef):
    create_ilist(moddef, "or", "OR0", "output", ["input1", "input2"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.75

def test_calculate_flip_probability_nor_two_inputs(moddef):
    create_ilist(moddef, "nor", "NOR0", "output", ["input1", "input2"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.25

def test_calculate_flip_probability_or_three_inputs(moddef):
    create_ilist(moddef, "or", "OR0", "output", ["input1", "input2", "input3"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.875

def test_calculate_flip_probability_nor_three_inputs(moddef):
    create_ilist(moddef, "nor", "NOR0", "output", ["input1", "input2", "input3"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.125

def test_calculate_flip_probability_or_four_inputs(moddef):
    create_ilist(moddef, "or", "OR0", "output", ["input1", "input2", "input3", "input4"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.9375

def test_calculate_flip_probability_xor(moddef):
    create_ilist(moddef, "and", "AND0", "middle1", ["input1", "input2"])
    create_ilist(moddef, "and", "AND1", "middle2", ["input3", "input4"])
    create_ilist(moddef, "xor", "XOR0", "output", ["middle1", "middle2"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == .375

def test_calculate_flip_probability_xnor(moddef):
    create_ilist(moddef, "and", "AND0", "middle1", ["input1", "input2"])
    create_ilist(moddef, "and", "AND1", "middle2", ["input3", "input4"])
    create_ilist(moddef, "xnor", "XNOR0", "output", ["middle1", "middle2"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.625

def test_calculate_flip_probability_not(moddef):
    create_ilist(moddef, "and", "AND0", "mid", ["input1", "input2"])
    create_ilist(moddef, "not", "NOT0", "output", ["mid"])
    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.75

def test_calculate_flip_probability_complx(moddef):
    create_ilist(moddef, "not", "NOT0", "output", ["mid1"]) # not(.6875) = .3125
    create_ilist(moddef, "xor", "XOR0", "mid1", ["mid2", "mid3"]) # xor(.25, .875) = .6875
    create_ilist(moddef, "or", "OR0", "mid2", ["mid4", "input1"]) # or(.75, .5) = .875
    create_ilist(moddef, "and", "AND1", "mid3", ["input2", "input3"]) # .25
    create_ilist(moddef, "or", "OR1", "mid4", ["input4", "input5"]) # .75

    prob = calculate_flip_probability(ModuleDefWrapper(moddef), "output")
    assert prob == 0.3125
