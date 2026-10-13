"""
Abstract engine for "ordered midpoint hypergraphs" (RESEARCH_PLAN P1.4, Track U2).

An ordered midpoint hypergraph on vertices 0..n-1 is a set of labeled edges (i, j, k), i<j<k,
j = "midpoint", such that
  (a) every j is the midpoint of at most one edge,
  (b) linearity: two edges share at most one vertex,
  (c) (optional) F7-freeness: no 5 edges forming F7 = {012,034,056,135,246}.
Every (4,5)-set gives one (START_HERE section 2). c_hyp(n) = min alpha over such hypergraphs, where
alpha = largest vertex set containing no edge. c_hyp(n) <= f(n) (realizability is not imposed).

Engine: OR-tools CP-SAT, CEGAR loop.  Boolean e[i,j,k]; static constraints (a), (b), m bounds, a
reflection lex-leader constraint.  Lazy cuts:
  * alpha cut: if the solution has alpha > T, pick several (T+1)-subsets I of independent sets and
    add  sum_{i<j<k in I} e[i,j,k] >= 1  (valid: an alpha<=T hypergraph has an edge in every
    (T+1)-set).  Cuts are valid for every T' <= T, so all cuts are kept while T is decreased.
  * F7 cut: after each solution, find every F7 copy and add "not all 5 edges".
Why CP-SAT and not pysat: the cut pool is small (hundreds to few thousands of clauses), CP-SAT's
presolve + LNS + multi-worker portfolio handle the cardinality/lex constraints natively, and
re-solving from scratch with a solution hint was fast enough for the sizes needed (n <= 16).

Reflection symmetry j -> n-1-j: (i,j,k) -> (n-1-k, n-1-j, n-1-i).  The reflected hypergraph is again
an ordered midpoint hypergraph with the same alpha, same m, same F7-freeness (and, for real sets,
the reflected set -A is again a (4,5)-set with the same h).  So each reflection orbit has a member
whose edge-indicator vector (in a fixed variable order) is lexicographically <= its reflection's;
requiring this loses no orbit.  All lazy cuts are properties of alpha/F7 only (invariant under
reflection), so they never remove both members of an orbit.
"""
from __future__ import annotations

import gzip
import itertools
import json
import random
import time

from ortools.sat.python import cp_model

from .saturated import alpha_of_edges, is_linear

# ----------------------------------------------------------------------------- combinatorics


