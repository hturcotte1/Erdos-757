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
import os
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

    def __init__(self, n, m_min=0, m_exact=None, symmetry=True, m_max=None, monotone=False,
                 medial=False, cores=None, core_max_edges=None, core_lit_budget=None):
        self.n = n
        self.model = cp_model.CpModel()
        self.tri = triples(n)
        self.e = {t: self.model.NewBoolVar("e%d_%d_%d" % t) for t in self.tri}
        self.ncuts = 0
        self.nf7 = 0
        self.strong_cuts = True
        self.eager_T = None
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
        self.constraint_counts = {}
        if monotone:
            self.constraint_counts["monotone"] = self.add_monotone()
        if medial:
            self.constraint_counts["medial"] = self.add_medial()
        if cores:
            self.constraint_counts["cores"] = self.add_cores(cores, core_max_edges, core_lit_budget)
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

    def add_alpha_cut(self, I, rhs=1):
        """sum of e over triples inside I >= rhs.  Valid whenever rhs <= |I| - T, because
        alpha(H) >= alpha(H[I]) >= |I| - e(I) (delete one vertex per edge inside I)."""
        lits = [self.e[t] for t in itertools.combinations(sorted(I), 3)]
        if rhs == 1:
            self.model.AddBoolOr(lits)
        else:
            self.model.Add(sum(lits) >= rhs)
        self.ncuts += 1

    # ---- realizability consequences (exact, see kb/known_results.md K30, K31) -------------------
    def add_monotone(self):
        """K30 monotone midpoints: edges (i,j,k),(i',j',k') with i<=i', k<=k', (i,k)!=(i',k')
        need j<j' (x_j=(x_i+x_k)/2 < (x_i'+x_k')/2).  Clause not both when j>=j'.  Returns #clauses."""
        cnt = 0
        for a in self.tri:
            for b in self.tri:
                if a[0] <= b[0] and a[2] <= b[2] and (a[0], a[2]) != (b[0], b[2]) and a[1] >= b[1]:
                    self.model.AddBoolOr([self.e[a].Not(), self.e[b].Not()])
                    cnt += 1
        return cnt

    def add_medial(self):
        """K31 no medial triangle: edges (a,b,c),(a,p,e),(c,q,e), a<b<c, a<p<e, c<q<e (a,c,e are
        endpoints of both edges they lie in).  x_q-x_p = x_b-x_a gives a repeated difference."""
        n, cnt = self.n, 0
        for a in range(n):
            for c in range(a + 2, n):
                for e in range(c + 1, n):
                    for b in range(a + 1, c):
                        for p in range(a + 1, e):
                            if p in (b, c):
                                continue
                            for q in range(c + 1, e):
                                self.model.AddBoolOr([self.e[(a, b, c)].Not(), self.e[(a, p, e)].Not(),
                                                      self.e[(c, q, e)].Not()])
                                cnt += 1
        return cnt

    def add_cores(self, cores, max_edges=None, lit_budget=None):
        """Forbidden-pattern library (data/forbidden_ordered_n7.json, _n8.json).  For each core on v
        ranks and each strictly increasing embedding of 0..v-1 into 0..n-1 (core and its reflection):
          order / diff cores: clause NOT(all edges of S)   (sound: S forces order-infeasibility or a
              parallelogram, i.e. a repeated difference);
          extra_ap cores (S forces an AP T not in S): clause NOT(all S) OR e[T], because a pattern
              that contains S AND lists T is not excluded by this core.
        Returns (#clauses, #literals).  Cores with more than max_edges edges are skipped; if
        lit_budget is given, cores are added by increasing size until the budget is exhausted."""
        n = self.n
        clauses = set()
        lits = 0
        order = sorted(cores, key=lambda c: (len(c["edges"]), c["n"]))
        for c in order:
            if max_edges is not None and len(c["edges"]) > max_edges:
                continue
            v = c["n"]
            if v > n:
                continue
            variants = []
            for refl in (False, True):
                if refl:
                    ed = [(v - 1 - k, v - 1 - j, v - 1 - i) for i, j, k in c["edges"]]
                    rel = None if c["relation"] is None else sorted(v - 1 - x for x in c["relation"])
                else:
                    ed = [tuple(e) for e in c["edges"]]
                    rel = c["relation"]
                variants.append((tuple(sorted(ed)), tuple(rel) if rel else None))
            new = set()
            for ed, rel in set(variants):
                for emb in itertools.combinations(range(n), v):
                    S = tuple(sorted(tuple(emb[x] for x in e) for e in ed))
                    T = tuple(emb[x] for x in rel) if (c["kind"] == "extra_ap") else None
                    new.add((S, T))
            if lit_budget is not None and lits + sum(len(S) + (T is not None) for S, T in new) > lit_budget:
                break
            for S, T in new:
                if (S, T) in clauses:
                    continue
                clauses.add((S, T))
                cl = [self.e[x].Not() for x in S]
                if T is not None:
                    cl.append(self.e[T])
                self.model.AddBoolOr(cl)
                lits += len(cl)
        return len(clauses), lits

    def add_f7_eager(self):
        """Forbid every copy of F7 up front: for each 7-subset of vertices and each distinct
        labeling of F7 on it (5040/|Aut|), NOT(all 5 triples are edges).  Returns #clauses."""
        F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
        pats = set()
        for perm in itertools.permutations(range(7)):
            pats.add(frozenset(frozenset(perm[v] for v in blk) for blk in F7))
        pats = [[tuple(sorted(b)) for b in pat] for pat in pats]
        cnt = 0
        for sub in itertools.combinations(range(self.n), 7):
            for pat in pats:
                self.model.AddBoolOr([self.e[tuple(sub[x] for x in b)].Not() for b in pat])
                cnt += 1
        self.constraint_counts["f7_eager"] = cnt
        return cnt

    def add_eager_alpha(self, T, sample=None, rng=None):
        """Eager encoding of alpha <= T: every (T+1)-subset I of the vertices contains an edge, i.e.
        OR_{i<j<k in I} e[i,j,k].  C(n, T+1) clauses; exact, so no alpha cuts are needed afterwards."""
        lits_of = {t: self.e[t] for t in self.tri}
        if sample is None:
            subsets = itertools.combinations(range(self.n), T + 1)
        else:  # hybrid mode: a random sample of subsets (the rest comes from lazy cuts)
            rng = rng or random.Random(0)
            subsets = (tuple(sorted(rng.sample(range(self.n), T + 1))) for _ in range(sample))
        for I in subsets:
            self.model.AddBoolOr([lits_of[t] for t in itertools.combinations(I, 3)])
        self.ncuts += 0
        self.eager_T = T

    def add_nogood(self, edges):
        self.model.AddBoolOr([self.e[tuple(sorted(x))].Not() for x in edges])
        self.nf7 += 1

    def hint(self, edges):
        es = {tuple(sorted(x)) for x in edges}
        self.model.ClearHints()
        for t in self.tri:
            self.model.AddHint(self.e[t], 1 if t in es else 0)


