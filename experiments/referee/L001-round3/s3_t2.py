"""S3: Case T2 (x,y not in P, some 3-AP {a,x,y}) and Case T0, re-derived independently.
Run: python3 -I s3_t2.py  (from this directory)."""
import itertools, random, sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
from r3lib import A_BASE, is45_py, is45_np, h_sat, ap_triples, third_points

t0 = time.time()
A = [F(a) for a in A_BASE]; AS = set(A)
P = third_points(A)
# lines y = s*x + c for the three roles
lines = []
for a in A:
    lines.append(('x_mid', a, F(2), -a))        # 2x = a + y
    lines.append(('y_mid', a, F(1, 2), a / 2))  # 2y = a + x
    lines.append(('a_mid', a, F(-1), 2 * a))    # 2a = x + y
assert len({(s, c) for _, _, s, c in lines}) == 42, 'distinct (role,a) must give distinct lines'


def cross_aps(x, y):
    out = []
    for a in A:
        if 2 * x == a + y: out.append(('x_mid', a))
        if 2 * y == a + x: out.append(('y_mid', a))
        if 2 * a == x + y: out.append(('a_mid', a))
    return out


# ---- intersections
npar = 0; pts = set()
for (r1, a1, s1, c1), (r2, a2, s2, c2) in itertools.combinations(lines, 2):
    if s1 == s2:
        npar += 1
        continue
    x = (c2 - c1) / (s1 - s2); y = s1 * x + c1
    assert y == s2 * x + c2
    pts.add((x, y))
print('line pairs:', 42 * 41 // 2, 'parallel:', npar, 'non-parallel:', 42 * 41 // 2 - npar, '| distinct intersection points:', len(pts))
filt = sorted((x, y) for x, y in pts if x != y and x not in AS and y not in AS)
n45 = sum(1 for x, y in filt if is45_py(A + [x, y]))
mult = [len(cross_aps(x, y)) for x, y in filt]
dens = sorted({v.denominator for x, y in filt for v in (x, y)})
print('after removing x=y and x or y in A:', len(filt), '| (4,5):', n45, '| min #cross APs:', min(mult), '| denominators:', dens)
# structural reason: two cross APs {a,x,y},{a',x,y} -> the 4-set {a,a',x,y} has <= 4 distinct distances
viol = 0
for x, y in filt:
    c = cross_aps(x, y)
    a1, a2 = c[0][1], c[1][1]
    assert a1 != a2
    q = (a1, a2, x, y)
    if len({abs(u - v) for u, v in itertools.combinations(q, 2)}) > 4: viol += 1
print('intersection points whose 4-set {a,a\',x,y} has >= 5 distances (should be 0):', viol)
inP = sum(1 for x, y in filt if x in P or y in P)
print('intersection points with a coordinate in P (would be T1 anyway):', inP)

# ---- generic points on each line
rng = random.Random(757)
res = {}
for role, a, s, c in lines:
    outc = []
    for _ in range(8):
        x = F(rng.randint(-2_000_000, 4_000_000), 999_983)
        y = s * x + c
        assert x not in P and y not in P and x != y and x not in AS and y not in AS
        B = A + [x, y]
        naps = len(ap_triples(B))
        assert naps == 13 and len(cross_aps(x, y)) == 1
        if is45_np(B):
            outc.append(h_sat(B, start=10)[0])
        else:
            outc.append('not45')
    res[(role, a)] = outc
live = {k: v for k, v in res.items() if any(o != 'not45' for o in v)}
mixed = {k: v for k, v in res.items() if len(set(v)) > 1}
print('lines with (4,5) generic points:', len(live), '| h values there:', sorted({o for v in live.values() for o in v}, key=str))
print('lines with no (4,5) generic point:', sorted((r, str(a)) for (r, a), v in res.items() if (r, a) not in live))
print('lines with mixed outcomes among 8 samples:', len(mixed))

# ---- T0: random generic pairs
t0r = {}
for _ in range(100):
    x = F(rng.randint(-2_000_000, 4_000_000), 1_000_033); y = F(rng.randint(-2_000_000, 4_000_000), 1_000_037)
    B = A + [x, y]
    assert len(ap_triples(B)) == 12
    k = h_sat(B, start=10)[0] if is45_np(B) else 'not45'
    t0r[k] = t0r.get(k, 0) + 1
print('T0 random pairs (12 APs each):', t0r)
print('time %.1fs' % (time.time() - t0))
