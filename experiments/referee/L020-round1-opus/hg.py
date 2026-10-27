"""Independent 3-graph routines for the L020 referee (round 1, opus).

Written from scratch for this review: no import of e757/, judge/, or any prover script.
All arithmetic is exact (Python ints, numpy integer arrays used only for exhaustive
subset enumeration).  Vertices are 0..n-1, edges are bitmasks (int) or tuples.
"""
import itertools
import numpy as np


# ---------------------------------------------------------------- basics
def to_masks(edges):
    return [sum(1 << x for x in e) for e in edges]


def popcount(x):
    return bin(x).count("1")


def bits(x):
    out = []
    while x:
        lb = x & -x
        out.append(lb.bit_length() - 1)
        x ^= lb
    return out


def vertex_set(edges):
    s = set()
    for e in edges:
        s.update(e)
    return s


def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for x in e:
            d[x] += 1
    return d


def is_3uniform(edges):
    return all(len(e) == 3 and len(set(e)) == 3 for e in edges) and \
        len(set(frozenset(e) for e in edges)) == len(edges)


def is_linear(edges):
    S = [frozenset(e) for e in edges]
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            if len(S[i] & S[j]) >= 2:
                return False
    return True


def is_connected(n, edges):
    """connected as a 3-graph on vertex set 0..n-1 (every vertex must be reached)."""
    if n == 0:
        return True
    adj = [set() for _ in range(n)]
    for e in edges:
        for x in e:
            for y in e:
                if x != y:
                    adj[x].add(y)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def components(vertices, edges):
    """components (as (vertex list, edge list)) of the 3-graph on `vertices`."""
    vertices = list(vertices)
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in edges:
        a = find(e[0])
        for x in e[1:]:
            b = find(x)
            if a != b:
                parent[b] = a
    groups = {}
    for v in vertices:
        groups.setdefault(find(v), []).append(v)
    out = []
    for r, vs in groups.items():
        vs_set = set(vs)
        es = [e for e in edges if e[0] in vs_set]
        out.append((sorted(vs), es))
    return out


def relabel(vertices, edges):
    idx = {v: i for i, v in enumerate(sorted(vertices))}
    return len(idx), [tuple(sorted(idx[x] for x in e)) for e in edges], idx


# ---------------------------------------------------------------- F7
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]


def _is_F7_copy(es):
    """es: 5 edges (tuples).  True iff isomorphic to F7 (brute force over bijections)."""
    vs = sorted(vertex_set(es))
    if len(vs) != 7:
        return False
    target = set(frozenset(e) for e in es)
    for perm in itertools.permutations(vs):
        img = set(frozenset(perm[x] for x in e) for e in F7)
        if img == target:
            return True
    return False


def _is_F7_struct(es):
    """structural test: 7 vertices, linear, degree sequence 3,2,2,2,2,2,2."""
    vs = vertex_set(es)
    if len(vs) != 7 or not is_linear(es):
        return False
    d = {}
    for e in es:
        for x in e:
            d[x] = d.get(x, 0) + 1
    return sorted(d.values()) == [2, 2, 2, 2, 2, 2, 3]


def f7_copies(edges, both=True):
    """all 5-subsets of edges forming a copy of F7 (any 5 edges: a copy of F7 has 5 edges)."""
    found = []
    masks = to_masks(edges)
    for comb in itertools.combinations(range(len(edges)), 5):
        u = 0
        for i in comb:
            u |= masks[i]
        if popcount(u) != 7:
            continue
        es = [edges[i] for i in comb]
        s = _is_F7_struct(es)
        if both:
            c = _is_F7_copy(es)
            assert s == c, ("F7 tests disagree", es)
        if s:
            found.append(comb)
    return found


# ---------------------------------------------------------------- (P3)
def p3_exhaustive_min(edges):
    """min over nonempty edge subsets E' of |union E'| - |E'| (exhaustive, numpy).
    (P3) [e(S) <= |S|-2 for all |S|>=2] holds iff this minimum is >= 2."""
    m = len(edges)
    masks = to_masks(edges)
    assert max(masks).bit_length() <= 32
    U = np.zeros(1 << m, dtype=np.uint32)
    for i in range(m):
        U[1 << i:1 << (i + 1)] = U[0:1 << i] | np.uint32(masks[i])
    cv = np.bitwise_count(U).astype(np.int16)
    ce = np.bitwise_count(np.arange(1 << m, dtype=np.uint32)).astype(np.int16)
    diff = cv - ce
    diff[0] = 127
    k = int(np.argmin(diff))
    return int(diff[k]), k


