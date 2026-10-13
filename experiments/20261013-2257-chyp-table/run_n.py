"""Usage: python3 run_n.py N F7(0/1) TIME_LIMIT [WORKERS] [USE_HY(0/1)]. Writes results/n{N}_f7{F7}_hy{HY}.json"""
import json, sys, os, time
from e757.cpsat_model import solve_min_alpha
n, f7, tl = int(sys.argv[1]), bool(int(sys.argv[2])), float(sys.argv[3])
w = int(sys.argv[4]) if len(sys.argv) > 4 else 4
hy = bool(int(sys.argv[5])) if len(sys.argv) > 5 else False
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); os.makedirs(d, exist_ok=True)
t = time.time()
a, e, s = solve_min_alpha(n, forbid_f7=f7, time_limit=tl, workers=w, verbose=True, use_hy=hy)
s["per_T"] = {str(k): v for k, v in s["per_T"].items()}
json.dump({"n": n, "f7_free": f7, "use_hy": hy, "alpha": a, "edges": e, "stats": s, "wall": round(time.time() - t, 1)},
          open(os.path.join(d, "n%d_f7%d_hy%d.json" % (n, int(f7), int(hy))), "w"))
print("DONE", n, f7, a, s["optimal"], round(time.time() - t, 1))
