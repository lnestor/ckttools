from ckttools.bitpattern.bit_pattern import BitPattern

def test_len():
    pattern = BitPattern("101")
    assert len(pattern) == 3

def test_count_with_no_unknowns():
    pattern = BitPattern("101")
    assert pattern.count() == 1

def test_count_with_unknowns():
    pattern = BitPattern("1xx")
    assert pattern.count() == 4

def test_is_subset_of_when_not_subset():
    pattern1 = BitPattern("101")
    pattern2 = BitPattern("11x")
    assert not pattern1.is_subset_of(pattern2)

def test_is_subset_of_when_subset():
    pattern1 = BitPattern("101")
    pattern2 = BitPattern("1xx")
    assert pattern1.is_subset_of(pattern2)

def test_intersection():
    pattern1 = BitPattern("1x1")
    pattern2 = BitPattern("10x")
    expected = BitPattern("101")
    assert pattern1.intersection(pattern2) == expected
    assert pattern2.intersection(pattern1) == expected