def _kuhn_saturates(m, cand):
    """cand[i] = list of allowed vertices for edge i.  True iff a matching saturating all edges exists."""
    match_v = {}

    def try_edge(i, seen):
        for v in cand[i]:
            if v in seen:
                continue
            seen.add(v)
            if v not in match_v or try_edge(match_v[v], seen):
                match_v[v] = i
                return True
        return False
    for i in range(m):
        if not try_edge(i, set()):
            return False
    return True


def p3_hall(n, edges):
    """(P3) via: for every pair {x,y}, the edges have distinct representatives in V minus {x,y}
    (each edge represented by one of its own vertices).  Own Kuhn augmenting-path matching."""
    m = len(edges)
    if m == 0:
        return True
    for x in range(n):
        for y in range(x + 1, n):
            cand = [[v for v in e if v != x and v != y] for e in edges]
            if not _kuhn_saturates(m, cand):
                return False
    return True


def in_C(n, edges, hall_only=True):
    if not is_3uniform(edges) or not is_linear(edges):
        return False
    if f7_copies(edges, both=False):
        return False
    if hall_only:
        return p3_hall(n, edges)
    return p3_exhaustive_min(edges)[0] >= 2


# ---------------------------------------------------------------- transversals
def _greedy_disjoint(uncov_masks, allowed):
    used = 0
    c = 0
    for e in uncov_masks:
        a = e & allowed
        if a & used == 0:
            used |= a
            c += 1
    return c


def tau_bb(edges):
    """exact transversal number by branch and bound (own code)."""
    masks = to_masks(edges)
    if not masks:
        return 0
    best = [len(masks)]

    def rec(rem, k):
        if not rem:
            if k < best[0]:
                best[0] = k
            return
        if k + _greedy_disjoint(rem, -1) >= best[0]:
            return
        # branch on the edge of rem that meets the fewest other remaining edges? use first edge.
        e = rem[0]
        for x in bits(e):
            xb = 1 << x
            rec([f for f in rem if not f & xb], k + 1)
    rec(masks, 0)
    return best[0]


def has_transversal_of_size(edges, k, forced_in=0, forced_out=0):
    """exists a transversal T with |T| <= k, forced_in subset T, T disjoint from forced_out."""
    masks = to_masks(edges)

    def rec(chosen, excl, cnt):
        unc = [e for e in masks if not e & chosen]
        if not unc:
            return True
        if cnt >= k:
            return False
        if cnt + _greedy_disjoint(unc, ~excl) > k:
            return False
        e = unc[0]
        av = e & ~excl
        if av == 0:
            return False
        ex = excl
        for x in bits(av):
            xb = 1 << x
            if rec(chosen | xb, ex, cnt + 1):
                return True
            ex |= xb
        return False
    if forced_in & forced_out:
        return False
    return rec(forced_in, forced_out, popcount(forced_in))


def all_min_transversals(edges, t):
    """every transversal of size exactly t (all are minimum if tau = t); each found once."""
    masks = to_masks(edges)
    out = []

    def rec(chosen, excl, cnt):
        unc = [e for e in masks if not e & chosen]
        if not unc:
            assert cnt == t, "found a transversal smaller than t"
            out.append(chosen)
            return
        if cnt >= t:
            return
        if cnt + _greedy_disjoint(unc, ~excl) > t:
            return
        e = unc[0]
        av = e & ~excl
        ex = excl
        for x in bits(av):
            xb = 1 << x
            rec(chosen | xb, ex, cnt + 1)
            ex |= xb
    rec(0, 0, 0)
    return out


