"""
Independent exact DFS over the abstract ordered-midpoint class O(n).  [verified-here when tests pass]

Purpose: a second implementation (independent of e757.cpsat_model) for deciding questions such as
"is there a member of O(n) with >= m_min edges and alpha <= T?" (the f(16) certificate needs two
independent engines).  It imports nothing from e757.cpsat_model; e757.saturated.alpha_of_edges and
e757.realizability are used only by tests / cross-checks.

The class O(n).  Vertices 0..n-1 are ranks.  A labeled edge (i, j, k), i < j < k, has midpoint j.  A
set of edges is in O(n) iff
  (a) every j is the midpoint of at most one edge;
  (b) linear: two edges share at most one vertex;
  (c) monotone midpoints (kb/known_results.md K30): if (i,j,k), (i',j',k') are edges with i <= i',
      k <= k' and (i,k) != (i',k') then j < j';
  (d) optionally F7-free (F7 = {012,034,056,135,246} as an unlabeled 3-graph: a centre c, three
      pairwise-disjoint lines {c,a_t,b_t}, and the two further lines {a_1,a_2,a_3}, {b_1,b_2,b_3}).
alpha = size of the largest vertex set containing no edge.

DFS.  Interior vertices j = 1..n-2 are processed in increasing order; for j we choose a pair (i,k),
i < j < k, or "no edge" (a "none", counted against the budget (n-2) - m_min).

Why the DFS test for (c) is exactly (c).  When the new edge E = (i,j,k) is added, every earlier edge
E' = (i',j',k') has j' < j (and j' != j by (a)).  Condition (c) for the ordered pair (E', E) reads
"i' <= i and k' <= k and (i',k') != (i,k)  ==>  j' < j", which holds.  Condition (c) for the ordered
pair (E, E') reads "i <= i' and k <= k' and (i,k) != (i',k')  ==>  j < j'", whose conclusion is false;
so the pair is legal iff NOT (i <= i' and k <= k' and (i,k) != (i',k')).  The case (i,k) = (i',k')
is excluded anyway by linearity (the edges would share two vertices).  Hence E is legal w.r.t. (c) iff
k > M[i], where M[i] = max{k' : earlier edge (i',j',k') with i' >= i}  (0 if none).  M is a
"staircase" that only grows as edges are added, which is also why "k is not currently allowed for any
i" stays true for the rest of the branch (used in the look-ahead below).

Alpha pruning (sound).  At the entry of level j let E_cur be the edges chosen so far (midpoints < j),
R = {j, ..., n-2} the undecided midpoints and R_f the subset of R that can still be the midpoint of
some edge (exists i < r < k with pairs (i,r), (r,k), (i,k) unused and k > M[i]; linearity and the
staircase only get tighter along a branch, so a vertex of R \\ R_f is a forced "none").  Every edge
of the final hypergraph is either in E_cur or has its midpoint in R_f.  So if S is a vertex set
disjoint from R_f containing no edge of E_cur, then S contains no edge of the final hypergraph:
alpha_final >= alpha(E_cur restricted to V \\ R_f).  Hence if V \\ R_f has an E_cur-independent set of
size T+1 the whole subtree can be discarded.  (In particular, at a leaf R_f is empty and the test is
the exact test alpha > T.)  Also, every vertex of R \\ R_f is a forced none, so the budget
check  nones_used + |R \\ R_f| <= (n-2) - m_min  is a further sound prune.

Reflection j -> n-1-j maps (i,j,k) -> (n-1-k, n-1-j, n-1-i); it preserves (a)-(d) and alpha.  It is NOT
used to prune the DFS (the DFS order is not reflection-compatible); `up_to_reflection=True` only
filters leaves to one representative per orbit (sorted edge tuple <= its reflection), which is exact.

Optional Henning-Yeo pruning (`use_hy`): for F7-free linear 3-graphs 17*tau <= 5n + 3m
(Henning-Yeo 2021, [published]); with alpha <= T, tau >= n - T so m >= ceil((12 n - 17 T)/3).
This uses a published theorem as an axiom, so it is OFF by default.

API:
    min_alpha(n, m_min=0, forbid_f7=False, ...)  -> (alpha, edges, stats)
    enumerate_solutions(n, T, m_min=0, m_exact=None, callback=None, forbid_f7=False, ...) -> stats
    exists(n, T, m_min, ...) -> edges or None
    independence_number(n, edges)  (own exact routine)
"""
from __future__ import annotations

import itertools
import time

# ------------------------------------------------------------------------------ independence number


def _edge_tables(n, edges):
    """by_v[v] = list of (maskOfOtherTwo) for edges through v."""
    by_v = [[] for _ in range(n)]
    for (a, b, c) in edges:
        by_v[a].append((1 << b) | (1 << c))
        by_v[b].append((1 << a) | (1 << c))
        by_v[c].append((1 << a) | (1 << b))
    return by_v


