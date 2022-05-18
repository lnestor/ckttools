from .default_dip_finder import DefaultDipFinder
from .chosen_dip_finder import ChosenDipFinder

class DipFinderFactory:
    FINDERS = [DefaultDipFinder, ChosenDipFinder]

    def get(self, moddef, dip_file):
        if dip_file is not None:
            return ChosenDipFinder(moddef, dip_file)
        else:
            return DefaultDipFinder(moddef)
