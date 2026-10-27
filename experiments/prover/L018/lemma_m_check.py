"""lemma_m_check.py -- numerical checks of Theorem 2 (Lemma M) of L018 (exact integers):
(A) every census graph (connected, class C, Delta<=3, n<=14) with Delta<=2: 7*slack >= n2 (n2 = #degree-2 vertices),
    and slack == 11*nu(G) - 3|E(G)| for the dual graph G;
(B) random linear 3-graphs with Delta<=2 (not necessarily connected, isolated vertices allowed, NOT required to be in C):
    7*(slack - 3*n0) >= n2 and the dual identity;
(C) random simple subcubic graphs: 7*nu >= 2|E|."""
import glob, random, collections, sys
import networkx as nx
from hg import tau_of
def dual(E, n):
    inc = collections.defaultdict(list)
    for i, e in enumerate(E):
        for v in e: inc[v].append(i)
    G = nx.Graph(); G.add_nodes_from(range(len(E)))
    for v, L in inc.items():
        if len(L) == 2: G.add_edge(*L)
    n2 = sum(1 for v in range(n) if len(inc[v]) == 2)
    n0 = sum(1 for v in range(n) if len(inc[v]) == 0)
    return G, n2, n0
def nu(G):
    return len(nx.max_weight_matching(G, maxcardinality=True))
cntA = 0; minA = None
for fn in sorted(glob.glob('/home/user/Erdos-757/experiments/20261027-0230-red-config/out/cls_*.txt')):
    n = int(fn.split('_')[-2])
    for line in open(fn):
        t = line.split()
        if not t: continue
        if t[0] == 'C': t = t[1:]
        m = int(t[0]); E = [tuple(map(int, x.split('.'))) for x in t[1:1+m]]
        d = collections.Counter(v for e in E for v in e)
        if max(d.values()) > 2: continue
        tau = tau_of(E); s = 3*n + 2*m - 11*tau
        G, n2, n0 = dual(E, n)
        assert s == 11*nu(G) - 3*G.number_of_edges() + 3*n0, (E, s)
        assert 7*s >= n2, (E, s, n2)
        cntA += 1
        r = (7*s - n2)
        minA = r if minA is None else min(minA, r)
print('(A) census Delta<=2 graphs checked:', cntA, ' min of 7*slack - n2:', minA)
random.seed(18)
cntB = 0; minB = None
for trial in range(4000):
    n = random.randint(3, 22)
    E = []; deg = [0]*n
    for _ in range(random.randint(1, 3*n)):
        e = tuple(sorted(random.sample(range(n), 3)))
        if any(deg[v] >= 2 for v in e): continue
        if any(len(set(e) & set(f)) > 1 for f in E): continue
        E.append(e)
        for v in e: deg[v] += 1
    if not E: continue
    tau = tau_of(E); s = 3*n + 2*len(E) - 11*tau
    G, n2, n0 = dual(E, n)
    assert s == 11*nu(G) - 3*G.number_of_edges() + 3*n0
    assert 7*(s - 3*n0) >= n2, (E, s)
    cntB += 1
    r = 7*(s - 3*n0) - n2; minB = r if minB is None else min(minB, r)
print('(B) random linear Delta<=2 3-graphs:', cntB, ' min of 7*(slack-3n0) - n2:', minB)
cntC = 0; tight = 0
for trial in range(20000):
    N = random.randint(2, 18)
    G = nx.Graph(); G.add_nodes_from(range(N))
    for _ in range(random.randint(1, 2*N)):
        u, v = random.sample(range(N), 2)
        if G.degree(u) < 3 and G.degree(v) < 3: G.add_edge(u, v)
    k = nu(G); e = G.number_of_edges()
    assert 7*k >= 2*e, (N, list(G.edges()))
    tight += (7*k == 2*e and e > 0); cntC += 1
# the extremal example K4 with one subdivided edge
G = nx.complete_graph(4); G.remove_edge(0, 1); G.add_edges_from([(0, 4), (4, 1)])
print('(C) random subcubic graphs:', cntC, ' with 7nu = 2|E|:', tight, '; K4 with a subdivided edge: nu =', nu(G), '|E| =', G.number_of_edges())
