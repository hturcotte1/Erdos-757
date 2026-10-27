"""Per-class pattern profile of the 45 classes of L020 Theorem 1 (own code), plus tau and degree checks.
Usage: python3 patterns45.py K29_classes.json [start end]"""
import sys, json, itertools, time
from ref4 import *

data = json.load(open(sys.argv[1]))
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3]) if len(sys.argv) > 3 else len(data)
tot = {'a':0,'b':0,'e':0,'f':0,'c':0,'d':0,'i':0}
flags = {'e_8_20':0, 'f_10_18':0, 'b_3_25':0, 'theta3':0, 'theta_any':0}
cond_fail = 0
t0 = time.time()
for ci in range(lo, hi):
    rec = data[ci]
    edges = [tuple(sorted(e)) for e in rec['edges']]
    verts = set(range(29))
    assert set().union(*map(set, edges)) == verts and len(edges) == 23
    assert is_linear(edges)
    deg = degrees(edges, verts)
    assert sorted(deg.values()).count(2) == 18 and sorted(deg.values()).count(3) == 11
    tK = tau(edges); assert tK == 12, (ci, tK)
    sK = slack(29, 23, tK); assert sK == 1
    prof = {'a':0,'b':0,'e':0,'f':0,'c':0,'d':0,'i':0}
    cells_e = []; cells_f = []; cells_b = []
    for v in sorted(verts):
        if deg[v] != 3: continue
        ev = [e for e in edges if v in e]
        pairs = [tuple(sorted(set(e) - {v})) for e in ev]
        G = induced(edges, {v})
        comps, iso = components(G, verts - {v})
        # no pair inside an edge of G
        for P in pairs:
            assert not any(set(P) <= set(e) for e in G)
        cinfo = []
        for (vs, es) in comps:
            tF = tau(es); cinfo.append((len(vs), len(es), tF, slack(len(vs), len(es), tF), vs, es))
        tG = sum(c[2] for c in cinfo)
        assert tG == tK - 1, (ci, v, tG)
        assert sum(c[3] for c in cinfo) + 3*len(iso) == sK + 2
        r = len(comps)
        if iso:
            prof['i'] += 1; continue
        def loc(x):
            for i,(vs,es) in enumerate(comps):
                if x in vs: return i
            raise AssertionError
        dist = [tuple(sorted({loc(x) for x in P})) for P in pairs]
        nsplit = sum(1 for d in dist if len(d) == 2)
        if r == 1:
            prof['a'] += 1; continue
        if r >= 3:
            prof['d'] += 1; continue
        # r == 2
        inside = [d[0] for d in dist if len(d) == 1]
        if len(set(inside)) < len(inside):
            prof['c'] += 1; continue
        cellpair = tuple(sorted((c[0], c[1], c[2]) for c in cinfo))
        if nsplit == 3:
            prof['b'] += 1; cells_b.append(cellpair)
            # condition: the three vertices on each side pairwise NC
            ok = True
            for i in range(2):
                vs, es = comps[i]; tF = cinfo[i][2]
                side = [x for P in pairs for x in P if x in vs]
                assert len(side) == 3
                for x, y in itertools.combinations(side, 2):
                    if cotransversal(es, vs, {x, y}, tF): ok = False
            if not ok: cond_fail += 1; print('COND FAIL (b)', ci, v)
        elif nsplit == 1:
            prof['e'] += 1; cells_e.append(cellpair)
            # condition: e-configurations on both sides
            sp = [P for P,d in zip(pairs,dist) if len(d) == 2][0]
            ok = True
            for i in range(2):
                vs, es = comps[i]; tF = cinfo[i][2]
                Pin = [P for P,d in zip(pairs,dist) if d == (i,)][0]
                z = [x for x in sp if x in vs][0]
                for x in Pin:
                    if cotransversal(es, vs, {z, x}, tF): ok = False
                if any(set(Pin) <= set(e) for e in es): ok = False
            if not ok: cond_fail += 1; print('COND FAIL (e)', ci, v)
        elif nsplit == 2:
            prof['f'] += 1; cells_f.append(cellpair)
            i1 = inside[0]; i2 = 1 - i1
            vs1, es1 = comps[i1]; vs2, es2 = comps[i2]
            P1 = [P for P,d in zip(pairs,dist) if d == (i1,)][0]
            splits = [P for P,d in zip(pairs,dist) if len(d) == 2]
            ce = [x for P in splits for x in P if x in vs1]
            df = [x for P in splits for x in P if x in vs2]
            assert len(ce) == 2 and len(df) == 2
            ok = True
            for x in P1:
                for y in ce:
                    if cotransversal(es1, vs1, {x, y}, cinfo[i1][2]): ok = False
            if cotransversal(es2, vs2, set(df), cinfo[i2][2]): ok = False
            # F1 + w(P1, {c,e}) not in C
            w = 100
            Fplus = es1 + [tuple(sorted((w,) + tuple(P1))), tuple(sorted((w,) + tuple(ce)))]
            if in_C(Fplus, vs1 | {w}): ok = False
            if not ok: cond_fail += 1; print('COND FAIL (f)', ci, v)
            # Theta = (6,3,2) f-side + (22,17,9)
            c1 = (len(vs1), len(es1), cinfo[i1][2]); c2 = (len(vs2), len(es2), cinfo[i2][2])
            if c1 == (6,3,2) and c2 == (22,17,9): prof.setdefault('theta', 0); prof['theta'] = prof.get('theta',0) + 1
            if c1 == (18,13,7) and c2 == (10,7,4): prof['f1018'] = prof.get('f1018',0) + 1
    has_e = any(cp == ((8,5,3),(20,15,8)) for cp in cells_e)
    has_b = any(cp == ((3,1,1),(25,19,10)) for cp in cells_b)
    th = prof.get('theta', 0); f1018 = prof.get('f1018', 0)
    flags['e_8_20'] += has_e; flags['b_3_25'] += has_b; flags['f_10_18'] += (f1018 > 0)
    flags['theta3'] += (th == 3); flags['theta_any'] += (th > 0)
    for k in tot: tot[k] += prof[k]
    print(f"class {ci}: patterns a={prof['a']} b={prof['b']} e={prof['e']} f={prof['f']} c={prof['c']} d={prof['d']} i={prof['i']} | e-cells {sorted(set(cells_e))} | b-cells {sorted(set(cells_b))} | f-cells {sorted(set(cells_f))} | theta={th} f(10,7,4)+(18,13,7)={f1018} | {time.time()-t0:.0f}s", flush=True)
print('TOTAL patterns', tot)
print('FLAGS (classes with): pattern-(e) (8,5,3)+(20,15,8):', flags['e_8_20'], '| pattern-(f) (10,7,4)+(18,13,7):', flags['f_10_18'], '| pattern-(b) E1+(25,19,10):', flags['b_3_25'], '| exactly 3 theta-vertices:', flags['theta3'], '| >=1 theta:', flags['theta_any'])
print('condition failures:', cond_fail)
