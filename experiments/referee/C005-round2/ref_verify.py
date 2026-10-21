#!/usr/bin/env python3
"""Independent referee verifier for an Erdős #757 construction claim (round-2 referee).

Does NOT import e757 or judge. Everything decisive is exact integer arithmetic.

Checks:
  1. parse the set with Fraction, distinctness, scale to integers (exact; (4,5) and Sidon are
     invariant under x -> q x + t with q != 0);
  2. LITERAL (4,5) check: every one of the C(n,4) 4-subsets has >= 5 distinct absolute differences;
  3. weak-Sidon check (all C(n,2) sums distinct) -- a consequence of (2), re-checked directly;
  4. conflict structure from the DEFINITION of Sidon: two distinct pairs with the same difference
     cannot both lie in a Sidon subset; record every such conflict (union of the two pairs);
  5. exact h(A) by a frontier dynamic programme over a path decomposition of the conflict hypergraph
     (justified in the docstring of frontier_dp);
  6. optional witness check (Sidon by definition, subset, size);
  7. Fraction comparison h/n vs 4/7.
"""
import itertools
import json
import sys
import time
from fractions import Fraction
from math import lcm


def parse_set(raw):
    vals = [Fraction(str(x)) for x in raw]
    if len(set(vals)) != len(vals):
        raise ValueError("repeated elements")
    vals.sort()
    den = 1
    for v in vals:
        den = lcm(den, v.denominator)
    ints = [int(v * den) for v in vals]
    assert all(Fraction(i, den) == v for i, v in zip(ints, vals))
    assert len(set(ints)) == len(ints)
    return ints, den


def check_45_literal(A):
    """Every 4-subset has >= 5 distinct absolute differences. Returns (ok, bad_quadruple, hist)."""
    n = len(A)
    hist = {}
    for a, b, c, d in itertools.combinations(range(n), 4):
        xa, xb, xc, xd = A[a], A[b], A[c], A[d]
        # sorted, so all differences below are positive
        s = {xb - xa, xc - xa, xd - xa, xc - xb, xd - xb, xd - xc}
        k = len(s)
        hist[k] = hist.get(k, 0) + 1
        if k < 5:
            return False, (xa, xb, xc, xd), hist
    return True, None, hist


def check_weak_sidon(A):
    sums = {}
    for i, j in itertools.combinations(range(len(A)), 2):
        s = A[i] + A[j]
        if s in sums:
            return False, (sums[s], (i, j))
        sums[s] = (i, j)
    return True, None


def conflicts_from_definition(A):
    """All pairs of distinct index-pairs with equal difference. Returns list of frozensets (unions)
    and the dict difference -> list of pairs."""
    n = len(A)
    by_diff = {}
    for i, j in itertools.combinations(range(n), 2):
        by_diff.setdefault(A[j] - A[i], []).append((i, j))
    conflicts = set()
    for d, pairs in by_diff.items():
        if len(pairs) >= 2:
            for p, q in itertools.combinations(pairs, 2):
                conflicts.add(frozenset(p) | frozenset(q))
    return sorted(conflicts, key=lambda s: sorted(s)), by_diff


def is_sidon_by_definition(S):
    S = sorted(S)
    diffs = [y - x for x, y in itertools.combinations(S, 2)]
    return len(diffs) == len(set(diffs))


def frontier_dp(n, edges, order=None, max_frontier=26, return_witness=True):
    """Exact maximum independent set of a hypergraph (edges = sets of vertex indices; an
    independent set contains no edge entirely).

    Justification. Fix a vertex order v_0..v_{n-1}. For vertex u let last(u) be the largest
    position among vertices sharing an edge with u (last(u) = pos(u) if u is isolated). After
    processing positions 0..i the "frontier" F_i is {u : pos(u) <= i < last(u)}. Any edge whose
    maximum vertex is at position k has all its other vertices in F_{k-1}, so when position k is
    processed the feasibility of choosing v_k is decided by the chosen-status of frontier vertices
    alone. Vertices leaving the frontier never appear in a later edge, so their status may be
    forgotten after keeping the best count per remaining state (projection). Hence the DP computes
    max over all independent sets exactly: by induction on i, the table T_i maps each achievable
    chosen-pattern on F_i to the maximum size of an independent set of {v_0..v_i} inducing that
    pattern. Cost: sum_i 2^{|F_i|} states (times edges), so it needs a small frontier.
    """
    if order is None:
        order = list(range(n))
    pos = {v: i for i, v in enumerate(order)}
    last = {v: pos[v] for v in range(n)}
    for e in edges:
        m = max(pos[v] for v in e)
        for v in e:
            last[v] = max(last[v], m)
    edges_by_last = {}
    for e in edges:
        k = max(pos[v] for v in e)
        edges_by_last.setdefault(k, []).append(e)
    frontier_sizes = []
    # state: (frozenset of chosen frontier vertices) -> (best size, witness list or None)
    table = {frozenset(): (0, [] if return_witness else None)}
    for i, v in enumerate(order):
        new_table = {}
        es = edges_by_last.get(i, [])
        for state, (size, wit) in table.items():
            # option 1: do not choose v
            key = state
            cur = new_table.get(key)
            if cur is None or cur[0] < size:
                new_table[key] = (size, wit)
            # option 2: choose v if no edge with max v becomes fully chosen
            ok = True
            for e in es:
                if all((u == v) or (u in state) for u in e):
                    ok = False
                    break
            if ok:
                key = state | {v}
                cur = new_table.get(key)
                if cur is None or cur[0] < size + 1:
                    new_table[key] = (size + 1, (wit + [v]) if return_witness else None)
        # project: drop vertices whose last position is i
        leaving = {u for u in range(n) if last[u] == i}
        table = {}
        for state, val in new_table.items():
            key = frozenset(u for u in state if u not in leaving)
            cur = table.get(key)
            if cur is None or cur[0] < val[0]:
                table[key] = val
        fs = len({u for u in range(n) if pos[u] <= i < last[u]})
        frontier_sizes.append(fs)
        if fs > max_frontier:
            raise RuntimeError(f"frontier too large: {fs} at position {i}")
    best = max(table.values(), key=lambda t: t[0])
    return best[0], best[1], frontier_sizes


