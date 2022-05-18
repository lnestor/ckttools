from ckttools.sat.dips.chosen_dip_finder import ChosenDipFinder
from ckttools.sat.dips.default_dip_finder import DefaultDipFinder
from ckttools.sat.dips.dip_finder_factory import DipFinderFactory

def test_without_specified_dips():
    args = {"dips": "some dips here"}
    dip_finder = DipFinderFactory().get("moddef", args)
    assert isinstance(dip_finder, ChosenDipFinder)

def test_with_specified_dips():
    dip_finder = DipFinderFactory().get("moddef", {})
    assert isinstance(dip_finder, DefaultDipFinder)