def hy_m_need(n, T):
    """Henning-Yeo (linear + F7-free, [published]): 17*tau <= 5n + 3m.  A hypergraph with alpha <= T
    has tau = n - alpha >= n - T, hence m >= ceil((17(n-T) - 5n)/3).  Valid only under F7-freeness."""
    return max(0, -((5 * n - 17 * (n - T)) // 3))


def triples(n):
    return [(i, j, k) for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n)]


def is_ordered_midpoint_hypergraph(n, edges):
    """(a) + (b) + vertex range; returns bool."""
    mids = [j for (_, j, _) in edges]
    if len(set(mids)) != len(mids):
        return False
    if not all(0 <= i < j < k < n for (i, j, k) in edges):
        return False
    return is_linear(edges)


def find_f7(edges, limit=None):
    """All copies of F7 = {012,034,056,135,246} in the 3-uniform hypergraph `edges`.
    Returns a list of 5-tuples of edges.  F7 = a point p on three edges E1,E2,E3 plus two edges
    T1, T2 that each take one further point from each Ei, T1, T2 complementary."""
    es = {frozenset(e): tuple(e) for e in edges}
    inc = {}
    for e in es:
        for v in e:
            inc.setdefault(v, []).append(e)
    out = []
    seen = set()
    for p, lst in inc.items():
        if len(lst) < 3:
            continue
        for E in itertools.combinations(lst, 3):
            rest = [sorted(e - {p}) for e in E]
            # choose x_t in rest[t]; T1 = {x1,x2,x3}, T2 = complements; fix x_1 = rest[0][0]
            for c2 in (0, 1):
                for c3 in (0, 1):
                    T1 = frozenset((rest[0][0], rest[1][c2], rest[2][c3]))
                    T2 = frozenset((rest[0][1], rest[1][1 - c2], rest[2][1 - c3]))
                    if T1 in es and T2 in es:
                        key = frozenset(E + (T1, T2))
                        if key not in seen:
                            seen.add(key)
                            out.append(tuple(es[x] if x in es else tuple(sorted(x)) for x in
                                             list(E) + [T1, T2]))
                            if limit and len(out) >= limit:
                                return out
    return out


def is_f7_free(edges):
    return not find_f7(edges, limit=1)


def independent_sets(n, edges, size, limit=50, rng=None, want_max=False):
    """Up to `limit` independent sets (as sorted tuples) of exactly `size` vertices.
    With want_max, returns instead (alpha, one maximum independent set) computed exactly."""
    rng = rng or random.Random(0)
    by_v = [[] for _ in range(n)]
    for e in edges:
        for v in e:
            by_v[v].append(frozenset(e))
    deg = [len(x) for x in by_v]
    order = sorted(range(n), key=lambda v: (-deg[v], rng.random()))
    pos = {v: t for t, v in enumerate(order)}
    masks_by_last = [[] for _ in range(n)]
    for e in edges:
        ps = sorted(pos[v] for v in e)
        masks_by_last[ps[2]].append((1 << ps[0]) | (1 << ps[1]) | (1 << ps[2]))
    res = []
    best = [0, 0]  # size, mask

    def rec(i, chosen, sz):
        if want_max:
            if sz + (n - i) <= best[0]:
                return
            if i == n:
                best[0], best[1] = sz, chosen
                return
        else:
            if len(res) >= limit or sz + (n - i) < size:
                return
            if sz == size:
                res.append(tuple(sorted(order[t] for t in range(n) if chosen >> t & 1)))
                return
        c2 = chosen | (1 << i)
        if all(m & c2 != m for m in masks_by_last[i]):
            rec(i + 1, c2, sz + 1)
        rec(i + 1, chosen, sz)

    rec(0, 0, 0)
    if want_max:
        return best[0], tuple(sorted(order[t] for t in range(n) if best[1] >> t & 1))
    return res


# ----------------------------------------------------------------------------- model


class Model:
    """Wrapper: CP-SAT model + variable table + cut bookkeeping."""

    def __init__(self, n, m_min=0, m_exact=None, symmetry=True, m_max=None):
        self.n = n
        self.model = cp_model.CpModel()
        self.tri = triples(n)
        self.e = {t: self.model.NewBoolVar("e%d_%d_%d" % t) for t in self.tri}
        self.ncuts = 0
        self.nf7 = 0
        M = self.model
        # (a) at most one edge per midpoint
        for j in range(1, n - 1):
            M.AddAtMostOne([self.e[(i, j, k)] for i in range(j) for k in range(j + 1, n)])
        # (b) linearity: any pair of vertices lies in at most one edge
        for a, b in itertools.combinations(range(n), 2):
            lits = [self.e[t] for t in self.tri if a in t and b in t]
            if len(lits) > 1:
                M.AddAtMostOne(lits)
        total = sum(self.e.values())
        if m_exact is not None:
            M.Add(total == m_exact)
        else:
            if m_min > 0:
                M.Add(total >= m_min)
            if m_max is not None:
                M.Add(total <= m_max)
        self.total = total
        if symmetry:
            self._add_lex()

    def _add_lex(self):
        """e-vector <=_lex its reflection (document: see module docstring)."""
        n, M = self.n, self.model
        refl = lambda t: (n - 1 - t[2], n - 1 - t[1], n - 1 - t[0])  # noqa: E731
        pairs = []
        used = set()
        for t in self.tri:
            r = refl(t)
            if r == t or r in used:
                continue
            used.add(t)
            pairs.append((self.e[t], self.e[r]))
        eq_prev = None  # None means constant True
        for idx, (a, b) in enumerate(pairs):
            if eq_prev is None:
                M.AddBoolOr([a.Not(), b])  # a <= b
            else:
                M.AddBoolOr([eq_prev.Not(), a.Not(), b])
            if idx == len(pairs) - 1:
                break
            eq = M.NewBoolVar("eq%d" % idx)
            pre = [] if eq_prev is None else [eq_prev.Not()]
            M.AddBoolOr(pre + [a, b, eq])
            M.AddBoolOr(pre + [a.Not(), b.Not(), eq])
            eq_prev = eq

    def add_alpha_cut(self, I):
        self.model.AddBoolOr([self.e[t] for t in itertools.combinations(sorted(I), 3)])
        self.ncuts += 1

    def add_nogood(self, edges):
        self.model.AddBoolOr([self.e[tuple(sorted(x))].Not() for x in edges])
        self.nf7 += 1

    def hint(self, edges):
        es = {tuple(sorted(x)) for x in edges}
        self.model.ClearHints()
        for t in self.tri:
            self.model.AddHint(self.e[t], 1 if t in es else 0)


def build_model(n, m_min=0, m_exact=None, forbid_f7="lazy", symmetry=True, m_max=None):
    """Static part of the model (constraints (a), (b), m bounds, lex symmetry breaking).
    forbid_f7 'lazy' means F7 no-goods are added by the CEGAR loops; 'none' disables them.
    Returns a `Model` (attribute .model is the cp_model.CpModel)."""
    if forbid_f7 not in ("lazy", "none"):
        raise ValueError("forbid_f7 must be 'lazy' or 'none'")
    mod = Model(n, m_min=m_min, m_exact=m_exact, symmetry=symmetry, m_max=m_max)
    mod.forbid_f7 = forbid_f7
    return mod


def _solve(mod, time_left, workers=4, seed=0):
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = max(0.5, time_left)
    s.parameters.num_workers = workers
    s.parameters.random_seed = seed
    st = s.Solve(mod.model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        edges = [t for t in mod.tri if s.Value(mod.e[t])]
        return "SAT", edges
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


def _cegar_step(mod, edges, T, rng, ncuts_per_iter, stats):
    """Check one solution. Returns ('ok', alpha) if alpha<=T and F7-free (if requested);
    otherwise adds cuts and returns ('cut', alpha)."""
    n = mod.n
    if mod.forbid_f7 == "lazy":
        copies = find_f7(edges)
        if copies:
            for c in copies:
                mod.add_nogood(c)
            stats["f7_cuts"] += len(copies)
            return "cut", None
    a, _ = independent_sets(n, edges, 0, want_max=True)
    if a <= T:
        return "ok", a
    sets = independent_sets(n, edges, T + 1, limit=ncuts_per_iter, rng=rng)
    for I in sets:
        mod.add_alpha_cut(I)
    stats["alpha_cuts"] += len(sets)
    return "cut", a


def solve_min_alpha(n, m_min=0, forbid_f7=True, time_limit=600, m_exact=None, symmetry=True,
                    start_T=None, ncuts_per_iter=40, workers=4, verbose=False, seed=0, use_hy=False,
                    m_max=None):
    """Minimum alpha over ordered midpoint hypergraphs on n vertices (m >= m_min edges).
    Returns (alpha_min, witness_edges, stats).  stats['optimal'] tells whether alpha_min is proved
    optimal (the infeasibility of T = alpha_min - 1 was proved by UNSAT within the time limit);
    otherwise alpha_min is only an upper bound and stats['lower'] the proved lower bound.
    Decreasing-T strategy: all cuts stay valid when T decreases.
    use_hy (needs forbid_f7): when testing alpha <= T also impose m >= hy_m_need(n, T), a consequence
    of the PUBLISHED Henning-Yeo theorem; the result is then 'optimal modulo Henning-Yeo'.  With
    use_hy=False the proof is by the solver alone."""
    t0 = time.time()
    rng = random.Random(seed)
    mod = build_model(n, m_min=m_min, m_exact=m_exact, forbid_f7="lazy" if forbid_f7 else "none",
                      symmetry=symmetry, m_max=m_max)
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0, "optimal": False, "lower": 1,
             "per_T": {}, "use_hy": bool(use_hy and forbid_f7)}
    hy_added = 0
    best_edges, best_alpha = None, None
    T = start_T if start_T is not None else n  # alpha <= n is always true
    while True:
        tT = time.time()
        status = "?"
        if use_hy and forbid_f7 and m_exact is None:
            need = hy_m_need(n, T)
            if need > hy_added:  # monotone in decreasing T, so permanent
                mod.model.Add(mod.total >= need)
                hy_added = need
        while True:
            left = time_limit - (time.time() - t0)
            if left <= 0:
                status = "TIMEOUT"
                break
            r, edges = _solve(mod, left, workers=workers, seed=seed)
            stats["solves"] += 1
            if r == "UNSAT":
                status = "UNSAT"
                break
            if r == "UNKNOWN":
                status = "TIMEOUT"
                break
            kind, a = _cegar_step(mod, edges, T, rng, ncuts_per_iter, stats)
            if kind == "ok":
                best_edges, best_alpha = list(edges), a
                status = "SAT"
                break
            if verbose and stats["solves"] % 20 == 0:
                print("n=%d T=%d solves=%d alpha_cuts=%d f7=%d t=%.0fs" % (
                    n, T, stats["solves"], stats["alpha_cuts"], stats["f7_cuts"],
                    time.time() - t0), flush=True)
        stats["per_T"][T] = (status, round(time.time() - tT, 2))
        if verbose:
            print("n=%d T=%d -> %s (%.1fs)" % (n, T, status, time.time() - tT), flush=True)
        if status == "SAT":
            T = best_alpha - 1
            if T < 1:
                stats["optimal"], stats["lower"] = True, best_alpha
                break
            mod.hint(best_edges)
            continue
        if status == "UNSAT":
            stats["optimal"], stats["lower"] = True, T + 1
        else:
            stats["lower"] = T + 1 if best_alpha is None else 1
            stats["lower"] = 1
        break
    stats["time"] = round(time.time() - t0, 2)
    stats["cuts_total"] = mod.ncuts + mod.nf7
    if best_alpha is None:
        # never found a solution within T=n: infeasible model (e.g. m_min too large)
        return None, None, stats
    return best_alpha, best_edges, stats


def feasible_alpha_le(n, T, m_min=0, m_exact=None, forbid_f7=True, time_limit=600,
                      symmetry=True, ncuts_per_iter=40, workers=4, seed=0, m_max=None, use_hy=False):
    """Decide: is there a hypergraph with alpha <= T?  Returns ('SAT'|'UNSAT'|'UNKNOWN', edges, stats)."""
    t0 = time.time()
    rng = random.Random(seed)
    mod = build_model(n, m_min=m_min, m_exact=m_exact, forbid_f7="lazy" if forbid_f7 else "none",
                      symmetry=symmetry, m_max=m_max)
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0}
    if use_hy and forbid_f7 and m_exact is None:
        mod.model.Add(mod.total >= hy_m_need(n, T))
    while True:
        left = time_limit - (time.time() - t0)
        if left <= 0:
            return "UNKNOWN", None, stats
        r, edges = _solve(mod, left, workers=workers, seed=seed)
        stats["solves"] += 1
        if r != "SAT":
            stats["time"] = round(time.time() - t0, 2)
            return r, None, stats
        kind, a = _cegar_step(mod, edges, T, rng, ncuts_per_iter, stats)
        if kind == "ok":
            stats["time"] = round(time.time() - t0, 2)
            return "SAT", edges, stats


