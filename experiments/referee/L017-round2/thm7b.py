"""Referee round 2, L017, Theorem 7 PART B (corrected: m(H) = |V(G)|, so tau(H) = |V(G)| - nu(G)): for every simple graph G with
Delta<=3 on at most NMAX vertices build the dual linear 3-graph H (G-vertex -> H-edge with 3 slots, G-edge -> degree-2 vertex,
unfilled slots -> degree-1 vertices, plus n0 isolated vertices) and check tau(H) = m - nu(G) (ILP; brute force for small H) and
s(H) = 3 n0 + 11 nu(G) - 3 |E(G)|; record the least slack of a connected H with m >= 2."""
import subprocess, itertools, sys, random
import networkx as nx, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
GENG = '/home/user/Erdos-757/experiments/referee/L013-round2/out/nauty_build/geng'
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
def graphs(n):
    out = subprocess.run([GENG, '-q', '-D3', str(n)], capture_output=True, text=True, timeout=600).stdout.split()
    return [nx.from_graph6_bytes(s.encode()) for s in out]
def nu(G): return len(nx.max_weight_matching(G, maxcardinality=True))
def tau_ilp(n, edges):
    if not edges: return 0
    A = np.zeros((len(edges), n))
    for i, e in enumerate(edges):
        for v in e: A[i, v] = 1
    res = milp(c=np.ones(n), constraints=LinearConstraint(A, lb=np.ones(len(edges))), integrality=np.ones(n), bounds=Bounds(0, 1))
    assert res.success; return int(round(res.fun))
def tau_brute(n, edges):
    es = [set(e) for e in edges]
    for k in range(n+1):
        for S in itertools.combinations(range(n), k):
            if all(set(S) & e for e in es): return k
def dual(G, n0):
    nodes = list(G.nodes()); idx = {v: i for i, v in enumerate(nodes)}; m = len(nodes)
    edges = [[] for _ in range(m)]; nv = 0
    for u, v in G.edges():
        edges[idx[u]].append(nv); edges[idx[v]].append(nv); nv += 1
    for i in range(m):
        while len(edges[i]) < 3: edges[i].append(nv); nv += 1
    return nv + n0, [tuple(e) for e in edges]
random.seed(20261027); checked = 0; mism = 0; min_conn = None; tight = 0; brute = 0
for n in range(1, NMAX+1):
    for G in graphs(n):
        N = G.number_of_nodes(); M = G.number_of_edges(); v = nu(G)
        for n0 in (0, random.choice((1, 2))):
            nH, EH = dual(G, n0); mH = len(EH); assert mH == N
            assert all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(EH, 2))
            degs = [0]*nH
            for e in EH:
                for x in e: degs[x] += 1
            assert max(degs) <= 2 and degs.count(2) == M and degs.count(0) == n0
            tH = tau_ilp(nH, EH); checked += 1
            if n <= 5: assert tau_brute(nH, EH) == tH; brute += 1
            sH = 3*nH + 2*mH - 11*tH
            if tH != mH - v or sH != 3*n0 + 11*v - 3*M: mism += 1; print('MISMATCH', nx.to_graph6_bytes(G, header=False).strip(), n0, tH, mH - v, sH)
            if sH == 0: tight += 1; assert M == 0 and n0 == 0
            if n0 == 0 and mH >= 2 and nx.is_connected(G) and (min_conn is None or sH < min_conn): min_conn = sH
    print('n=%d done' % n, flush=True)
print('PART B: %d dual 3-graphs checked (%d also by brute force): mismatches of tau(H)=m-nu(G) or s(H)=3n0+11nu-3|E(G)|: %d; tight ones: %d (all are perfect matchings: asserted); min slack of a connected H with m>=2: %s' % (checked, brute, mism, tight, min_conn))
