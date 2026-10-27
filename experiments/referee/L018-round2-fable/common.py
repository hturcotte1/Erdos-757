"""Referee round 2 (fable) helpers for L018. Own code; nothing imported from e757/, judge/ or
experiments/prover/.  Exact integer arithmetic throughout."""
from itertools import combinations
from collections import defaultdict


def parse_found(line):
    """'FOUND: (0,1,2) (0,3,4) ...' -> list of frozensets."""
    body = line.split(':', 1)[1]
    edges = []
    for tok in body.split():
        tok = tok.strip('(),')
        if not tok:
            continue
        a, b, c = (int(t) for t in tok.split(','))
        edges.append(frozenset((a, b, c)))
    return edges


def vertices(edges):
    vs = set()
    for e in edges:
        vs |= e
    return vs


def degrees(edges, vs=None):
    d = defaultdict(int)
    if vs is not None:
        for v in vs:
            d[v] = 0
    for e in edges:
        for v in e:
            d[v] += 1
    return d


def is_linear(edges):
    for e, f in combinations(edges, 2):
        if len(e & f) >= 2:
            return False
    return True


def is_connected(edges, vs):
    vs = set(vs)
    if not vs:
        return True
    start = next(iter(vs))
    seen = {start}
    stack = [start]
    inc = defaultdict(list)
    for e in edges:
        for v in e:
            inc[v].append(e)
    while stack:
        v = stack.pop()
        for e in inc[v]:
            for w in e:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
    return seen == vs


def tau(edges):
    """Exact transversal number by branch and bound (branch on the vertices of an uncovered
    edge; lower bound = greedy packing of pairwise disjoint uncovered edges)."""
    edges = list(edges)
    best = [len(edges)]

    def packing(rem):
        used = set()
        k = 0
        for e in rem:
            if not (e & used):
                used |= e
                k += 1
        return k

    def rec(rem, size):
        if not rem:
            if size < best[0]:
                best[0] = size
            return
        if size + packing(rem) >= best[0]:
            return
        # choose the uncovered edge with the fewest ... just the first one
        e = rem[0]
        for v in sorted(e):
            rem2 = [f for f in rem if v not in f]
            rec(rem2, size + 1)

    rec(edges, 0)
    return best[0]


def slack(edges, n):
    return 3 * n + 2 * len(edges) - 11 * tau(edges)


def has_f7(edges):
    """F7 = {012,034,056,135,246}: 5 edges on 7 vertices, degrees 3,2^6 (Lemma 0.7, valid for
    linear 3-graphs). Checked over all 5-subsets of edges."""
    for sub in combinations(edges, 5):
        vs = set()
        for e in sub:
            vs |= e
        if len(vs) != 7:
            continue
        d = degrees(sub)
        ds = sorted(d.values())
        if ds == [2, 2, 2, 2, 2, 2, 3]:
            return True
    return False


def bip_matching_saturates_left(left_adj, right_set):
    """Is there a matching saturating all left vertices? left_adj: list of sets of right
    vertices. Simple augmenting-path algorithm."""
    match_r = {}

    def try_augment(u, seen):
        for r in left_adj[u]:
            if r in seen:
                continue
            seen.add(r)
            if r not in match_r or try_augment(match_r[r], seen):
                match_r[r] = u
                return True
        return False

    for u in range(len(left_adj)):
        if not try_augment(u, set()):
            return False
    return True


def hall_condition(edges, vs):
    """e_ind(S) <= |S|-2 for every S with |S|>=2  <=>  for every pair {u,v} the edges have an
    SDR avoiding u and v (Hall)."""
    vs = sorted(vs)
    for u, v in combinations(vs, 2):
        left = [set(e) - {u, v} for e in edges]
        if not bip_matching_saturates_left(left, None):
            return False
    return True


def in_class_C(edges, vs):
    return is_linear(edges) and (not has_f7(edges)) and hall_condition(edges, vs)


def value_of(Z, edges, vs_all):
    """value(Z) = 3|Z| + 2 e(Z) - 11 tau(E_Z)."""
    Z = set(Z)
    EZ = [e for e in edges if e & Z]
    return 3 * len(Z) + 2 * len(EZ) - 11 * tau(EZ), EZ


def tau_ilp(edges):
    """Exact transversal number by CP-SAT (second method, independent of the branching code)."""
    from ortools.sat.python import cp_model
    edges = list(edges)
    vs = sorted(vertices(edges))
    mdl = cp_model.CpModel()
    x = {v: mdl.NewBoolVar(f'x{v}') for v in vs}
    for e in edges:
        mdl.Add(sum(x[v] for v in e) >= 1)
    mdl.Minimize(sum(x.values()))
    sol = cp_model.CpSolver()
    sol.parameters.num_search_workers = 1
    st = sol.Solve(mdl)
    assert st == cp_model.OPTIMAL
    return int(round(sol.ObjectiveValue()))