def build_model(n, m_min=0, m_exact=None, forbid_f7="lazy", symmetry=True, m_max=None, **mopts):
    """Static part of the model (constraints (a), (b), m bounds, lex symmetry breaking).
    forbid_f7 'lazy' means F7 no-goods are added by the CEGAR loops; 'none' disables them.
    Returns a `Model` (attribute .model is the cp_model.CpModel)."""
    if forbid_f7 not in ("lazy", "none", "eager"):
        raise ValueError("forbid_f7 must be 'lazy', 'eager' or 'none'")
    mod = Model(n, m_min=m_min, m_exact=m_exact, symmetry=symmetry, m_max=m_max, **mopts)
    mod.forbid_f7 = forbid_f7
    if forbid_f7 == "eager":
        mod.add_f7_eager()
        mod.forbid_f7 = "none"  # nothing left to do lazily
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
    a, Imax = independent_sets(n, edges, 0, want_max=True)
    if a <= T:
        return "ok", a
    sets = independent_sets(n, edges, T + 1, limit=ncuts_per_iter, rng=rng)
    for I in sets:
        mod.add_alpha_cut(I)
    stats["alpha_cuts"] += len(sets)
    if mod.strong_cuts:
        # counting cuts: e(I') >= |I'| - T for I' inside the independent set found
        for s_ in range(T + 2, a + 1):
            for _ in range(1 if s_ < a else 1):
                sub = Imax if s_ == a else rng.sample(Imax, s_)
                mod.add_alpha_cut(sub, rhs=s_ - T)
                stats["alpha_cuts"] += 1
    return "cut", a


