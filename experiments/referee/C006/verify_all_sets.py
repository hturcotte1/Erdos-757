#!/usr/bin/env python3
"""Robustness check (not load-bearing): independently re-verify every set in
experiments/20261027-0400-realize-21-18-9/sets_21_19_9_realizable.json.
No e757/ or judge/ imports.  (4,5) by all 4-subsets; h by 2^n enumeration against the
violation sets of the Sidon definition (equal sums of multiset pairs)."""
import itertools, json, sys
import numpy as np

P = "/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9/sets_21_19_9_realizable.json"
data = json.load(open(P))
bad = 0
summary = {}
for rec in data:
    A = rec["set"]
    assert all(type(x) is int for x in A)
    n = len(A)
    A = sorted(A)
    ok45 = len(set(A)) == n and all(len({abs(x - y) for x, y in itertools.combinations(B, 2)}) >= 5
                                    for B in itertools.combinations(A, 4))
    ps = {}
    for i, j in itertools.combinations_with_replacement(range(n), 2):
        ps.setdefault(A[i] + A[j], []).append((i, j))
    viol = {frozenset(p) | frozenset(q) for v in ps.values() for p, q in itertools.combinations(v, 2)}
    N = 1 << n
    masks = np.arange(N, dtype=np.int64)
    ind = np.ones(N, dtype=bool)
    for v in viol:
        vm = sum(1 << i for i in v)
        ind &= (masks & vm) != vm
    pc = np.bitwise_count(masks.astype(np.uint64))
    h = int(pc[ind].max())
    m = sum(1 for v in viol if len(v) == 3)
    q4 = sum(1 for v in viol if len(v) == 4)
    deg = [sum(1 for v in viol if i in v) for i in range(n)]
    key = (n, m, n - h, max(deg), q4, ok45)
    summary[key] = summary.get(key, 0) + 1
    if not (ok45 and n == 21 and h == 12 and m == 19 and q4 == 0):
        bad += 1
        print("BAD", rec["cls"], key)
print("sets:", len(data), " (n, m, tau, maxdeg, #4-point additive quadruples, is45) -> count:", summary)
print("all are 21-point (4,5)-sets with h = 12:", bad == 0)
sys.exit(1 if bad else 0)
