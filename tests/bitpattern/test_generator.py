from ckttools.bitpattern.bit_pattern import BitPattern
from ckttools.bitpattern.generator import Generator

def test_size():
    gen = Generator(["x0x"])
    assert gen.size() == 4

def test_generate():
    gen = Generator(["x0x"])
    pattern1 = BitPattern("x0x")
    pattern2 = BitPattern(gen.generate())
    assert pattern2.is_subset_of(pattern1)

def test_sample_when_given_larger_than_sample_space():
    gen = Generator(["x01"])
    samples = [s for s in gen.sample(100)]
    assert len(samples) == 2

