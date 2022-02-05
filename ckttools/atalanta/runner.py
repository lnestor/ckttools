import subprocess

def run_atalanta(bench_filename, fault_filename, log_filename, output_filename, num_samples=None):
    if num_samples is None:
        args = ["bin/atalanta", "-A", bench_filename, "-f", fault_filename, "-t", output_filename]
    else:
        args = ["bin/atalanta", "-D", str(num_samples), bench_filename, "-f", fault_filename, "-t", output_filename]

    rslt = subprocess.run(args, capture_output=True, text=True)

    if "error" in rslt.stderr.lower():
        raise RuntimeError(rslt.stderr)

    with open(log_filename, "w") as f:
        f.write("%s\n" % rslt.stdout)
        f.write("----\n")
        f.write(rslt.stderr)
