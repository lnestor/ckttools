from ckttools.vast.create import create_ilist

def test_create_ilist():
    ilist = create_ilist("and", "AND0", "output", ["input1", "input2"])

    assert ilist.children()[0].module == "and"
    assert ilist.children()[0].children()[0].children()[0].name == "output"
    assert ilist.children()[0].children()[1].children()[0].name == "input1"
    assert ilist.children()[0].children()[2].children()[0].name == "input2"
