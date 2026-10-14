"""Referee L003 round 2: judge spot-check claim files.  For n = 6..11: 3 random (seeded) saturated classes with h = f(n)
from MY enumeration output, and the gluing witness of nonsat.py (n = 6, 7, 9, 11) plus one perturbed member x0 + s v.
Writes experiments/referee/L003-round2/spot/<id>.json (read by judge/judge.py; the judge is used read-only)."""
import os, sys, json, gzip, random
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nonsat as ns

F = {6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7}
SRC = {6: "sat_n6_k0_l0.txt", 7: "sat_n7_k0_l0.txt", 8: "sat_n8_k0_l0.txt", 9: "sat_n9_k0_l0.txt", 10: "sat_n10_k0_l0.txt",
       11: "sat_n11_k1_l1.txt.gz"}
out = os.path.join(HERE, "spot"); os.makedirs(out, exist_ok=True)
random.seed(4242)
k = 0


def dump(cid, s, h, note):
    global k
    sv = [str(Fr(t)) if Fr(t).denominator != 1 else int(t) for t in s]
    json.dump({"id": cid, "type": "construction", "set": sv, "claimed_h": h, "notes": note}, open(os.path.join(out, cid + ".json"), "w"))
    k += 1


for n in range(6, 12):
    p = os.path.join(HERE, SRC[n]); op = gzip.open if p.endswith(".gz") else open
    cl = [line.split()[2:] for line in op(p, "rt") if line.startswith("S ") and int(line.split()[1]) == F[n]]
    for i, s in enumerate(random.sample(cl, min(3, len(cl)))):
        dump("refL003r2_sat%d_%d" % (n, i), [int(t) for t in s], F[n], "referee L003 round 2: saturated class from satcheck")
rec = json.load(open(os.path.join(ns.ROOT, "data", "small_records.json")))["sets"]
S6 = [int(t) for t in open(os.path.join(HERE, "sat_n6_k0_l0.txt")).read().split("\n")[0].split()[2:]]
gl = {6: [0, 1, 2], 7: [0, 1, 2, 5], 9: S6, 11: rec["8"]["set"]}
def perturbed(x0):
    """a member x0 + s v of the family of nonsat.py (s = 1/97 scaled into the order interval), re-checked from definitions."""
    x0 = sorted(Fr(t) for t in x0); n = len(x0); P = ns.aps(x0)
    rows = []
    for (l, j, r) in P:
        row = [Fr(0)] * n; row[l] += 1; row[r] += 1; row[j] -= 2; rows.append(row)
    basis, rk = ns.nullspace(rows, n)
    v = next(b for b in basis if ns.rank([x0, [Fr(1)] * n, b], n) == 3)
    s = Fr(1, 97)
    while True:
        xs = [a + s * b for a, b in zip(x0, v)]
        if sorted(xs) == xs and len(set(xs)) == n and ns.is45(xs) and ns.aps(xs) == P and ns.h_def(xs) == F[n]:
            return xs
        s /= 3


for n, B in sorted(gl.items()):
    C, q, t = ns.find_glue([0, 1, 2], B, n)
    dump("refL003r2_glue%d" % n, C, F[n], "referee L003 round 2: {0,1,2} glued to %s*B+%s" % (q, t))
    dump("refL003r2_glue%d_pert" % n, perturbed(C), F[n], "referee L003 round 2: perturbed member of the gluing family")
for key in ("8", "11"):
    dump("refL003r2_rec%s_pert" % key, perturbed(rec[key]["set"]), F[int(key)], "referee L003 round 2: perturbed member of the record-set family")
print("wrote", k, "claim files to", out)
