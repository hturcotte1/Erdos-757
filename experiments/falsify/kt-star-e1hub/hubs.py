#!/usr/bin/env python3
"""E1-hub falsifier library (re-implementation; uses L021 kt.py only for min-transversal enumeration, A, and DEF;
class-C membership by the L014 verifier pyverify.py; independent tau check by CP-SAT).
Vertices 0..n-1, edges = 3-tuples.  Hub: new v,x,y,z and edges {x,y,z},{v,x,a},{v,y,b},{v,z,c}."""
import sys, json, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness')
import kt, pyverify
import networkx as nx

PIECES = [kt.Piece(p['edges'], p['name']) for p in json.load(open(
    '/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']]
assert len(PIECES) == 32

def degs(n, E):
    d = [0] * n
    for e in E:
        for x in e: d[x] += 1
    return d

def popc(x): return bin(x).count('1')

def bconfigs(n, E, t):
    """all triples {a,b,c} of vertices of degree <= 2, not an edge, no two in a common minimum transversal.
    returns (list of triples, number of minimum transversals, set of vertices in no min transversal among low vertices)."""
    d = degs(n, E)
    em = kt.masks(E)
    T = kt.min_transversals(em, t)
    assert T and all(popc(x) == t for x in T)
    low = [x for x in range(n) if d[x] <= 2]
    lowmask = 0
    for x in low: lowmask |= 1 << x
    cop = [0] * n
    inT = 0
    for tr in T:
        inT |= tr
        l = tr & lowmask
        m = l
        while m:
            b = m & -m; m ^= b
            cop[b.bit_length() - 1] |= l
    noco = {x: lowmask & ~cop[x] & ~(1 << x) for x in low}
    Es = set(frozenset(e) for e in E)
    out = []
    for a in low:
        na = noco[a] >> (a + 1) << (a + 1)
        for b in low:
            if b <= a or not (na >> b) & 1: continue
            nb = noco[b] & noco[a] >> (b + 1) << (b + 1)
            c_mask = nb
            while c_mask:
                cb = c_mask & -c_mask; c_mask ^= cb
                c = cb.bit_length() - 1
                if frozenset((a, b, c)) in Es: continue
                out.append((a, b, c))
    notin = [x for x in low if not (inT >> x) & 1]
    return out, len(T), notin

def add_hub(n, E, a, b, c):
    v, x, y, z = n, n + 1, n + 2, n + 3
    return n + 4, list(E) + [(x, y, z), (a, v, x), (b, v, y), (c, v, z)]

def inc_graph(n, E):
    G = nx.Graph()
    for x in range(n): G.add_node(('v', x), t=0)
    for i, e in enumerate(E):
        G.add_node(('e', i), t=1)
        for x in e: G.add_edge(('v', x), ('e', i))
    return G

def wl_hash(n, E, rounds=4):
    d = degs(n, E)
    inc = [[] for _ in range(n)]
    for i, e in enumerate(E):
        for x in e: inc[x].append(i)
    col = [d[x] for x in range(n)]
    ecol = [0] * len(E)
    for _ in range(rounds):
        ecol = [hash(tuple(sorted(col[x] for x in e))) for e in E]
        col = [hash((col[x], tuple(sorted(ecol[i] for i in inc[x])))) for x in range(n)]
    return hash((n, len(E), tuple(sorted(col)), tuple(sorted(ecol))))

class Registry:
    """isomorphism-class registry (WL hash + exact networkx isomorphism of incidence graphs)"""
    def __init__(self): self.d = {}; self.count = 0
    def lookup(self, n, E):
        h = wl_hash(n, E)
        G = inc_graph(n, E)
        for (G2, rec) in self.d.get(h, []):
            if nx.is_isomorphic(G, G2, node_match=lambda p, q: p['t'] == q['t']): return rec, False
        rec = {}
        self.d.setdefault(h, []).append((G, rec)); self.count += 1
        return rec, True

def cpsat_tau(n, E, ub=None):
    from ortools.sat.python import cp_model
    M = cp_model.CpModel()
    xs = [M.NewBoolVar(f'x{i}') for i in range(n)]
    for e in E: M.AddBoolOr([xs[i] for i in e])
    M.Minimize(sum(xs))
    S = cp_model.CpSolver(); S.parameters.num_workers = 1; S.parameters.max_time_in_seconds = 600
    r = S.Solve(M)
    assert r == cp_model.OPTIMAL
    return int(round(S.ObjectiveValue()))

def is_piece(n, E, t):
    """return name of the L* piece isomorphic to (n,E), or None"""
    G = None
    for P in PIECES:
        if P.n == n and P.m == len(E) and P.tau == t:
            if G is None: G = inc_graph(n, E)
            if nx.is_isomorphic(G, inc_graph(P.n, P.edges), node_match=lambda p, q: p['t'] == q['t']): return P.name
    return None

def analyse_H(n, E, t_expected=None):
    """full evaluation of H (assumed Delta<=3): membership in C, tau (two methods), A, DEF, DEF proper."""
    r = {}
    m = len(E)
    r['n'] = n; r['m'] = m
    r['inC'] = pyverify.in_C(E)
    if not r['inC']: return r
    t = kt.tau_masks(kt.masks(E))
    t2 = cpsat_tau(n, E)
    assert t == t2, ('tau mismatch', E, t, t2)
    if t_expected is not None: assert t == t_expected, ('tau != tau(G)+2', E, t, t_expected)
    r['tau'] = t
    r['A'] = kt.A_value(n, m, t)
    r['piece'] = is_piece(n, E, t)
    r['DEF'] = kt.deficiency(n, E, PIECES, proper=False)
    r['DEFp'] = kt.deficiency(n, E, PIECES, proper=True)
    r['P'] = r['A'] + r['DEF']; r['Pp'] = r['A'] + r['DEFp']
    return r
