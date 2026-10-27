"""C7 addition: every class of cell (23,21,10) has a vertex degree outside {2,3}; (3,1,1) trivially (degrees 1)."""
import collections
from ref2 import read_cell, degrees
D = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
for c in ['23_21_10', '3_1_1']:
    L = read_cell(D + 'cell_%s.txt' % c)
    bad = 0; hist = collections.Counter()
    for (n, E, t) in L:
        d = degrees(range(n), E)
        vals = set(d.values())
        hist[tuple(sorted(collections.Counter(d.values()).items()))] += 0
        if vals <= {2, 3}: bad += 1
        hist['has_deg>=4'] += any(v >= 4 for v in vals); hist['has_deg<=1'] += any(v <= 1 for v in vals)
    print(c, 'classes', len(L), 'classes with all degrees in {2,3}:', bad, {k: v for k, v in hist.items() if v})
