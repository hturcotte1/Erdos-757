"""W2 case (delta): H covered by v and the pieces F_v = P1, F_w = P2 (v in P2, d_{P2}(v) = 2), F_{w'} = P3 (v in P3, d_{P3}(v) = 2),
w != w' in P1 with d_{P1}(w) = d_{P1}(w') = 2 (co-vertices of v on different edges: e_j contains w, e_k contains w', e_l the third).
Construction (complete, see README): H - v = P1 + D-components; P2 is placed at a new vertex v: every component of P2 - v is either
F-type (isomorphic to a component of P1 - w, identified with it) or D-type (new component); P3 is then placed at v: every component of
P3 - v is F-type (iso to a component of P1 - w'), D-type identified with an existing D component (iso), or new.
All structural requirements are re-verified on the final H.  P1,P2,P3 range over all pieces with >= 8 vertices (rich included).
n <= 46 and n >= 25 are not imposed in the enumeration; counts by n are reported.
usage: python3 w2_delta.py [p1index_start p1index_end]"""
import sys, itertools, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from w2lib import *
t0 = time.time()
pieces = load_pieces()
big = [P for P in pieces if P['n'] >= 8]
lo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
hi = int(sys.argv[2]) if len(sys.argv) > 2 else len(big)

def inv(n, edges, S):
    E = inner_edges(edges, S)
    d = {x: 0 for x in S}
    for e in E:
        for x in e: d[x] += 1
    return (len(S), len(E), tuple(sorted(d.values())))

# precompute comps for every (piece, vertex)
CM_ = {}
for P in big:
    for x in range(P['n']):
        cs = comps_minus(P['n'], P['edges'], x)
        CM_[(P['name'], x)] = [(c, inv(P['n'], P['edges'], c)) for c in cs]

def place_options(Cx, targets_F, existingD, base_n, Pedges, E1_):
    """Cx: list of (comp, inv) of P - x.  targets_F: list of (comp K in P1-del, inv) -> F-type targets (vertex ids = P1 ids);
    existingD: list of (frozenset of H vertex ids, inv, edges list) -> D-type targets.
    Yields (assign) = list over comps of ('F', K_index, phi) / ('D', D_index, phi) / ('N',) with injective use of targets."""
    def rec(i, usedF, usedD):
        if i == len(Cx):
            yield []; return
        comp, iv = Cx[i]
        # F-type
        for ki, (K, kiv) in enumerate(targets_F):
            if ki in usedF or kiv != iv: continue
            yield_f = list(isos(Pedges, comp, E1_, K))
            for phi in yield_f:
                for rest in rec(i + 1, usedF | {ki}, usedD):
                    yield [('F', ki, phi)] + rest
        for di, (Dset, div, Dedges) in enumerate(existingD):
            if di in usedD or div != iv: continue
            for phi in isos(Pedges, comp, Dedges, Dset):
                for rest in rec(i + 1, usedF, usedD | {di}):
                    yield [('D', di, phi)] + rest
        for rest in rec(i + 1, usedF, usedD):
            yield [('N',)] + rest
    yield from rec(0, frozenset(), frozenset())

def gen_opts3(P1, w, w2, Dlist, E1, TF_w2):
    """all (P3, v3, Cx3, assign3) placements of a piece P3 at v (comps F-type onto comps of P1 - w', D-type onto Dlist, or new) with
    w in the image of the F-type comps and every edge at v3 meeting the F-type image."""
    for P3 in big:
        for v3 in range(P3['n']):
            if P3['deg'][v3] != 2: continue
            Cx3 = CM_[(P3['name'], v3)]
            for assign3 in place_options(Cx3, TF_w2, Dlist, P1['n'], P3['edges'], E1):
                Fimg = set()
                for (comp, iv), a in zip(Cx3, assign3):
                    if a[0] == 'F': Fimg |= set(a[2][x] for x in comp)
                if w not in Fimg: continue
                if not all(any(a[0] == 'F' and (x in comp) and (x in a[2]) for (comp, iv), a in zip(Cx3, assign3) for x in e if x != v3)
                           for e in P3['edges'] if v3 in e): continue
                yield (P3, v3, Cx3, assign3)

