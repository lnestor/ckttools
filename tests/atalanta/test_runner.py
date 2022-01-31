from ckttools.atalanta.runner import run_atalanta
import pytest

BAD_BENCH = """# example
#

INPUT(in1)
INPUT(in2)
INPUT(in3)
OUTPUT(out1)

out1 = and(in1, in2)
"""

GOOD_BENCH = """# example
#

INPUT(in1)
INPUT(in2)
OUTPUT(out1)

out1 = and(in1, in2)
"""

GOOD_FAULT = "out1 /0"
BAD_FAULT = "out2 /1"

def test_run_atalanta_with_bench_error(tmp_path):
    bench_file = tmp_path / "example.bench"
    fault_file = tmp_path / "example.flt"
    log_file = tmp_path / "example.log"
    output_file = tmp_path / "example.test"

    bench_file.write_text(BAD_BENCH)
    fault_file.write_text(GOOD_FAULT)

    with pytest.raises(RuntimeError):
        run_atalanta(bench_file, fault_file, log_file, output_file)

def test_run_atalanta_with_fault_error(tmp_path):
    bench_file = tmp_path / "example.bench"
    fault_file = tmp_path / "example.flt"
    log_file = tmp_path / "example.log"
    output_file = tmp_path / "example.test"

    bench_file.write_text(GOOD_BENCH)
    fault_file.write_text(BAD_FAULT)

    with pytest.raises(RuntimeError):
        run_atalanta(bench_file, fault_file, log_file, output_file)
