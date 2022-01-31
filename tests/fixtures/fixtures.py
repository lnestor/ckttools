import os

def get_fixture_path(filename):
    return os.path.abspath(os.path.join("tests/fixtures", filename) + ".v")

