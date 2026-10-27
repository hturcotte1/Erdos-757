"""Independent referee verifier for L019 (written from scratch; imports nothing from e757/, judge/, hg.py, pyverify.py).

3-graphs: vertex labels are ints, edges are frozensets of size 3.  Everything exact (ints).
Routines: linearity; F7 copies (formulation: two DISJOINT edges g1,g2 plus a centre c outside them with three edges
through c forming a perfect matching g1<->g2); (P3) by brute force over all subsets (n<=18) and by the Hall/SDR
formulation with an independently coded augmenting-path matching; tau by branch and bound (branch on an uncovered edge
of maximum degree, lower bound = greedy disjoint uncovered edges); all minimum transversals; CP-SAT cross-check of tau.
"""
import itertools, random

def read_cell(path, K=None):
    out = []
    with open(path) as fh:
        for line in fh:
            a = list(map(int, line.split()))
            if not a:
                continue
            n, m, t = a[:3]
            E = [frozenset(a[3 + 3 * i:6 + 3 * i]) for i in range(m)]
            assert len(a) == 3 + 3 * m, path
            out.append((n, m, t, E))
            if K is not None and len(out) >= K:
                break
    return out

def degrees(V, E):
    d = {v: 0 for v in V}
    for e in E:
        for v in e:
            d[v] += 1
    return d

def is_linear(E):
    if any(len(e) != 3 for e in E):
        return False
    if len(set(E)) != len(E):
        return False
    return all(len(a & b) <= 1 for a, b in itertools.combinations(E, 2))

def f7_copies(E):
    """All copies of F7 = {012,034,056,135,246} as frozensets of 5 edges.
    Characterisation: edges 135 and 246 are disjoint; centre 0 is outside both; the three edges at 0 are {0,a,b} with
    a in 135, b in 246, and the three (a,b) pairs form a perfect matching between the two disjoint edges."""
    Es = set(E)
    at = {}
    for e in E:
        for v in e:
            at.setdefault(v, []).append(e)
    res = set()
    for g1, g2 in itertools.combinations(E, 2):
        if g1 & g2:
            continue
        for c, es in at.items():
            if c in g1 or c in g2 or len(es) < 3:
                continue
            cand = []
            for e in es:
                r = e - {c}
                a = r & g1
                b = r & g2
                if len(a) == 1 and len(b) == 1:
                    cand.append((next(iter(a)), next(iter(b)), e))
            for trio in itertools.combinations(cand, 3):
                if len({t[0] for t in trio}) == 3 and len({t[1] for t in trio}) == 3:
                    res.add(frozenset([g1, g2] + [t[2] for t in trio]))
    return res

def has_f7(E):
    return len(f7_copies(E)) > 0

def e_inside(E, S):
    S = set(S)
    return sum(1 for e in E if e <= S)

def p3_brute(V, E):
    """(P3): e(S) <= |S|-2 for all S with |S| >= 2; brute force over all subsets (bitmask).  Returns (ok, witness)."""
    V = sorted(V)
    idx = {v: i for i, v in enumerate(V)}
    masks = [sum(1 << idx[v] for v in e) for e in E]
    n = len(V)
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 2:
            continue
        cnt = 0
        for mk in masks:
            if mk & S == mk:
                cnt += 1
        if cnt > k - 2:
            return False, frozenset(V[i] for i in range(n) if S >> i & 1)
    return True, None

def saturated_sets(V, E, min_size=3):
    """all S with |S| >= min_size and e(S) = |S|-2 (brute force over subsets)."""
    V = sorted(V)
    idx = {v: i for i, v in enumerate(V)}
    masks = [sum(1 << idx[v] for v in e) for e in E]
    n = len(V)
    out = []
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < min_size:
            continue
        cnt = 0
        for mk in masks:
            if mk & S == mk:
                cnt += 1
        if cnt == k - 2:
            out.append(frozenset(V[i] for i in range(n) if S >> i & 1))
    return out

def _max_matching_edges_to_vertices(E, forbidden):
    """size of a maximum matching in the bipartite graph edges -> vertices (vertex side excludes `forbidden`).
    Independent implementation: Kuhn's algorithm with iterative DFS."""
    match_v = {}  # vertex -> edge index
    size = 0
    for i, e in enumerate(E):
        avail = [v for v in e if v not in forbidden]
        # DFS for augmenting path from edge i
        visited = set()
        def try_edge(j):
            for v in E[j]:
                if v in forbidden or v in visited:
                    continue
                visited.add(v)
                if v not in match_v or try_edge(match_v[v]):
                    match_v[v] = j
                    return True
            return False
        if try_edge(i):
            size += 1
    return size

