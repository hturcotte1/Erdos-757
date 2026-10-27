"""Referee #1 (L021, round 1): independent core. Does NOT import kt.py, e757 or the judge.
Methods: tau and DEF by CP-SAT integer programs (OR-tools); minimum transversals of small pieces by
brute force over all k-subsets; induced copies by VF2 monomorphisms of typed incidence graphs (networkx)
followed by an induced-edge count; class C membership by direct tests (pairs for linearity, an explicit
F7 search, and (P3) by Hall/matching for every vertex pair)."""
import itertools, re
import networkx as nx
from networkx.algorithms import isomorphism as iso
from ortools.sat.python import cp_model

def parse_cell(path):
    out = []
    for l in open(path):
        if l.startswith('FOUND'):
            out.append([tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)])
    return out

def nv(edges):
    return 1 + max(max(e) for e in edges) if edges else 0

def degrees(n, edges):
    d = [0]*n
    for e in edges:
        for x in e: d[x] += 1
    return d

def connected(n, edges):
    if n == 0: return True
    adj = [set() for _ in range(n)]
    for e in edges:
        for x in e:
            adj[x] |= set(e) - {x}
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n

def is_linear(edges):
    seen = set()
    for e in edges:
        if len(set(e)) != 3: return False
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen.add(p)
    return True

def has_F7(n, edges):
    """F7 = {012,034,056,135,246}: a centre c with three edges {c,a1,b1},{c,a2,b2},{c,a3,b3} and two further
    edges {x1,x2,x3}, {y1,y2,y3} with {xi,yi} = {ai,bi}."""
    E = set(frozenset(e) for e in edges)
    inc = [[] for _ in range(n)]
    for e in edges:
        for x in e: inc[x].append(e)
    for c in range(n):
        if len(inc[c]) < 3: continue
        for e1, e2, e3 in itertools.combinations(inc[c], 3):
            P = [tuple(x for x in e if x != c) for e in (e1, e2, e3)]
            for bits in itertools.product((0, 1), repeat=3):
                X = frozenset(P[i][bits[i]] for i in range(3))
                Y = frozenset(P[i][1-bits[i]] for i in range(3))
                if X in E and Y in E: return True
    return False

def _match_all_edges(edges, verts_ok):
    """bipartite matching edges -> allowed vertices; True iff every edge can be matched."""
    match = {}
    def aug(i, seen):
        for x in edges[i]:
            if x in verts_ok and x not in seen:
                seen.add(x)
                if x not in match or aug(match[x], seen):
                    match[x] = i; return True
        return False
    for i in range(len(edges)):
        if not aug(i, set()): return False
    return True

def p3_ok(n, edges):
    """e(S) <= |S|-2 for all |S|>=2  <=>  for every pair {x,y}, edges match into V minus {x,y} (Hall)."""
    if not edges: return True
    allv = set(range(n))
    for x, y in itertools.combinations(range(n), 2):
        if not _match_all_edges(edges, allv - {x, y}): return False
    return True

def in_C(n, edges):
    return is_linear(edges) and not has_F7(n, edges) and p3_ok(n, edges)

def tau_ilp(n, edges):
    if not edges: return 0
    md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(n)]
    for e in edges: md.AddBoolOr([x[v] for v in e])
    md.Minimize(sum(x))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 600
    r = s.Solve(md); assert r == cp_model.OPTIMAL, r
    return int(round(s.ObjectiveValue()))

def min_transversals_bf(n, edges, t=None):
    """all minimum transversals by brute force over k-subsets (small n only)."""
    em = [sum(1 << v for v in e) for e in edges]
    k = 0
    while True:
        res = []
        for c in itertools.combinations(range(n), k):
            m = sum(1 << v for v in c)
            if all(m & e for e in em): res.append(m)
        if res:
            if t is not None: assert k == t, (k, t)
            return k, res
        k += 1

def A_val(n, m, t):
    return 27*n + 35*m - 132*t

def incidence(n, edges):
    G = nx.Graph()
    for v in range(n): G.add_node(('v', v), t=0)
    for i, e in enumerate(edges):
        G.add_node(('e', i), t=1)
        for v in e: G.add_edge(('v', v), ('e', i))
    return G

def induced_copies(hn, hedges, pn, pedges):
    """set of frozensets U (|U| = pn) with H[U] isomorphic to the piece."""
    if pn > hn: return set()
    GH = incidence(hn, hedges); GP = incidence(pn, pedges)
    GM = iso.GraphMatcher(GH, GP, node_match=lambda a, b: a['t'] == b['t'])
    hsets = [frozenset(e) for e in hedges]
    out = set()
    for mp in GM.subgraph_monomorphisms_iter():
        U = frozenset(h[1] for h, p in mp.items() if h[0] == 'v')
        if U in out: continue
        if sum(1 for e in hsets if e <= U) == len(pedges): out.add(U)
    return out

def DEF_ilp(hn, hedges, copies):
    """copies: list of (U frozenset, W). exact max over families of disjoint copies of sum W - 35 |E*|, >= 0."""
    if not copies: return 0, []
    md = cp_model.CpModel()
    y = [md.NewBoolVar('y%d' % i) for i in range(len(copies))]
    for v in range(hn):
        cs = [y[i] for i, (U, w) in enumerate(copies) if v in U]
        if len(cs) > 1: md.Add(sum(cs) <= 1)
    z = []
    for j, e in enumerate(hedges):
        es = set(e)
        trig = [i for i, (U, w) in enumerate(copies) if (es & U) and not es <= U]
        if trig:
            zj = md.NewBoolVar('z%d' % j); z.append(zj)
            for i in trig: md.AddImplication(y[i], zj)
    md.Maximize(sum(copies[i][1]*y[i] for i in range(len(copies))) - 35*sum(z))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 600
    r = s.Solve(md); assert r == cp_model.OPTIMAL, r
    fam = [i for i in range(len(copies)) if s.Value(y[i])]
    return int(round(s.ObjectiveValue())), fam

def DEF_of_family(hn, hedges, fam_sets_weights):
    """direct evaluation from the definition."""
    Us = [U for U, w in fam_sets_weights]
    for a, b in itertools.combinations(Us, 2): assert not (a & b)
    allU = frozenset().union(*Us) if Us else frozenset()
    estar = 0
    for e in hedges:
        es = set(e)
        if es & allU and not any(es <= U for U in Us): estar += 1
    return sum(w for U, w in fam_sets_weights) - 35*estar
