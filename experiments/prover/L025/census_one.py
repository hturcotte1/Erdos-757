import sys, time
from census import *
n, m, t = map(int, sys.argv[1:4])
L = load_cell(n, m, t)
t0 = time.time()
cnt = 0; ncnt = {}; bc_ne = 0; bc_e = 0
for k, (n0, m0, t0_, E) in enumerate(L):
    h = Hyp(E, range(n0))
    if h.maxdeg() > 3: continue
    assert h.tau() == t0_
    cnt += 1
    nc, bc = nc_info(h)
    for p in nc:
        x, y = sorted(p, key=lambda u: h.deg[u])
        key = (h.deg[x], h.deg[y], int(p in h.sig))
        ncnt[key] = ncnt.get(key, 0) + 1
    for tr, ise in bc:
        if ise: bc_e += 1
        else: bc_ne += 1
print((n, m, t), 'classes(D<=3)', cnt, 'NC types', dict(sorted(ncnt.items())), 'b-conf non-edge', bc_ne, 'edge', bc_e, 'time %.1f' % (time.time() - t0), flush=True)
