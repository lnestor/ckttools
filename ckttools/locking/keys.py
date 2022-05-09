import easylock
import locking.globals as GLOBALS
import pyverilog.vparser.ast as vast

def create_keys(moddef, start, count):
    keys = [create_key(moddef, number) for number in range(start, start + count)]
    return keys

def create_key(moddef, number):
    key_name = "keyIn_%i_%i" % (GLOBALS.pass_index, number)
    moddef.create_input(key_name)
    return key_name
