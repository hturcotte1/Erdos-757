"""Probe: sample depth-3 prefixes of (n,T,m) class-O DFS, run each with wall timeout, record nodes/solutions/CPU.
usage: python3 probe.py n T m nsample tl P  (run from repo root with PYTHONPATH=.)"""
import sys, os, json, subprocess, time, resource
from concurrent.futures import ThreadPoolExecutor
from e757 import ordered_dfs_split as S
n, T, m, ns, tl, P = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6])
here = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
pres = S.list_prefixes(n, T, m, 3)
N = len(pres)
step = max(1, N // ns)
idxs = list(range(step // 2, N, step))[:ns]
print("cell", n, T, m, "prefixes", N, "sampled", len(idxs), "list time %.1f" % (time.time() - t0), flush=True)
def run(i):
    cmd = ["nice", "-n", "5", S.BIN] + S._base_args(n, T, m, True) + ["mode=enum", "pre=" + pres[i], "tl=%g" % tl]
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    w0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    wall = time.time() - w0
    sols = [l[4:] for l in p.stdout.splitlines() if l.startswith("SOL")]
    d = [l for l in p.stdout.splitlines() if l.startswith("DONE")][-1]
    st = dict(kv.split("=") for kv in d.split()[1:])
    res = {"idx": i, "prefix": pres[i], "nodes": int(st["nodes"]), "solutions": int(st["solutions"]),
           "timed_out": int(st["timed_out"]), "time_wall": float(st["time"]), "wall": wall}
    if sols:
        open(os.path.join(here, "samples", "n%d_m%d_prefix_%05d.sol" % (n, m, i)), "w").write("\n".join(sols) + "\n")
    print(json.dumps(res), flush=True)
    return res
with ThreadPoolExecutor(P) as ex:
    out = list(ex.map(run, idxs))
json.dump({"n": n, "T": T, "m": m, "prefixes": N, "tl": tl, "results": out}, open(os.path.join(here, "raw_n%d_T%d_m%d.json" % (n, T, m)), "w"))
