"""Theorem 3 of L020 on a random sample of degree-3 vertices of stored near-tight graphs (own code).
Checks (i) tau drop 1 / slack +2 / no pair inside an edge of G, (ii) |Y|<=1 and the slack bookkeeping,
(iv)/(v) r bounds and the stated configuration conditions. Usage: python3 thm3_sample.py SEED COUNT"""
import sys, random, itertools, time
from ref4 import *
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
random.seed(int(sys.argv[1])); COUNT = int(sys.argv[2])
pool = []
for fn in ['cell_10_7_4.txt','cell_8_5_3.txt','cell_12_10_5.txt','cell_15_11_6.txt','cell_19_16_8.txt','cell_22_17_9.txt','cell_26_22_11.txt','cell_14_12_6.txt','cell_17_13_7.txt']:
    for idx,(n,m,t,edges) in enumerate(parse_cell_file(I+fn)):
        verts = set().union(*map(set,edges)); deg = degrees(edges, verts)
        if max(deg.values()) > 3: continue
        for v in verts:
            if deg[v] == 3: pool.append((fn, idx, v))
print('degree-3 instances in the pool:', len(pool))
STRAT = len(sys.argv) > 3
if STRAT:
    byshape = {}
    for (fn, idx, v) in pool:
        n, m, t, edges = parse_cell_file(I+fn)[idx]
        verts = set().union(*map(set, edges)); G = induced(edges, {v}); comps, iso = components(G, verts - {v})
        ev = [e for e in edges if v in e]; pairs = [tuple(sorted(set(e)-{v})) for e in ev]
        def L(x):
            for i,(vs,es) in enumerate(comps):
                if x in vs: return i
            return None
        shape = (len(comps), len(iso), tuple(sorted(tuple(sorted({L(x) for x in P if L(x) is not None})) for P in pairs)))
        byshape.setdefault(shape, []).append((fn, idx, v))
    print('shapes:', {k: len(w) for k, w in byshape.items()})
    sample = []
    for k, w in byshape.items(): sample += random.sample(w, min(COUNT, len(w)))
else:
    sample = random.sample(pool, COUNT)
