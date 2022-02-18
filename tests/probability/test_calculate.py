import ckttools.probability as prob

def test_or_two_inputs():
    result = prob.or_([0.5, 0.25])
    assert result == 0.625

def test_or_three_inputs():
    result = prob.or_([0.5, 0.25, .125])
    assert result == 0.671875

def test_xor_two_inputs():
    result = prob.xor([0.4, 0.25])
    assert result - .45 < 1e-6

def test_xor_three_inputs():
    result = prob.xor([0.4, 0.25, 0.1])
    assert abs(result - .45) < 1e-2
