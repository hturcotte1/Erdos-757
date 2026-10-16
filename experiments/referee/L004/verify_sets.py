"""Referee L004, check S: every stored census set (post/real_*.json.gz) re-verified from the definitions (own code):
distinct integers; (4,5) (every 4-subset has >= 5 distinct distances); its rank-order 3-AP pattern equals the stored
edges; m = 12; h = 8 by exhaustive Sidon search; alpha of the 3-AP hypergraph = 8; h/n > 4/7 is false-equal (8/14 = 4/7);
affine normal forms pairwise distinct; A_base present. Also writes 25 random sets as judge claim files.
usage: python3 verify_sets.py POSTDIR SPOTDIR"""
import sys, gzip, json, glob, os, random, collections, itertools
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "realize14.py")).read().split("if __name__")[0])
POST, SPOT = sys.argv[1], sys.argv[2]
rows = []
for f in sorted(glob.glob(os.path.join(POST, "real_*.json.gz"))):
    rows += json.load(gzip.open(f, "rt"))["real"]
print("stored sets", len(rows))
prob = collections.Counter(); nfs = []
for r in rows:
    S = r["set"]
    if not all(isinstance(x, int) for x in S): prob["non_int"] += 1
    if len(set(S)) != 14 or sorted(S) != S: prob["not_distinct_sorted"] += 1
    if not is45(S): prob["not45"] += 1
    aps = three_aps(sorted(S))
    if aps != set(tuple(e) for e in r["edges"]): prob["pattern_mismatch"] += 1
    if len(aps) != 12: prob["m_not_12"] += 1
    h = sidon_max(S); al = alpha_ap(14, aps)
    if h != 8: prob["h_not_8"] += 1
    if al != 8: prob["alpha_not_8"] += 1
    if Fraction(h, 14) < Fraction(4, 7): prob["RECORD"] += 1
    nfs.append(normal_form(S))
AB = (0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056)
print("distinct normal forms", len(set(nfs)), "A_base present", normal_form(AB) in set(nfs))
print("max coordinate in normal forms", max(max(v) for v in nfs))
print("PROBLEMS", dict(prob))
os.makedirs(SPOT, exist_ok=True)
random.seed(4004)
for q, r in enumerate(random.sample(rows, 25)):
    json.dump({"id": "L004ref%02d" % q, "type": "construction", "set": r["set"], "claimed_h": 8,
               "notes": "referee L004 spot check (census class)"}, open(os.path.join(SPOT, "L004ref%02d.json" % q), "w"))
json.dump({"id": "L004refAB", "type": "construction", "set": list(AB), "claimed_h": 8, "notes": "A_base"},
          open(os.path.join(SPOT, "L004refAB.json"), "w"))
