from ckttools.atalanta.runner import run_atalanta
import pytest

BAD_BENCH = """# example
#

INPUT(in1)
INPUT(in2)
OUTPUT(out1)

out1 = and(in1, in2)
"""

GOOD_FAULT = "out1 /0"

@pytest.mark.skip(reason="Atalanta can't read the files")
def test_run_atalanta_with_bench_error(tmpdir):
    # bench_file = tmp_path / "example.bench"
    # fault_file = tmp_path / "example.flt"
    # log_file = tmp_path / "example.log"
    # output_file = tmp_path / "example.test"

    # bench_file.write_text(BAD_BENCH)
    # fault_file.write_text(GOOD_FAULT)

    bench_file = tmpdir.join("example.bench")
    bench_file.write(BAD_BENCH)
    fault_file = tmpdir.join("example.flt")
    log_file = tmpdir.join("example.log")
    output_file = tmpdir.join("example.test")

    with pytest.raises(RuntimeError):
        run_atalanta(bench_file, fault_file, log_file, output_file)

@pytest.mark.skip(reason="Atalanta can't read the files")
def test_run_atalanta_with_fault_error():
    raise
