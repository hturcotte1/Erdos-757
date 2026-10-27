"""Referee round 2, L017, Theorem 7: (a) 11 nu(G) >= 3|E(G)| for all simple graphs with Delta<=3 up to NMAX vertices (nauty geng),
equality only for E(G) empty, minimum positive value and the extremal graphs; (b) for every such G build the dual linear 3-graph H
(each G-vertex is an H-edge with three slots, each G-edge a degree-2 vertex, unfilled slots degree-1 vertices, plus n0 isolated
vertices) and check tau(H) = m - nu(G) (tau by ILP and, for small H, by brute force) and s(H) = 3 n0 + 11 nu - 3|E(G)|.
Also the specific small cases named in the referee task."""
import subprocess, itertools, sys, random
import networkx as nx, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
GENG = '/home/user/Erdos-757/experiments/referee/L013-round2/out/nauty_build/geng'
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
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
random.seed(20261027)
total = 0; viol = 0; eq_pos = 0; minpos = {}; checked_tau = 0; mism = 0; min_conn_slack = None
for n in range(1, NMAX+1):
    gs = graphs(n)
    for G in gs:
        M = G.number_of_edges(); v = nu(G); val = 11*v - 3*M; total += 1
        if val < 0: viol += 1; print('VIOLATION', nx.to_graph6_bytes(G))
        if M > 0 and val == 0: eq_pos += 1
        if M > 0 and (n not in minpos or val < minpos[n][0]): minpos[n] = (val, nx.to_graph6_bytes(G, header=False).strip(), M, v)
        if n <= 8:
            n0 = random.choice((0, 0, 1, 2)); nH, EH = dual(G, n0)
            assert all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(EH, 2))
            tH = tau_ilp(nH, EH); checked_tau += 1
            if tH != M - v or 3*nH + 2*M - 11*tH != 3*n0 + val: mism += 1; print('MISMATCH', nx.to_graph6_bytes(G), n0, tH, M - v)
            if n <= 5: assert tau_brute(nH, EH) == tH
            if nx.is_connected(G) and M >= 1:
                sH = 3*nH + 2*M - 11*tH - 3*n0
                if min_conn_slack is None or sH < min_conn_slack: min_conn_slack = sH
    print('n=%d: %d graphs with Delta<=3 processed' % (n, len(gs)), flush=True)
print('PART A: %d graphs, violations of 11nu>=3M: %d; graphs with M>0 and 11nu=3M: %d' % (total, viol, eq_pos))
for n in sorted(minpos): print('   n=%d: min 11nu-3M over M>0 = %d at graph6 %s (M=%d, nu=%d)' % (n, minpos[n][0], minpos[n][1].decode(), minpos[n][2], minpos[n][3]))
print('PART B: %d dual 3-graphs: tau(H) = m - nu(G) and s(H) = 3n0 + 11nu - 3|E(G)| mismatches: %d; min slack of connected dual H with m>=2 (n0=0): %s' % (checked_tau, mism, min_conn_slack))
for name, G in (('K3', nx.complete_graph(3)), ('K4', nx.complete_graph(4)), ('K_{1,3}', nx.star_graph(3)), ('P2', nx.path_graph(2)), ('K4 subdivided edge', nx.from_graph6_bytes(b'D]w')), ('K_{3,3}', nx.complete_bipartite_graph(3, 3)), ('Petersen', nx.petersen_graph())):
    print('   %s: |E|=%d nu=%d 11nu-3|E|=%d' % (name, G.number_of_edges(), nu(G), 11*nu(G) - 3*G.number_of_edges()))
