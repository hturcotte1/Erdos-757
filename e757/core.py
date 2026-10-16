"""
Erdos Problem #757 toolkit: exact checks for (4,5)-sets and their AP-hypergraphs.

Everything uses exact integer / rational arithmetic. Requires: Python 3.9+, sympy.
    pip install sympy

Main functions
--------------
ap_edges(A)              3-term APs of A as (left, middle, right) triples
is_45_set(A)             every 4 points determine >= 5 distinct distances
is_weak_sidon(A)         all sums x+y with x<y distinct
alpha(A)                 largest Sidon subset size h(A) = independence number of H(A)
                         (valid for weak Sidon sets, in particular (4,5)-sets)
ap_rank_report(A)        rank of the AP equation system; solution dim 2 means the AP
                         hypergraph determines A up to x -> q*x + t ("affinely rigid")
realize(labeled_edges, n, tries=20, seed=0)
                         try to realize an abstract labeled hypergraph (each edge given as
                         (endpoint, midpoint, endpoint) on vertices 0..n-1) as the exact
                         AP-hypergraph of a (4,5)-set of integers, using a generic point of
                         the solution space. Returns (True, sorted_integer_list) or (False, reason).

Run this file directly to reproduce the checks quoted in the Part 2 supplement.
"""
from __future__ import annotations

import itertools
import random
from fractions import Fraction

import sympy as sp


# ---------------------------------------------------------------- basic checks
def ap_edges(A):
    """Works for ints and Fractions (exact). Returns (left, middle, right) triples."""
    A = sorted(A)
    lookup = {Fraction(x): x for x in A}
    out = []
    for i, a in enumerate(A):
        for c in A[i + 2:]:
            b = (Fraction(a) + Fraction(c)) / 2
            if b in lookup:
                out.append((a, lookup[b], c))
    return out


def distinct_distances(q):
    return len({abs(x - y) for x, y in itertools.combinations(q, 2)})


def is_45_set(A):
    return all(distinct_distances(q) >= 5 for q in itertools.combinations(A, 4))


def is_weak_sidon(A):
    sums = [x + y for x, y in itertools.combinations(sorted(A), 2)]
    return len(sums) == len(set(sums))


def is_sidon(S):
    S = sorted(S)
    sums = [x + y for i, x in enumerate(S) for y in S[i:]]
    return len(sums) == len(set(sums))


def alpha(A, edges=None):
    """Exact independence number of the AP-hypergraph (branch and bound).
    For weak Sidon A this equals h(A), the largest Sidon subset (Ma-Tang Lemma 2.3)."""
    A = sorted(A)
    edges = ap_edges(A) if edges is None else edges
    idx = {x: i for i, x in enumerate(A)}
    n = len(A)
    masks = [sum(1 << idx[v] for v in e) for e in edges]
    best = 0

    def rec(i, cur, size):
        nonlocal best
        if size + (n - i) <= best:
            return
        if i == n:
            best = max(best, size)
            return
        nxt = cur | (1 << i)
        if all((m & nxt) != m for m in masks):
            rec(i + 1, nxt, size + 1)
        rec(i + 1, cur, size)

    rec(0, 0, 0)
    return best


def degrees(A, edges=None):
    edges = ap_edges(A) if edges is None else edges
    d = {x: 0 for x in A}
    for e in edges:
        for v in e:
            d[v] += 1
    return d


# ---------------------------------------------------------------- rigidity
def ap_matrix(n, labeled_edges):
    """labeled_edges: list of (i, j, k) with j the midpoint; vertices 0..n-1."""
    rows = []
    for i, j, k in labeled_edges:
        r = [0] * n
        r[i] += 1
        r[k] += 1
        r[j] -= 2
        rows.append(r)
    return sp.Matrix(rows) if rows else sp.zeros(0, n)


