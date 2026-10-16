"""Decide whether a class-O' pattern with (n=14, m=11, alpha<=8) exists (the non-saturated extremal case at n=14).
UNSAT would complete the count of extremal 14-point sets (L004)."""
import json, os, sys, time
from e757.cpsat_model import feasible_alpha_le, load_cores
repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 7000
t = time.time()
r, e, s = feasible_alpha_le(14, 8, m_exact=11, forbid_f7=True, use_hy=False, time_limit=tl, workers=3,
                            monotone=True, medial=True, cores=cores, core_lit_budget=2_000_000)
out = {"n": 14, "T": 8, "m_exact": 11, "result": r, "edges": e, "stats": str(s)[:2000], "wall": round(time.time() - t, 1)}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "n14_m11_result.json"), "w"), indent=1)
print("DONE", r, out["wall"], flush=True)