def p3_hall(V, E):
    """(P3) via Hall: for every pair {x,y} the edges have an SDR avoiding x and y.  (Equivalent to e(S)<=|S|-2 for all
    |S|>=2: if e(S)>=|S|-1 take D = edges inside S and x,y in S; conversely a Hall violator D with
    |cup D \\ {x,y}| < |D| gives S = cup D + {x,y} with e(S) >= |D| >= |S|-1.)"""
    V = sorted(V)
    for x, y in itertools.combinations(V, 2):
        if _max_matching_edges_to_vertices(E, {x, y}) < len(E):
            return False
    return True

def in_C(V, E, brute_limit=18):
    if not is_linear(E):
        return False
    if has_f7(E):
        return False
    if len(V) <= brute_limit:
        return p3_brute(V, E)[0]
    return p3_hall(V, E)

def tau(E):
    """transversal number by branch and bound."""
    E = list(set(E))
    if not E:
        return 0
    best = [len(E)]  # trivial upper bound: one vertex per edge
    def lower_bound(rem):
        # greedy maximal set of pairwise disjoint edges
        used = set(); cnt = 0
        for e in rem:
            if not (e & used):
                used |= e; cnt += 1
        return cnt
    def rec(rem, k):
        if not rem:
            if k < best[0]:
                best[0] = k
            return
        if k + lower_bound(rem) >= best[0]:
            return
        # branch on an uncovered edge whose vertices have maximum total degree in rem
        deg = {}
        for e in rem:
            for v in e:
                deg[v] = deg.get(v, 0) + 1
        e = max(rem, key=lambda f: sum(deg[v] for v in f))
        for v in sorted(e, key=lambda v: -deg[v]):
            rec([f for f in rem if v not in f], k + 1)
    rec(E, 0)
    return best[0]

def all_min_transversals(E, t=None):
    """all transversals of size tau (frozensets).  Branch on the first uncovered edge, no exclusion (every minimum
    transversal contains a vertex of every uncovered edge, so it is reached)."""
    E = list(set(E))
    if t is None:
        t = tau(E)
    out = set()
    def rec(rem, chosen):
        if not rem:
            if len(chosen) == t:
                out.add(chosen)
            return
        if len(chosen) >= t:
            return
        e = rem[0]
        for v in e:
            rec([f for f in rem if v not in f], chosen | {v})
    rec(E, frozenset())
    return t, out

def all_min_transversals_brute(V, E, t):
    V = sorted(V)
    out = set()
    for T in itertools.combinations(V, t):
        Ts = set(T)
        if all(e & Ts for e in E):
            out.add(frozenset(T))
    return out

def tau_cpsat(E, V=None):
    from ortools.sat.python import cp_model
    V = sorted(V if V is not None else set().union(*E))
    mdl = cp_model.CpModel()
    x = {v: mdl.NewBoolVar('x%d' % v) for v in V}
    for e in E:
        mdl.AddBoolOr([x[v] for v in e])
    mdl.Minimize(sum(x.values()))
    sol = cp_model.CpSolver()
    sol.parameters.num_search_workers = 1
    sol.parameters.max_time_in_seconds = 120
    st = sol.Solve(mdl)
    assert st == cp_model.OPTIMAL, st
    return int(round(sol.ObjectiveValue()))

def slack(n, E, t=None):
    if t is None:
        t = tau(E)
    return 3 * n + 2 * len(E) - 11 * t

def cotransversal_vertices(E, t=None):
    t, Ts = all_min_transversals(E, t)
    co = set()
    for T in Ts:
        co |= T
    return t, Ts, co

def adjacent(E, y, z):
    return any(y in e and z in e for e in E)

def fold(V, E, x, y, z):
    """K°_{x;y,z}: delete x, identify y,z into zeta := y.  Returns (V2, E2) with E2 a LIST (duplicates kept so that
    injectivity can be checked), zeta = y."""
    E2 = []
    for e in E:
        if x in e:
            continue
        f = frozenset(y if v == z else v for v in e)
        E2.append(f)
    V2 = set(V) - {x, z}
    return V2, E2

def random_linear(n, m, rng, max_tries=5000):
    E = []; pairs = set(); tries = 0
    while len(E) < m and tries < max_tries:
        tries += 1
        e = frozenset(rng.sample(range(n), 3))
        ps = [frozenset(p) for p in itertools.combinations(e, 2)]
        if any(p in pairs for p in ps):
            continue
        E.append(e); pairs.update(ps)
    return E
