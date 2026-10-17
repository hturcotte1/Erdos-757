"""Find realizable 14-point (4,5)-sets with exactly 11 three-term APs and h = 9 (tau = 5): the bound tau <= 5 of
L007 is attained in the realizable class (hence in O).  Construction: A_base (scaled by 4) plus one point x forming a
new AP with two points of A_base (B, 15 points), minus one point u, keeping only 14-point sets with m = 11."""
import sys, itertools, json
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import ap_edges, is_45_set, alpha, KNOWN
A0 = KNOWN["A_base (Ma-Tang 14-point, h=8)"]
A = [4 * a for a in A0]; S = set(A)
cand = set()
for a, b in itertools.combinations(A, 2):
    cand |= {(a + b) // 2, 2 * a - b, 2 * b - a}
cand -= S
found = []
for x in sorted(cand):
    B = sorted(A + [x])
    if not is_45_set(B): continue
    for u in B:
        C = [y for y in B if y != u]
        E = ap_edges(C)
        if len(E) != 11: continue
        h = alpha(C, E)
        found.append(dict(set=C, m=len(E), h=h, x=x, u=u))
hs = sorted({f['h'] for f in found})
print('14-point subsets with m = 11 obtained this way:', len(found), 'h values:', hs)
w = next(f for f in found if f['h'] == 9)
C = w['set']; g = min(C); C0 = [(y - g) for y in C]
from math import gcd
d = 0
for y in C0: d = gcd(d, y)
C0 = [y // d for y in C0]
print('witness (normalized):', C0, 'is (4,5):', is_45_set(C0), 'm =', len(ap_edges(C0)), 'h =', alpha(C0))
json.dump(dict(witness=C0, m=len(ap_edges(C0)), h=alpha(C0), count_m11=len(found), h_values=hs), open('witness_14_11.json', 'w'), indent=1)
