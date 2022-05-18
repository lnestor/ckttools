from .default_dip_finder import DefaultDipFinder
from .chosen_dip_finder import ChosenDipFinder

class DipFinderFactory:
    FINDERS = [DefaultDipFinder, ChosenDipFinder]

    def get(self, moddef, args):
        if "dips" in args:
            return ChosenDipFinder(moddef, args["dips"])
        else:
            return DefaultDipFinder(moddef)