stats = dict(P1w=0, P2_placements=0, P3_placements=0, glue_candidates=0, struct_ok=0, n_le_46=0, n_ge_25_le_46=0, inC3=0, A_nonneg=0,
             A_neg=0, Pneg=0, inC3_n_ge_25=0, A_neg_n_ge_25=0)
byn = {}
out = []
seenH = set()

def edge_fsets(P, v, assign, Cx):
    """for each edge of P at v: frozenset of P1-ids of its F-type co-vertices (under the placement)."""
    img = {}
    for (comp, iv), a in zip(Cx, assign):
        if a[0] == 'F':
            for x in comp: img[x] = a[2][x]
    res = []
    for e in P['edges']:
        if v in e: res.append(frozenset(img[x] for x in e if x != v and x in img))
    return res

def p2_list(P1, w, TF_w, E1):
    n1 = P1['n']; res = []
    for P2 in big:
        for v2 in range(P2['n']):
            if P2['deg'][v2] != 2: continue
            Cx2 = CM_[(P2['name'], v2)]
            for assign2 in place_options(Cx2, TF_w, [], n1, P2['edges'], E1):
                mp = {v2: n1}; nxt = n1 + 1
                for (comp, iv), a in zip(Cx2, assign2):
                    if a[0] == 'F':
                        for x, y in a[2].items(): mp[x] = y
                    else:
                        for x in sorted(comp):
                            mp[x] = nxt; nxt += 1
                Fimg = {mp[x] for (comp, iv), a in zip(Cx2, assign2) if a[0] == 'F' for x in comp}
                e_v2 = [e for e in P2['edges'] if v2 in e]
                if not all(any(mp[x] in Fimg for x in e if x != v2) for e in e_v2): continue
                H2edges = set(E1) | set(tuple(sorted(mp[y] for y in e)) for e in P2['edges'])
                Dlist = []
                for (comp, iv), a in zip(Cx2, assign2):
                    if a[0] == 'N':
                        ids = frozenset(mp[x] for x in comp)
                        Dlist.append((ids, iv, [e for e in H2edges if all(y in ids for y in e)]))
                res.append(dict(P2=P2, v2=v2, Fimg=Fimg, mp=mp, nxt=nxt, H2edges=H2edges, V2=set(mp.values()), Dlist=Dlist,
                                fsets=edge_fsets(P2, v2, assign2, Cx2)))
    return res

def p3_raw(P1, w2, TF_w2, E1):
    res = []
    for P3 in big:
        for v3 in range(P3['n']):
            if P3['deg'][v3] != 2: continue
            Cx3 = CM_[(P3['name'], v3)]
            for assign3 in place_options(Cx3, TF_w2, [], P1['n'], P3['edges'], E1):
                Fimg = set()
                for (comp, iv), a in zip(Cx3, assign3):
                    if a[0] == 'F': Fimg |= set(a[2][x] for x in comp)
                if not all(any(a[0] == 'F' and (x in comp) for (comp, iv), a in zip(Cx3, assign3) for x in e if x != v3)
                           for e in P3['edges'] if v3 in e): continue
                res.append((P3, v3, Cx3, assign3, Fimg, edge_fsets(P3, v3, assign3, Cx3)))
    index = {}
    for i, r in enumerate(res):
        for fs in set(r[5]): index.setdefault(fs, []).append(i)
    return res, index