def solve_min_alpha(n, m_min=0, forbid_f7=True, time_limit=600, m_exact=None, symmetry=True,
                    start_T=None, ncuts_per_iter=40, workers=4, verbose=False, seed=0, use_hy=False,
                    m_max=None, eager=True, **mopts):
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
                      symmetry=symmetry, m_max=m_max, **mopts)
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0, "optimal": False, "lower": 1,
             "per_T": {}, "use_hy": bool(use_hy and forbid_f7)}
    hy_added = 0
    best_edges, best_alpha = None, None
    T = start_T if start_T is not None else n  # alpha <= n is always true
    while True:
        tT = time.time()
        status = "?"
        if eager and T < n:
            mod.add_eager_alpha(T)
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
                      symmetry=True, ncuts_per_iter=40, workers=4, seed=0, m_max=None, use_hy=False,
                      eager=True, **mopts):
    """Decide: is there a hypergraph with alpha <= T?  Returns ('SAT'|'UNSAT'|'UNKNOWN', edges, stats)."""
    t0 = time.time()
    rng = random.Random(seed)
    mod = build_model(n, m_min=m_min, m_exact=m_exact, forbid_f7="lazy" if forbid_f7 else "none",
                      symmetry=symmetry, m_max=m_max, **mopts)
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0, "constraints": dict(mod.constraint_counts)}
    if use_hy and forbid_f7 and m_exact is None:
        mod.model.Add(mod.total >= hy_m_need(n, T))
    if eager is True:
        mod.add_eager_alpha(T)
    elif eager:  # hybrid: eager clauses for `eager` random (T+1)-subsets, the rest lazily
        mod.add_eager_alpha(T, sample=int(eager), rng=rng)
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
                        workers=4, seed=0, setup=None, **mopts):
    """Enumerate ALL hypergraphs with alpha <= T and exactly m_exact edges (up to reflection if
    symmetry=True: lex-minimal representatives).  Each found solution is blocked by
    OR(not e for e in solution), which is sound because m is fixed (a different solution with the
    same m cannot contain this one).  If out_path is given (.jsonl.gz) solutions are streamed there
    and not kept.  Returns (count, solutions_or_None, status) with status 'COMPLETE', 'LIMIT' or
    'TIMEOUT'."""
    t0 = time.time()
    rng = random.Random(seed)
    mod = build_model(n, m_exact=m_exact, forbid_f7="lazy" if forbid_f7 else "none",
                      symmetry=symmetry, **mopts)
    stats = {"alpha_cuts": 0, "f7_cuts": 0}
    if setup:
        setup(mod)  # e.g. case-split constraints
    enumerate_solutions.last = {"constraints": dict(mod.constraint_counts)}
    mod.add_eager_alpha(T)  # exact encoding of alpha <= T (C(n,T+1) clauses)
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


# ----------------------------------------------------------------------------- native enumeration


