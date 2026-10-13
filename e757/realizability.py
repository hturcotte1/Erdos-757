"""
Exact realizability oracle for labeled ORDERED AP patterns.

Setting: vertices 0..n-1 are ranks, x_0 < x_1 < ... < x_{n-1}; a labeled edge (i, j, k) with
i < j < k means 2 x_j = x_i + x_k.  A pattern is *realizable* if some strictly increasing rational
point of the solution space has exactly these 3-APs and is a (4,5)-set.

Everything that decides is exact (Fractions); there are no floats.

Order feasibility, in gap variables g_t = x_{t+1} - x_t (t = 0..n-2): an edge (i,j,k) is the row
    sum_{t=i}^{j-1} g_t - sum_{t=j}^{k-1} g_t = 0.
By Stiemke's lemma exactly one of
  (a) there is g > 0 with E g = 0 (equivalently g >= 1 with E g = 0, by homogeneity);
  (b) there is y with w = E^T y >= 0, w != 0   (a Farkas certificate: for any g > 0 with E g = 0,
      0 = y.(E g) = w.g > 0, a contradiction).
Both are feasibility problems over x >= 0, A x = b, solved by an exact two-phase simplex
(Bland's rule) with Fractions.  Each answer is re-verified before it is returned; if verification
fails we return None ("unknown") rather than guess.

Forced relations (decisions are identities on the solution space, found by linear algebra):
  * 'extra_ap'  (a,b,c): x_a + x_c - 2 x_b is in the row space of the AP equations, (a,b,c) unlisted.
  * 'diff'      (a,b,c,d) a<b<c<d: x_a + x_d - x_b - x_c is in the row space.  (This is the
    parallelogram; it forces two coincident distances, ab=cd and ac=bd, so the 4-set has <= 4
    distinct distances.)
  * 'nonlinear' two listed edges inside one 4-set (they share 2 points: two coincident distances).
For a strictly increasing configuration these are exactly the ways the (4,5)-property or the AP list
can be forced to fail, because a 4-set has >= 5 distinct distances unless it carries >= 2
coincidences, each of which is an AP (shared point) or the parallelogram relation (disjoint pairs).
"""
from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

from .core import ap_edges, is_45_set

F = Fraction


# --------------------------------------------------------------------------- exact linear algebra
def _rref(rows, ncols):
    """Reduced row echelon form over Q. Returns (rows, pivot_cols). rows: lists of Fractions."""
    R = [[F(x) for x in r] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = next((t for t in range(r, len(R)) if R[t][c] != 0), None)
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]
        pv = R[r][c]
        if pv != 1:
            R[r] = [x / pv for x in R[r]]
        for t in range(len(R)):
            if t != r and R[t][c] != 0:
                f = R[t][c]
                R[t] = [a - f * b for a, b in zip(R[t], R[r])]
        piv.append(c)
        r += 1
        if r == len(R):
            break
    return R[:r], piv


def _in_rowspace(vec, rref_rows, piv):
    v = [F(x) for x in vec]
    for row, c in zip(rref_rows, piv):
        if v[c] != 0:
            f = v[c]
            v = [a - f * b for a, b in zip(v, row)]
    return all(x == 0 for x in v)


def _nullspace(rows, ncols):
    R, piv = _rref(rows, ncols) if rows else ([], [])
    free = [c for c in range(ncols) if c not in set(piv)]
    basis = []
    for fcol in free:
        v = [F(0)] * ncols
        v[fcol] = F(1)
        for row, pc in zip(R, piv):
            v[pc] = -row[fcol]
        basis.append(v)
    return basis


