#!/usr/bin/env python3 -I
"""Referee verifier (round 2) for claim C003-reader-5-9-K6.  Pure Python, no project imports.

Stages:
  A. parse the claim file strictly (all entries must be JSON integers), distinctness, sort
  B. rebuild S_6 from the stated definition (O, phi) with Fractions and compare EXACTLY
  C. (4,5)-property: every one of the C(65,4) 4-subsets has >= 5 distinct absolute differences
  D. weak Sidon: all sums x+y (x<y) distinct
  E. conflict structure straight from the definition: all pairs of distinct 2-subsets with equal
     positive difference; classify (3-AP / 4-point parallelogram); linearity of the 3-AP hypergraph
  F. witness: 37 distinct elements of the set, all positive differences distinct
  G. exact Fraction comparison 37/65 vs 4/7
Writes verify_c003.json next to this file.
"""
import itertools
import json
import sys
import time
from fractions import Fraction
from math import lcm

HERE = "/home/user/Erdos-757/experiments/referee/C003-round2"
CLAIM = "/home/user/Erdos-757/results/claims/C003-reader-5-9-K6.json"
out = {}
t0 = time.time()

# ---- A. strict parse --------------------------------------------------------------------------
raw = json.load(open(CLAIM))
assert raw["id"] == "C003-reader-5-9-K6" and raw["type"] == "construction"
assert all(type(x) is int for x in raw["set"]), "non-integer entry in set"
A = sorted(raw["set"])
n = len(A)
assert len(set(A)) == n, "duplicate points"
assert len(raw["set"]) == 65
out["n"] = n
out["set_is_sorted_in_file"] = raw["set"] == A
out["claimed_h"] = raw["claimed_h"]
print(f"A: n={n}, distinct, all ints, min={A[0]} max={A[-1]}")

# ---- B. rebuild from the definition -----------------------------------------------------------
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
def phi(x):
    return Fraction(101) + Fraction(18, 269) * x
S = set()
level = {}
for j in range(7):
    for x in O:
        p = Fraction(x)
        for _ in range(j):
            p = phi(p)
        S.add(p)
        level.setdefault(p, j)          # minimal level of each point
S = sorted(S)
den = 1
for p in S:
    den = lcm(den, p.denominator)
ints = [p * den for p in S]
assert all(v.denominator == 1 for v in ints)
ints = [int(v) for v in ints]
out["rebuild_n"] = len(S)
out["rebuild_scale"] = den
out["rebuild_scale_is_269^6"] = (den == 269 ** 6)
out["rebuild_equals_claim_set"] = (ints == A)
print(f"B: rebuilt |S_6|={len(S)} scale={den} (=269^6: {den == 269**6}) equals claim set: {ints == A}")
assert ints == A
lvl = [level[Fraction(a, den)] for a in A]
out["minimal_levels_sorted"] = lvl
print("B: minimal levels in sorted order:", lvl)

# ---- C. (4,5)-property by brute force ----------------------------------------------------------
t = time.time()
cnt = 0
worst = 7
bad = None
for q in itertools.combinations(A, 4):
    a, b, c, d = q
    ds = {b - a, c - a, d - a, c - b, d - b, d - c}   # sorted, so all positive
    cnt += 1
    if len(ds) < worst:
        worst = len(ds)
    if len(ds) < 5:
        bad = q
        break
out["four_subsets_checked"] = cnt
out["min_distinct_distances_over_4subsets"] = worst
out["is_45_set"] = bad is None
print(f"C: checked {cnt} 4-subsets (expected {65*64*63*62//24}); min #distinct distances = {worst}; (4,5): {bad is None}; {time.time()-t:.1f}s")
assert bad is None and cnt == 677040

# ---- D. weak Sidon ----------------------------------------------------------------------------
sums = [x + y for x, y in itertools.combinations(A, 2)]
out["weak_sidon"] = len(sums) == len(set(sums))
print("D: weak Sidon:", out["weak_sidon"])
assert out["weak_sidon"]

# ---- E. conflict structure from the definition --------------------------------------------------
bydiff = {}
for i in range(n):
    for j in range(i + 1, n):
        bydiff.setdefault(A[j] - A[i], []).append((i, j))
