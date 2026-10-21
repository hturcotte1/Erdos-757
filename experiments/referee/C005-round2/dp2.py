#!/usr/bin/env python3
"""Exact h(A) by a frontier DP (bitmask states) over a path decomposition of the 3-AP hypergraph.

The hypergraph is built here from the set with Python ints (no e757, no judge). Same justification
as ref_verify.frontier_dp: processing vertices in a fixed order, the only information needed about
processed vertices is the chosen-status of those that still share an edge with an unprocessed
vertex (the frontier); the maximum over independent sets is computed exactly by keeping, for every
achievable chosen-pattern on the frontier, the maximum size seen so far.

Usage: python3 dp2.py claim.json [order]   order in {zigzag, sorted, greedy, all}
"""
import itertools
import json
import sys
import time
from fractions import Fraction
from math import lcm


def load(path):
    raw = json.load(open(path))["set"]
    vals = sorted(Fraction(str(x)) for x in raw)
    assert len(set(vals)) == len(vals)
    den = 1
    for v in vals:
        den = lcm(den, v.denominator)
    return [int(v * den) for v in vals]


def aps_of(A):
    n = len(A)
    idx = {x: i for i, x in enumerate(A)}
    out = []
    for i in range(n):
        for k in range(i + 2, n):
            s = A[i] + A[k]
            if s % 2 == 0 and (s // 2) in idx:
                j = idx[s // 2]
                assert i < j < k
                out.append((i, j, k))
    return out


def frontier_profile(n, edges, order):
    pos = {v: i for i, v in enumerate(order)}
    last = {v: pos[v] for v in range(n)}
    for e in edges:
        m = max(pos[v] for v in e)
        for v in e:
            last[v] = max(last[v], m)
    return [sum(1 for u in range(n) if pos[u] <= i < last[u]) for i in range(n)], pos, last


def greedy_order(n, edges):
    """Greedy: repeatedly add the vertex minimising the resulting frontier size."""
    nbr = {v: set() for v in range(n)}
    for e in edges:
        for v in e:
            nbr[v] |= set(e) - {v}
    order, placed = [], set()
    while len(order) < n:
        best, bestv = None, None
        for v in range(n):
            if v in placed:
                continue
            S = placed | {v}
            fs = sum(1 for u in S if nbr[u] - S)
            key = (fs, v)
            if best is None or key < best:
                best, bestv = key, v
        order.append(bestv)
        placed.add(bestv)
    return order


def dp(n, edges, order, max_frontier=24, verbose=True):
    fs, pos, last = frontier_profile(n, edges, order)
    if max(fs) > max_frontier:
        raise RuntimeError(f"max frontier {max(fs)} > {max_frontier}")
    # bit of vertex v = its position
    edges_by_last = {}
    for e in edges:
        k = max(pos[v] for v in e)
        others = 0
        for v in e:
            if pos[v] != k:
                others |= 1 << pos[v]
        edges_by_last.setdefault(k, []).append(others)
    table = {0: 0}  # bitmask of chosen frontier positions -> best size
    t0 = time.time()
    maxstates = 0
    for i, v in enumerate(order):
        es = edges_by_last.get(i, [])
        bit = 1 << i
        new = {}
        for state, size in table.items():
            # skip v
            if new.get(state, -1) < size:
                new[state] = size
            # take v: forbidden iff some edge with max position i has all its other vertices chosen
            if all((state & o) != o for o in es):
                s2 = state | bit
                if new.get(s2, -1) < size + 1:
                    new[s2] = size + 1
        # project out leaving vertices (last == i)
        leave_mask = 0
        for u in range(n):
            if last[u] == i:
                leave_mask |= 1 << pos[u]
        keep = ~leave_mask
        table = {}
        for state, size in new.items():
            s = state & keep
            if table.get(s, -1) < size:
                table[s] = size
        maxstates = max(maxstates, len(table))
    if verbose:
        print(f"  DP done: states max {maxstates}, time {time.time()-t0:.1f}s")
    return max(table.values()), max(fs)


def zigzag(n):
    out = []
    lo, hi = 0, n - 1
    while lo <= hi:
        out.append(lo)
        if hi != lo:
            out.append(hi)
        lo += 1
        hi -= 1
    return out


def main():
    A = load(sys.argv[1])
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    n = len(A)
    edges = aps_of(A)
    print(f"n = {n}, m = {len(edges)} APs")
    orders = {}
    if which in ("zigzag", "all"):
        orders["zigzag"] = zigzag(n)
    if which in ("greedy", "all"):
        orders["greedy"] = greedy_order(n, edges)
    if which in ("sorted",):
        orders["sorted"] = list(range(n))
    results = {}
    for name, order in orders.items():
        fs, _, _ = frontier_profile(n, edges, order)
        print(f"order {name}: max frontier {max(fs)}; profile {fs}")
        try:
            h, mf = dp(n, edges, order)
            print(f"  h({name}) = {h}")
            results[name] = h
        except RuntimeError as e:
            print("  skipped:", e)
    print("RESULTS:", results)


if __name__ == "__main__":
    main()
