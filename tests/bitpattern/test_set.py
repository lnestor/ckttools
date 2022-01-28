from ckttools.bitpattern.set import Set

def test_pattern_length():
    pattern_set = Set(["101"])
    assert pattern_set.pattern_length() == 3

def test_total_possible_patterns():
    pattern_set = Set(["101"])
    assert pattern_set.total_possible_patterns() == 8

def test_count():
    pattern_set = Set(["101", "x00"])
    assert pattern_set.count() == 3

def test_intersection():
    pattern_set1 = Set(["1x1", "x00"])
    pattern_set2 = Set(["1xx", "000"])
    expected = Set(["1x1", "100", "000"])

    assert pattern_set1.intersection(pattern_set2) == expected
    assert pattern_set2.intersection(pattern_set1) == expected

def test_equals_when_not_equals():
    pattern_set1 = Set(["1x1", "x00"])
    pattern_set2 = Set(["1xx", "000"])
    assert not pattern_set1 == pattern_set2

def test_equals_when_equals():
    pattern_set1 = Set(["1x1", "x00"])
    pattern_set2 = Set(["x00", "1x1"])
    assert pattern_set1 == pattern_set2
