from ckttools.vast.create import *
from ckttools.vast.search import get_input_names, get_wire_names
import pytest
import pyverilog.vparser.ast as vast

@pytest.fixture
def moddef():
    return vast.ModuleDef("Example", vast.Paramlist([]), vast.Portlist([]), [])

def test_create_ilist(moddef):
    ilist_output = create_ilist(moddef, "and", "AND0", "output", ["input1", "input2"])
    ilist = moddef.items[1]

    assert ilist.children()[0].module == "and"
    assert ilist.children()[0].children()[0].children()[0].name == "output"
    assert ilist.children()[0].children()[1].children()[0].name == "input1"
    assert ilist.children()[0].children()[2].children()[0].name == "input2"
    assert ilist_output == "output"
    assert get_wire_names(moddef) == ["output"]

def test_create_ilist_dont_add_output_wire(moddef):
    ilist = create_ilist(moddef, "and", "AND0", "output", ["input1", "input2"], add_output_wire=False)
    assert get_wire_names(moddef) == []

def test_create_input(moddef):
    input_decl = create_input(moddef, "test_input")
    assert get_input_names(moddef) == ["test_input"]
    assert moddef.items[0] == input_decl
    assert moddef.children()[1].ports[0] == vast.Port("test_input", None, None, None)

def test_create_wire(moddef):
    wire_decl = create_wire(moddef, "test_wire")
    assert get_wire_names(moddef) == ["test_wire"]
    assert moddef.items[0] == wire_decl
