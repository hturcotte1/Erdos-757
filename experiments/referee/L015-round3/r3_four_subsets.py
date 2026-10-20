#!/usr/bin/env python3
"""Referee round 3, L015: literal (4,5) test on the integer sets I_K for K <= KMAX:
every 4-subset must determine >= 5 distinct positive differences (|B-B| >= 11).
Also: distinctness, weak Sidon (all sums x+y, x<y distinct) as a control statistic.
Usage: r3_four_subsets.py KMAX"""
from itertools import combinations
import sys, time

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]

def integer_set(K):
    # I_K = {269^(K-j) N_j(x)} with N_0 = x, N_j = 101*269^j + 18 N_{j-1}
    pts = set()
    Nj = {x: x for x in O}
    pts |= {269 ** K * v for v in Nj.values()}
    for j in range(1, K + 1):
        Nj = {x: 101 * 269 ** j + 18 * Nj[x] for x in O}
        pts |= {269 ** (K - j) * v for v in Nj.values()}
    return sorted(pts)

fails = []
for K in range(0, KMAX + 1):
    A = integer_set(K)
    n = len(A)
    t0 = time.time()
    assert len(set(A)) == n
    mind = 99
    count = 0
    worst = None
    for a, b, c, d in combinations(A, 4):
        # six positive differences
        diffs = {b - a, c - a, d - a, c - b, d - b, d - c}
        count += 1
        if len(diffs) < mind:
            mind = len(diffs); worst = (a, b, c, d)
    ok = mind >= 5
    if not ok:
        fails.append("K=%d min distinct differences %d at %s" % (K, mind, worst))
    # weak Sidon control
    ws = len({a + b for a, b in combinations(A, 2)}) == n * (n - 1) // 2
    print("K=%d n=%d 4-subsets=%d min #distinct positive differences=%d (need >=5): %s; weak Sidon=%s; %.1fs"
          % (K, n, count, mind, "OK" if ok else "FAIL", ws, time.time() - t0))
print("ALL 4-SUBSET CHECKS OK (K<=%d)" % KMAX if not fails else "FAILURES: %s" % fails)
sys.exit(1 if fails else 0)
