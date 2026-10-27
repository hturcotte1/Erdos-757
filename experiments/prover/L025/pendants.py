"""L025: number of degree-1 vertices (n_1) in the stored near-tight classes (Delta<=3), and in K29."""
from hyp25 import *
from census import NEAR
res = {}
for (n, m, t) in NEAR:
    hist = {}
    for (n0, m0, t0, E) in load_cell(n, m, t):
        h = Hyp(E, range(n0))
        if h.maxdeg() > 3: continue
        n1 = sum(1 for v in h.V if h.deg[v] == 1)
        hist[n1] = hist.get(n1, 0) + 1
    print((n, m, t), 'slack', 3*n+2*m-11*t, 'n_1 histogram', dict(sorted(hist.items())))
hist = {}
for (n0, m0, t0, E) in load_k29():
    h = Hyp(E, range(n0)); n1 = sum(1 for v in h.V if h.deg[v] == 1); hist[n1] = hist.get(n1, 0) + 1
print('K29 n_1 histogram', hist)
