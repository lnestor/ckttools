import easylock
import locking.globals as GLOBALS
import pyverilog.vparser.ast as vast
from vast.create import create_input

def create_keys(moddef, start, count):
    keys = [create_key(moddef, number) for number in range(start, start + count)]
    return keys

def create_key(moddef, number):
    key_name = "keyIn_%i_%i" % (GLOBALS.pass_index, number)
    create_input(moddef, key_name)
    return key_name
