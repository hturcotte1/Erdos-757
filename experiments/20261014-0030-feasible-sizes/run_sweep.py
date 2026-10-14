"""Sweep of the record-feasible sizes with realizability-CEGAR (e757.cpsat_model.solve_realizable).
Constraints: linearity, midpoint injectivity, F7 (lazy), K30 monotone, K31 medial, forbidden cores
(literal budget 1e6), alpha<=T encoded eagerly (n=18) or hybrid (random sample of (T+1)-sets + lazy cuts).
Every failure of realize_exact is turned into a minimal core and learnt (sound for every m).
Usage: python3 run_sweep.py [TIME_PER_SIZE_S] [WORKERS]   (resumable: skips cases whose results JSON exists)"""
import json, os, subprocess, sys, time
from e757.cpsat_model import solve_realizable, load_cores
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 3600
w = int(sys.argv[2]) if len(sys.argv) > 2 else 2
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.abspath(os.path.join(here, "..", ".."))
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
# n, T, m_exact, m_min, eager, time limit.  n=23 / n=25 are split into one case per m (20 min each).
CASES = [
    (18, 10, 16, 0, True, tl),
    (20, 11, 18, 0, 20000, tl),
    (22, 12, 20, 0, 20000, tl),
    (23, 13, 19, 0, 20000, tl / 3), (23, 13, 20, 0, 20000, tl / 3), (23, 13, 21, 0, 20000, tl / 3),
    (25, 14, 21, 0, 20000, tl / 3), (25, 14, 22, 0, 20000, tl / 3), (25, 14, 23, 0, 20000, tl / 3),
]
for n, T, me, mm, eager, tl_case in CASES:
    outp = os.path.join(here, "results", "n%d_T%d_m%d.json" % (n, T, me))
    if os.path.exists(outp):  # resumable: finished cases are skipped
        print("SKIP", outp, flush=True)
        continue
    t0 = time.time()
    print("START", n, T, me, mm, eager, flush=True)
    st, info = solve_realizable(n, T, m_exact=me, m_min=mm, time_limit=tl_case, workers=w, eager=eager,
                                monotone=True, medial=True, cores=cores, core_lit_budget=1_000_000,
                                verbose=True)
    out = {"n": n, "T": T, "m_exact": me, "m_min": mm, "eager": eager, "status": st,
           "stats": info["stats"], "wall_s": round(time.time() - t0, 1)}
    if st == "SAT":
        out.update(edges=info["edges"], set=info["set"], alpha_of_pattern=info.get("alpha"))
        r = subprocess.run([sys.executable, repo + "/scripts/new_claim.py", "--slug", "cpsat-n%d-T%d" % (n, T),
                            "--set", ",".join(str(x) for x in info["set"])], capture_output=True, text=True, cwd=repo)
        out["new_claim_stdout"] = r.stdout[-2000:]
        out["new_claim_stderr"] = r.stderr[-1000:]
    json.dump(out, open(outp + ".tmp", "w")); os.replace(outp + ".tmp", outp)
    print("DONE", n, T, st, out["wall_s"], flush=True)
