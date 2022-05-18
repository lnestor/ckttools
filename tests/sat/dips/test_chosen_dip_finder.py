from ckttools.sat.dips.chosen_dip_finder import ChosenDipFinder
import pytest

DIPS = """2
00
01
10
11
"""

class DummyModdef():
    @property
    def primary_inputs(self):
        return ["G1", "G2", "G3", "G4"]

    @property
    def key_inputs(self):
        return ["K1", "K2", "K3", "K4"]

@pytest.fixture()
def moddef():
    return DummyModdef()

def test_can_find_dip_with_dips_remaining(moddef, tmp_path):
    dip_file = tmp_path / "dips.txt"
    dip_file.write_text(DIPS)

    dip_finder = ChosenDipFinder(moddef, dip_file)
    assert dip_finder.can_find_dip()

def test_can_find_dip_with_no_dips_remaining(moddef, tmp_path):
    dip_file = tmp_path / "dips.txt"
    dip_file.write_text(DIPS)

    dip_finder = ChosenDipFinder(moddef, dip_file)
    dip_finder.can_find_dip()
    dip_finder.can_find_dip()
    dip_finder.can_find_dip()
    dip_finder.can_find_dip()
    assert not dip_finder.can_find_dip()

def test_get_inputs_returns_specified_dips_with_one_liner(moddef, tmp_path):
    dip_file = tmp_path / "dips.txt"
    dip_file.write_text(DIPS)

    dip_finder = ChosenDipFinder(moddef, dip_file)
    dip_finder.can_find_dip()
    dips = dip_finder.get_dip()
    assert dips["G1"] == False
    assert dips["G2"] == False

    dip_finder.can_find_dip()
    dips = dip_finder.get_dip()
    assert dips["G1"] == False
    assert dips["G2"] == True

    dip_finder.can_find_dip()
    dips = dip_finder.get_dip()
    assert dips["G1"] == True
    assert dips["G2"] == False

    dip_finder.can_find_dip()
    dips = dip_finder.get_dip()
    assert dips["G1"] == True
    assert dips["G2"] == True

def test_get_keys_returns_dummy(moddef):
    dip_finder = ChosenDipFinder(moddef, "dip_file")
    keys1, keys2 = dip_finder.get_keys()
    assert keys1["K1"] == "X"
    assert keys1["K2"] == "X"
    assert keys1["K3"] == "X"
    assert keys1["K4"] == "X"
    assert keys2["K1"] == "X"
    assert keys2["K2"] == "X"
    assert keys2["K3"] == "X"
    assert keys2["K4"] == "X"
