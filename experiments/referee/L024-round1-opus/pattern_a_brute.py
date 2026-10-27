"""Brute-force completeness cross-check of pattern_a_ref.py on the small type triples:
all g (or g-orbit representatives), ALL triples of pairwise disjoint admissible pairs, Claim B tested directly against
all triples of minimum transversals (no restriction to candidates, no maximality reduction, no branching).
usage: python3 pattern_a_brute.py <maxn> [--all-g]
"""
import sys, time
from itertools import combinations, product
import pattern_a_ref as R
from rlib import degs

maxn = int(sys.argv[1])
all_g = '--all-g' in sys.argv
t0 = time.time()
TL = R.type_list('poor') + R.type_list('rich10')
tot = 0
for types in TL:
    types = list(types)
    n = 1 + sum(R.P[x][0] for x in types)
    if n > maxn:
        continue
    offs, Eall, nG = [], [], 0
    for nm in types:
        nn, E = R.P[nm]
        offs.append(nG)
        Eall += [tuple(x + nG for x in e) for e in E]
        nG += nn
    mts = [[T << offs[i] for T in R.MT[nm][1]] for i, nm in enumerate(types)]
    unions = [a | b | c for a in mts[0] for b in mts[1] for c in mts[2]]
    dF = [degs(*R.P[nm]) for nm in types]
    gc = []
    for i, nm in enumerate(types):
        if all_g:
            reps = [x for x in range(R.P[nm][0]) if dF[i][x] <= 2]
        else:
            reps = [o[0] for o in R.orbits(nm) if dF[i][o[0]] <= 2]
        gc.append([x + offs[i] for x in reps])
    cnt = 0
    for g in product(*gc):
        gE = tuple(sorted(g))
        gm = sum(1 << x for x in gE)
        EG = Eall + [gE]
        d = degs(nG, EG)
        inedge = set(p for e in EG for p in combinations(e, 2))
        pairs = [(a, b) for a, b in combinations(range(nG), 2) if d[a] <= 2 and d[b] <= 2 and (a, b) not in inedge]
        pm = [(1 << a) | (1 << b) for a, b in pairs]
        Ug = [u for u in unions if u & gm]
        for i, j, k in combinations(range(len(pairs)), 3):
            if pm[i] & pm[j] or pm[i] & pm[k] or pm[j] & pm[k]:
                continue
            a, b, c = pm[i], pm[j], pm[k]
            ok = True
            for u in Ug:
                if (u & a) and (u & b) and (u & c):
                    ok = False
                    break
            if ok:
                cnt += 1
    tot += cnt
    print(n, types, 'brute configs', cnt, 'elapsed %.0f' % (time.time() - t0), flush=True)
print('BRUTE TOTAL', tot)
