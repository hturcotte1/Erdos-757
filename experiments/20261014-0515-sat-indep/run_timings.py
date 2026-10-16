"""Timings of e757.sat_indep for n=8..13 at T = min alpha (SAT) and T-1 (UNSAT proof), m free.
Usage: python3 run_timings.py [solver] [time_limit_s]"""
import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, sys, time
sys.path.insert(0, "/home/user/Erdos-757")
from e757.sat_indep import decide

solver = sys.argv[1] if len(sys.argv) > 1 else "glucose4"
TL = float(sys.argv[2]) if len(sys.argv) > 2 else 400
MIN_ALPHA = {8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8}
rows = []
for n, T in MIN_ALPHA.items():
    for TT in (T, T - 1):
        t = time.time()
        st, r = decide(n, TT, None, solver=solver, time_limit=TL)
        dt = time.time() - t
        extra = {} if st == "SAT" else {k: r[k] for k in ("iterations", "f7_nogoods", "core_nogoods", "nclauses")}
        row = dict(n=n, T=TT, status=st, seconds=round(dt, 2), solver=solver, **extra)
        rows.append(row)
        print(json.dumps(row), flush=True)
json.dump(rows, open(f"results/timings_{solver}.json", "w"), indent=1)
