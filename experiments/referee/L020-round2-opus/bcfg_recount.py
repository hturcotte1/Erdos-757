"""Independent recount of the b-configuration table added to L020's Definitions (edges allowed / non-edge only),
plus e-configuration counts, on the stored slack-2 lists (Delta<=3, connected)."""
import itertools
from hgr2 import HG, parse_list
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
for c in ['cell_9_4_3', 'cell_10_8_4', 'cell_13_9_5', 'cell_16_10_6', 'cell_6_3_2', 'cell_20_15_8']:
    tot = b_any = b_ne = e_cls = 0
    for (n, m, t, E) in parse_list(I + c + '.txt'):
        V = list(range(n)); K = HG(V, E)
        if max(K.deg(u) for u in V) > 3: continue
        comps, iso = K.components(V, K.full)
        if len(comps) != 1 or iso: continue
        tot += 1
        assert K.tau() == t
        low = [u for u in V if K.deg(u) <= 2]
        nc = set()
        for x, y in itertools.combinations(low, 2):
            if K.tau((x, y)) != t - 2: nc.add(frozenset((x, y)))
        Es = set(E)
        ba = bn = False
        for tr in itertools.combinations(low, 3):
            if all(frozenset(p) in nc for p in itertools.combinations(tr, 2)):
                ba = True
                if tuple(sorted(tr)) not in Es: bn = True
        ee = False
        for z in low:
            nb = [u for u in low if frozenset((z, u)) in nc]
            for x, y in itertools.combinations(nb, 2):
                if not (K.inc[x] & K.inc[y]): ee = True
        b_any += ba; b_ne += bn; e_cls += ee
    print('%-14s classes %4d  b-config (edges allowed) %4d  b-config (non-edge only) %3d  e-config %4d' % (c, tot, b_any, b_ne, e_cls))
