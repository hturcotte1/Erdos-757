"""Independent check of the Delta<=2 cells cell(24,15,9,2) (engine: 0 classes) and cell(25,15,9,2) (engine: 2 classes).
A connected linear 3-graph H with Delta<=2 <-> a connected simple graph G (vertices = edges of H, edges = degree-2 vertices of H),
Delta(G)<=3, with 3-deg_G(i) pendant vertices on hyperedge i; n(H) = m + e(G) + ... : n = e(G) + (3m - 2e(G)) = 3m - e(G).
H in C is automatic (F7 needs a degree-3 vertex; (P3): for a set F of f hyperedges |V(F)| = 3f - e_G[F] >= f+2 since e_G[F] <= 2f-2 for simple graphs with Delta<=3).
tau(H) = m - nu(G) (cover of hyperedges by vertices of degree 2 pair up along a matching).  Isomorphism classes of H <-> of G (geng).
usage: python3 indep_delta2.py m e tau"""
import subprocess, sys, networkx as nx
m, e, tau = map(int, sys.argv[1:4])
geng = '/home/user/Erdos-757/experiments/referee/L013-round2/bin/geng'
out = subprocess.run([geng, '-c', '-D3', str(m), f'{e}:{e}', '-q'], capture_output=True, text=True).stdout.split()
cnt = 0
for g6 in out:
    G = nx.from_graph6_bytes(g6.encode())
    nu = len(nx.max_weight_matching(G, maxcardinality=True))
    if m - nu == tau: cnt += 1
print(f'H with m={m}, n={3*m-e}, tau={tau}, Delta<=2: graphs G with {m} vertices, {e} edges, Delta<=3 generated {len(out)}; classes with nu={m-tau}: {cnt}')
