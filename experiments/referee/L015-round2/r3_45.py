#!/usr/bin/env python3
"""Literal (4,5) test on I_K = 269^K S_K: for every 4-subset B, |B - B| (the set {a-b : a,b in B}) >= 11.
Also the distribution of |B-B|: predicted 11 exactly for the 4-sets containing one of the 9(K+1) APs
(9(K+1)(n-3) of them, each containing exactly one AP by linearity) and 13 for all others.
Own code; standard library only.  Usage: python3 r3_45.py K1 K2 ...
"""
import sys
sys.path.insert(0, ".")
from r2_family import build
from itertools import combinations
from collections import Counter

allok = True
for K in map(int, sys.argv[1:]):
    copies, S, I = build(K)
    n = len(I)
    dist = Counter()
    for B in combinations(I, 4):
        dist[len({a - b for a in B for b in B})] += 1
    total = sum(dist.values())
    want11 = 9 * (K + 1) * (n - 3)
    ok = min(dist) >= 11 and dist[11] == want11 and set(dist) <= {11, 13} and total == n * (n - 1) * (n - 2) * (n - 3) // 24
    allok &= ok
    print("K=%d n=%d 4-subsets=%d min|B-B|=%d distribution=%s predicted #11=%d -> %s"
          % (K, n, total, min(dist), dict(sorted(dist.items())), want11, "OK" if ok else "FAIL"), flush=True)
print("ALL R3 (4,5) CHECKS OK" if allok else "R3 FAILED")
