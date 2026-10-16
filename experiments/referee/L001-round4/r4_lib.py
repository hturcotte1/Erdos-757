"""Referee round 4 primitives for L001.  Imports nothing from e757/, judge/, the authors' scripts,
or earlier referee folders.  Exact arithmetic only (int / Fraction)."""
import itertools
from fractions import Fraction as Fr
from math import gcd

A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


def n_dists(q):
    return len({abs(u - v) for u, v in itertools.combinations(q, 2)})


def is45_full(pts):
    """Definition: distinct points, every 4-subset has >= 5 distinct distances (all C(n,4) checked)."""
    pts = list(pts)
    if len(set(pts)) != len(pts):
        return False
    return all(n_dists(q) >= 5 for q in itertools.combinations(pts, 4))


def is_sidon(pts):
    """Definition: all sums u+v (u<=v, repetition allowed) distinct; duplicates -> False."""
    L = sorted(pts)
    if len(set(L)) != len(L):
        return False
    sums = [L[i] + L[j] for i in range(len(L)) for j in range(i, len(L))]
    return len(sums) == len(set(sums))


def sidon_subsets(pts, k):
    return [c for c in itertools.combinations(sorted(pts), k) if is_sidon(c)]


def h_maxsat(pts):
    """Largest Sidon subset by exact MaxSAT (pysat RC2) on ALL sum collisions u+v=w+z
    ({u,v} != {w,z} as multisets): hard clause 'not all of the distinct points chosen'."""
    from pysat.examples.rc2 import RC2
    from pysat.formula import WCNF
    pts = sorted(pts)
    n = len(pts)
    assert len(set(pts)) == n
    by_sum = {}
    for i in range(n):
        for j in range(i, n):
            by_sum.setdefault(pts[i] + pts[j], []).append((i, j))
    w = WCNF()
    for lst in by_sum.values():
        for (i, j), (k, l) in itertools.combinations(lst, 2):
            w.append([-(v + 1) for v in sorted({i, j, k, l})])
    for i in range(n):
        w.append([i + 1], weight=1)
    with RC2(w) as rc2:
        m = rc2.compute()
    S = [pts[v - 1] for v in m if v > 0]
    assert is_sidon(S)
    return len(S), S


# ---------- lines  alpha*X + beta*Y = gamma  (integers), normalised ----------
def norm_line(a, b, c):
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return (a, b, c)


def relation_lines(S):
    """All lines in the (X,Y)-plane on which S u {X,Y} has a sum coincidence s1+s2 = s3+s4 with
    {s1,s2} != {s3,s4} as multisets of SYMBOLS.  S must be a Sidon set of integers.
    Symbol = (cx, cy, const)."""
    syms = [(0, 0, s) for s in S] + [(1, 0, 0), (0, 1, 0)]
    sums = [tuple(p + q for p, q in zip(syms[i], syms[j]))
            for i in range(len(syms)) for j in range(i, len(syms))]
    out = set()
    for u, v in itertools.combinations(sums, 2):
        a, b, c = u[0] - v[0], u[1] - v[1], v[2] - u[2]
        if a == 0 and b == 0:
            assert c != 0, 'S is not Sidon'
            continue
        out.add(norm_line(a, b, c))
    return out


def intersect(l1, l2):
    """Intersection point of two lines (Fractions) or None if parallel/identical."""
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    return (Fr(c1 * b2 - c2 * b1, det), Fr(a1 * c2 - a2 * c1, det))


def on_line(l, p):
    return l[0] * p[0] + l[1] * p[1] == l[2]
