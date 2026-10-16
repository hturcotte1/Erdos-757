"""Resumable n=16 case split with e757.sat_indep (independent cross-check of experiments/20261014-0450-n16-cases).
30 cases: m in {13,14} x vertex1 in {0 (vertex 1 not a midpoint), 2..15 (edge (0,1,k))}, T=9.
Each case: enumerate_all (all solutions; COMPLETE with 0 solutions = UNSAT) -> results/case_m{M}_k{K}.json
(written atomically; existing files are skipped, so the script can be restarted).
Usage: python3 run_cases.py [time_limit_s=3000] [only_m] [only_k]
"""
import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, os, sys, time
sys.path.insert(0, "/home/user/Erdos-757")
from e757.sat_indep import enumerate_all

TL = float(sys.argv[1]) if len(sys.argv) > 1 else 3000
only_m = int(sys.argv[2]) if len(sys.argv) > 2 else None
only_k = int(sys.argv[3]) if len(sys.argv) > 3 else None
N, T = 16, 9
os.makedirs("results", exist_ok=True)
for m in (13, 14):
    for k in [0] + list(range(2, N)):
        if (only_m is not None and m != only_m) or (only_k is not None and k != only_k):
            continue
        out = f"results/case_m{m}_k{k}.json"
        if os.path.exists(out):
            continue
        t = time.time()
        sols, st = enumerate_all(N, T, m, vertex1=k, time_limit=TL, return_stats=True, max_solutions=1000)
        rec = dict(n=N, T=T, m=m, vertex1=k, status=st["status"], n_solutions=len(sols),
                   solutions=[list(map(list, s)) for s in sols],
                   seconds=round(time.time() - t, 1),
                   stats={x: st[x] for x in ("nclauses", "iterations", "f7_nogoods", "core_nogoods", "solver")})
        json.dump(rec, open(out + ".tmp", "w"))
        os.replace(out + ".tmp", out)
        print(m, k, rec["status"], rec["n_solutions"], rec["seconds"], flush=True)
