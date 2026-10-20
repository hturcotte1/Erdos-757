#!/usr/bin/env python3
"""Referee round 3, L015: census by DIFFERENCES (not sums) of I_K, K<=KMAX: group all pairs a<b by b-a;
every class must have size <= 2, and a class of size 2 must be two pairs sharing a point (a 3-AP),
never two disjoint pairs (which would be a relation on 4 distinct points / a parallelogram).
Also: the number of 3-APs found this way must be 9(K+1), and for every class of size 2 the shared
point must be the middle.  Usage: r8_diff_census.py KMAX"""
from itertools import combinations
import sys
KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
def N(x, j):
    v = x
    for i in range(1, j + 1):
        v = 101 * 269 ** i + 18 * v
    return v
def I(K):
    return sorted({269 ** (K - j) * N(x, j) for j in range(K + 1) for x in O})
fails = []
for K in range(KMAX + 1):
    A = I(K)
    byd = {}
    for a, b in combinations(A, 2):
        byd.setdefault(b - a, []).append((a, b))
    big = {d: v for d, v in byd.items() if len(v) >= 2}
    sizes = sorted({len(v) for v in big.values()})
    disjoint = 0; aps = set()
    for d, v in big.items():
        if len(v) != 2:
            fails.append("K=%d difference %d repeated %d times" % (K, d, len(v))); continue
        (a, b), (c, e) = v
        pts = {a, b, c, e}
        if len(pts) == 4:
            disjoint += 1; fails.append("K=%d disjoint equal-length pairs %s" % (K, v)); continue
        # shared point must be the middle of the 3-set
        s = sorted(pts)
        if not (s[1] in (a, b) and s[1] in (c, e) and s[0] + s[2] == 2 * s[1]):
            fails.append("K=%d class not a 3-AP: %s" % (K, v))
        aps.add(tuple(s))
    ok = len(aps) == 9 * (K + 1) and disjoint == 0 and sizes == [2]
    if not ok: fails.append("K=%d aps=%d sizes=%s disjoint=%d" % (K, len(aps), sizes, disjoint))
    print("K=%2d n=%3d repeated differences=%3d (class sizes %s) disjoint-pair classes=%d 3-APs=%d (9(K+1)=%d) %s"
          % (K, len(A), len(big), sizes, disjoint, len(aps), 9 * (K + 1), "OK" if ok else "FAIL"))
print("ALL DIFFERENCE-CENSUS CHECKS OK (K<=%d)" % KMAX if not fails else "FAILURES: %s" % fails[:5])
sys.exit(1 if fails else 0)