def _lp_feasible(A, b):
    """Exact phase-1 simplex (Bland). Find x >= 0 with A x = b, or None. A: list of rows."""
    m = len(A)
    N = len(A[0]) if m else 0
    if m == 0:
        return []
    T = []
    for i in range(m):
        row = [F(x) for x in A[i]]
        rhs = F(b[i])
        if rhs < 0:
            row = [-x for x in row]
            rhs = -rhs
        T.append(row + [F(1) if k == i else F(0) for k in range(m)] + [rhs])
    basis = [N + i for i in range(m)]
    W = N + m
    z = [F(0)] * (W + 1)
    for i in range(m):
        for j in range(N):
            z[j] -= T[i][j]
        z[W] -= T[i][W]
    while True:
        enter = next((j for j in range(W) if z[j] < 0), None)
        if enter is None:
            break
        best = None
        for i in range(m):
            if T[i][enter] > 0:
                ratio = T[i][W] / T[i][enter]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None:  # cannot happen in phase 1 (objective bounded below by 0)
            return None
        _, lv = best
        pv = T[lv][enter]
        T[lv] = [x / pv for x in T[lv]]
        for i in range(m):
            if i != lv and T[i][enter] != 0:
                f = T[i][enter]
                T[i] = [a - f * c for a, c in zip(T[i], T[lv])]
        f = z[enter]
        z = [a - f * c for a, c in zip(z, T[lv])]
        basis[lv] = enter
    if z[W] != 0:  # phase-1 objective -(sum of artificials) < 0: infeasible
        return None
    x = [F(0)] * N
    for i in range(m):
        if basis[i] < N:
            x[basis[i]] = T[i][W]
    return x


# --------------------------------------------------------------------------- order feasibility
def _check_edges(n, edges):
    for (i, j, k) in edges:
        if not (0 <= i < j < k < n):
            raise ValueError(f"edge {(i, j, k)} must satisfy 0 <= i < j < k < {n}")


def _gap_rows(n, edges):
    rows = []
    for (i, j, k) in edges:
        r = [0] * (n - 1)
        for t in range(i, j):
            r[t] += 1
        for t in range(j, k):
            r[t] -= 1
        rows.append(r)
    return rows


def _verify_point(n, edges, g):
    if len(g) != n - 1 or any(x <= 0 for x in g):
        return False
    return all(sum(a * b for a, b in zip(r, g)) == 0 for r in _gap_rows(n, edges))


def _verify_farkas(n, edges, y):
    E = _gap_rows(n, edges)
    w = [sum(y[e] * E[e][t] for e in range(len(E))) for t in range(n - 1)]
    return all(x >= 0 for x in w) and any(x > 0 for x in w)


def _gaps_to_x(g):
    tot = sum(g)
    x = [F(0)]
    for v in g:
        x.append(x[-1] + v / tot)
    return x


def order_feasible(n, edges):
    """Exact decision: does {2x_j = x_i + x_k} have a strictly increasing solution?

    Returns (True, {'x': [Fractions with x_0=0, x_{n-1}=1], 'gaps': [...]}),
            (False, {'y': [Fractions, one per edge], 'w': [...]}) with E^T y = w >= 0, w != 0,
         or (None, reason) if exact verification of either certificate failed."""
    edges = [tuple(e) for e in edges]
    _check_edges(n, edges)
    if n <= 1:
        return True, {"x": [F(0)] * n, "gaps": []}
    if not edges:
        g = [F(1)] * (n - 1)
        return True, {"x": _gaps_to_x(g), "gaps": g}
    E = _gap_rows(n, edges)
    m, G = len(E), n - 1
    # (b) Farkas: variables y+ (m), y- (m), w (G);  sum_e E[e][t] (y+ - y-)_e - w_t = 0;  sum w = 1.
    A, b = [], []
    for t in range(G):
        A.append([E[e][t] for e in range(m)] + [-E[e][t] for e in range(m)]
                 + [-1 if s == t else 0 for s in range(G)])
        b.append(0)
    A.append([0] * (2 * m) + [1] * G)
    b.append(1)
    sol = _lp_feasible(A, b)
    if sol is not None:
        y = [sol[e] - sol[m + e] for e in range(m)]
        if _verify_farkas(n, edges, y):
            w = [sum(y[e] * E[e][t] for e in range(m)) for t in range(G)]
            return False, {"y": y, "w": w}
        return None, "farkas verification failed"
    # (a) point: g = 1 + h, h >= 0, E h = -E 1
    A = [list(r) for r in E]
    b = [-sum(r) for r in E]
    sol = _lp_feasible(A, b)
    if sol is not None:
        g = [1 + h for h in sol]
        if _verify_point(n, edges, g):
            return True, {"x": _gaps_to_x(g), "gaps": g}
    return None, "point verification failed"


