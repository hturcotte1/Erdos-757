"""Referee #1 (L021): Theorem 6 (KT for Delta <= 2) and its lemmas, tested independently.
(1) theta table of 6.3 on every connected simple subcubic graph with <= 7 vertices (networkx atlas);
    c=5, e=7 is exactly K4 with one edge subdivided;
(2) for every connected simple subcubic G with N <= 7 (atlas) and random connected subcubic G with 8 <= N <= NMAX:
    build H (one H-edge per G-vertex, one H-vertex per G-edge, pendant vertices), check H in C_3,
    tau(H) by ILP = N - nu(G) (networkx matching), A = 132 nu - 16N - 27M, DEF by ILP over induced copies of all
    32 pieces, P >= 0; record the minimum of P."""
import os, sys, json, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcore import *
from networkx.generators.atlas import graph_atlas_g
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
NR = int(sys.argv[2]) if len(sys.argv) > 2 else 300
src = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']
pcs = [(p['name'], nv(p['edges']), [tuple(e) for e in p['edges']], p['W']) for p in src]
atlas = [g for g in graph_atlas_g() if g.number_of_nodes() >= 1 and nx.is_connected(g) and max(dict(g.degree()).values() or [0]) <= 3]
K4s = nx.Graph([(0,1),(0,2),(1,3),(2,3),(1,2),(1,4),(2,4)])  # placeholder, replaced below
K4s = nx.Graph([('b','d'),('b','e'),('c','d'),('c','e'),('d','e'),('a','b'),('a','c')])
neg = []
for g in atlas:
    c, e = g.number_of_nodes(), g.number_of_edges()
    th = 50*c - 27*e - 66*(c % 2)
    if th < 0: neg.append((c, e, th, nx.is_isomorphic(g, K4s)))
print('(1) atlas connected subcubic graphs:', len(atlas), '; negative theta:', sorted(set(neg)))
def build_H(G):
    nodes = list(G.nodes()); idx = {x: i for i, x in enumerate(nodes)}
    hv = {}; k = 0
    for (x, y) in G.edges(): hv[frozenset((x, y))] = k; k += 1
    edges = []
    for x in nodes:
        e = [hv[frozenset((x, y))] for y in G.neighbors(x)]
        while len(e) < 3: e.append(k); k += 1
        edges.append(tuple(e))
    return k, edges
def rand_subcubic(N, rng):
    while True:
        G = nx.Graph(); G.add_nodes_from(range(N))
        tries = 0
        while tries < 6*N:
            tries += 1
            a, b = rng.randrange(N), rng.randrange(N)
            if a != b and not G.has_edge(a, b) and G.degree(a) < 3 and G.degree(b) < 3 and rng.random() < 0.8:
                G.add_edge(a, b)
        if nx.is_connected(G): return G
rng = random.Random(20261027)
graphs = list(atlas) + [rand_subcubic(rng.randrange(8, NMAX + 1), rng) for _ in range(NR)]
minP = None; fails = 0; cnt = 0; negA = 0
for G in graphs:
    N, M = G.number_of_nodes(), G.number_of_edges()
    n, e = build_H(G)
    assert len(e) == N and n == 3*N - M
    assert max(degrees(n, e)) <= 2 and in_C(n, e)
    t = tau_ilp(n, e); nu = len(nx.max_weight_matching(G, maxcardinality=True))
    A = A_val(n, N, t)
    ok1 = (t == N - nu) and (A == 132*nu - 16*N - 27*M)
    copies = []
    for (nm, pn, pe, W) in pcs:
        for U in induced_copies(n, e, pn, pe): copies.append((U, W))
    D, fam = DEF_ilp(n, e, copies)
    P = A + D
    if A < 0: negA += 1
    if not ok1 or P < 0: fails += 1; print('FAIL', N, M, list(G.edges()), t, nu, A, D)
    minP = P if minP is None else min(minP, P); cnt += 1
print('(2) graphs tested:', cnt, '(atlas', len(atlas), '+ random', NR, ', N <=', NMAX, ') with A<0:', negA, ' failures:', fails, ' min P:', minP)