def ap_rank_report(A):
    A = sorted(A)
    idx = {x: i for i, x in enumerate(A)}
    E = ap_edges(A)
    M = ap_matrix(len(A), [(idx[a], idx[b], idx[c]) for a, b, c in E])
    rk = M.rank()
    return {"n": len(A), "m": len(E), "rank": rk, "solution_dim": len(A) - rk,
            "affinely_rigid": len(A) - rk == 2}


# ---------------------------------------------------------------- realizability
def realize(labeled_edges, n, tries=20, seed=0):
    """Generic-point realizability test for a labeled 3-uniform hypergraph.

    Over Q, a relation that fails at one random point of the solution space fails
    generically, so a failure at every one of several random points means the
    relation is (with overwhelming probability) forced by the AP equations.
    Returns (True, integer_set) or (False, reason)."""
    rnd = random.Random(seed)
    M = ap_matrix(n, labeled_edges)
    basis = M.nullspace()
    want = {frozenset(e) for e in labeled_edges}
    last_reason = "no attempt"
    for _ in range(tries):
        v = sp.zeros(n, 1)
        for b in basis:
            v += rnd.randint(-10**6, 10**6) * b
        den = sp.ilcm(*[sp.fraction(x)[1] for x in v]) if n else 1
        vals = [int(x * den) for x in v]
        if len(set(vals)) < n:
            last_reason = "two points forced equal"
            continue
        pos = {i: vals[i] for i in range(n)}
        got = set()
        for a, b, c in itertools.permutations(range(n), 3):
            if a < c and pos[a] + pos[c] == 2 * pos[b]:
                got.add(frozenset((a, b, c)))
        if got != want:
            last_reason = "extra AP forced" if want <= got else "edge not an AP (bad labeling)"
            continue
        if not is_45_set(vals):
            last_reason = "(4,5) condition violated"
            continue
        return True, sorted(vals)
    return False, last_reason


# ---------------------------------------------------------------- self-test
KNOWN = {
    "A_base (Ma-Tang 14-point, h=8)": [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056],
    "12-point example 1 (omega issue #9804)": [0, 178, 198, 218, 227, 235, 272, 276, 287, 317, 356, 436],
    "12-point example 2 (omega issue #9804)": [-336, -168, -44, -24, -4, 0, 39, 44, 49, 80, 102, 160],
}

if __name__ == "__main__":
    for name, A in KNOWN.items():
        E = ap_edges(A)
        a = alpha(A, E)
        n = len(A)
        print(f"{name}")
        print(f"  n={n} m={len(E)} (n-2={n-2})  (4,5)={is_45_set(A)}  h={a}  ratio={a/n:.4f}"
              f"  maxdeg={max(degrees(A, E).values())}")
        print(f"  Henning-Yeo slack 5n+3m-17*tau = {5*n + 3*len(E) - 17*(n - a)}")
        print(f"  rigidity: {ap_rank_report(A)}")

    fib = [1, 2]
    while len(fib) < 40:
        fib.append(fib[-1] + fib[-2])
    print("Fibonacci caveat: {1,2,3,5} is a (4,5)-set?", is_45_set([1, 2, 3, 5]))
    for n in (10, 20, 30):
        B = fib[1:1 + n]  # 2,3,5,8,...
        print(f"  {{F_3..}} n={n}: (4,5)={is_45_set(B)} h={alpha(B)} ratio={alpha(B)/n:.4f}")

    # F7 = AG(2,3) minus two points: not realizable over Q under any midpoint labeling
    F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    reasons = {}
    for lab in itertools.product(range(3), repeat=5):
        edges = []
        for e, k in zip(F7, lab):
            mid = e[k]
            ends = [x for x in e if x != mid]
            edges.append((ends[0], mid, ends[1]))
        ok, r = realize(edges, 7, tries=5)
        reasons[r if not ok else "REALIZED"] = reasons.get(r if not ok else "REALIZED", 0) + 1
    print("F7 over Q, 243 midpoint labelings:", reasons)