for P1 in big[lo:hi]:
    n1 = P1['n']; E1 = [tuple(e) for e in P1['edges']]
    low = [x for x in range(n1) if P1['deg'][x] == 2]
    P2cache = {w: p2_list(P1, w, CM_[(P1['name'], w)], E1) for w in low}
    P3cache = {w2: p3_raw(P1, w2, CM_[(P1['name'], w2)], E1) for w2 in low}
    for w in low:
        for w2 in low:
            if w2 == w: continue
            stats['P1w'] += 1
            TF_w2 = CM_[(P1['name'], w2)]
            raw3, idx3 = P3cache[w2]
            for o2 in P2cache[w]:
                if w2 not in o2['Fimg'] or w in o2['Fimg']: continue
                P2 = o2['P2']; v2 = o2['v2']; H2edges = o2['H2edges']; V2 = o2['V2']; H2n = o2['nxt']; Dlist = o2['Dlist']
                stats['P2_placements'] += 1
                if Dlist:
                    opts3 = [(P3, v3, Cx3, assign3) for (P3, v3, Cx3, assign3) in gen_opts3(P1, w, w2, Dlist, E1, TF_w2)]
                else:
                    cand_idx = set()
                    for fs in set(o2['fsets']): cand_idx.update(idx3.get(fs, ()))
                    opts3 = [(raw3[i][0], raw3[i][1], raw3[i][2], raw3[i][3]) for i in sorted(cand_idx) if w in raw3[i][4]]
                for (P3, v3, Cx3, assign3) in opts3:
                    stats['P3_placements'] += 1
                    mp3 = {v3: n1}; nx3 = H2n
                    for (comp, iv), a in zip(Cx3, assign3):
                        if a[0] in ('F', 'D'):
                            for x, y in a[2].items(): mp3[x] = y
                        else:
                            for x in sorted(comp):
                                mp3[x] = nx3; nx3 += 1
                    n = nx3
                    Eset = set(H2edges) | set(tuple(sorted(mp3[y] for y in e)) for e in P3['edges'])
                    E = sorted(Eset)
                    stats['glue_candidates'] += 1
                    V1 = set(range(n1)); V3 = set(mp3.values()); vv = n1
                    ev = [e for e in E if vv in e]
                    if len(ev) != 3: continue
                    ej = [e for e in ev if w in e]; ek = [e for e in ev if w2 in e]
                    if len(ej) != 1 or len(ek) != 1 or ej[0] == ek[0]: continue
                    el = [e for e in ev if e != ej[0] and e != ek[0]][0]
                    if w in ek[0] or w in el or w2 in ej[0] or w2 in el: continue
                    if w in V2 or w2 in V3: continue
                    if not all(any(y in V1 for y in e) for e in ev): continue
                    ok = (len(inner_edges(E, V1)) == P1['m'] and len(inner_edges(E, V2)) == P2['m']
                          and len(inner_edges(E, V3)) == P3['m'])
                    if not ok: continue
                    cv = comps_of(n, E, {vv}); cw = comps_of(n, E, {w}); cw2 = comps_of(n, E, {w2})
                    if frozenset(V1) not in cv or frozenset(V2) not in cw or frozenset(V3) not in cw2: continue
                    if (V1 | V2 | V3 | {vv}) != set(range(n)): continue
                    key = (n, tuple(E))
                    if key in seenH: continue
                    seenH.add(key)
                    stats['struct_ok'] += 1
                    if n > 46: continue
                    stats['n_le_46'] += 1
                    byn[n] = byn.get(n, 0) + 1
                    if n >= 25: stats['n_ge_25_le_46'] += 1
                    rec = dict(P1=P1['name'], w=w, w2=w2, P2=P2['name'], v2=v2, P3=P3['name'], v3=v3, edges=E)
                    before = stats['inC3']; beforeA = stats['A_neg']
                    p = evaluate(n, E, pieces, stats, 'delta', rec)
                    if stats['inC3'] > before:
                        if n >= 25: stats['inC3_n_ge_25'] += 1
                        if stats['A_neg'] > beforeA and n >= 25: stats['A_neg_n_ge_25'] += 1
                        out.append(rec)
                        if p is not None and p < 0: print('NEGATIVE P', rec, flush=True)
    print(P1['name'], 'done', stats, f'{time.time()-t0:.0f}s', flush=True)
    json.dump(dict(stats=stats, by_n=byn, configs=out, range=[lo, hi], version='delta2'),
              open(f'/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2/w2_delta2_results_{lo}_{hi}.json', 'w'))
print('TOTAL', stats, 'by_n', dict(sorted(byn.items())), f'{time.time()-t0:.0f}s')