conflicts = []          # frozensets of point indices that cannot all lie in a Sidon subset
for d, prs in bydiff.items():
    if len(prs) > 1:
        for p, q in itertools.combinations(prs, 2):
            conflicts.append(frozenset(p) | frozenset(q))
sizes = {}
for c in conflicts:
    sizes[len(c)] = sizes.get(len(c), 0) + 1
out["conflict_sizes"] = sizes
max_mult = max(len(v) for v in bydiff.values())
out["max_multiplicity_of_a_difference"] = max_mult
aps = sorted(set(c for c in conflicts if len(c) == 3))
# every 3-conflict must be a genuine 3-AP {a,b,c} with a+c=2b
for c in aps:
    a, b, cc = sorted(c)
    assert A[a] + A[cc] == 2 * A[b]
# and conversely every 3-AP (midpoint lookup with integers) must appear
pos = {v: i for i, v in enumerate(A)}
aps2 = set()
for i in range(n):
    for k in range(i + 2, n):
        s = A[i] + A[k]
        if s % 2 == 0 and (s // 2) in pos:
            aps2.add(frozenset((i, pos[s // 2], k)))
assert set(aps) == aps2
m = len(aps)
out["num_3APs"] = m
# linearity: two APs share <= 1 point
lin = all(len(e & f) <= 1 for e, f in itertools.combinations(aps, 2))
out["linear"] = lin
deg = [0] * n
for e in aps:
    for v in e:
        deg[v] += 1
out["degree_sequence_sorted"] = sorted(deg, reverse=True)
mids = set()
for e in aps:
    a, b, c = sorted(e)
    mids.add(b)
out["num_midpoints"] = len(mids)
out["non_midpoints"] = [A[i] for i in range(n) if i not in mids]
# level span of each AP (minimal levels)
spans = {}
for e in aps:
    ls = [lvl[v] for v in e]
    sp = max(ls) - min(ls)
    spans[sp] = spans.get(sp, 0) + 1
out["AP_level_spans"] = spans
print(f"E: conflicts by size {sizes}; max multiplicity of a difference {max_mult}; 3-APs m={m}; linear={lin}; midpoints={len(mids)}; non-midpoints={out['non_midpoints']}; level spans {spans}")
print("E: degree sequence:", out["degree_sequence_sorted"])
assert sizes.get(4, 0) == 0 and lin

# ---- F. witness ----------------------------------------------------------------------------------
W = raw["witness_sidon_subset"]
assert all(type(x) is int for x in W)
Ws = sorted(W)
assert len(set(Ws)) == len(Ws) and set(Ws) <= set(A)
wd = [y - x for x, y in itertools.combinations(Ws, 2)]
out["witness_size"] = len(Ws)
out["witness_is_sidon"] = len(wd) == len(set(wd))
out["witness_sums_distinct"] = len(set(x + y for x, y in itertools.combinations_with_replacement(Ws, 2))) == len(Ws) * (len(Ws) + 1) // 2
print(f"F: witness size {len(Ws)}, subset of A, Sidon (differences distinct): {out['witness_is_sidon']}, sums distinct: {out['witness_sums_distinct']}")
assert out["witness_is_sidon"] and out["witness_sums_distinct"] and len(Ws) == 37

# ---- G. exact ratio ---------------------------------------------------------------------------------
r = Fraction(37, 65)
out["ratio"] = str(r)
out["ratio_lt_4_7"] = r < Fraction(4, 7)
out["ratio_margin"] = str(Fraction(4, 7) - r)
print(f"G: 37/65 = {r} < 4/7: {r < Fraction(4,7)}; 4/7 - 37/65 = {Fraction(4,7)-r}; 37*7={37*7} vs 4*65={4*65}")
assert r < Fraction(4, 7)

# save the conflict hypergraph for the solvers
json.dump({"A": A, "aps": [sorted(e) for e in aps], "levels": lvl}, open(f"{HERE}/hypergraph.json", "w"))
out["elapsed_s"] = round(time.time() - t0, 1)
json.dump(out, open(f"{HERE}/verify_c003.json", "w"), indent=1)
print("ALL STAGES PASSED; elapsed", out["elapsed_s"], "s")
