"""L020 Proposition 6 on every NC pair of the ten stored slack<=1 lists (Delta<=3, connected), own code.
Checks tau(K-x-y) = tau-1, s(K-x-y) = s+5-2|d(x,y)| computed from the actual (n,m,tau), >= 0, and for
d(x)=d(y)=2: sigma=1, s(K)=1, K-x-y = disjoint union of <=5 tight graphs (no isolated vertex), Delta<=3,
each component containing a vertex of an edge meeting {x,y}."""
from collections import Counter
from hgr2 import HG, parse_list, popc
from patt import slack
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
cells = ['cell_3_1_1', 'cell_8_5_3', 'cell_10_7_4', 'cell_12_10_5', 'cell_14_12_6', 'cell_15_11_6', 'cell_17_13_7',
         'cell_19_16_8', 'cell_22_17_9', 'cell_26_22_11']
types = Counter(); fails = []; ngr = 0; maxcomp = 0; comp_hist = Counter()
for c in cells:
    for gi, (n, m, t, E) in enumerate(parse_list(I + c + '.txt')):
        V = list(range(n)); K = HG(V, E)
        if max(K.deg(u) for u in V) > 3: continue
        comps, iso = K.components(V, K.full)
        if len(comps) != 1 or iso: continue
        ngr += 1
        tK = K.tau(); assert tK == t
        sK = slack(n, m, t); assert sK in (0, 1)
        low = [u for u in V if K.deg(u) <= 2]
        for i in range(len(low)):
            for j in range(i + 1, len(low)):
                x, y = low[i], low[j]
                em = K.mask_without((x, y))
                txy = K.tau_mask(em)
                if txy == tK - 2: continue  # co-transversal
                sigma = 1 if K.inc[x] & K.inc[y] else 0
                dx, dy = sorted((K.deg(x), K.deg(y)))
                types[(dx, dy, sigma)] += 1
                dpart = popc(K.inc[x] | K.inc[y])
                if dpart != dx + dy - sigma: fails.append(('partial', c, gi, x, y))
                if txy != tK - 1: fails.append(('tau', c, gi, x, y)); continue
                sxy = slack(n - 2, m - dpart, txy)
                if sxy != sK + 5 - 2 * dpart or sxy < 0: fails.append(('slack', c, gi, x, y))
                if (dx, dy) == (2, 2):
                    if sigma != 1 or sK != 1 or sxy != 0: fails.append(('22', c, gi, x, y))
                    cs, iso2 = K.components([u for u in V if u not in (x, y)], em)
                    if iso2: fails.append(('22iso', c, gi, x, y))
                    near = set(u for k in range(len(K.E)) if (K.inc[x] | K.inc[y]) >> k & 1 for u in K.E[k]) - {x, y}
                    if len(near) != 5: fails.append(('22near', c, gi, x, y, len(near)))
                    for (Vc, emc) in cs:
                        if slack(len(Vc), popc(emc), K.tau_mask(emc)) != 0: fails.append(('22tight', c, gi, x, y))
                        if not (Vc & near): fails.append(('22touch', c, gi, x, y))
                    if len(cs) > 5: fails.append(('22count', c, gi, x, y))
                    maxcomp = max(maxcomp, len(cs)); comp_hist[len(cs)] += 1
print('graphs', ngr, 'NC pairs', sum(types.values()), 'types (dmin,dmax,sigma):', dict(sorted(types.items())))
print('type (2,2,1): number of components of K-x-y histogram', dict(sorted(comp_hist.items())), 'max', maxcomp)
print('FAILS', len(fails), fails[:10])
