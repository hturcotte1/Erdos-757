#!/usr/bin/env python3
"""Referee round 3, L015: the explicit Sidon subset T_K = U_{j<=K} phi^j(U*) for K <= KMAX,
in exact integer form (scaled by 269^K): T_K subset of I_K, |T_K| = 7+5K, all sums
a+b (a<=b) distinct (Sidon by definition), no 3-AP, and T_K = U* u phi(T_{K-1}).
Usage: r5_witness.py KMAX"""
from itertools import combinations
import sys, time

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
Ustar = [0, 98, 101, 117, 119, 159, 269]

def N(x, j):
    v = x
    for i in range(1, j + 1):
        v = 101 * 269 ** i + 18 * v
    return v

def integer_set(base, K):
    return sorted({269 ** (K - j) * N(x, j) for j in range(K + 1) for x in base})

fails = []
prevT = None
for K in range(0, KMAX + 1):
    t0 = time.time()
    I = integer_set(O, K)
    T = integer_set(Ustar, K)
    ok_sub = set(T) <= set(I)
    ok_size = len(T) == 7 + 5 * K
    sums = [a + b for a, b in combinations(T, 2)] + [2 * a for a in T]
    ok_sidon = len(set(sums)) == len(sums)
    ok_ap = not any(a + c == 2 * u for a, u, c in combinations(T, 3)) if K <= 12 else None
    # self-similarity: T_K = 269^K U* u (phi(T_{K-1}) scaled): phi in integer form: p -> 101*269^K + 18 p (p an element of I_{K-1} scaled by 269^(K-1))
    if prevT is not None:
        img = {101 * 269 ** K + 18 * p for p in prevT}
        ok_ss = set(T) == {269 ** K * u for u in Ustar} | img
    else:
        ok_ss = True
    prevT = T
    ok = ok_sub and ok_size and ok_sidon and (ok_ap is not False) and ok_ss
    print("K=%2d |I_K|=%3d |T_K|=%3d (7+5K=%3d) subset=%s sidon=%s(distinct sums %d) 3AP-free=%s selfsim=%s %.1fs"
          % (K, len(I), len(T), 7 + 5 * K, ok_sub, ok_sidon, len(set(sums)), ok_ap, ok_ss, time.time() - t0), flush=True)
    if not ok:
        fails.append(K)
print("ALL WITNESS CHECKS OK (K<=%d)" % KMAX if not fails else "FAILURES at K=%s" % fails)
sys.exit(1 if fails else 0)
