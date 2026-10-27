"""Proposition 6 of L020 on the stored near-tight lists (own code): NC pairs, slack identity, tight decomposition.
Usage: python3 prop6_check.py cell files..."""
import sys, itertools, time
from ref4 import *
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
types = {}
total_nc = 0; fails = 0; graphs = 0
t0 = time.time()
for fn in sys.argv[1:]:
    recs = parse_cell_file(I + fn)
    ncls = 0; nc_classes = 0
    for (n, m, t_stored, edges) in recs:
        verts = set().union(*map(set, edges))
        assert len(verts) == n, (fn, n, len(verts))
        deg = degrees(edges, verts)
        if max(deg.values()) > 3: continue
        ncls += 1; graphs += 1
        tK = tau(edges); assert tK == t_stored, (fn, tK, t_stored)
        sK = slack(n, m, tK); assert 0 <= sK <= 1, (fn, sK)
        comps, iso = components(edges, verts); assert len(comps) == 1 and not iso
        assert in_C(edges, verts), fn
        has_nc = False
        low = [v for v in verts if deg[v] <= 2]
        for x, y in itertools.combinations(sorted(low), 2):
            Hxy = induced(edges, {x, y}); txy = tau(Hxy)
            if txy == tK - 2: continue   # co-transversal
            has_nc = True; total_nc += 1
            sigma = 1 if any({x, y} <= set(e) for e in edges) else 0
            bd = deg[x] + deg[y] - sigma
            typ = (min(deg[x], deg[y]), max(deg[x], deg[y]), sigma)
            types[typ] = types.get(typ, 0) + 1
            ok = (txy == tK - 1)
            sxy = slack(n - 2, m - bd, txy)
            ok &= (sxy == sK + 5 - 2*bd) and sxy >= 0
            if deg[x] == 2 and deg[y] == 2:
                ok &= (sigma == 1 and sK == 1)
                cs, iso2 = components(Hxy, verts - {x, y})
                parts = len(cs) + len(iso2)
                ok &= parts <= 5
                for (vs, es) in cs:
                    tF = tau(es); ok &= (slack(len(vs), len(es), tF) == 0) and max(degrees(es, vs).values()) <= 3
                ok &= (len(iso2) == 0)   # an isolated vertex has slack 3, so none can occur in a slack-0 remainder
            if not ok:
                fails += 1; print('FAIL', fn, x, y, typ, txy, sxy)
        nc_classes += has_nc
    print(f'{fn}: Delta<=3 classes {ncls}, with an NC pair {nc_classes}  ({time.time()-t0:.0f}s)', flush=True)
print('graphs', graphs, 'NC pairs', total_nc, 'types', dict(sorted(types.items())), 'FAILS', fails)
