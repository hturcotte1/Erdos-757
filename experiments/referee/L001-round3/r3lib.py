"""Round-3 referee primitives for L001 (A_base two-point extensions).

Written from scratch for this review. Imports NOTHING from e757/, judge/, the authors' scripts
(extend.py, bruteforce_check.py) or the earlier referee folders.

Exactness: every value is a fractions.Fraction or an int; sets are scaled to integers by the
lcm of the denominators before any numpy work (int64; all magnitudes here are < 10^6).

Two exact, definition-level methods for h (largest Sidon subset), both different from the
judge's branch-and-bound:
  * h_sat:   CDCL SAT (pysat/CaDiCaL) on the sum-collision clauses + a cardinality constraint;
  * h_brute: numpy enumeration of ALL 2^n subsets (n <= 22) against the sum-collision masks.
Neither uses the AP / weak-Sidon reduction: the conflicts are ALL pairs of distinct 2-multisets
{p,q} != {r,s} (p<=q, r<=s) with p+q = r+s, i.e. the Sidon definition itself.
"""
import itertools
from fractions import Fraction as F
from math import lcm, gcd

import numpy as np
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


def to_ints(vals):
    """exact scaling of rationals to integers; returns (ints, D)"""
    fr = [F(v) for v in vals]
    D = 1
    for v in fr:
        D = lcm(D, v.denominator)
    out = [int(v * D) for v in fr]
    assert all(F(o, D) == v for o, v in zip(out, fr))
    return out, D


# ---------------------------------------------------------------- (4,5) tests
def is45_py(vals):
    """pure-Python definition: distinct, and every 4 points have >= 5 distinct |differences|."""
    pts = [F(v) for v in vals]
    if len(set(pts)) != len(pts):
        return False
    for q in itertools.combinations(pts, 4):
        if len({abs(u - v) for u, v in itertools.combinations(q, 2)}) < 5:
            return False
    return True


_QUADS = {}


def _quads(n):
    if n not in _QUADS:
        _QUADS[n] = np.array(list(itertools.combinations(range(n), 4)), dtype=np.int64).reshape(-1, 4)
    return _QUADS[n]


def is45_np(vals):
    """numpy version of the same definition (all C(n,4) quadruples)."""
    ints, _ = to_ints(vals)
    if len(set(ints)) != len(ints):
        return False
    n = len(ints)
    if n < 4:
        return True
    v = np.array(ints, dtype=np.int64)
    P = v[_quads(n)]
    d = np.abs(P[:, [0, 0, 0, 1, 1, 2]] - P[:, [1, 2, 3, 2, 3, 3]])
    d.sort(axis=1)
    distinct = 1 + (np.diff(d, axis=1) != 0).sum(axis=1)
    return bool((distinct >= 5).all())


# ---------------------------------------------------------------- Sidon
def is_sidon(S):
    """definition: all sums p+q with p<=q (p,q in S) are distinct."""
    L = sorted(F(v) for v in S)
    if len(set(L)) != len(L):
        return False
    sums = [L[i] + L[j] for i in range(len(L)) for j in range(i, len(L))]
    return len(sums) == len(set(sums))


def collision_sets(vals):
    """index sets U = union of two distinct 2-multisets {i<=j},{k<=l} with equal sums.
    S is Sidon iff no such U is contained in S. Returns a sorted list of frozensets."""
    ints, _ = to_ints(vals)
    n = len(ints)
    bysum = {}
    for i in range(n):
        for j in range(i, n):
            bysum.setdefault(ints[i] + ints[j], []).append((i, j))
    out = set()
    for lst in bysum.values():
        for (i, j), (k, l) in itertools.combinations(lst, 2):
            out.add(frozenset((i, j, k, l)))
    return sorted(out, key=lambda s: sorted(s))


def h_sat(vals, start=None):
    """exact h by SAT: largest k such that 'exists Sidon subset of size >= k' is satisfiable.
    Returns (h, witness_values). The witness is re-checked with is_sidon."""
    n = len(vals)
    coll = collision_sets(vals)
    vals_f = [F(v) for v in vals]

    def solve(k):
        if k <= 0:
            return []
        if k > n:
            return None
        cl = [[-(i + 1) for i in sorted(U)] for U in coll]
        enc = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.seqcounter)
        with Solver(name='cadical153', bootstrap_with=cl + enc.clauses) as s:
            if not s.solve():
                return None
            m = s.get_model()
            W = [vals_f[i] for i in range(n) if m[i] > 0]
            assert len(W) >= k and is_sidon(W), 'SAT witness failed the definition check'
            return W

    k = start if start is not None else 1
    W = solve(k)
    if W is None:  # go down
        while W is None and k > 0:
            k -= 1
            W = solve(k)
        return k, W
    best = W
    while True:
        k = len(best) + 1
        W = solve(k)
        if W is None:
            return len(best), best
        best = W


_ALLMASK = {}


def h_brute(vals):
    """exact h by enumerating ALL 2^n subsets (n <= 22) with numpy; definition-level conflicts."""
    n = len(vals)
    assert n <= 22
    if n not in _ALLMASK:
        m = np.arange(1 << n, dtype=np.int64)
        pc = np.zeros(1 << n, dtype=np.int64)
        for i in range(n):
            pc += (m >> i) & 1
        _ALLMASK[n] = (m, pc)
    m, pc = _ALLMASK[n]
    bad = np.zeros(1 << n, dtype=bool)
    for U in collision_sets(vals):
        u = sum(1 << i for i in U)
        bad |= (m & u) == u
    good = ~bad
    h = int(pc[good].max())
    count_max = int((good & (pc == h)).sum())
    return h, count_max


# ---------------------------------------------------------------- APs
def ap_triples(vals):
    """all 3-APs (as sorted value triples) in a set of distinct rationals"""
    L = sorted(F(v) for v in vals)
    S = set(L)
    out = []
    for i in range(len(L)):
        for k in range(i + 2, len(L)):
            mid = (L[i] + L[k]) / 2
            if mid in S and mid != L[i] and mid != L[k]:
                out.append((L[i], mid, L[k]))
    return out


def third_points(vals):
    """all reals v NOT in vals such that {v,p,q} is a 3-AP for some distinct p,q in vals.
    Complete: in a 3-AP {v,p,q} either v is the middle (v=(p+q)/2), or p is (v=2p-q), or q is (v=2q-p)."""
    L = [F(v) for v in vals]
    S = set(L)
    out = set()
    for p, q in itertools.combinations(L, 2):
        out.update(((p + q) / 2, 2 * p - q, 2 * q - p))
    return out - S
