"""
Midpoint maps: the hypergraph-first way to search for (4,5)-sets.

Background (see kb/00_START_HERE.md, sections 2 and 6):
* A (4,5)-set is weak Sidon, so each point is the midpoint of at most one 3-AP.
* Every known record set is midpoint-saturated: every point except min and max is a midpoint.
* Such a set is described by a midpoint map  mid[j] = (i, k)  meaning  x_j = (x_i + x_k) / 2.

Fix x[lo] = 0 and x[hi] = 1. If the linear system has a unique solution, it is the
hitting probability of a random walk: from j jump to i or k with probability 1/2 each; x_j is the
probability of reaching `hi` before `lo` (a discrete harmonic function). No ordering has to be
imposed in advance: an average of two distinct values lies strictly between them.

Typical loop:  propose mid  ->  alpha_of_edges (cheap, combinatorial)  ->  solve_midpoint_map  ->
check_values  ->  if good, write a claim JSON and run judge/judge.py.
"""
from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

from .core import ap_edges, is_45_set


def edges_of_map(mid):
    """mid: dict j -> (i, k). Returns labeled edges (i, j, k), midpoint in the middle."""
    return [(i, j, k) for j, (i, k) in mid.items()]


def solve_midpoint_map(n, lo, hi, mid):
    """Solve x_j = (x_i + x_k)/2 for all j in mid, with x_lo = 0, x_hi = 1.

    mid must give an equation for every vertex other than lo and hi (saturated map).
    Returns a list of Fractions, or None if the system is singular."""
    unknown = [v for v in range(n) if v not in (lo, hi)]
    if set(mid) != set(unknown):
        raise ValueError("saturated map needs exactly one equation per non-boundary vertex")
    col = {v: c for c, v in enumerate(unknown)}
    size = len(unknown)
    rows = []
    for j in unknown:
        i, k = mid[j]
        row = [Fraction(0)] * (size + 1)
        row[col[j]] += 2
        for v in (i, k):
            if v == hi:
                row[size] += 1  # move the constant x_hi = 1 to the right-hand side
            elif v != lo:
                row[col[v]] -= 1
        rows.append(row)
    # Gauss-Jordan elimination over the rationals
    r = 0
    for c in range(size):
        piv = next((t for t in range(r, size) if rows[t][c] != 0), None)
        if piv is None:
            return None
        rows[r], rows[piv] = rows[piv], rows[r]
        p = rows[r][c]
        rows[r] = [x / p for x in rows[r]]
        for t in range(size):
            if t != r and rows[t][c] != 0:
                f = rows[t][c]
                rows[t] = [a - f * b for a, b in zip(rows[t], rows[r])]
        r += 1
    vals = [Fraction(0)] * n
    vals[hi] = Fraction(1)
    for v in unknown:
        vals[v] = rows[col[v]][size]
    return vals


def check_values(vals, edges):
    """Is `vals` a (4,5)-set whose AP hypergraph is exactly `edges` (labeled by vertex index)?
    Returns (ok, reason)."""
    n = len(vals)
    if len(set(vals)) < n:
        return False, "two points coincide"
    pos = {v: t for t, v in enumerate(vals)}
    got = {frozenset((pos[a], pos[b], pos[c])) for a, b, c in ap_edges(vals)}
    want = {frozenset(e) for e in edges}
    if got != want:
        return False, ("extra AP(s) forced" if want <= got else "a listed edge is not an AP")
    if not is_45_set(vals):
        return False, "(4,5) condition violated"
    return True, "ok"


def to_integers(vals):
    """Scale a list of Fractions to integers (common denominator)."""
    den = 1
    for v in vals:
        den = den * v.denominator // math.gcd(den, v.denominator)
    return [int(v * den) for v in vals]


def alpha_of_edges(n, edges):
    """Exact independence number of a 3-uniform hypergraph on vertices 0..n-1."""
    deg = [0] * n
    for e in edges:
        for v in e:
            deg[v] += 1
    order = sorted(range(n), key=lambda v: -deg[v])
    pos = {v: t for t, v in enumerate(order)}
    masks = []
    by_last = [[] for _ in range(n)]
    for e in edges:
        ps = sorted(pos[v] for v in e)
        m = (1 << ps[0]) | (1 << ps[1]) | (1 << ps[2])
        masks.append(m)
        by_last[ps[2]].append(m)
    full = (1 << n) - 1
    best = 0

    def rec(i, chosen, size):
        nonlocal best
        if size + (n - i) <= best:
            return
        if i == n:
            best = size
            return
        und = full ^ ((1 << i) - 1)
        avail = chosen | und
        used = loss = 0
        for m in masks:
            if m & avail == m:
                u = m & und
                if not (u & used):
                    used |= u
                    loss += 1
        if size + (n - i) - loss <= best:
            return
        c2 = chosen | (1 << i)
        if all(m & c2 != m for m in by_last[i]):
            rec(i + 1, c2, size + 1)
        rec(i + 1, chosen, size)

    rec(0, 0, 0)
    return best


def is_linear(edges):
    sets = [frozenset(e) for e in edges]
    return all(len(a & b) <= 1 for a, b in itertools.combinations(sets, 2))


def random_midpoint_map(n, rng=None):
    """Random saturated map on vertices 0..n-1 with boundary lo=0, hi=n-1 (a search baseline)."""
    rng = rng or random.Random()
    mid = {}
    for j in range(1, n - 1):
        i, k = rng.sample([v for v in range(n) if v != j], 2)
        mid[j] = (i, k)
    return 0, n - 1, mid


def map_of_set(A):
    """Midpoint map of a saturated (4,5)-set A (sorted). Returns (lo, hi, mid) on indices."""
    A = sorted(A)
    idx = {x: t for t, x in enumerate(A)}
    mid = {}
    for a, b, c in ap_edges(A):
        mid[idx[b]] = (idx[a], idx[c])
    return 0, len(A) - 1, mid
