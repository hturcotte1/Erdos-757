"""What does t2_isect_pts count?  Distinct pairwise intersections of the 36 T2 lines, before/after excluding x=y, x or y in A."""
import gzip, json
from fractions import Fraction as F
from itertools import combinations
ROOT = '/home/user/Erdos-757'
cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt'))}
tot_all = tot_kept = tot_stored = 0
for c in list(range(0, 54243, 5424)) + [20392, 23942, 18917]:
    A = sorted(cen[c]['set']); S = set(A)
    L = [(F(2), F(-a)) for a in A] + [(F(1, 2), F(a, 2)) for a in A] + [(F(-1), F(2 * a)) for a in A]   # y = m x + q
    P = set()
    for (m1, q1), (m2, q2) in combinations(L, 2):
        if m1 != m2:
            x = (q2 - q1) / (m1 - m2); P.add((x, m1 * x + q1))
    kept = {p for p in P if p[0] != p[1] and p[0] not in S and p[1] not in S}
    tot_all += len(P); tot_kept += len(kept); tot_stored += rows[c]['t2_isect_pts']
    print(c, 'distinct intersections', len(P), 'after exclusions', len(kept), 'stored t2_isect_pts', rows[c]['t2_isect_pts'])
print('totals over these classes: all', tot_all, 'kept', tot_kept, 'stored', tot_stored)
