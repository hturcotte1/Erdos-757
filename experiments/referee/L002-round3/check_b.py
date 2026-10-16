"""Referee round 3, check B: compare ./vr output on the census sets with the census records.
Inputs: vr_census.out (lines from './vr set'), census_edges.txt (stored edge lists, same order).
Checks: every line is 'SET is45 h=7 alpha=7 m=10', the rank-order AP pattern equals the stored edges,
normalized forms (own normalization in vr) are pairwise distinct; prints the class count."""
import sys
from collections import Counter
bad = Counter(); norms = set(); n = 0
with open(sys.argv[1]) as fv, open(sys.argv[2]) as fe:
    for lv, le in zip(fv, fe):
        n += 1
        head, norm = lv.rstrip('\n').split(' ; ')
        f = head.split()
        if f[0] != 'SET' or f[1] != 'is45': bad['not45'] += 1
        if f[2] != 'h=7': bad['h!=7'] += 1
        if f[3] != 'alpha=7': bad['alpha!=7'] += 1
        if f[4] != 'm=10': bad['m!=10'] += 1
        pat = head.split('pat=')[1].split()
        if sorted(pat) != sorted(le.split()): bad['pattern!=stored'] += 1
        if norm in norms: bad['duplicate_class'] += 1
        norms.add(norm)
print('records=%d distinct_normal_forms=%d problems=%s' % (n, len(norms), dict(bad)))
with open(sys.argv[3], 'w') as fo:
    for x in sorted(norms): fo.write(x + '\n')
