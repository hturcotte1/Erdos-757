"""Referee round-2 primitives for L001.  NO imports from e757/, judge/, or the authors' scripts.

Everything is exact.  Points may be Fractions; they are mapped to integers by multiplying by the
lcm of denominators (an affine map: preserves (4,5), Sidon, APs).
Methods:
  is45(pts)            : definition: every 4-subset has >= 5 distinct absolute differences (all C(n,4) checked)
  is_sidon(S)          : definition: all positive differences distinct
  hmax_brute(pts, k)   : definition-level brute force: returns (has Sidon k-subset witness, has Sidon (k+1)-subset)
  hmax_ilp(pts)        : ILP (scipy.optimize.milp / HiGHS): max sum z, s.t. for every two distinct pairs with equal
                         difference, sum of z over the union of their points <= |union|-1.  Does not use APs.
"""
import itertools
from fractions import Fraction as F
from math import gcd
import numpy as np

ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


def lcm(a, b):
    return a * b // gcd(a, b)


def to_ints(pts):
    pts = [F(p) for p in pts]
    L = 1
    for p in pts:
        L = lcm(L, p.denominator)
    out = [int(p * L) for p in pts]
    assert all(F(o, L) == p for o, p in zip(out, pts))
    return out, L


def is45(pts):
    P, _ = to_ints(pts)
    if len(set(P)) != len(P):
        return False
    for q in itertools.combinations(P, 4):
        a, b, c, d = q
        if len({abs(a - b), abs(a - c), abs(a - d), abs(b - c), abs(b - d), abs(c - d)}) < 5:
            return False
    return True


def is_sidon(S):
    S = sorted(S)
    seen = set()
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            d = S[j] - S[i]
            if d in seen:
                return False
            seen.add(d)
    return True


def sidon_k_subset(P, k):
    """first Sidon k-subset of integer list P (lexicographic), or None. Pure definition."""
    for c in itertools.combinations(sorted(P), k):
        if is_sidon(c):
            return c
    return None


def hmax_brute(pts, lo):
    """exact h by brute force, assuming h>=lo is to be confirmed: returns h exactly
    (searches k = lo, lo+1, ... until no Sidon k-subset)."""
    P, L = to_ints(pts)
    k = lo
    w = sidon_k_subset(P, k)
    if w is None:
        # go down
        while w is None and k > 0:
            k -= 1
            w = sidon_k_subset(P, k)
        return k, [F(v, L) for v in w]
    best = (k, w)
    while True:
        w2 = sidon_k_subset(P, k + 1)
        if w2 is None:
            return best[0], [F(v, L) for v in best[1]]
        k += 1
        best = (k, w2)


def conflicts(P):
    """all index-unions of two distinct pairs with equal positive difference"""
    n = len(P)
    by_d = {}
    for i in range(n):
        for j in range(n):
            if P[j] > P[i]:
                by_d.setdefault(P[j] - P[i], []).append((i, j))
    out = set()
    for d, lst in by_d.items():
        for p, q in itertools.combinations(lst, 2):
            out.add(frozenset(p) | frozenset(q))
    return [tuple(sorted(c)) for c in out]


def hmax_ilp(pts):
    from scipy.optimize import milp, LinearConstraint, Bounds
    P, _ = to_ints(pts)
    n = len(P)
    C = conflicts(P)
    c = -np.ones(n)
    if not C:
        return n
    M = np.zeros((len(C), n))
    ub = np.zeros(len(C))
    for r, cc in enumerate(C):
        for v in cc:
            M[r, v] = 1
        ub[r] = len(cc) - 1
    res = milp(c, constraints=[LinearConstraint(M, -np.inf, ub)], integrality=np.ones(n),
               bounds=Bounds(0, 1))
    assert res.success, res.message
    z = np.round(res.x).astype(int)
    S = [P[i] for i in range(n) if z[i] == 1]
    assert is_sidon(S)            # the ILP optimum is genuinely Sidon (definition check)
    return int(round(-res.fun))


def three_aps(P):
    """3-term APs (as sorted value triples) in the integer list P (definition: sorted p<q<r with q-p=r-q)"""
    s = sorted(P)
    S = set(s)
    out = []
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            r = 2 * s[j] - s[i]
            if r in S and r > s[j]:
                out.append((s[i], s[j], r))
    return out