def tau_cpsat(n, edges, time_limit=60.0):
    from ortools.sat.python import cp_model
    md = cp_model.CpModel()
    x = [md.NewBoolVar(f"x{i}") for i in range(n)]
    for e in edges:
        md.AddBoolOr([x[v] for v in e])
    md.Minimize(sum(x))
    sv = cp_model.CpSolver()
    sv.parameters.num_workers = 1
    sv.parameters.max_time_in_seconds = time_limit
    st = sv.Solve(md)
    assert st == cp_model.OPTIMAL, sv.StatusName(st)
    T = [i for i in range(n) if sv.Value(x[i])]
    return int(round(sv.ObjectiveValue())), T


def cpsat_no_transversal_of_size(n, edges, k, time_limit=60.0):
    """True iff CP-SAT proves there is no transversal with <= k vertices."""
    from ortools.sat.python import cp_model
    md = cp_model.CpModel()
    x = [md.NewBoolVar(f"x{i}") for i in range(n)]
    for e in edges:
        md.AddBoolOr([x[v] for v in e])
    md.Add(sum(x) <= k)
    sv = cp_model.CpSolver()
    sv.parameters.num_workers = 1
    sv.parameters.max_time_in_seconds = time_limit
    st = sv.Solve(md)
    return st == cp_model.INFEASIBLE


def slack(n, m, t):
    return 3 * n + 2 * m - 11 * t


# ---------------------------------------------------------------- isomorphism
def wl_invariant(n, edges, table, rounds=None):
    """1-WL colour refinement on the vertex/edge incidence graph; colours are global ids
    (shared `table`), so the returned sorted colour lists are comparable across graphs.
    Different invariants => non-isomorphic (sound)."""
    m = len(edges)
    N = n + m
    nbr = [[] for _ in range(N)]
    for j, e in enumerate(edges):
        for x in e:
            nbr[x].append(n + j)
            nbr[n + j].append(x)
    col = [("v", len(nbr[i])) if i < n else ("e",) for i in range(N)]
    col = [table.setdefault(c, len(table)) for c in col]
    R = rounds if rounds is not None else N
    for _ in range(R):
        sig = [(col[i], tuple(sorted(col[j] for j in nbr[i]))) for i in range(N)]
        col = [table.setdefault(("r", s), len(table)) for s in sig]
    return tuple(sorted(col)), col


def iso_exact(n1, e1, n2, e2):
    """exact isomorphism test of two 3-graphs by backtracking over vertex maps with
    WL-colour constraints (own code).  Returns a bijection or None."""
    if n1 != n2 or len(e1) != len(e2):
        return None
    table = {}
    inv1, c1 = wl_invariant(n1, e1, table)
    inv2, c2 = wl_invariant(n2, e2, table)
    if inv1 != inv2:
        return None
    n = n1
    E2 = set(frozenset(e) for e in e2)
    inc1 = [[] for _ in range(n)]
    for e in e1:
        for x in e:
            inc1[x].append(e)
    order = sorted(range(n), key=lambda v: (sum(1 for _ in inc1[v]) * -1, v))
    # order so that each next vertex is adjacent to earlier ones when possible
    adj1 = [set() for _ in range(n)]
    for e in e1:
        for x in e:
            for y in e:
                if x != y:
                    adj1[x].add(y)
    seen = []
    rest = set(range(n))
    while rest:
        cands = [v for v in rest if any(w in adj1[v] for w in seen)]
        v = min(cands) if cands else min(rest)
        seen.append(v)
        rest.discard(v)
    order = seen
    phi = {}
    used = set()
    deg1 = degrees(n, e1)

    def ok(v):
        # every edge of e1 all of whose vertices are mapped must map to an edge of e2
        for e in inc1[v]:
            if all(x in phi for x in e):
                if frozenset(phi[x] for x in e) not in E2:
                    return False
        return True

    def rec(i):
        if i == n:
            return True
        v = order[i]
        for w in range(n):
            if w in used or c1[v] != c2[w]:
                continue
            phi[v] = w
            used.add(w)
            if ok(v) and rec(i + 1):
                return True
            del phi[v]
            used.discard(w)
        return False
    if rec(0):
        # final check: edge sets map bijectively
        img = set(frozenset(phi[x] for x in e) for e in e1)
        assert img == E2
        return dict(phi)
    return None
