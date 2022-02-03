import sys, os

tests_dirname = os.path.dirname(os.path.abspath(__file__))
code_dirname = os.path.abspath(os.path.join(tests_dirname, "../ckttools"))

sys.path.append(code_dirname)