def enumerate_solutions(n, T, m_exact, callback=None, limit=None, time_limit=600,
                        forbid_f7=True, symmetry=True, out_path=None, ncuts_per_iter=40,
                        workers=4, seed=0):
    """Enumerate ALL hypergraphs with alpha <= T and exactly m_exact edges (up to reflection if
    symmetry=True: lex-minimal representatives).  Each found solution is blocked by
    OR(not e for e in solution), which is sound because m is fixed (a different solution with the
    same m cannot contain this one).  If out_path is given (.jsonl.gz) solutions are streamed there
    and not kept.  Returns (count, solutions_or_None, status) with status 'COMPLETE', 'LIMIT' or
    'TIMEOUT'."""
    t0 = time.time()
    rng = random.Random(seed)
    mod = build_model(n, m_exact=m_exact, forbid_f7="lazy" if forbid_f7 else "none",
                      symmetry=symmetry)
    stats = {"alpha_cuts": 0, "f7_cuts": 0}
    sols = None if out_path else []
    fh = gzip.open(out_path, "wt") if out_path else None
    count = 0
    status = "COMPLETE"
    try:
        while True:
            left = time_limit - (time.time() - t0)
            if left <= 0:
                status = "TIMEOUT"
                break
            r, edges = _solve(mod, left, workers=workers, seed=seed)
            if r == "UNSAT":
                break
            if r == "UNKNOWN":
                status = "TIMEOUT"
                break
            kind, a = _cegar_step(mod, edges, T, rng, ncuts_per_iter, stats)
            if kind == "cut":
                continue
            count += 1
            if callback:
                callback(edges, a)
            if fh:
                fh.write(json.dumps({"edges": edges, "alpha": a}) + "\n")
            else:
                sols.append((edges, a))
            mod.model.AddBoolOr([mod.e[t].Not() for t in edges])  # block (sound: m fixed)
            if limit and count >= limit:
                status = "LIMIT"
                break
    finally:
        if fh:
            fh.close()
    return count, sols, status


# ----------------------------------------------------------------------------- brute force (tests)


def brute_min_alpha(n, forbid_f7=True, m_min=0):
    """Exhaustive DFS over all ordered midpoint hypergraphs (for tests, n <= 9).  Returns min alpha.
    Uses: each added edge lowers alpha by at most 1."""
    best = [n]
    mids = list(range(1, n - 1))

    def rec(idx, edges, used_pairs):
        undecided = len(mids) - idx
        if idx == len(mids):
            if len(edges) < m_min:
                return
            if forbid_f7 and not is_f7_free(edges):
                return
            a = alpha_of_edges(n, edges)
            if a < best[0]:
                best[0] = a
            return
        if len(edges) + undecided < m_min:
            return
        if edges and alpha_of_edges(n, edges) - undecided >= best[0]:
            return
        j = mids[idx]
        for i in range(j):
            for k in range(j + 1, n):
                p = ((1 << (i * n + j)) | (1 << (j * n + k)) | (1 << (i * n + k)))
                if p & used_pairs:
                    continue
                rec(idx + 1, edges + [(i, j, k)], used_pairs | p)
        rec(idx + 1, edges, used_pairs)

    rec(0, [], 0)
    return best[0]
