import subprocess

def run_atalanta(bench_filename, fault_filename, log_filename, output_filename):
    # rslt = subprocess.run(["bin/atalanta", "-A", bench_filename, "-f", fault_filename, "-t", output_filename], capture_output=True, text=True)
    rslt = subprocess.run(["bin/atalanta", "-A", bench_filename, "-f", fault_filename], capture_output=True, text=True)

    import pdb; pdb.set_trace()
    if "Error" in rslt.stderr:
        raise RuntimeError(rslt.stderr)

    with open(log_filename, "w") as f:
        f.write("%s\n" % rslt.stdout)
        f.write("----\n")
        f.write(rslt.stderr)