def enumerate_native(n, T, m_exact, path, limit=None, time_limit=3600, progress_path=None,
                     core_max_edges=4, cores=None, monotone=True, medial=True, setup=None,
                     report_every=5000):
    """Enumerate ALL solutions (no symmetry breaking) of: ordered midpoint hypergraph on n vertices,
    exactly m_exact edges, alpha <= T (eager), F7 forbidden (eager), K30/K31/cores (core_max_edges).
    Uses CP-SAT's enumerate_all_solutions (1 worker) and streams one JSON line (list of triples) per
    solution to `path`, flushed per solution.  Returns (count, status) with status 'EXHAUSTED'
    (all solutions listed), 'TIMEOUT' or 'LIMIT'.  A progress JSON is rewritten periodically."""
    t0 = time.time()
    mod = build_model(n, m_exact=m_exact, forbid_f7="eager", symmetry=False, monotone=monotone,
                      medial=medial, cores=cores, core_max_edges=core_max_edges)
    mod.add_eager_alpha(T)
    if setup:
        setup(mod)
    built = time.time() - t0
    tri = mod.tri
    evars = [mod.e[t] for t in tri]
    fh = open(path, "w")

    def prog(status):
        if progress_path:
            json.dump({"n": n, "T": T, "m": m_exact, "count": cb.count, "status": status,
                       "elapsed_s": round(time.time() - t0, 1), "build_s": round(built, 1),
                       "constraints": mod.constraint_counts,
                       "rate_per_s": round(cb.count / max(time.time() - t0 - built, 1e-9), 1)},
                      open(progress_path + ".tmp", "w"))
            os.replace(progress_path + ".tmp", progress_path)

    class CB(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.count = 0
            self.last = time.time()

        def on_solution_callback(self):
            fh.write(json.dumps([list(t) for t, v in zip(tri, evars) if self.Value(v)]) + "\n")
            fh.flush()
            self.count += 1
            if limit and self.count >= limit:
                self.hit_limit = True
                self.StopSearch()
            if self.count % report_every == 0 or time.time() - self.last > 30:
                self.last = time.time()
                prog("RUNNING")

    cb = CB()
    cb.hit_limit = False
    prog("RUNNING")
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_workers = 1
    solver.parameters.max_time_in_seconds = max(1.0, time_limit - built)
    st = solver.Solve(mod.model, cb)
    fh.close()
    if cb.hit_limit:
        status = "LIMIT"
    elif st in (cp_model.OPTIMAL, cp_model.INFEASIBLE):
        status = "EXHAUSTED"
    else:
        status = "TIMEOUT"
    prog(status)
    return cb.count, status


# ----------------------------------------------------------------------------- fast pattern checks


def core_hit(E, core):
    """Does the edge set E (set of triples) contain an order-preserving image of the core's S (or its
    reflection) that violates it?  (extra_ap cores: T absent from E.)  Backtracking over edges."""
    v = core["n"]
    for refl in (False, True):
        if refl:
            ed = [(v - 1 - k, v - 1 - j, v - 1 - i) for i, j, k in core["edges"]]
            rel = None if core["relation"] is None else tuple(sorted(v - 1 - x for x in core["relation"]))
        else:
            ed = [tuple(x) for x in core["edges"]]
            rel = None if core["relation"] is None else tuple(core["relation"])
        ed = sorted(ed)

        def rec(t, mp):
            if t == len(ed):
                # mp must be strictly increasing on its (all-core) domain
                ks = sorted(mp)
                if any(mp[a] >= mp[b] for a, b in zip(ks, ks[1:])):
                    return False
                if core["kind"] == "extra_ap" and tuple(mp[x] for x in rel) in E:
                    return False
                return True
            for e in E:
                nm = dict(mp)
                ok = True
                for a, b in zip(ed[t], e):
                    if nm.setdefault(a, b) != b:
                        ok = False
                        break
                if ok and len(set(nm.values())) == len(nm):
                    if rec(t + 1, nm):
                        return True
            return False

        if rec(0, {}):
            return True
    return False


def satisfies_all(n, edges, cores=None, monotone=True, medial=True, f7=True):
    """Fast check of linearity, midpoint injectivity, K30, K31, F7-freeness and the cores
    (same semantics as the clause set).  Does NOT check alpha."""
    if not is_ordered_midpoint_hypergraph(n, edges):
        return False
    if (monotone or medial) and C_viol_basic(n, edges, monotone, medial):
        return False
    if f7 and not is_f7_free(edges):
        return False
    E = {tuple(e) for e in edges}
    for core in (cores or []):
        if core["n"] <= n and core_hit(E, core):
            return False
    return True


def C_viol_basic(n, edges, monotone, medial):
    return constraint_violations(n, edges, monotone=monotone, medial=medial, cores=None)


# ----------------------------------------------------------------------------- realizability CEGAR


def _learn_core(mod, S, T=None, max_embed=20000):
    """Add the no-good 'not all of S (or T present)' for the pattern S found by the realizability
    oracle, generalised to every strictly increasing re-embedding of S's support (and its
    reflection) when C(n, v) <= max_embed.  Sound for any m: S forces a failure by itself.
    For an extra-AP core the clause is NOT(all S) OR e[T]."""
    n = mod.n
    sup = sorted({v for e in S for v in e} | (set(T) if T else set()))
    rl = {v: t for t, v in enumerate(sup)}
    Sr = [tuple(rl[v] for v in e) for e in S]
    Tr = tuple(rl[v] for v in T) if T else None
    v = len(sup)
    variants = {(tuple(sorted(Sr)), Tr)}
    variants.add((tuple(sorted((v - 1 - k, v - 1 - j, v - 1 - i) for i, j, k in Sr)),
                  None if Tr is None else tuple(sorted(v - 1 - x for x in Tr))))
    from math import comb
    added = 0
    for Sv, Tv in variants:
        if comb(n, v) <= max_embed:
            embs = itertools.combinations(range(n), v)
        elif Sv == tuple(sorted(Sr)):
            embs = [tuple(sup)]  # only the instance found
        else:
            embs = [tuple(n - 1 - x for x in reversed(sup))]  # its reflection
        for emb in embs:
            cl = [mod.e[tuple(emb[x] for x in e)].Not() for e in Sv]
            if Tv is not None:
                cl.append(mod.e[tuple(emb[x] for x in Tv)])
            mod.model.AddBoolOr(cl)
            added += 1
    return added


def solve_realizable(n, T, m_exact=None, m_min=0, m_max=None, forbid_f7=True, time_limit=3600,
                     workers=4, seed=0, eager=True, ncuts_per_iter=40, max_rounds=10**9,
                     verbose=False, **mopts):
    """CEGAR over REALIZABILITY: find an ordered midpoint hypergraph with alpha <= T (and the given
    m range) that e757.realizability.realize_exact accepts.  Every failure is turned into a minimal
    core (deletion filter) and learnt as a no-good (all re-embeddings).  Returns
    (status, info) with status 'SAT' (info['edges'], info['set'] = verified integer set),
    'UNSAT' (no realizable hypergraph exists in the searched class: all learnt clauses are
    consequences of exact linear algebra) or 'UNKNOWN' (time limit)."""
    from . import realizability as RZ
    t0 = time.time()
    rng = random.Random(seed)
    mod = build_model(n, m_min=m_min, m_exact=m_exact, m_max=m_max,
                      forbid_f7="lazy" if forbid_f7 else "none", **mopts)
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0, "rounds": 0, "learnt": 0,
             "fail_kinds": {}, "constraints": dict(mod.constraint_counts)}
    if eager is True:
        mod.add_eager_alpha(T)
    elif eager:
        mod.add_eager_alpha(T, sample=int(eager), rng=rng)
    stats["model_built_s"] = round(time.time() - t0, 1)
    info = {"stats": stats}
    while True:
        left = time_limit - (time.time() - t0)
        if left <= 0 or stats["rounds"] >= max_rounds:
            stats["time"] = round(time.time() - t0, 1)
            return "UNKNOWN", info
        r, edges = _solve(mod, left, workers=workers, seed=seed)
        stats["solves"] += 1
        if r == "UNSAT":
            stats["time"] = round(time.time() - t0, 1)
            return "UNSAT", info
        if r == "UNKNOWN":
            stats["time"] = round(time.time() - t0, 1)
            return "UNKNOWN", info
        kind, a = _cegar_step(mod, edges, T, rng, ncuts_per_iter, stats)
        if kind == "cut":
            continue
        stats["rounds"] += 1
        ok, cert = RZ.order_feasible(n, edges)
        if ok is None:
            raise RuntimeError("order_feasible inconclusive")
        if not ok:
            S = RZ.iis(n, edges)
            Tx = None
            fk = "order"
        else:
            fr = RZ.forced_relations(n, edges)
            if fr["extra_ap"]:
                rel = ("extra_ap", fr["extra_ap"][0])
                S, Tx, fk = RZ.forbidden_core(n, edges, rel), tuple(fr["extra_ap"][0]), "extra_ap"
            elif fr["diff"]:
                S, Tx, fk = RZ.forbidden_core(n, edges, ("diff", tuple(fr["diff"][0]))), None, "diff"
            else:
                res = RZ.realize_exact(n, edges)
                if res[0]:
                    info.update(edges=[list(e) for e in edges], set=res[1], alpha=a)
                    stats["time"] = round(time.time() - t0, 1)
                    return "SAT", info
                raise RuntimeError("realize_exact failed without a forced relation: %r" % (res[:2],))
        stats["fail_kinds"][fk] = stats["fail_kinds"].get(fk, 0) + 1
        stats["learnt"] += _learn_core(mod, S, Tx)
        if verbose and stats["rounds"] % 10 == 0:
            print("round", stats["rounds"], stats["fail_kinds"], "learnt", stats["learnt"],
                  round(time.time() - t0), flush=True)


