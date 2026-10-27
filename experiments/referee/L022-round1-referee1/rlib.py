# Independent referee library for L022 round 1 (referee 1).
# Written from scratch: does NOT import e757, judge, or any experiments/prover code.
# Exact arithmetic only (int / Fraction) for every decision.
from fractions import Fraction
from itertools import combinations
import random


# ---------------------------------------------------------------- hypergraphs
def edges_norm(edges):
    return sorted(tuple(sorted(e)) for e in edges)


def verts(edges, extra=()):
    s = set(extra)
    for e in edges:
        s.update(e)
    return sorted(s)


def degree(edges, x):
    return sum(1 for e in edges if x in e)


def is_linear(edges):
    seen = set()
    for e in edges:
        for p in combinations(sorted(e), 2):
            if p in seen:
                return False
            seen.add(p)
    return True


def components(V, edges):
    """V: iterable of vertices; edges inside V. Returns list of (vertex set, edge list)."""
    V = list(V)
    parent = {v: v for v in V}

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in edges:
        a = f(e[0])
        for y in e[1:]:
            b = f(y)
            if a != b:
                parent[b] = a
    comp = {}
    for v in V:
        comp.setdefault(f(v), set()).add(v)
    out = []
    for r, S in comp.items():
        out.append((S, [e for e in edges if e[0] in S]))
    return out


def induced(edges, S):
    S = set(S)
    return [e for e in edges if all(x in S for x in e)]


def _masks(edges, V):
    idx = {v: i for i, v in enumerate(V)}
    return [sum(1 << idx[x] for x in e) for e in edges], idx


def tau(edges, V=None):
    """Exact transversal number by branch and bound on bitmasks."""
    if not edges:
        return 0
    if V is None:
        V = verts(edges)
    E, idx = _masks(edges, V)
    best = [len(E)]  # trivial upper bound (one vertex per edge)

    def lb(T):
        # greedy disjoint uncovered edges
        used = 0
        c = 0
        for e in E:
            if e & T == 0 and e & used == 0:
                used |= e
                c += 1
        return c

    def rec(T, k, forb):
        if k + lb(T) >= best[0]:
            return
        for e in E:
            if e & T == 0:
                break
        else:
            best[0] = k
            return
        avail = e & ~forb
        f2 = forb
        while avail:
            b = avail & -avail
            avail ^= b
            rec(T | b, k + 1, f2)
            f2 |= b
    rec(0, 0, 0)
    return best[0]


def all_min_transversals(edges, V=None):
    """Return (tau, list of bitmasks over V, V). Every minimum transversal exactly once."""
    if V is None:
        V = verts(edges)
    if not edges:
        return 0, [0], V
    t = tau(edges, V)
    E, idx = _masks(edges, V)
    out = []

    def rec(T, k, forb):
        for e in E:
            if e & T == 0:
                break
        else:
            out.append(T)
            return
        if k == t:
            return
        avail = e & ~forb
        f2 = forb
        while avail:
            b = avail & -avail
            avail ^= b
            rec(T | b, k + 1, f2)
            f2 |= b
    rec(0, 0, 0)
    out = [T for T in out if bin(T).count('1') == t]
    assert len(set(out)) == len(out)
    return t, out, V


def slack(edges, V):
    return 3 * len(V) + 2 * len(edges) - 11 * tau(edges, V)


F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]


def contains_F7(edges):
    """Brute force: a vertex c of degree >= 3 with three edges, plus two more edges
    forming F7 with them (the centre of F7 is its unique degree-3 vertex)."""
    E = [tuple(e) for e in edges]
    Es = set(frozenset(e) for e in E)
    V = verts(E)
    for c in V:
        at = [e for e in E if c in e]
        if len(at) < 3:
            continue
        for e1, e2, e3 in combinations(at, 3):
            P = [tuple(x for x in e if x != c) for e in (e1, e2, e3)]
            if len(set(P[0]) | set(P[1]) | set(P[2])) != 6:
                continue
            # choose one vertex of each pair for edge g, the rest for edge h
            for a in P[0]:
                for b in P[1]:
                    for d in P[2]:
                        g = frozenset((a, b, d))
                        h = frozenset(set(P[0] + P[1] + P[2]) - g)
                        if g in Es and h in Es:
                            return True
    return False


def P3_ok(edges, V):
    """e(S) <= |S|-2 for all S with |S|>=2 (exhaustive; small n only)."""
    V = list(V)
    n = len(V)
    E, idx = _masks(edges, V)
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 2:
            continue
        cnt = sum(1 for e in E if e & S == e)
        if cnt > k - 2:
            return False
    return True


# ---------------------------------------------------------------- point sets
def ap_triples(points):
    """points: dict label->Fraction/int. Returns set of (left,mid,right) label triples."""
    labs = sorted(points, key=lambda l: points[l])
    val = {points[l]: l for l in labs}
    out = set()
    for i in range(len(labs)):
        for k in range(i + 2, len(labs)):
            a, c = points[labs[i]], points[labs[k]]
            s = a + c
            if s % 2 == 0 if isinstance(s, int) else True:
                mid = Fraction(s) / 2
                # find label with value mid
                for l in labs[i + 1:k]:
                    if points[l] == mid:
                        out.add((labs[i], l, labs[k]))
    return out


def is_45_bruteforce(vals):
    vals = list(vals)
    if len(set(vals)) != len(vals):
        return False
    for B in combinations(vals, 4):
        d = set(abs(x - y) for x, y in combinations(B, 2))
        if len(d) < 5:
            return False
    return True


def is_45_fast(vals):
    """Weak Sidon + linear APs (equivalent to (4,5) by L022 0.2, which this
    referee re-proved by hand); used for large sets; cross-checked against
    the brute force on small sets."""
    vals = sorted(vals)
    n = len(vals)
    if len(set(vals)) != n:
        return False
    sums = {}
    for i in range(n):
        for j in range(i + 1, n):
            s = vals[i] + vals[j]
            if s in sums:
                return False
            sums[s] = (i, j)
    S = set(vals)
    aps = []
    for i in range(n):
        for k in range(i + 2, n):
            s = vals[i] + vals[k]
            if (Fraction(s) / 2) in S:
                aps.append((vals[i], Fraction(s) / 2, vals[k]))
    pairs = set()
    for a in aps:
        for p in combinations(sorted(a), 2):
            if p in pairs:
                return False
            pairs.add(p)
    return True


# ---------------------------------------------------------------- exact linear algebra
def rref(rows, ncols):
    """rows: list of lists of Fractions. Returns (R, pivots)."""
    M = [list(map(Fraction, r)) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def rank(rows, ncols):
    return len(rref(rows, ncols)[1])


def nullspace(rows, ncols):
    R, piv = rref(rows, ncols) if rows else ([], [])
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][f]
        basis.append(v)
    return basis


def ap_form(n, a, b, c):
    """X_a + X_c - 2 X_b."""
    v = [0] * n
    v[a] += 1
    v[c] += 1
    v[b] -= 2
    return v
