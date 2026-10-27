"""Richness computed directly on the stored class lists (experiments/20261027-0300-transversal-richness/inputs/)."""
from itertools import combinations
from rlib import load_cell, degs, min_transversals, in_C3
INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
for fn in ['cell_17_13_7.txt', 'cell_10_7_4.txt', 'cell_8_5_3.txt', 'cell_15_11_6.txt']:
    for idx, (n, m, t, E) in enumerate(load_cell(INP + fn)):
        d = degs(n, E)
        if max(d) > 3:
            print(fn, idx, 'Delta', max(d), '(not a piece: Delta > 3)')
            continue
        tt, mts = min_transversals(n, E)
        nct = [(x, y) for x, y in combinations(range(n), 2) if not any((T >> x & 1) and (T >> y & 1) for T in mts)]
        print(fn, idx, 'n,m,tau', (n, m, tt), 'inC3', in_C3(n, E), 'rich', not nct, 'non-co-transversal pairs', len(nct))
