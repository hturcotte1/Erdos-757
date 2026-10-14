"""S2b: confirm every T1b rejection of s2 with the pure-Python (4,5) definition (guards against numpy false negatives)."""
import itertools, sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
from r3lib import A_BASE, is45_py, is45_np, third_points
t0 = time.time()
A = [F(a) for a in A_BASE]; AS = set(A)
P = third_points(A)
Pok = sorted(x for x in P if is45_py(A + [x]))
pairs = set()
for x in Pok:
    for y in third_points(A + [x]):
        pairs.add(frozenset((x, y)))
ys = sorted({v for pr in pairs for v in pr})
single_py = {v: (v not in AS) and is45_py(A + [v]) for v in ys}
single_np = {v: (v not in AS) and is45_np(A + [v]) for v in ys}
print('distinct coordinates in T1b pairs:', len(ys), '| single (4,5) py==np on all:', single_py == single_np,
      '| singles (4,5):', sum(single_py.values()))
npair = nacc = 0; dis = 0
for pr in pairs:
    x, y = sorted(pr)
    if single_py[x] and single_py[y]:
        npair += 1
        a, b = is45_py(A + [x, y]), is45_np(A + [x, y])
        dis += (a != b); nacc += a
print('pairs with both singles (4,5):', npair, '| accepted (py):', nacc, '| py/np disagreements:', dis)
print('time %.1fs' % (time.time() - t0))
