"""Referee (fable, L024 round 1): own primitives, independent of hyp24.py and kt.py.
Brute force wherever feasible. Exact integers only."""
import itertools, json, re
import networkx as nx
from networkx.algorithms import isomorphism as iso

CLOSURE = '/home/user/Erdos-757/experiments/prover/L021/closure_results.json'
RICH_IN = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'

def load_pieces():
    D = json.load(open(CLOSURE))
    out = []
    for P in D['pieces']:
        E = [tuple(sorted(e)) for e in P['edges']]
        out.append(dict(name=P['name'], n=P['n'], m=len(E), edges=E, W_claimed=P['W'], tau_claimed=P['tau']))
    return out

def read_cell_txt(path):
    """lines: n m tau then 3m vertex labels"""
    out = []
    for l in open(path):
        t = l.split()
        if not t: continue
        n, m, tau = int(t[0]), int(t[1]), int(t[2])
        v = list(map(int, t[3:]))
        assert len(v) == 3 * m, (path, l[:40])
        E = [tuple(sorted(v[3*i:3*i+3])) for i in range(m)]
        out.append((n, m, tau, E))
    return out

def degrees(n, E):
    d = [0]*n
    for e in E:
        for x in e: d[x] += 1
    return d

def is_transversal(T, E):
    return all(any(x in T for x in e) for e in E)

def tau_brute(n, E):
    """smallest k such that some k-subset meets all edges (brute force by size)."""
    if not E: return 0
    for k in range(0, n+1):
        for T in itertools.combinations(range(n), k):
            S = set(T)
            if all(S & set(e) for e in E): return k
    raise RuntimeError

def min_transversals_brute(n, E, t):
    res = []
    for T in itertools.combinations(range(n), t):
        S = set(T)
        if all(S & set(e) for e in E): res.append(frozenset(T))
    return res

def tau_bb(n, E):
    """branch and bound tau (for n up to ~31); independent implementation (branch on an edge of max 'uncovered weight')."""
    E = [set(e) for e in E]
    best = [len(E)]
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        # greedy disjoint lower bound
        used = set(); lb = 0
        for e in rem:
            if not (e & used): used |= e; lb += 1
        if k + lb >= best[0]: return
        e = min(rem, key=lambda f: sum(1 for x in f))  # any edge
        for x in sorted(e):
            rec([f for f in rem if x not in f], k+1)
    rec(E, 0)
    return best[0]

def is_linear(E):
    seen = set()
    for e in E:
        for p in itertools.combinations(e, 2):
            if p in seen: return False
            seen.add(p)
    return True

def has_F7(E):
    """brute force: some 5 edges span 7 vertices, are linear, with degree sequence (3,2,2,2,2,2,2).
    Any linear 5-edge 3-graph on 7 vertices with this degree sequence is F7 (see review)."""
    for sub in itertools.combinations(E, 5):
        V = set()
        for e in sub: V |= set(e)
        if len(V) != 7: continue
        d = {}
        for e in sub:
            for x in e: d[x] = d.get(x, 0) + 1
        if sorted(d.values(), reverse=True) != [3,2,2,2,2,2,2]: continue
        if is_linear(sub): return True
    return False

def p3_brute(n, E):
    """e(S) <= |S|-2 for every S with |S| >= 2; full enumeration of subsets by bitmask."""
    em = [sum(1 << x for x in e) for e in E]
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 2: continue
        c = 0
        for e in em:
            if e & S == e: c += 1
        if c > k - 2: return False
    return True

def in_C3(n, E):
    d = degrees(n, E)
    if d and max(d) > 3: return False, 'degree'
    if not is_linear(E): return False, 'linear'
    if has_F7(E): return False, 'F7'
    if not p3_brute(n, E): return False, 'P3'
    return True, 'ok'

def incidence_graph(n, E):
    G = nx.Graph()
    for x in range(n): G.add_node(('v', x), kind=0)
    for i, e in enumerate(E):
        G.add_node(('e', i), kind=1)
        for x in e: G.add_edge(('v', x), ('e', i))
    return G

def isomorphic(n1, E1, n2, E2):
    if n1 != n2 or len(E1) != len(E2): return False
    if sorted(degrees(n1, E1)) != sorted(degrees(n2, E2)): return False
    nm = iso.categorical_node_match('kind', -1)
    return nx.is_isomorphic(incidence_graph(n1, E1), incidence_graph(n2, E2), node_match=nm)

def automorphism_orbits(n, E):
    """orbits of vertices under the automorphism group (networkx VF2 on the incidence graph)."""
    G = incidence_graph(n, E)
    nm = iso.categorical_node_match('kind', -1)
    GM = iso.GraphMatcher(G, G, node_match=nm)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for phi in GM.isomorphisms_iter():
        for x in range(n):
            y = phi[('v', x)][1]
            a, b = find(x), find(y)
            if a != b: parent[a] = b
    orbits = {}
    for x in range(n): orbits.setdefault(find(x), []).append(x)
    return list(orbits.values())

def connected(n, E):
    adj = [set() for _ in range(n)]
    for e in E:
        for x in e: adj[x] |= set(e)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n

def A_val(n, m, t): return 27*n + 35*m - 132*t
