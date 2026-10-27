"""L021: test KT (epsilon = 1/6, the 32-piece list L) on every connected linear 3-graph of maximum degree <= 2 whose dual
graph G (vertices = edges of H, one G-edge per degree-2 vertex) has N <= NMAX vertices: G runs over all connected
simple graphs with max degree <= 3 (nauty geng -c -D3), H = dual with 3 - deg_G(x) pendant degree-1 vertices at each x.
Every such H lies in C (shown in L021 Step 6.1).  A(H) = 132 nu(G) - 16 N - 27 M (Theorem 7 of L017: tau = N - nu(G));
the code recomputes tau of H directly and DEF by kt.deficiency.  Usage: python3 delta2_test.py NMAX"""
import sys, subprocess, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
import networkx as nx
GENG = '/home/user/Erdos-757/experiments/referee/L013-round2/bin/geng'
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
pieces = [Piece(p['edges'], p['name']) for p in R['pieces']]
NMAX = int(sys.argv[1])
tot = 0; neg = 0; eq = 0; minP = None; special = 0
for N in range(1, NMAX + 1):
    out = subprocess.run([GENG, '-cq', '-D3', str(N)], capture_output=True, text=True).stdout.split()
    cntN = 0
    for g6 in out:
        G = nx.from_graph6_bytes(g6.encode())
        M = G.number_of_edges()
        # build H
        slots = {x: [] for x in G.nodes()}
        hv = 0
        for (x, y) in G.edges():
            slots[x].append(hv); slots[y].append(hv); hv += 1
        for x in G.nodes():
            while len(slots[x]) < 3:
                slots[x].append(hv); hv += 1
        edges = [tuple(sorted(slots[x])) for x in G.nodes()]
        n = hv; m = len(edges)
        t = tau_masks(masks(edges))
        nu = len(nx.max_weight_matching(G, maxcardinality=True))
        assert t == N - nu, (g6, t, N, nu)
        A = A_value(n, m, t)
        assert A == 132 * nu - 16 * N - 27 * M
        D = deficiency(n, edges, pieces, proper=False) if A < 0 else 0
        P = A + D
        tot += 1; cntN += 1
        if A < 0: special += 1
        if P < 0:
            neg += 1; print('KT FAILS', g6, n, m, t, A, D, flush=True)
        if P == 0: eq += 1
        minP = P if minP is None else min(minP, P)
    print(f'N={N}: {cntN} connected subcubic G', flush=True)
print(f'delta2_test NMAX={NMAX}: {tot} graphs, A<0 in {special}, KT failures {neg}, equality {eq}, min(A+DEF) {minP}')