def _indep_search(by_v, cand, chosen, size, best, stop_at):
    """Branch and bound; returns the largest independent size found (>= best) with early exit at
    stop_at.  cand: bitmask of vertices that may still be added (already filtered so that adding any
    single candidate to `chosen` creates no full edge)."""
    if size > best:
        best = size
        if best >= stop_at:
            return best
    while cand:
        if size + cand.bit_count() <= best:
            return best
        v = (cand & -cand).bit_length() - 1
        cand &= cand - 1
        # include v
        c2 = chosen | (1 << v)
        cand2 = cand
        for om in by_v[v]:
            # om = the other two vertices of an edge through v
            inter = om & chosen
            if inter == om:  # cannot happen (cand is filtered), defensive
                cand2 = -1
                break
            if inter:  # exactly one of the two is in chosen -> the other becomes forbidden
                cand2 &= ~(om ^ inter)
        if cand2 != -1:
            best = _indep_search(by_v, cand2, c2, size + 1, best, stop_at)
            if best >= stop_at:
                return best
        # exclude v: continue loop
    return best


def independence_number(n, edges, allowed=None, stop_at=None):
    """Exact alpha of the 3-graph `edges` on vertices 0..n-1 restricted to the vertex mask
    `allowed` (default all).  With stop_at, may return early once a set of that size is found."""
    by_v = _edge_tables(n, edges)
    if allowed is None:
        allowed = (1 << n) - 1
    return _indep_search(by_v, allowed, 0, 0, 0, stop_at if stop_at is not None else n + 1)


# ------------------------------------------------------------------------------ F7


def has_f7(edges):
    """True iff the 3-graph contains F7 = {012,034,056,135,246} as a (not nec. induced) subgraph."""
    es = set(frozenset(e) for e in edges)
    if len(es) < 5:
        return False
    deg = {}
    for e in es:
        for v in e:
            deg.setdefault(v, []).append(e)
    for c, lines in deg.items():
        if len(lines) < 3:
            continue
        for l1, l2, l3 in itertools.combinations(lines, 3):
            p1, p2, p3 = (tuple(sorted(l - {c})) for l in (l1, l2, l3))
            if len({*p1, *p2, *p3}) != 6:
                continue
            for s2 in (0, 1):
                for s3 in (0, 1):
                    P = frozenset((p1[0], p2[s2], p3[s3]))
                    Q = frozenset((p1[1], p2[1 - s2], p3[1 - s3]))
                    if P in es and Q in es:
                        return True
    return False


# ------------------------------------------------------------------------------ the DFS


