"""Referee #3 (round 2) own library for L024 checks. Imports nothing from e757, judge, hyp24 or kt.
3-graphs: n (vertices 0..n-1), edges = list of 3-tuples."""
import json, itertools

PIECES_PATH = '/home/user/Erdos-757/experiments/prover/L021/closure_results.json'

def load_pieces():
    d = json.load(open(PIECES_PATH))
    out = []
    for p in d['pieces']:
        out.append(dict(name=p['name'], n=p['n'], edges=[tuple(sorted(e)) for e in p['edges']], W=p['W'], tau=p['tau']))
    return out

def degrees(n, E):
    d = [0] * n
    for e in E:
        for x in e: d[x] += 1
    return d

def is_linear(E):
    seen = set()
    for e in E:
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen.add(p)
    return True

def components(V, E):
    """components of the induced subgraph on vertex set V (edges of E inside V); returns list of sets"""
    V = set(V); par = {x: x for x in V}
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in E:
        if all(x in V for x in e):
            a = f(e[0])
            for x in e[1:]:
                b = f(x)
                if a != b: par[b] = a
    comps = {}
    for x in V: comps.setdefault(f(x), set()).add(x)
    return list(comps.values())

def induced_edges(S, E):
    S = set(S)
    return [e for e in E if all(x in S for x in e)]

def _search(E, k, chosen, out, allsets):
    # find transversals of size <= k by branching on the first uncovered edge
    for e in E:
        if not (chosen & set(e)):
            if k == 0: return False
            found = False
            for x in e:
                chosen.add(x)
                r = _search(E, k - 1, chosen, out, allsets)
                chosen.discard(x)
                if r:
                    found = True
                    if not allsets: return True
            return found
    out.add(frozenset(chosen))
    return True

def tau(E):
    k = 0
    while True:
        out = set()
        if _search(E, k, set(), out, False): return k
        k += 1

def min_transversals(E):
    t = tau(E)
    out = set()
    _search(E, t, set(), out, True)
    return t, [T for T in out if len(T) == t]

def iso(n1, E1, n2, E2):
    """backtracking isomorphism test between two 3-graphs (vertex lists 0..n-1)"""
    if n1 != n2 or len(E1) != len(E2): return False
    d1, d2 = degrees(n1, E1), degrees(n2, E2)
    if sorted(d1) != sorted(d2): return False
    S2 = set(frozenset(e) for e in E2)
    inc1 = [[] for _ in range(n1)]
    for e in E1:
        for x in e: inc1[x].append(e)
    order = sorted(range(n1), key=lambda x: -d1[x])
    mp = {}; used = set()
    def ok(x):
        for e in inc1[x]:
            if all(y in mp for y in e):
                if frozenset(mp[y] for y in e) not in S2: return False
        return True
    def bt(i):
        if i == n1: return True
        x = order[i]
        for y in range(n2):
            if y in used or d2[y] != d1[x]: continue
            mp[x] = y; used.add(y)
            if ok(x) and bt(i + 1): return True
            del mp[x]; used.discard(y)
        return False
    return bt(0)
