"""L025: b-configurations (non-edge) in stored cells of any slack, classified by type
(degrees, adjacencies); prints the graphs having a non-edge b-configuration.  Usage: python3 census2.py n m t [maxshow]"""
import sys, time
from itertools import combinations
from hyp25 import *
from census import nc_info
n, m, t = map(int, sys.argv[1:4]); maxshow = int(sys.argv[4]) if len(sys.argv) > 4 else 3
L = load_cell(n, m, t); t0 = time.time(); cnt = 0; types = {}; shown = 0
for k, (n0, m0, tt, E) in enumerate(L):
    h = Hyp(E, range(n0))
    if h.maxdeg() > 3: continue
    cnt += 1
    nc, bc = nc_info(h)
    for tr, ise in bc:
        if ise: continue
        ds = tuple(h.deg[u] for u in tr)
        sg = tuple(int(frozenset(p) in h.sig) for p in combinations(tr, 2))
        key = (tuple(sorted(ds)), tuple(sorted(sg)))
        types[key] = types.get(key, 0) + 1
        if shown < maxshow:
            shown += 1
            print('class', k, 'E', E, 'triple', tr, 'deg', ds, 'sig(ab,ac,bc)', sg, flush=True)
print((n, m, t), 'slack', 3*n+2*m-11*t, 'classes(D<=3)', cnt, 'non-edge b-conf types', types, 'time %.1f' % (time.time()-t0))
