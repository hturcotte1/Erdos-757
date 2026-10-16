"""Build the c_hyp table for n in a range: solver-only (no Henning-Yeo input), with and without F7.
Usage: python3 table.py NMIN NMAX [WORKERS] [TIME_LIMIT].  Writes results/table_n{n}.json per n."""
import json, os, sys, time
from e757.cpsat_model import solve_min_alpha, feasible_alpha_le
nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
w = int(sys.argv[3]) if len(sys.argv) > 3 else 4
tl = float(sys.argv[4]) if len(sys.argv) > 4 else 1200
MTL = float(sys.argv[5]) if len(sys.argv) > 5 else 60  # time limit per min-m step
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); os.makedirs(d, exist_ok=True)
for n in range(nmin, nmax + 1):
    row = {"n": n}
    for f7 in (True, False):
        t = time.time()
        a, e, s = solve_min_alpha(n, forbid_f7=f7, time_limit=tl, workers=w)
        key = "f7" if f7 else "nof7"
        row[key] = {"alpha": a, "edges": e, "optimal": s["optimal"], "time": round(time.time() - t, 1),
                    "solves": s["solves"], "per_T": {str(k): v for k, v in s["per_T"].items()}}
        # minimum number of edges among hypergraphs with alpha <= c_hyp: tighten m_max top-down
        if a is not None and s["optimal"]:
            tm = time.time()
            best_e, proved = e, len(e) <= 1
            while len(best_e) > 1:  # m = 0 gives alpha = n > c_hyp, so m = 1 is trivially optimal
                r, e2, s2 = feasible_alpha_le(n, a, forbid_f7=f7, m_max=len(best_e) - 1,
                                              time_limit=MTL, workers=w)
                if r == "SAT":
                    best_e = e2
                elif r == "UNSAT":
                    proved = True
                    break
                else:
                    break
            proved = proved or len(best_e) <= 1
            row[key]["min_m"] = len(best_e)
            row[key]["min_m_proved_optimal"] = proved
            row[key]["min_m_edges"] = best_e
            row[key]["min_m_time"] = round(time.time() - tm, 1)
        print(n, key, a, row[key].get("min_m"), row[key].get("min_m_proved_optimal"), row[key]["optimal"], row[key]["time"], flush=True)
    json.dump(row, open(os.path.join(d, "table_n%d.json" % n), "w"))