# ----------------------------------------------------------------------------- independent checker


def load_cores(*paths):
    """Cores from data/forbidden_ordered_n*.json files."""
    out = []
    for p in paths:
        out.extend(json.load(open(p))["cores"])
    return out


def constraint_violations(n, edges, monotone=True, medial=True, cores=None):
    """Pure-python re-statement of the K30 / K31 / core constraints (independent of the clause
    generator).  Returns a list of human-readable violations (empty = pattern satisfies all)."""
    E = {tuple(e) for e in edges}
    bad = []
    if monotone:
        for (i, j, k) in E:
            for (i2, j2, k2) in E:
                if i <= i2 and k <= k2 and (i, k) != (i2, k2) and not j < j2:
                    bad.append(("monotone", (i, j, k), (i2, j2, k2)))
    if medial:
        for (a, b, c) in E:
            for (a2, p, e) in E:
                if a2 == a and e > c and p != b:
                    for (c2, q, e2) in E:
                        if c2 == c and e2 == e:
                            bad.append(("medial", (a, b, c), (a, p, e), (c, q, e)))
    for core in (cores or []):
        v = core["n"]
        if v > n:
            continue
        for refl in (False, True):
            if refl:
                ed = [(v - 1 - k, v - 1 - j, v - 1 - i) for i, j, k in core["edges"]]
                rel = None if core["relation"] is None else sorted(v - 1 - x for x in core["relation"])
            else:
                ed = [tuple(x) for x in core["edges"]]
                rel = core["relation"]
            for emb in itertools.combinations(range(n), v):
                if all(tuple(emb[x] for x in e) in E for e in ed):
                    if core["kind"] == "extra_ap" and tuple(emb[x] for x in rel) in E:
                        continue
                    bad.append(("core", core["kind"], emb, tuple(map(tuple, ed))))
    return bad


