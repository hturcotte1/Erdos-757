#!/usr/bin/env python3
"""Generalised hub: replace E_1 by any L* piece F.  H = G' + F + v + edges {v,q_i,g_i}, q_i distinct low-degree (deg<=2) vertices of F,
g_i distinct low-degree vertices of G'.  tau(H) = tau(G')+tau(F)+1 iff for every S subset of {1,2,3} with q_S inside a min transversal of F,
no min transversal of G' contains g_{complement of S}.  (Derived in this script's header; every kept H is re-checked: tau(H) is computed by
two solvers and must equal tau(G')+tau(F)+1.)   usage: fhub.py OUT.jsonl cell1 cell2 ... (cells 'n,m,t')"""
import sys, json, time, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hubs, kt
from hubs import popc
inv = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory.json')))
out = open(sys.argv[1], 'a')
want = set(tuple(map(int, k.split(','))) for k in sys.argv[2:])
# per-piece data
PD = []
for P in hubs.PIECES:
    em = kt.masks(P.edges)
    T = kt.min_transversals(em, P.tau)
    low = [x for x in range(P.n) if P.deg[x] <= 2]
    def cot(mask): return any((t & mask) == mask for t in T)
    trip = []
    for q in itertools.combinations(low, 3):
        if frozenset(q) in set(frozenset(e) for e in P.edges): pass   # q inside an edge of F is allowed (only the v-edges matter)
        qm = [1 << x for x in q]
        S_ok = {}
        for r in range(4):
            for S in itertools.combinations(range(3), r):
                mk = 0
                for i in S: mk |= qm[i]
                S_ok[S] = cot(mk)
        if S_ok[(0, 1, 2)]: continue          # all three in a min transversal of F: tau(H) = tau+tau_F
        forb = []                                    # forbidden co-transversal index sets U (subsets of {0,1,2} of g indices)
        for S, ok in S_ok.items():
            if ok:
                forb.append(tuple(i for i in range(3) if i not in S))
        # keep minimal ones
        forb = [u for u in forb if not any(set(w) < set(u) for w in forb)]
        trip.append((q, forb))
    PD.append((P, T, trip))
reg = hubs.Registry()
stats = dict(pieces=len(PD), G=0, pairs=0, built=0, inC=0, newclasses=0, minP=None, hits=0)
t0 = time.time()
for ck in sorted(inv, key=lambda k: eval(k)):
    n0, m0, t_ = eval(ck)
    if (n0, m0, t_) not in want: continue
    info = inv[ck]
    for g in [g for g in kt.read_cell(info['file'])]:
        n = kt.nverts(g)
        if max(hubs.degs(n, g)) > 3: continue
        d = hubs.degs(n, g)
        A0 = kt.A_value(n, len(g), t_)
        T1 = kt.min_transversals(kt.masks(g), t_)
        low = [x for x in range(n) if d[x] <= 2]
        def cot(mask): return any((t & mask) == mask for t in T1)
        stats['G'] += 1
        for (P, TF, trip) in PD:
            if A0 - (-P.W) - 0 >= 0 and A0 - P.W >= 0: continue   # need A(H) = A(G')-W(F) < 0
            for (q, forb) in trip:
                for gs in itertools.permutations(low, 3):
                    if any(cot(sum(1 << gs[i] for i in u)) for u in forb if len(u) > 0): continue
                    if () in forb: continue
                    stats['pairs'] += 1
                    nF = P.n
                    # build H: G' on 0..n-1, F on n..n+nF-1, v = n+nF
                    v = n + nF
                    E = list(g) + [tuple(n + x for x in e) for e in P.edges] + [(v, n + q[i], gs[i]) for i in range(3)]
                    nH = v + 1
                    stats['built'] += 1
                    rec, new = reg.lookup(nH, E)
                    if not new: continue
                    stats['newclasses'] += 1
                    if max(hubs.degs(nH, E)) > 3: continue
                    r = hubs.analyse_H(nH, E, t_ + P.tau + 1)
                    if not r['inC']: continue
                    stats['inC'] += 1
                    if stats['minP'] is None or r['P'] < stats['minP']: stats['minP'] = r['P']
                    out.write(json.dumps(dict(type='FH', cell=ck, F=P.name, q=q, g=gs, G=g, **r, H=E)) + '\n'); out.flush()
                    if r['P'] < 0 or (r['piece'] is None and r['Pp'] < 0):
                        stats['hits'] += 1; print('HIT', ck, P.name, q, gs, r, E, flush=True)
    print(ck, stats, '[%.0fs]' % (time.time() - t0), flush=True)
json.dump(stats, open(sys.argv[1] + '.stats.json', 'w'))
