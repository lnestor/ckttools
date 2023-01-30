import subprocess
import os

def synthesize(path):
    savedir, filename = os.path.split(path)
    output_filename = "%s_syn.v" % filename[0:-2]

    commands = [
        "read_verilog %s" % path,
        "clean",
        "opt",
        "techmap",
        "opt",
        "write_verilog -noattr %s/%s" % (savedir, output_filename)
    ]

    subprocess.run(["yosys"], input="\n".join(commands), text=True)
    return "%s/%s" % (savedir, output_filename)
