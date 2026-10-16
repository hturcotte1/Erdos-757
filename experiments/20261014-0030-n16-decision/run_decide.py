"""n=16-style decision: does an ordered midpoint hypergraph exist with alpha <= T and exactly M edges
(F7-free, monotone K30, medial K31, forbidden cores)?  If yes, enumerate ALL (lex-minimal under
reflection) and run each through e757.realizability.realize_exact.
Usage: python3 run_decide.py N T M TIME [WORKERS] [LIT_BUDGET] [OUTTAG]"""
import gzip, json, os, sys, time
from e757.cpsat_model import enumerate_solutions, load_cores
from e757.realizability import realize_exact
n, T, M, tl = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
w = int(sys.argv[5]) if len(sys.argv) > 5 else 4
budget = int(float(sys.argv[6])) if len(sys.argv) > 6 else 2_500_000
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.abspath(os.path.join(here, "..", ".."))
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
res_dir = os.path.join(here, "results"); os.makedirs(res_dir, exist_ok=True)
tag = "n%d_T%d_m%d" % (n, T, M)
t0 = time.time()
sols_path = os.path.join(res_dir, tag + "_solutions.jsonl.gz")
count, _, status = enumerate_solutions(n, T, M, time_limit=tl, workers=w, out_path=sols_path,
                                       monotone=True, medial=True, cores=cores, core_lit_budget=budget)
info = enumerate_solutions.last
out = {"n": n, "T": T, "m_exact": M, "status": status, "n_solutions_up_to_reflection": count,
       "constraints": info["constraints"], "core_literal_budget": budget, "workers": w,
       "wall_s": round(time.time() - t0, 1), "realizable": []}
if count:
    for line in gzip.open(sols_path, "rt"):
        rec = json.loads(line)
        r = realize_exact(n, [tuple(e) for e in rec["edges"]])
        if r[0]:
            out["realizable"].append({"edges": rec["edges"], "set": r[1]})
        else:
            out.setdefault("reasons", {}).setdefault(r[1], 0)
            out["reasons"][r[1]] += 1
    out["n_realizable"] = len(out["realizable"])
json.dump(out, open(os.path.join(res_dir, tag + ".json"), "w"))
print("DONE", tag, status, "solutions", count, "realizable", len(out["realizable"]), out["constraints"], out["wall_s"])
