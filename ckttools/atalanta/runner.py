import subprocess

def run_atalanta(bench_filename, fault_filename, log_filename, output_filename):
    rslt = subprocess.run(["bin/atalanta", "-A", bench_filename, "-f", fault_filename, "-t", output_filename], capture_output=True, text=True)

    # TODO: parse stderr for error
    with open(log_filename, "w") as f:
        f.write("%s\n" % rslt.stdout)
        f.write("----\n")
        f.write(rslt.stderr)
