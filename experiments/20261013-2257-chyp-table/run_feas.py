"""Decide 'exists hypergraph with alpha <= T on n vertices' (eager alpha encoding, lazy F7).
Usage: python3 run_feas.py N T F7(0/1) HY(0/1) TIME [WORKERS] [M_EXACT]. Writes results/feas_n{N}_T{T}_...json"""
import json, sys, os, time
from e757.cpsat_model import feasible_alpha_le
n, T, f7, hy, tl = int(sys.argv[1]), int(sys.argv[2]), bool(int(sys.argv[3])), bool(int(sys.argv[4])), float(sys.argv[5])
w = int(sys.argv[6]) if len(sys.argv) > 6 else 4
me = int(sys.argv[7]) if len(sys.argv) > 7 else None
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); os.makedirs(d, exist_ok=True)
t = time.time()
r, e, s = feasible_alpha_le(n, T, forbid_f7=f7, use_hy=hy, time_limit=tl, workers=w, m_exact=me)
out = {"n": n, "T": T, "f7_free": f7, "use_hy": hy, "m_exact": me, "result": r, "edges": e, "stats": s, "wall": round(time.time() - t, 1)}
json.dump(out, open(os.path.join(d, "feas_n%d_T%d_f7%d_hy%d_m%s.json" % (n, T, int(f7), int(hy), me)), "w"))
print("DONE", n, T, r, s, round(time.time() - t, 1))