def main():
    path = sys.argv[1]
    t0 = time.time()
    claim = json.load(open(path))
    print("id:", claim.get("id"), "type:", claim.get("type"))
    A, den = parse_set(claim["set"])
    n = len(A)
    print(f"n = {n}; all values integral after scaling by {den}; distinct: True; min={A[0]} max={A[-1]}")

    ok, bad, hist = check_45_literal(A)
    print(f"(4,5) literal check over all C({n},4) = {sum(hist.values())} quadruples: {'PASS' if ok else 'FAIL'}; "
          f"histogram of #distinct differences: {dict(sorted(hist.items()))}; bad={bad}; t={time.time()-t0:.1f}s")
    if not ok:
        sys.exit(1)

    ws, info = check_weak_sidon(A)
    print(f"weak Sidon (all C(n,2) sums distinct): {ws} {info if not ws else ''}")

    conflicts, by_diff = conflicts_from_definition(A)
    sizes = {}
    for c in conflicts:
        sizes[len(c)] = sizes.get(len(c), 0) + 1
    print(f"conflicts from the Sidon definition: {len(conflicts)}; union sizes: {sizes}; "
          f"differences with multiplicity: {sorted(len(p) for p in by_diff.values() if len(p) >= 2)}")
    # each 3-element conflict must be a 3-AP (i<j<k with A[i]+A[k]=2A[j])
    aps = []
    for c in conflicts:
        if len(c) == 3:
            i, j, k = sorted(c)
            assert A[i] + A[k] == 2 * A[j], c
            aps.append((i, j, k))
        else:
            print("NOTE: 4-element conflict (parallelogram) present:", sorted(c))
    print(f"number of 3-APs m = {len(aps)}")
    deg = [0] * n
    for e in aps:
        for v in e:
            deg[v] += 1
    print("AP-degree histogram:", {d: deg.count(d) for d in sorted(set(deg))})
    print("non-midpoints:", [i for i in range(n) if not any(j == i for _, j, _ in aps)])

    edges = [frozenset(c) for c in conflicts]
    t1 = time.time()
    h, wit, fsz = frontier_dp(n, edges, order=list(range(n)))
    print(f"frontier DP (sorted order): h = {h}; max frontier = {max(fsz)}; t={time.time()-t1:.1f}s")
    W = sorted(A[v] for v in wit)
    assert len(W) == h and is_sidon_by_definition(W), "DP witness is not Sidon!"
    print("DP witness is Sidon by definition, size", len(W))
    json.dump({"h": h, "witness_indices": sorted(wit), "frontier_sizes": fsz, "aps": aps, "n": n},
              open(sys.argv[2], "w") if len(sys.argv) > 2 else sys.stdout, indent=0)

    if "witness_sidon_subset" in claim:
        Wc = [Fraction(str(x)) for x in claim["witness_sidon_subset"]]
        Wc_int = [int(v * den) for v in Wc]
        sub = set(Wc_int) <= set(A)
        sid = is_sidon_by_definition(Wc_int)
        print(f"claimed witness: size {len(Wc_int)}, distinct {len(set(Wc_int)) == len(Wc_int)}, subset {sub}, Sidon {sid}")
    ch = claim.get("claimed_h")
    print(f"claimed_h = {ch}; computed h = {h}; agree: {ch == h}")
    r = Fraction(h, n)
    print(f"h/n = {r} = {float(r):.6f}; 4/7 = {float(Fraction(4,7)):.6f}; h/n < 4/7: {r < Fraction(4, 7)}; "
          f"7h = {7*h}, 4n = {4*n}")
    print(f"total time {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
