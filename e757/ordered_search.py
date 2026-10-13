"""
Ordered midpoint-map search: enumerate (4,5)-sets by their AP structure, in sorted order.

Label the points of a candidate set by their rank: x_0 < x_1 < ... < x_{n-1}, with x_0 = 0 and
x_{n-1} = 1. Each interior point j is the midpoint of at most one 3-AP {i, j, k} with i < j < k
(Ma-Tang Lemma 2.4), so a set is described by choices c_j in {None} U {(i, k) : i < j < k}.
Fixing ranks removes the relabelling symmetry; only the reflection j -> n-1-j remains.

Pruning, in order of cost:
  1. linearity: two APs may share at most one point (Ma-Tang Lemma 2.5);
  2. budget: at most `max_none` interior points are not midpoints (Henning-Yeo: beating 4/7 at size n
     needs m >= m_need, see e757.fn_bounds.beat_feasibility);
  3. order feasibility: an LP checks that 0 = x_0 < ... < x_{n-1} = 1 is compatible with the AP
     equations chosen so far (scipy HiGHS; floats, used only for pruning);
  4. alpha target: near the leaves, alpha(current edges) - (#undecided points) > target prunes.
Leaves are realized exactly (Fractions), checked for (4,5) exactly, and h is computed exactly.

This is a correct but plain Python DFS. Expected reach: complete enumeration for n <= 10-11, and
randomized / restricted runs (seeded with partial structures) beyond that. For n >= 14 rewrite the
core in a compiled language or drive it with CP-SAT; keep the exact leaf check.

Example:
    from e757.ordered_search import search
    for hit in search(n=10, target_alpha=6, max_none=1, limit=10):
        print(hit)   # search returns a list
"""
from __future__ import annotations

import itertools
import random
from fractions import Fraction

from .core import ap_edges, is_45_set, alpha

try:
    import numpy as np
    from scipy.optimize import linprog
    HAVE_SCIPY = True
except Exception:  # noqa: BLE001
    HAVE_SCIPY = False


def _order_lp(n, edges, want_point=False):
    """Max t s.t. x_{j+1} - x_j >= t, x_0 = 0, x_{n-1} = 1, and 2 x_j = x_i + x_k for edges.
    Returns (feasible_with_t>1e-9, x or None)."""
    if not HAVE_SCIPY:
        return True, None
    nv = n + 1  # x_0..x_{n-1}, t
    c = np.zeros(nv)
    c[n] = -1.0
    A_ub, b_ub = [], []
    for j in range(n - 1):
        row = np.zeros(nv)
        row[j] = 1.0
        row[j + 1] = -1.0
        row[n] = 1.0
        A_ub.append(row)
        b_ub.append(0.0)
    A_eq, b_eq = [], []
    r = np.zeros(nv); r[0] = 1.0; A_eq.append(r); b_eq.append(0.0)
    r = np.zeros(nv); r[n - 1] = 1.0; A_eq.append(r); b_eq.append(1.0)
    for i, j, k in edges:
        r = np.zeros(nv)
        r[i] += 1.0
        r[k] += 1.0
        r[j] -= 2.0
        A_eq.append(r)
        b_eq.append(0.0)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), A_eq=np.array(A_eq),
                  b_eq=np.array(b_eq), bounds=[(None, None)] * n + [(None, 1.0)], method="highs")
    if res.status != 0:
        return False, None
    ok = -res.fun > 1e-9
    return ok, (res.x[:n] if want_point else None)


def _exact_realization(n, edges, rng, tries=8):
    """Exact rational point of {x_0=0, x_{n-1}=1, AP equations} with strictly increasing coords
    and the (4,5) property, chosen generically near the LP interior point.
    Returns a list of Fractions or None."""
    import sympy as sp
    M = sp.zeros(len(edges) + 2, n)
    rhs = sp.zeros(len(edges) + 2, 1)
    M[0, 0] = 1
    M[1, n - 1] = 1
    rhs[1] = 1
    for r, (i, j, k) in enumerate(edges, start=2):
        M[r, i] += 1
        M[r, k] += 1
        M[r, j] -= 2
    try:
        sol, params = M.gauss_jordan_solve(rhs)
    except ValueError:  # inconsistent system
        return None
    pivots = M.rref()[1]
    free_cols = [c for c in range(n) if c not in pivots]
    ok, x0 = _order_lp(n, edges, want_point=True)
    if not ok:
        return None
    den = 10 ** 6
    for t in range(tries):
        subs = {}
        for p, col in zip(list(params), free_cols):
            base = float(x0[col]) if x0 is not None else rng.random()
            subs[p] = sp.Rational(int(round(base * den)) + rng.randint(-50, 50) * (t + 1), den)
        vals = [Fraction(str(sp.nsimplify(sol[idx].subs(subs)))) for idx in range(n)]
        if all(vals[a] < vals[a + 1] for a in range(n - 1)) and is_45_set(vals):
            return vals
    return None


def search(n, target_alpha, max_none=0, limit=None, seed=0, order=None, time_check=None):
    """Return a list of dicts {set, h, m, n} for (4,5)-sets on n points (ranked 0..n-1) whose AP
    hypergraph has independence number <= target_alpha and at most max_none non-midpoints.

    order: sequence of interior vertices in the order they are decided (default 1..n-2).
    Exhaustive for the given parameters (up to LP numerical tolerance in pruning)."""
    rng = random.Random(seed)
    interior = list(order) if order is not None else list(range(1, n - 1))
    edges = []
    pair_used = set()
    found = 0
    seen_sets = set()

    def options(j):
        opts = [(i, k) for i in range(j) for k in range(j + 1, n)]
        rng.shuffle(opts)
        return opts

    def rec(pos, nones):
        nonlocal found
        if limit is not None and found >= limit:
            return
        remaining = len(interior) - pos
        if remaining <= 4 and edges:
            lo = alpha(list(range(n)), [tuple(e) for e in edges]) - remaining
            if lo > target_alpha:
                return
        if pos == len(interior):
            labeled = [tuple(e) for e in edges]
            vals = _exact_realization(n, labeled, rng)
            if vals is None:
                return
            key = tuple(vals)
            if key in seen_sets:
                return
            seen_sets.add(key)
            real_edges = ap_edges(vals)
            h = alpha(vals, real_edges)
            if h <= target_alpha:
                found += 1
                yield_list.append({"set": vals, "h": h, "m": len(real_edges), "n": n})
            return
        j = interior[pos]
        for (i, k) in options(j):
            prs = [frozenset(p) for p in itertools.combinations((i, j, k), 2)]
            if any(p in pair_used for p in prs):
                continue
            edges.append((i, j, k))
            pair_used.update(prs)
            ok, _ = _order_lp(n, edges)
            if ok:
                rec(pos + 1, nones)
            edges.pop()
            for p in prs:
                pair_used.discard(p)
            if limit is not None and found >= limit:
                return
        if nones < max_none:
            rec(pos + 1, nones + 1)

    yield_list = []
    rec(0, 0)
    return yield_list
