"""n=16, T=9 via realizability-CEGAR (solve_realizable), m in {13,14}. Usage: run_realizable.py M_MIN M_MAX TIME WORKERS"""
import json, os, subprocess, sys, time
from e757.cpsat_model import solve_realizable, load_cores
mmin, mmax, tl, w = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.abspath(os.path.join(here, "..", ".."))
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
t0 = time.time()
st, info = solve_realizable(16, 9, m_min=mmin, m_max=mmax, time_limit=tl, workers=w, eager=True,
                            monotone=True, medial=True, cores=cores, core_lit_budget=1_000_000, verbose=True)
out = {"n": 16, "T": 9, "m_min": mmin, "m_max": mmax, "status": st, "stats": info["stats"], "wall_s": round(time.time() - t0, 1)}
if st == "SAT":
    out.update(edges=info["edges"], set=info["set"])
    r = subprocess.run([sys.executable, repo + "/scripts/new_claim.py", "--slug", "cpsat-n16-T9", "--set", ",".join(map(str, info["set"]))], capture_output=True, text=True, cwd=repo)
    out["new_claim_stdout"] = r.stdout[-2000:]
json.dump(out, open(os.path.join(here, "results", "realizable_n16_T9_m%d_%d.json" % (mmin, mmax)), "w"))
print("DONE", st, out["wall_s"])