def verify_certificate(n, edges, feasible, cert):
    """Independent exact re-check of a certificate returned by order_feasible."""
    edges = [tuple(e) for e in edges]
    if feasible is True:
        x = cert["x"]
        return (len(x) == n and all(x[t] < x[t + 1] for t in range(n - 1))
                and all(x[i] + x[k] == 2 * x[j] for i, j, k in edges))
    if feasible is False:
        return _verify_farkas(n, edges, cert["y"])
    return False


def iis(n, edges):
    """Irreducible order-infeasible subset of edges (deletion filter); None if edges are feasible.
    Raises if order_feasible is inconclusive."""
    edges = [tuple(e) for e in edges]
    ok, _ = order_feasible(n, edges)
    if ok is None:
        raise RuntimeError("order_feasible inconclusive")
    if ok:
        return None
    cur = list(edges)
    t = 0
    while t < len(cur):
        trial = cur[:t] + cur[t + 1:]
        ok, _ = order_feasible(n, trial)
        if ok is None:
            raise RuntimeError("order_feasible inconclusive")
        if ok:
            t += 1
        else:
            cur = trial
    return cur


# --------------------------------------------------------------------------- forced relations
def _x_rows(n, edges):
    rows = []
    for (i, j, k) in edges:
        r = [0] * n
        r[i] += 1
        r[k] += 1
        r[j] -= 2
        rows.append(r)
    return rows


def _rel_vec(n, rel):
    kind = rel[0]
    v = [0] * n
    if kind == "extra_ap":
        a, b, c = rel[1]
        v[a] += 1; v[c] += 1; v[b] -= 2
    elif kind == "diff":
        a, b, c, d = rel[1]  # a < b < c < d : x_a + x_d - x_b - x_c
        v[a] += 1; v[d] += 1; v[b] -= 1; v[c] -= 1
    else:
        raise ValueError(rel)
    return v


def forced_relations(n, edges):
    """Relations forced identically on the solution space of the AP equations (assumes the pattern
    is order-feasible, otherwise they are vacuous).  Returns dict with lists:
    'extra_ap' [(a,b,c)], 'diff' [(a,b,c,d)], 'nonlinear' [(e1,e2)]."""
    edges = [tuple(e) for e in edges]
    R, piv = _rref(_x_rows(n, edges), n) if edges else ([], [])
    listed = {frozenset(e) for e in edges}
    out = {"extra_ap": [], "diff": [], "nonlinear": []}
    for a, b, c in itertools.combinations(range(n), 3):
        if frozenset((a, b, c)) in listed:
            continue
        if _in_rowspace(_rel_vec(n, ("extra_ap", (a, b, c))), R, piv):
            out["extra_ap"].append((a, b, c))
    for q in itertools.combinations(range(n), 4):
        if _in_rowspace(_rel_vec(n, ("diff", q)), R, piv):
            out["diff"].append(q)
    for e1, e2 in itertools.combinations(edges, 2):
        if len(set(e1) & set(e2)) >= 2:
            out["nonlinear"].append((e1, e2))
    return out


