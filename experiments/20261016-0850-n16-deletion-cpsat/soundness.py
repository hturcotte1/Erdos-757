"""Solver-free soundness checks of the (b),(c) conditions on real extremal sets (n=14) and a hand-made n=16 example."""
import gzip, json, os, sys, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model16 import *
from e757.core import ap_edges

def pattern_of(vals):
    A = sorted(vals); idx = {x: i for i, x in enumerate(A)}
    return len(A), sorted((idx[a], idx[b], idx[c]) for a, b, c in ap_edges(A)) if False else None

def edges_of(vals):
    A = sorted(vals)
    idx = {x: i for i, x in enumerate(A)}
    return sorted((i, idx[(A[i] + A[k]) // 2], k) for i in range(len(A)) for k in range(i + 2, len(A))
                  if (A[i] + A[k]) % 2 == 0 and (A[i] + A[k]) // 2 in idx)

out = {}
abase = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
E = edges_of(abase)
ok, det = check_conditions(14, E, 8, "ge9")
print("A_base m=%d" % len(E), ok, {k: (v if not isinstance(v, list) else len(v)) for k, v in det.items()})
out["A_base"] = {"ok": ok, "m": len(E), "npairs_witness": det["npairs_witness"], "npairs_via_m": det["npairs_via_m"]}
rows = []
with gzip.open(os.path.join(REPO, "data/census_n14_m12_classes.jsonl.gz"), "rt") as f:
    for line in f:
        rows.append(json.loads(line))
rng = random.Random(1)
sample = rng.sample(rows, 60)
res = []
for r in sample:
    Er = edges_of(r["set"])
    assert sorted(map(tuple, r["edges"])) == Er, "census edges != recomputed"
    ok, det = check_conditions(14, Er, 8, "ge9")
    res.append((ok, len(det["pair_viol"]), det["npairs_via_m"]))
print("census sample: %d/%d satisfy; pairs-resolved-by-m counts %s" % (sum(r[0] for r in res), len(res), sorted(set(r[2] for r in res))))
out["census_sample"] = {"n": len(res), "ok": sum(r[0] for r in res), "npairs_via_m_values": sorted(set(r[2] for r in res))}
json.dump(out, open(os.path.join(HERE, "soundness_n14.json"), "w"), indent=1)
