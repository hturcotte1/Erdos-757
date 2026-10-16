"""Are there 2-point extensions of A_base that are NOT (4,5)-sets and have h = 9?  (Bears on the title wording.)"""
import sys, collections
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round4')
import r4_locus as L
from r4_lib import A_BASE, is45_full, h_maxsat, on_line
r = L.locus(A_BASE, 0, 'title', want_points=True)
wl = [tuple(l) for l in r['whole_lines_list(scaled)']]
iso = sorted(p for p in r['_pts'] if not any(on_line(l, p) for l in wl))
A = [Fr(a) for a in A_BASE]
hs = collections.Counter()
n45 = 0
for x, y in iso:
    B = A + [x / L.SC, y / L.SC]
    n45 += is45_full(B)
    hs[h_maxsat(B)[0]] += 1
print('isolated D points (ordered):', len(iso), '| unordered:', len({frozenset(p) for p in iso}), '| (4,5):', n45, '| h distribution (MaxSAT):', dict(hs))
print('example:', [str(v / L.SC) for v in iso[0]])
