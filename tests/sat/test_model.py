from ckttools.sat.model import extract
import pytest
import z3

@pytest.fixture()
def model():
    problem = z3.And(z3.Bool("a"), z3.Bool("b"))
    solver = z3.Solver()
    solver.add(problem)
    solver.check()
    return solver.model()

def test_extract(model):
    values = extract(model, ["b"])
    assert values["b"] == True
    assert "a" not in values

def test_extract_with_completion(model):
    values = extract(model, ["c"], completion=True)
    assert values["c"] == False
