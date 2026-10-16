"""Step 3: Case T2 (and T0) recomputed independently.
Lines (ordered (x,y)):  x_mid: 2x = a + y ; y_mid: 2y = a + x ; a_mid: 2a = x + y   (a in A) -> 42 lines.
 - all pairwise intersections (exact), filtered (x != y, x,y notin A): count, (4,5)?, number of cross APs
 - random generic points on every line: count APs of B, (4,5)?, h (brute force) if (4,5)
 - random generic pairs (T0)
"""
import itertools, sys, time, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import *

t0 = time.time()
A = [F(a) for a in ABASE]
Aset = set(A)
# line: (role, a, alpha, beta, gamma) meaning alpha*x + beta*y = gamma
lines = []
for a in A:
    lines.append(('x_mid', a, F(2), F(-1), a))     # 2x - y = a
    lines.append(('y_mid', a, F(-1), F(2), a))     # -x + 2y = a
    lines.append(('a_mid', a, F(1), F(1), 2 * a))  # x + y = 2a
assert len(lines) == 42
pts = set()
npairs_nonpar = 0
for L1, L2 in itertools.combinations(lines, 2):
    det = L1[2] * L2[3] - L2[2] * L1[3]
    if det == 0:
        # parallel: check distinct (no identical lines)
        assert not (L1[2] * L2[4] == L2[2] * L1[4]), (L1, L2)
        continue
    npairs_nonpar += 1
    x = (L1[4] * L2[3] - L2[4] * L1[3]) / det
    y = (L1[2] * L2[4] - L2[2] * L1[4]) / det
    assert L1[2] * x + L1[3] * y == L1[4] and L2[2] * x + L2[3] * y == L2[4]
    pts.add((x, y))
print('non-parallel line pairs:', npairs_nonpar, '| distinct intersection points:', len(pts))
flt = [(x, y) for x, y in pts if x != y and x not in Aset and y not in Aset]
print('after filtering x!=y, x,y notin A:', len(flt))


def cross_aps(x, y):
    return sum(1 for (r, a, al, be, ga) in lines if al * x + be * y == ga)


n45 = sum(1 for x, y in flt if is45(A + [x, y]))
print('intersection points that are (4,5):', n45, '| min #cross APs at them:', min(cross_aps(x, y) for x, y in flt))
# denominators of intersection points
print('denominators occurring:', sorted({p.denominator for xy in flt for p in xy}))

rng = random.Random(7)
summary = {}
for (r, a, al, be, ga) in lines:
    res = []
    for _ in range(6):
        x = F(rng.randrange(-3000 * 1000003, 6000 * 1000003), 1000003)
        y = (ga - al * x) / be
        B = A + [x, y]
        P, _ = to_ints(B)
        nap = len(three_aps(P))
        ok = is45(B)
        h = hmax_brute(B, 10)[0] if ok else None
        res.append((nap, ok, h))
    summary[(r, int(a))] = res
naps = {t[0] for v in summary.values() for t in v}
print('APs at random line points:', naps)
live = [k for k, v in summary.items() if any(t[1] for t in v)]
dead = [k for k, v in summary.items() if not any(t[1] for t in v)]
print('lines with (4,5) random points:', len(live), '| lines with none:', len(dead), dead)
print('h at (4,5) random line points:', {t[2] for v in summary.values() for t in v if t[1]})
mixed = [k for k, v in summary.items() if len({t[1] for t in v}) > 1]
print('lines with mixed (4,5) outcomes among samples (should be none):', mixed)
# T0
c = {}
for _ in range(60):
    x = F(rng.randrange(-3000 * 1000003, 6000 * 1000003), 1000003)
    y = F(rng.randrange(-3000 * 999983, 6000 * 999983), 999983)
    B = A + [x, y]
    ok = is45(B)
    h = hmax_brute(B, 10)[0] if ok else None
    c[(ok, h, len(three_aps(to_ints(B)[0])))] = c.get((ok, h, len(three_aps(to_ints(B)[0]))), 0) + 1
print('T0 random pairs (is45, h, #APs):', c)
print('time %.1fs' % (time.time() - t0))