# ----------------------------------------------------------------------------- brute force (tests)


def brute_exists(n, T, forbid_f7=True, m_min=0):
    """Exhaustive DFS (tests, n <= 9): is there an ordered midpoint hypergraph with alpha <= T?
    Pruning: each added edge lowers alpha by at most 1, so alpha(partial) - #undecided > T is dead."""
    mids = list(range(1, n - 1))

    def rec(idx, edges, used_pairs):
        undecided = len(mids) - idx
        if idx == len(mids):
            if len(edges) < m_min:
                return False
            if forbid_f7 and not is_f7_free(edges):
                return False
            return alpha_of_edges(n, edges) <= T
        if len(edges) + undecided < m_min:
            return False
        if alpha_of_edges(n, edges) - undecided > T:
            return False
        j = mids[idx]
        for i in range(j):
            for k in range(j + 1, n):
                p = ((1 << (i * n + j)) | (1 << (j * n + k)) | (1 << (i * n + k)))
                if p & used_pairs:
                    continue
                if rec(idx + 1, edges + [(i, j, k)], used_pairs | p):
                    return True
        return rec(idx + 1, edges, used_pairs)

    return rec(0, [], 0)


def brute_min_alpha(n, forbid_f7=True, m_min=0):
    """Minimum alpha by repeated brute_exists (tests)."""
    T = n
    while T > 0 and brute_exists(n, T - 1, forbid_f7, m_min):
        T -= 1
    return T