def is_forced(n, edges, relation):
    """Is `relation` (('order',) | ('extra_ap',(a,b,c)) | ('diff',(a,b,c,d))) forced by `edges`?
    For 'extra_ap' the triple must not be a listed edge.  'order' means order-infeasible."""
    edges = [tuple(e) for e in edges]
    if relation[0] == "order":
        ok, _ = order_feasible(n, edges)
        if ok is None:
            raise RuntimeError("order_feasible inconclusive")
        return not ok
    if relation[0] == "extra_ap" and frozenset(relation[1]) in {frozenset(e) for e in edges}:
        return False
    R, piv = _rref(_x_rows(n, edges), n) if edges else ([], [])
    return _in_rowspace(_rel_vec(n, relation), R, piv)


def forbidden_core(n, edges, relation):
    """Deletion filter: a minimal sub-pattern of `edges` that still forces `relation`
    (or is still order-infeasible for relation == ('order',)).  Raises if `edges` does not force it."""
    edges = [tuple(e) for e in edges]
    if not is_forced(n, edges, relation):
        raise ValueError("relation is not forced by the given edges")
    cur = list(edges)
    t = 0
    while t < len(cur):
        trial = cur[:t] + cur[t + 1:]
        if is_forced(n, trial, relation):
            cur = trial
        else:
            t += 1
    return cur


# --------------------------------------------------------------------------- exact realization
def _scale_to_ints(x):
    den = 1
    for v in x:
        den = den * v.denominator // math.gcd(den, v.denominator)
    return [int(v * den) for v in x]


def realize_exact(n, edges, tries=20, seed=0):
    """Exact realizability of the ordered pattern.

    Returns (True, integer_set) -- verified exactly: strictly increasing, AP set equals `edges`,
    (4,5)-set -- or (False, reason, forced_relation) with reason in
    'order-infeasible' (relation = certificate dict), 'forced extra AP' (relation = ('extra_ap', (a,b,c))),
    'forced repeated difference' (relation = ('diff', (a,b),(c,d)) meaning x_b-x_a = x_d-x_c, or for a
    nonlinear pattern ('nonlinear', e1, e2)), or 'inconclusive'."""
    edges = [tuple(e) for e in edges]
    _check_edges(n, edges)
    ok, cert = order_feasible(n, edges)
    if ok is None:
        return False, "inconclusive", cert
    if not ok:
        return False, "order-infeasible", cert
    fr = forced_relations(n, edges)
    if fr["extra_ap"]:
        return False, "forced extra AP", ("extra_ap", fr["extra_ap"][0])
    if fr["diff"]:
        a, b, c, d = fr["diff"][0]
        return False, "forced repeated difference", ("diff", (a, b), (c, d))
    if fr["nonlinear"]:
        e1, e2 = fr["nonlinear"][0]
        return False, "forced repeated difference", ("nonlinear", e1, e2)
    # No forced failure: a generic strictly increasing point works.  Build and verify exactly.
    rnd = random.Random(seed)
    g0 = cert["gaps"]
    basis = _nullspace(_gap_rows(n, edges), n - 1) if edges else [
        [F(1) if s == t else F(0) for s in range(n - 1)] for t in range(n - 1)]
    want = {frozenset(e) for e in edges}
    for attempt in range(tries):
        u = [F(0)] * (n - 1)
        span = 10 ** (3 + attempt)
        for v in basis:
            r = rnd.randint(-span, span)
            u = [a + r * b for a, b in zip(u, v)]
        eps_den = 1
        eps = None
        for t in range(n - 1):
            if u[t] != 0:
                cap = g0[t] / (2 * abs(u[t]))
                eps = cap if eps is None else min(eps, cap)
        if eps is None:
            g = list(g0)
        else:
            g = [a + (eps * rnd.randint(1, 10 ** 6) / 10 ** 6) * b for a, b in zip(g0, u)]
        x = _gaps_to_x(g)
        if not all(x[t] < x[t + 1] for t in range(n - 1)):
            continue
        vals = _scale_to_ints(x)
        got = {frozenset((vals.index(p), vals.index(q), vals.index(r))) for p, q, r in ap_edges(vals)}
        if got == want and is_45_set(vals):
            return True, vals
    return False, "inconclusive", "generic point failed verification (unexpected)"
