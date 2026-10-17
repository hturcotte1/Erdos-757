"""Referee L012 round 3: closure test on the 699 route-4 classes.  For every class H and EVERY vertex v of degree 4, the components of
H - v (connected cells plus isolated vertices) must form one of the four decompositions of (22,17) slack 1 and each component must be
isomorphic (igraph BLISS form) to a representative of the corresponding D4 cell list; also tau(H - v) = 9 is re-checked by brute force
(by the C tool chk afterwards).  Usage: python3 closure.py r4_699.txt celldir"""
import sys, re, itertools
from itertools import combinations
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L012-round3/src')
from iso_check import canon_igraph, parse
fn, celldir = sys.argv[1], sys.argv[2]
cells = {}
for typ in [(22, 17, 9), (19, 16, 8), (12, 10, 5), (10, 7, 4), (14, 12, 6), (8, 5, 3), (3, 1, 1)]:
    reps = parse('%s/cell_%d_%d_%d_D4.txt' % (celldir, *typ))
    cells[typ] = set(canon_igraph(e, typ[0]) for e in reps)
    assert len(cells[typ]) == len(reps)
decs = set([((3, 1, 1), (19, 16, 8)), ((8, 5, 3), (14, 12, 6)), ((10, 7, 4), (12, 10, 5)), ((22, 17, 9),)])
def tau_is(n, edges, t):
    masks = [sum(1 << v for v in e) for e in edges]
    def has(k): return any(all(mk & sum(1 << v for v in S) for mk in masks) for S in combinations(range(n), k))
    return (not has(t - 1)) and has(t)
G = parse(fn); ndel = 0; ncomp = 0; bad = 0; dec_count = {}; hv_lines = []
for H in G:
    deg = [0] * 23
    for e in H:
        for v in e: deg[v] += 1
    for v in range(23):
        if deg[v] != 4: continue
        ndel += 1
        Ev = [e for e in H if v not in e]; verts = [u for u in range(23) if u != v]
        # components by union-find over the 22 remaining vertices
        par = {u: u for u in verts}
        def f(x):
            while par[x] != x: x = par[x]
            return x
        for e in Ev:
            for u in e[1:]: par[f(u)] = f(e[0])
        comps = {}
        for u in verts: comps.setdefault(f(u), []).append(u)
        types = []
        for cv in comps.values():
            cv = sorted(cv); rel = {u: i for i, u in enumerate(cv)}; ce = [tuple(sorted(rel[u] for u in e)) for e in Ev if e[0] in rel]
            n_, m_ = len(cv), len(ce)
            if (n_, m_) == (1, 0): types.append((1, 0, 0)); continue
            typ = [t for t in cells if (t[0], t[1]) == (n_, m_)]
            if not typ: bad += 1; print('component type not in lists', (n_, m_)); continue
            typ = typ[0]; types.append(typ); ncomp += 1
            if canon_igraph(ce, n_) not in cells[typ]: bad += 1; print('component not isomorphic to any representative of', typ)
        tt = tuple(sorted(types))
        if tt not in decs: bad += 1; print('decomposition not among the four:', tt)
        dec_count[tt] = dec_count.get(tt, 0) + 1
        hv_lines.append('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in Ev))
print('classes', len(G), 'degree-4 deletions', ndel, 'components checked', ncomp, 'failures', bad)
print('decompositions met:', dec_count)
open('out/closure_Hv.txt', 'w').write('\n'.join(hv_lines) + '\n')
print('H - v graphs written to out/closure_Hv.txt (tau(H - v) = 9 is checked with chk 22 9)')
