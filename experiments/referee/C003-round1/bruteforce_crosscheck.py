#!/usr/bin/env python3
"""Cross-check the frontier DP of verify_c003.py against brute force (n <= 22).

(a) random 3/4-uniform hypergraphs, n <= 16, random vertex orders: DP == brute force over 2^n
(b) induced subsets (<= 22 points) of the C003 set, grown by random BFS in the AP hypergraph
    (dense), plus contiguous index windows: DP == brute force over all 2^k subsets, where a
    subset is tested from the Sidon DEFINITION for k <= 16 (all sums distinct) and by
    forbidden-union masks for 16 < k <= 22 (the masks themselves come from the sum census).
(c) the family members K=0 (11 points) and K=1 (20 points), rebuilt here from the page's O and
    phi with Fractions: brute force from the definition.
Does not import e757 or judge.
"""
import itertools
import json
import random
import resource
import sys
import time
from fractions import Fraction

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from verify_c003 import bfs_order, frontier_dp, is_sidon_sums, sum_census  # noqa: E402  (own code)

# memory cap (4 GB) is set by verify_c003 on import


def popcount_table(k):
    arr = np.arange(1 << k, dtype=np.uint32)
    pc = np.zeros(1 << k, dtype=np.uint8)
    x = arr.copy()
    while x.any():
        pc += (x & 1).astype(np.uint8)
        x >>= 1
    return arr, pc


def brute_masks(k, edges):
    arr, pc = popcount_table(k)
    bad = np.zeros(1 << k, dtype=bool)
    for e in edges:
        m = 0
        for v in e:
            m |= 1 << v
        bad |= (arr & np.uint32(m)) == np.uint32(m)
    good = pc[~bad]
    return int(good.max())


def brute_definition(B):
    """max Sidon subset by exhaustive DFS over all subsets, testing the definition directly."""
    k = len(B)
    best = 0

    def rec(i, chosen, sums):
        nonlocal best
        if i == k:
            best = max(best, len(chosen))
            return
        # include B[i] if all new sums are new (definition: sums x+y, x<=y, distinct)
        x = B[i]
        new = [x + y for y in chosen] + [2 * x]
        if len(set(new)) == len(new) and not (set(new) & sums):
            rec(i + 1, chosen + [x], sums | set(new))
        rec(i + 1, chosen, sums)

    rec(0, [], frozenset())
    return best


def forb_of(B):
    rels, _ = sum_census(B)
    return sorted({tuple(sorted(set(p) | set(q))) for p, q in rels})


def dp_alpha(k, F, order=None):
    if order is None:
        order = bfs_order(k, F, 0)
    return frontier_dp(k, F, order)[0]


def main():
    rng = random.Random(20261020)
    claim = json.load(open(sys.argv[1]))
    A = sorted(int(x) for x in claim["set"])
    n = len(A)
    t0 = time.time()

    # (a) random hypergraphs
    bad = 0
    for trial in range(400):
        k = rng.randint(4, 16)
        m = rng.randint(1, 3 * k)
        E = set()
        for _ in range(m):
            E.add(tuple(sorted(rng.sample(range(k), rng.choice([3, 3, 3, 4])))))
        E = sorted(E)
        bf = brute_masks(k, E)
        order = list(range(k))
        rng.shuffle(order)
        d1 = frontier_dp(k, E, order)[0]
        d2 = dp_alpha(k, E)
        if not (bf == d1 == d2):
            bad += 1
            print("MISMATCH (a)", k, E, bf, d1, d2)
    print(f"(a) random hypergraphs: 400 trials, mismatches = {bad} [{time.time() - t0:.1f}s]", flush=True)

    # (b) induced subsets of A
    F = forb_of(A)
    adj = {v: set() for v in range(n)}
    for e in F:
        for u in e:
            adj[u] |= set(e) - {u}
    bad = 0
    stats = []
    trials = 0
    t1 = time.time()
    subsets = []
    for trial in range(60):
        k = rng.randint(8, 22)
        start = rng.randrange(n)
        S = {start}
        frontier = [start]
        while len(S) < k:
            cand = sorted({w for u in S for w in adj[u]} - S)
            if not cand or rng.random() < 0.05:
                cand = sorted(set(range(n)) - S)
            S.add(rng.choice(cand))
        subsets.append(sorted(S))
    for lo in range(0, n - 19, 9):          # contiguous index windows of 20 points
        subsets.append(list(range(lo, lo + 20)))
    for idx in subsets:
        B = [A[i] for i in idx]
        k = len(B)
        Fb = forb_of(B)
        d = dp_alpha(k, Fb)
        bm = brute_masks(k, Fb)
        bd = brute_definition(B) if k <= 16 else None
        trials += 1
        stats.append((k, len(Fb), d))
        if d != bm or (bd is not None and bd != d):
            bad += 1
            print("MISMATCH (b)", idx, d, bm, bd)
    print(f"(b) induced subsets of the claim set: {trials} subsets (sizes {min(s[0] for s in stats)}.."
          f"{max(s[0] for s in stats)}, up to {max(s[1] for s in stats)} induced relations), "
          f"mismatches = {bad} [{time.time() - t1:.1f}s]", flush=True)

    # (c) family members rebuilt from O and phi
    O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]

    def phi(x):
        return Fraction(101) + Fraction(18, 269) * x

    for K in (0, 1):
        pts = set()
        cur = [Fraction(x) for x in O]
        for j in range(K + 1):
            pts |= set(cur)
            cur = [phi(x) for x in cur]
        P = sorted(pts)
        scale = 269 ** K
        B = [int(x * scale) for x in P]
        assert all((x * scale).denominator == 1 for x in P)
        t2 = time.time()
        bd = brute_definition(B)
        d = dp_alpha(len(B), forb_of(B))
        print(f"(c) family K={K}: n={len(B)} brute force (definition) h={bd}, DP h={d}, "
              f"expected 7+5K={7 + 5 * K} [{time.time() - t2:.1f}s]", flush=True)
        if K == 1:
            print("    K=1 member equals the claim set's 20 smallest-depth points? ",
                  "n/a (different scale)")
    print(f"total {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