hist = {}; fails = 0; t0 = time.time()
for (fn, idx, v) in sample:
    n, m, t_stored, edges = parse_cell_file(I+fn)[idx]
    verts = set().union(*map(set,edges)); deg = degrees(edges, verts)
    tK = tau(edges); assert tK == t_stored; sK = slack(n, m, tK)
    ev = [e for e in edges if v in e]; pairs = [tuple(sorted(set(e)-{v})) for e in ev]
    G = induced(edges, {v}); comps, iso = components(G, verts - {v})
    ok = True
    # (i)
    cov = [x for P in pairs for x in P]; ok &= len(set(cov)) == 6
    ok &= all(not any(set(P) <= set(e) for e in G) for P in pairs)
    cinfo = [(len(vs), len(es), tau(es)) for (vs, es) in comps]
    tG = sum(c[2] for c in cinfo); ok &= (tG == tK - 1)
    sG = sum(slack(*c) for c in cinfo) + 3*len(iso); ok &= (sG == sK + 2)
    # (ii)
    ok &= len(iso) <= 1 and iso == {x for x in cov if deg[x] == 1}
    if iso: ok &= (sK == 1) and all(slack(*c) == 0 for c in cinfo)
    for (vs, es), c in zip(comps, cinfo):
        ok &= in_C(es, vs) and max(degrees(es, vs).values()) <= 3 and 0 <= slack(*c) <= 3
        ok &= any(x in vs for x in cov)
        # free choice
        ok &= all(cotransversal(es, vs, {x}, c[2]) for x in vs)
    r = len(comps)
    def loc(x):
        for i,(vs,es) in enumerate(comps):
            if x in vs: return i
        return None   # isolated
    dist = [tuple(sorted({loc(x) for x in pairs[j] if loc(x) is not None})) for j in range(3)]
    if not iso:
        ok &= r <= 2
        if r == 1: pat = 'a'
        else:
            inside = [d[0] for d in dist if len(d) == 1]
            nsplit = 3 - len(inside)
            ok &= len(set(inside)) == len(inside)      # no two pairs in one component
            if nsplit == 3:
                pat = 'b'
                for i in range(2):
                    vs, es = comps[i]; side = [x for x in cov if x in vs]; ok &= len(side) == 3
                    for x, y in itertools.combinations(side, 2): ok &= not cotransversal(es, vs, {x,y}, cinfo[i][2])
            elif nsplit == 1:
                pat = 'e'
                sp = [P for P,d in zip(pairs,dist) if len(d) == 2][0]
                for i in range(2):
                    vs, es = comps[i]; Pin = [P for P,d in zip(pairs,dist) if d == (i,)][0]
                    z = [x for x in sp if x in vs][0]
                    for x in Pin: ok &= not cotransversal(es, vs, {z,x}, cinfo[i][2])
            else:
                pat = 'f'
                i1 = inside[0]; i2 = 1 - i1; vs1, es1 = comps[i1]; vs2, es2 = comps[i2]
                P1 = [P for P,d in zip(pairs,dist) if d == (i1,)][0]
                ce = [x for P,d in zip(pairs,dist) if len(d) == 2 for x in P if x in vs1]
                df = [x for P,d in zip(pairs,dist) if len(d) == 2 for x in P if x in vs2]
                for x in P1:
                    for y in ce: ok &= not cotransversal(es1, vs1, {x,y}, cinfo[i1][2])
                ok &= not cotransversal(es2, vs2, set(df), cinfo[i2][2])
                w = 10**6; Fp = es1 + [tuple(sorted((w,)+P1)), tuple(sorted((w,)+tuple(ce)))]
                ok &= not in_C(Fp, vs1 | {w})
    else:
        ok &= r <= 3
        y = next(iter(iso)); P3 = [P for P in pairs if y in P][0]; f = [x for x in P3 if x != y][0]
        ok &= deg[f] in (2, 3)
        others = [P for P in pairs if P != P3]
        jf = loc(f); Ff_vs, Ff_es = comps[jf]; tFf = cinfo[jf][2]
        def nc(j, x, z): return not cotransversal(comps[j][1], comps[j][0], {x, z}, cinfo[j][2])
        kinds = []
        for P in others:
            ls = {loc(x) for x in P}
            kinds.append(('in', next(iter(ls))) if len(ls) == 1 else ('split', tuple(sorted(ls))))
        if r == 1:
            pat = 'i1'
        elif r == 2:
            k1, k2 = kinds
            if k1[0] == 'in' and k2[0] == 'in':
                ok &= k1[1] != k2[1]
                Pin = others[0] if k1[1] == jf else others[1]      # the pair inside the component of f
                pat = 'i2-1'; ok &= all(nc(jf, x, f) for x in Pin)
            elif (k1[0] == 'in') != (k2[0] == 'in'):
                Pin, Psp = (others[0], others[1]) if k1[0] == 'in' else (others[1], others[0])
                jin = loc(Pin[0])
                if jin == jf:
                    pat = 'i2-2'; ok &= all(nc(jf, x, f) for x in Pin)
                else:
                    pat = 'i2-3'
                    c = [x for x in Psp if loc(x) == jin][0]; d = [x for x in Psp if loc(x) == jf][0]
                    ok &= all(nc(jin, x, c) for x in Pin) and nc(jf, d, f)
            else:
                pat = 'i2-4'
                acs = [x for P in others for x in P if loc(x) == jf]; bds = [x for P in others for x in P if loc(x) != jf]
                ok &= len(acs) == 2 and len(bds) == 2
                ok &= all(nc(jf, x, f) for x in acs) and nc(loc(bds[0]), bds[0], bds[1])
        else:
            pat = 'i3'
            pin = [P for P, k in zip(others, kinds) if k == ('in', jf)]
            spl = [P for P, k in zip(others, kinds) if k[0] == 'split' and jf not in k[1]]
            ok &= len(pin) == 1 and len(spl) == 1
            if pin: ok &= all(nc(jf, x, f) for x in pin[0])
    hist[pat] = hist.get(pat, 0) + 1
    if not ok: fails += 1
    print(f'{fn} class {idx} v={v}: pattern {pat}, components {cinfo}, iso {sorted(iso)} -> {"OK" if ok else "FAIL"}', flush=True)
print('histogram', hist, 'FAILS', fails, f'({time.time()-t0:.0f}s)')
