import subprocess
import signal
from .esignal import Signal
from .timeout import Timeout
from .retcode import Retcode

def _alarm_handler(signum, frame):
    raise Signal

def create_circuit(params):
    cmd = [
        "pysynth",
        "--saveDir", params["savedir"],
        "--benchName", params["name"],
        "--numBench", "1",
        "--numNodes", str(params["nodes"]),
        "--depth", str(params["depth"]),
        "--inputs", str(params["inputs"]),
        "--outputs", str(params["outputs"]),
        "--maxFanin", str(params["max_fanin"]),
        "--maxFanout", str(params["max_fanout"]),
        "--outType", "verilog"
    ]

    signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(params["timeout"])

    try:
        phandle = subprocess.Popen(cmd)
        output, _ = phandle.communicate()
        retcode = phandle.poll()
    except Signal:
        phandle.kill()
        raise Timeout(cmd=cmd, timeout=params["timeout"])
    except:
        raise
    else:
        signal.alarm(0)

    if retcode:
        raise Retcode(cmd, retcode, output=output)

    base = "%s_n%id%ii%io%i" % (params["name"], params["nodes"], params["depth"], params["inputs"], params["outputs"])
    path = "%s/%s/%s_0.v" % (params["savedir"], base, base)

    return path
