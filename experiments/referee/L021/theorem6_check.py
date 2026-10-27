"""Referee #2 (L021): numerical check of Theorem 6 (KT for Delta <= 2) on all connected subcubic dual graphs with N <= NMAX
vertices (nauty geng), using ONLY the two pieces named in Theorem 6 (E_1 and (8,5,3)#0 = {012,156,247,346,357}).
Own dual construction; tau via SAT; nu(G) by brute force over edge subsets (independent of networkx matching);
checks: tau = N - nu, A = 132 nu - 16 N - 27 M, Tutte-Berge lower bound of 6.2 (A >= 35|U| + sum theta_i for the
Tutte-Berge set U found by brute force), and P = A + DEF >= 0.  Usage: python3 theorem6_check.py NMAX"""
import sys, subprocess, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L021')
from ref_lib import *
import networkx as nx
GENG = '/home/user/Erdos-757/experiments/referee/L013-round2/bin/geng'
NMAX = int(sys.argv[1])
E1 = Piece([(0, 1, 2)], 'E1')
P853 = Piece([(0, 1, 2), (1, 5, 6), (2, 4, 7), (3, 4, 6), (3, 5, 7)], '(8,5,3)#0')
assert E1.W == 16 and P853.W == 5 and P853.tau == 3
pieces = [E1, P853]
# dual of (8,5,3)#0 is K4 with one edge subdivided (check)
def dual_graph(edges):
    G = nx.Graph(); G.add_nodes_from(range(len(edges)))
    inc = {}
    for i, e in enumerate(edges):
        for x in e: inc.setdefault(x, []).append(i)
    for x, l in inc.items():
        if len(l) == 2: G.add_edge(l[0], l[1])
        assert len(l) <= 2
    return G
K4s = nx.Graph([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]); K4s.remove_edge(1, 2); K4s.add_edges_from([(0, 1), (0, 2)])
print('dual of (8,5,3)#0 is K4 with one edge subdivided:', nx.is_isomorphic(dual_graph(P853.edges), K4s))
def nu_brute(G):
    E = list(G.edges()); best = 0
    for k in range(len(E), 0, -1):
        if k <= best: break
        for sub in itertools.combinations(E, k):
            vs = [v for e in sub for v in e]
            if len(set(vs)) == 2 * k: best = k; break
    return best
def tutte_berge_min(G):
    N = G.number_of_nodes(); best = None
    for k in range(N + 1):
        for U in itertools.combinations(G.nodes(), k):
            Gm = G.copy(); Gm.remove_nodes_from(U)
            o = sum(1 for c in nx.connected_components(Gm) if len(c) % 2 == 1)
            val = N + k - o
            if best is None or val < best[0]: best = (val, U)
    return best
t0 = time.time(); tot = 0; neg = 0; eq = 0; minP = None; special = 0; tb_checked = 0
for N in range(1, NMAX + 1):
    out = subprocess.run([GENG, '-cq', '-D3', str(N)], capture_output=True, text=True).stdout.split()
    cnt = 0
    for g6 in out:
        G = nx.from_graph6_bytes(g6.encode()); M = G.number_of_edges()
        slots = {x: [] for x in G.nodes()}; hv = 0
        for (x, y) in G.edges():
            slots[x].append(hv); slots[y].append(hv); hv += 1
        for x in G.nodes():
            while len(slots[x]) < 3: slots[x].append(hv); hv += 1
        edges = [tuple(sorted(slots[x])) for x in G.nodes()]
        n = hv; m = len(edges)
        assert is_linear(edges) and m == N and n == 3 * N - M
        t = tau_sat(n, edges)
        nu = nu_brute(G)
        assert t == N - nu, (g6, t, N, nu)
        A = CN * n + CM * m - CT * t
        assert A == 132 * nu - 16 * N - 27 * M
        # Tutte-Berge check of 6.2 for N <= 8 (brute force over U)
        if N <= 8:
            val, U = tutte_berge_min(G); assert val == 2 * nu
            Gm = G.copy(); Gm.remove_nodes_from(U)
            th = 0; o1 = 0; o5 = 0
            for c in nx.connected_components(Gm):
                ci = len(c); ei = Gm.subgraph(c).number_of_edges()
                th += 50 * ci - 27 * ei - 66 * (ci % 2)
                if ci == 1: o1 += 1
                if ci == 5 and ei == 7: o5 += 1
            assert A >= 35 * len(U) + th, (g6, A, U, th)
            tb_checked += 1
        D, fam, ncop = deficiency(n, edges, pieces, proper=False) if A < 0 else (0, [], 0)
        P = A + D
        tot += 1; cnt += 1
        if A < 0: special += 1
        if P < 0: neg += 1; print('KT FAILS', g6, n, m, t, A, D, flush=True)
        if P == 0: eq += 1
        minP = P if minP is None else min(minP, P)
    print(f'N={N}: {cnt} connected subcubic G  [{time.time()-t0:.0f}s]', flush=True)
print(f'theorem6_check NMAX={NMAX}: {tot} graphs, A<0 in {special}, KT failures {neg}, equality {eq}, min(A+DEF) {minP}, Tutte-Berge bound 6.2 checked on {tb_checked} graphs')
