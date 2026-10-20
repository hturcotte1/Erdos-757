#!/usr/bin/env python3
"""L015 / C7: non-vacuity controls for the checking code of C3-C5 (functions imported from v3_family.py and v4_h.py
by absolute path).
 (1) census: planting one point p = a + b - c (a, b, c from three different copies of S_3) must create a relation on
     4 distinct points, which the census must report;
 (2) literal 4-subset test: {2,3,5,8,...} style controls: {1,2,3,5} must FAIL (|B-B| = 9 < 11), {0,1,3,7} passes;
 (3) generic solver: h(A_base) = 8 (Ma-Tang's 14-point set), h of the third 12-point record = 7, h({1..9}) = 5
     (largest 3-AP-free subset of {1..9} has 5 points: e.g. {1,2,4,8,9}).
Run:  python3 -I v7_controls.py
"""
import sys
from itertools import combinations
sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/L015-round1/prover_rerun")
import v4_h  # noqa: E402

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]


def relations(A):
    A = sorted(A)
    bys = {}
    for i, a in enumerate(A):
        for b in A[i:]:
            bys.setdefault(a + b, []).append((a, b))
    return [(p, q) for v in bys.values() if len(v) > 1 for i, p in enumerate(v) for q in v[i + 1:]]


def min_BB(A):
    return min(len({u - v for u in B for v in B}) for B in combinations(sorted(A), 4))


K = 3
cps = [{x: 269 ** (K - j) * v4_h.N(j, x) for x in O} for j in range(K + 1)]
S = sorted(set().union(*[set(c.values()) for c in cps]))
a, b, c = cps[0][49], cps[2][75], cps[3][83]
p = a + b - c
assert p not in S
rel = relations(S + [p])
four = [r for r in rel if len(set(r[0]) | set(r[1])) == 4]
print("(1) planted p = a+b-c (copies 0, 2, 3) in S_3: relations", len(rel), "(S_3 alone: 36), on 4 distinct points:", len(four))
assert len(four) >= 1 and len(relations(S)) == 36
print("(2) min |B-B|: {1,2,3,5} ->", min_BB([1, 2, 3, 5]), " {0,1,3,7} ->", min_BB([0, 1, 3, 7]),
      " S_3 + planted point ->", min_BB(S + [p]))
assert min_BB([1, 2, 3, 5]) == 9 and min_BB([0, 1, 3, 7]) == 13 and min_BB(S + [p]) < 11
ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B12 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]
for name, A, hexp in (("A_base", ABASE, 8), ("12-pt record #3", B12, 7), ("{1..9}", list(range(1, 10)), 5)):
    v4_h.MEMO.clear()
    val = v4_h.solve(frozenset(A), frozenset(v4_h.ap_edges(A)))
    print(f"(3) generic solver: h({name}) = {val} (expected {hexp})")
    assert val == hexp
print("ALL CONTROLS OK")
