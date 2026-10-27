"""Referee #1 (L021): Theorem 7(v).
(a) role counts of L017 Theorem 4(iv) for the 32 pieces, from brute-force minimum transversals; strict version
    (pairs used as traces not inside an edge) and a conservative version (no such restriction);
(b) direct brute force, without the pattern analysis, for G = F1 + F2 (disjoint) over pieces with <= MAXN vertices:
    every vertex v with three edges {v} u P_j (pairwise disjoint pairs of vertices of G-degree <= 2, no pair inside an
    edge of G; all distributions, including the one leaving a component unmet): is tau(H) = tau(G)+1 ? if so, is H in
    C_3, and is H isomorphic to a piece?"""
import os, sys, json, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcore import *
HERE = os.path.dirname(os.path.abspath(__file__))
MAXN = int(sys.argv[1]) if len(sys.argv) > 1 else 10
src = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']
pcs = []
for p in src:
    e = [tuple(x) for x in p['edges']]; n = nv(e)
    t, T = min_transversals_bf(n, e)
    pcs.append(dict(name=p['name'], n=n, e=e, t=t, T=T, deg=degrees(n, e)))
def co(T, x, y): return any((t >> x) & 1 and (t >> y) & 1 for t in T)
def meets(T, S): return [t for t in T if any((t >> x) & 1 for x in S)]
for P in []:
    n, e, T, deg = P['n'], P['e'], P['T'], P['deg']
    att = [x for x in range(n) if deg[x] <= 2]
    inside = lambda a, b: any(a in f and b in f for f in e)
    allpairs = list(itertools.combinations(att, 2))
    res = {}
    for mode in ('strict', 'cons'):
        pairs = [q for q in allpairs if mode == 'cons' or not inside(*q)]
        rb = sum(1 for x, y, z in itertools.combinations(att, 3) if not co(T, x, y) and not co(T, x, z) and not co(T, y, z))
        rc = sum(1 for p1, p2 in itertools.combinations(pairs, 2) if not set(p1) & set(p2)
                 and not any(co(T, x, y) for x in p1 for y in p2))
        re_ = sum(1 for p1 in pairs for z in att if z not in p1 and not co(T, p1[0], z) and not co(T, p1[1], z))
        rf = sum(1 for p1 in pairs for c, d in itertools.combinations([x for x in att if x not in p1], 2)
                 if not any(co(T, x, y) for x in p1 for y in (c, d)))
        res[mode] = (rb, rc, re_, rf)
    print(P['name'], 'strict b,c,e,f1 =', res['strict'], ' conservative =', res['cons'])
# (b)
print('(b) direct brute force over pairs of pieces with <=', MAXN, 'vertices')
small = [P for P in pcs if P['n'] <= MAXN]
import random as _r
big = [P for P in pcs if P['name'] in ('(15,11,6)#0','(15,11,6)#11','(17,13,7)#0','(17,13,7)#4')]
PAIRS = [(pcs[i], pcs[j]) for i in range(len(pcs)) for j in range(i, len(pcs))]
canon = {}
def same_as_piece(n, e):
    G = incidence(n, e)
    for P in pcs:
        if P['n'] == n and len(P['e']) == len(e) and nx.is_isomorphic(G, incidence(P['n'], P['e']), node_match=lambda a, b: a['t'] == b['t']):
            return P['name']
    return None
tot_raise = 0; tot_raise_C3 = 0; bad = []
for (F1, F2) in PAIRS:
    if True:
        n1 = F1['n']; n = n1 + F2['n']
        e = list(F1['e']) + [tuple(x + n1 for x in f) for f in F2['e']]
        deg = degrees(n, e)
        TG = [t1 | (t2 << n1) for t1 in F1['T'] for t2 in F2['T']]
        att = [x for x in range(n) if deg[x] <= 2]
        inside = set()
        for f in e:
            for q in itertools.combinations(sorted(f), 2): inside.add(q)
        pairs = [q for q in itertools.combinations(att, 2) if q not in inside]
        pm = {q: sum(1 << k for k, t in enumerate(TG) if (t >> q[0]) & 1 or (t >> q[1]) & 1) for q in pairs}
        nraise = 0; nC3 = 0; nconf = 0
        for a in range(len(pairs)):
            pa = pairs[a]; ma = pm[pa]
            for b in range(a + 1, len(pairs)):
                pb = pairs[b]
                if set(pa) & set(pb): continue
                mab = ma & pm[pb]
                for c in range(b + 1, len(pairs)):
                    pc = pairs[c]
                    if set(pc) & (set(pa) | set(pb)): continue
                    nconf += 1
                    if mab & pm[pc]: continue
                    nraise += 1
                    v = n
                    H = e + [(v,) + pa, (v,) + pb, (v,) + pc]
                    H = [tuple(x) for x in H]
                    if max(degrees(n + 1, H)) <= 3 and in_C(n + 1, H):
                        nC3 += 1
                        assert tau_ilp(n + 1, H) == F1['t'] + F2['t'] + 1
                        nm = same_as_piece(n + 1, H) if connected(n + 1, H) else None
                        if nm is None: bad.append((F1['name'], F2['name'], pa, pb, pc))
        tot_raise += nraise; tot_raise_C3 += nC3
        print(F1['name'], '+', F2['name'], 'configs', nconf, 'tau-raising', nraise, 'in C_3', nC3, flush=True)
print('total tau-raising', tot_raise, 'in C_3', tot_raise_C3, 'NOT isomorphic to a piece:', len(bad), bad[:5])
