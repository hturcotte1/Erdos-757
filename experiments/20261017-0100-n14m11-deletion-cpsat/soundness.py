"""Solver-free soundness check of constraints (b),(c) (unconditional pair witnesses) at (14,12,T=8) on A_base and 50 random census classes."""
import gzip, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model14 import *

def edges_of(vals):
    A = sorted(vals); idx = {x: i for i, x in enumerate(A)}
    return sorted((i, idx[(A[i] + A[k]) // 2], k) for i in range(len(A)) for k in range(i + 2, len(A))
                  if (A[i] + A[k]) % 2 == 0 and (A[i] + A[k]) // 2 in idx)
abase = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
out = {}
E = edges_of(abase); ok, det = check14(14, E, 8)
print("A_base m=%d ok=%s %s" % (len(E), ok, det)); out["A_base"] = {"m": len(E), "ok": ok, "det": det}
rows = [json.loads(l) for l in gzip.open(os.path.join(REPO, "data/census_n14_m12_classes.jsonl.gz"), "rt")]
rng = random.Random(7); sample = rng.sample(range(len(rows)), 50); res = []
for i in sample:
    r = rows[i]; Er = edges_of(r["set"]); assert sorted(map(tuple, r["edges"])) == Er
    ok, det = check14(14, Er, 8); res.append({"row": i, "ok": ok})
    if not ok: print("VIOLATION row", i, det)
out["census_sample"] = {"seed": 7, "n": len(res), "n_ok": sum(x["ok"] for x in res), "rows": sample}
print("census sample %d/%d ok (m=12 rows: %s)" % (out["census_sample"]["n_ok"], len(res), {len(rows[i]["edges"]) for i in sample}))
json.dump(out, open(os.path.join(HERE, "soundness.json"), "w"), indent=1)
