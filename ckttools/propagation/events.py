from bitpattern import Set

class Events:
    """
    Represents a set of events where a specific key gate propagates to the output.
    This class does not contain propagation AND no-propagations events. Rather,
    any event that is not included in this class can be considered a no-propagation
    event.

    A propagation event needs both a primary input pattern and a key pattern. This
    class stores them by primary input patterns, meaning there can be many key
    patterns for a specific primary input.

    """

    def __init__(self):
        self.events = {}

    def add(self, input_pattern, key_patterns):
        """Add a new set of propagation events.

        Args:
            input_pattern (str): the input pattern for the propagation events
            key_patterns (list): a list with the key patterns for the propagation events

        """
        self.events[input_pattern] = bitpattern.Set(key_patterns)

    def get_probability(self, *others):
        if len(others) == 0:
            return self._get_unconditional_probability()
        else:
            return self._get_conditional_probability(others)

    def _get_unconditional_probability(self):
        pprops = []

        for input_pattern in self.events:
            key_patterns = self.events[input_pattern]
            pprops.append(key_patterns.count() / key_patterns.pattern_space_size())

        return sum(pprops) / len(pprops)

    def _get_conditional_probability(self, others):

        pprops = []

        for input_pattern in self.events:
            key_patterns = self.events[input_pattern]

            # TODO: skip if input pattern is not contained in some of self, others
            #       this is a solution only for others[0]
            if input_pattern not in others[0].events:
                continue

            total_intersection = others[0].events[input_pattern]
            for other in others[1:]:
                total_intersection = total_intersection.intersection(other.events[input_pattern])

            shared_patterns = key_patterns.intersection(total_intersection)
            pprops.append(shared_patterns.count() / total_intersection.count())

        return sum(pprops) / len(pprops)