def hy_m_need(n, T):
    """Henning-Yeo: alpha <= T  =>  m >= ceil((12 n - 17 T) / 3)  (F7-free linear 3-graphs)."""
    return max(0, -((17 * T - 12 * n) // 3))


def reflect_edges(n, edges):
    return sorted((n - 1 - k, n - 1 - j, n - 1 - i) for (i, j, k) in edges)


class Search:
    """One DFS run.  See module docstring.  Attributes after run(): nodes, leaves, solutions."""

    def __init__(self, n, T, m_min=0, m_exact=None, forbid_f7=False, monotone=True,
                 node_filter=None, use_hy=False, up_to_reflection=False, on_solution=None,
                 limit=None, time_limit=None, lower_T=True):
        self.n = n
        self.T = T
        self.forbid_f7 = forbid_f7
        self.monotone = monotone
        self.node_filter = node_filter
        self.up_to_reflection = up_to_reflection
        self.on_solution = on_solution
        self.limit = limit
        self.time_limit = time_limit
        self.deadline = None
        if m_exact is not None:
            m_min = m_exact
        self.m_min = m_min
        self.m_exact = m_exact
        self.use_hy = use_hy
        self.nodes = self.leaves = self.solutions = 0
        self.stopped = False
        self.timed_out = False
        self.best_alpha = None
        self.best_edges = None

    # -- helpers
    def _m_need(self):
        m = self.m_min
        if self.use_hy and self.forbid_f7:
            m = max(m, hy_m_need(self.n, self.T))
        return m

    def run(self):
        n = self.n
        if self.time_limit is not None:
            self.deadline = time.time() + self.time_limit
        if n < 3:
            self.leaves += 1
            self._leaf([])
            return self
        nb = [0] * n  # nb[v] = bitmask of vertices joined to v by an edge (pair graph)
        M = [0] * n
        self._rec(1, [], nb, M, 0)
        return self

    def _feasible_mid(self, r, nb, M):
        """Can r still be the midpoint of some edge?"""
        n = self.n
        nbr = nb[r]
        full = (1 << n) - 1
        for i in range(r):
            if (nbr >> i) & 1:
                continue
            lo = r if not self.monotone else max(r, M[i])
            allowed = full & ~((1 << (lo + 1)) - 1) & ~(nb[i] | nbr)
            if allowed:
                return True
        return False

    def _rec(self, j, edges, nb, M, nones):
        if self.stopped:
            return
        n = self.n
        self.nodes += 1
        if self.deadline is not None and (self.nodes & 1023) == 0 and time.time() > self.deadline:
            self.stopped = self.timed_out = True
            return
        budget = (n - 2) - self._m_need()  # number of nones allowed overall
        if self.m_exact is not None:
            budget = (n - 2) - self.m_exact
        # look-ahead: forced nones and alpha bound
        rf_mask = 0
        forced_none = 0
        for r in range(j, n - 1):
            if self._feasible_mid(r, nb, M):
                rf_mask |= 1 << r
            else:
                forced_none += 1
        if nones + forced_none > budget:
            return
        if len(edges) + (n - 1 - j) - forced_none < self._m_need():
            return  # not enough room left for m_min edges (same as the budget test; kept explicit)
        allowed = ((1 << n) - 1) & ~rf_mask
        if independence_number(n, edges, allowed, stop_at=self.T + 1) > self.T:
            return
        if j == n - 1:
            self.leaves += 1
            if len(edges) < self._m_need():
                return
            if self.m_exact is not None and len(edges) != self.m_exact:
                return
            self._leaf(edges)
            return
        # choose the edge for midpoint j
        full = (1 << n) - 1
        nbj = nb[j]
        for i in range(j):
            if (nbj >> i) & 1:
                continue
            lo = j if not self.monotone else max(j, M[i])
            allowed_k = full & ~((1 << (lo + 1)) - 1) & ~(nb[i] | nbj)
            while allowed_k:
                k = (allowed_k & -allowed_k).bit_length() - 1
                allowed_k &= allowed_k - 1
                e = (i, j, k)
                edges.append(e)
                if self.node_filter is not None and not self.node_filter(edges):
                    edges.pop()
                    continue
                if self.forbid_f7 and len(edges) >= 5 and has_f7(edges):
                    edges.pop()
                    continue
                nb2 = list(nb)
                nb2[i] |= (1 << j) | (1 << k)
                nb2[j] |= (1 << i) | (1 << k)
                nb2[k] |= (1 << i) | (1 << j)
                M2 = M
                if self.monotone:
                    M2 = list(M)
                    for i2 in range(i + 1):
                        if M2[i2] < k:
                            M2[i2] = k
                self._rec(j + 1, edges, nb2, M2, nones)
                edges.pop()
                if self.stopped:
                    return
        if nones + 1 <= budget:
            self._rec(j + 1, edges, nb, M, nones + 1)

    def _leaf(self, edges):
        n = self.n
        es = sorted(edges)
        if self.up_to_reflection and tuple(reflect_edges(n, es)) < tuple(es):
            return
        a = independence_number(n, es)
        if a > self.T:  # cannot happen (leaf test), defensive
            return
        self.solutions += 1
        if self.best_alpha is None or a < self.best_alpha:
            self.best_alpha, self.best_edges = a, list(es)
        if self.on_solution is not None:
            r = self.on_solution(list(es), a)
            if r == "stop":
                self.stopped = True
            elif isinstance(r, int):  # tighten target (branch and bound)
                self.T = min(self.T, r)
        if self.limit is not None and self.solutions >= self.limit:
            self.stopped = True

    def stats(self):
        return {"nodes": self.nodes, "leaves": self.leaves, "solutions": self.solutions,
                "timed_out": self.timed_out}


# ------------------------------------------------------------------------------ public API


def enumerate_solutions(n, T, m_min=0, m_exact=None, callback=None, forbid_f7=False,
                        monotone=True, up_to_reflection=False, use_hy=False, node_filter=None,
                        limit=None, time_limit=None):
    """Call callback(edges, alpha) for every member of O(n) with alpha <= T and >= m_min edges
    (== m_exact if given).  Returns stats dict (nodes, leaves, solutions, timed_out)."""
    s = Search(n, T, m_min=m_min, m_exact=m_exact, forbid_f7=forbid_f7, monotone=monotone,
               node_filter=node_filter, use_hy=use_hy, up_to_reflection=up_to_reflection,
               on_solution=(lambda e, a: callback(e, a)) if callback else None,
               limit=limit, time_limit=time_limit)
    s.run()
    return s.stats()


def exists(n, T, m_min=0, m_exact=None, forbid_f7=False, **kw):
    """Edges of some member of O(n) with alpha <= T and >= m_min edges, or None."""
    s = Search(n, T, m_min=m_min, m_exact=m_exact, forbid_f7=forbid_f7, limit=1, **kw)
    s.run()
    return s.best_edges


def min_alpha(n, m_min=0, forbid_f7=False, time_limit=None, **kw):
    """(alpha, edges, stats): the minimum alpha over members of O(n) with >= m_min edges
    (branch and bound: T is tightened to alpha-1 after each solution).  alpha is None if the class
    is empty.  If stats['timed_out'] the value is only an upper bound."""
    holder = {}

    def cb(edges, a):
        holder["a"], holder["e"] = a, edges
        return a - 1

    s = Search(n, n, m_min=m_min, forbid_f7=forbid_f7, on_solution=cb, time_limit=time_limit, **kw)
    s.run()
    return holder.get("a"), holder.get("e"), s.stats()
