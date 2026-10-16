"""Timings of the ordered-midpoint DFS. Usage (repo root): python3 experiments/20261014-0005-ordered-dfs/run_timings.py
Writes results.json next to this file.  Python for n<=10, C for n<=12 (n=13 and n=16 are separate jobs, see README)."""
import json, os, time, sys
sys.path.insert(0, os.getcwd())
from e757.ordered_dfs import min_alpha
from e757.ordered_dfs_c import run
here = os.path.dirname(os.path.abspath(__file__))
res = {"load": open("/proc/loadavg").read().split()[:3], "py": {}, "c": {}}
for n in range(5, 11):
    for f7 in (1, 0):
        t = time.time(); a, e, st = min_alpha(n, forbid_f7=bool(f7))
        res["py"]["n%d_f7%d" % (n, f7)] = {"alpha": a, "edges": e, "nodes": st["nodes"], "sec": round(time.time() - t, 2)}
        print("py", n, f7, a, st["nodes"], round(time.time() - t, 2), flush=True)
for n in range(5, 13):
    for f7 in (1, 0):
        t = time.time(); sols, st = run(n=n, mode="min", f7=f7, progress=0)
        a, e = sols[-1]
        res["c"]["n%d_f7%d" % (n, f7)] = {"alpha": a, "edges": e, "nodes": int(st["nodes"]), "sec": round(time.time() - t, 2)}
        print("c", n, f7, a, st["nodes"], round(time.time() - t, 2), flush=True)
json.dump(res, open(os.path.join(here, "results.json"), "w"), indent=1)
