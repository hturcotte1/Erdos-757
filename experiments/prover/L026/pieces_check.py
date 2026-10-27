"""L026 C1: the 32 pieces of L* (edge lists read from L021 closure_results.json as data), own code:
weights W = -A, property (L1) (every vertex lies in a minimum transversal), connectivity, membership
in C_3, maximum weight, and the pieces having an edge with two vertices of piece-degree 1 (used in
the proof of Theorem 12(c), case Y2) and the b-configurations of the pieces with >= 12 vertices
(Theorem 12(a), p = 1)."""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L
ps = L.load_pieces()
ws = {}
bad = 0
for P in ps:
    T = L.all_min_transversals(P.E, P.t)
    cov = 0
    for t in T: cov |= t
    L1 = cov == (1 << P.n) - 1
    conn = len(L.components(P.n, P.E)) == 1
    inC = L.in_C3(P.n, P.E)
    two1 = [e for e in P.E if sum(1 for u in e if P.deg[u] == 1) >= 2]
    co = set()
    for t in T:
        vs = [i for i in range(P.n) if t >> i & 1]
        for p in itertools.combinations(vs, 2): co.add(p)
    Es = set(tuple(sorted(e)) for e in P.E)
    bconf = [(a, b, c) for a, b, c in itertools.combinations(range(P.n), 3)
             if (a, b) not in co and (a, c) not in co and (b, c) not in co and (a, b, c) not in Es]
    ws.setdefault((P.n, P.m, P.t, P.W), 0); ws[(P.n, P.m, P.t, P.W)] += 1
    if not (L1 and conn and inC): bad += 1
    print(P.name, (P.n, P.m, P.t), 'W', P.W, 'L1', L1, 'connected', conn, 'inC3', inC,
          'edges with two deg-1 vertices', len(two1), 'b-confs', len(bconf))
print('summary (n,m,tau,W): count', ws, 'failures', bad)
