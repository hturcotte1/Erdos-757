"""Referee L001, case T2 (x,y not in P, AP {a,x,y}) and generic-family sanity samples."""
import itertools, json, random, sys, time
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001')
from rcore import A_BASE, is45, three_aps, max_sidon, ap_partners

t0 = time.time()
A = [Fr(a) for a in A_BASE]
Aset = set(A)
P = ap_partners(A)
# lines y = s*x + c for each a and each choice of midpoint in {a,x,y}
lines = []
for a in A:
    lines.append(('x_mid', a, Fr(2), -a))       # 2x = a + y
    lines.append(('y_mid', a, Fr(1, 2), a / 2))  # 2y = a + x
    lines.append(('a_mid', a, Fr(-1), 2 * a))    # 2a = x + y
assert len({(s, c) for _, _, s, c in lines}) == 42
# (i) abstract generic-point hypergraph: APs(A) + {a,X,Y}; alpha = 10 iff A has a maximum Sidon set avoiding a
apsA = three_aps(A)
res_alpha = {}
for a in A:
    h, W = max_sidon([b for b in A if b != a])
    res_alpha[str(a)] = h + 2 if h == 8 else None
    # brute-force alpha of the 16-vertex abstract hypergraph (vertices: A plus 'X','Y')
    V = A + ['X', 'Y']
    edges = [set(t) for t in apsA] + [{a, 'X', 'Y'}]
    best = 0
    for k in (11, 10, 9):
        if any(not any(e <= set(S) for e in edges) for S in itertools.combinations(V, k)):
            best = k
            break
    assert best == (10 if h == 8 else 9), (a, h, best)
print('T2 abstract alpha by a:', res_alpha, 'time', round(time.time() - t0, 1), flush=True)
# (ii) intersection points of two lines (exceptional points)
pts = set()
for (r1, a1, s1, c1), (r2, a2, s2, c2) in itertools.combinations(lines, 2):
    if s1 == s2:
        assert c1 != c2
        continue
    x = (c2 - c1) / (s1 - s2)
    y = s1 * x + c1
    assert y == s2 * x + c2
    pts.add((x, y))
pts_f = [(x, y) for x, y in pts if x != y and x not in Aset and y not in Aset]
print('intersection points (ordered):', len(pts), 'after filter:', len(pts_f),
      'unordered:', len({frozenset(p) for p in pts_f}))
n45 = 0
lin_viol = 0
for x, y in pts_f:
    B = A + [x, y]
    if is45(B):
        n45 += 1
        print('  (4,5) intersection point!', x, y)
    # structural reason: >= 2 APs through both x and y
    through = [t for t in three_aps(B) if x in t and y in t]
    if len(through) >= 2:
        lin_viol += 1
print('intersection points that are (4,5):', n45, '; points with >=2 APs through {x,y}:', lin_viol, 'of', len(pts_f))
# (iii) random generic points on each line: expect exactly 13 APs, (4,5), h = 10
rng = random.Random(757)
bad = 0
cnt = 0
for r, a, s, c in lines:
    for _ in range(3):
        x = Fr(rng.randrange(-3_000_000, 3_000_000), 1_000_003)
        y = s * x + c
        B = A + [x, y]
        assert x not in P and y not in P
        naps = len(three_aps(B))
        ok = is45(B)
        h = max_sidon(B)[0] if ok else None
        cnt += 1
        if naps != 13 or not ok or h != 10:
            bad += 1
            print('  line sample anomaly', r, a, x, y, naps, ok, h)
print('random generic line points:', cnt, 'anomalies:', bad)
# (iv) T1a samples: x in P_ok, y random generic -> h = 10
P_ok = sorted(v for v in P if is45(A + [v]))
bad = 0
for x in P_ok:
    for _ in range(2):
        y = Fr(rng.randrange(-3_000_000, 3_000_000), 1_000_033)
        B = A + [x, y]
        ok = is45(B)
        h = max_sidon(B)[0] if ok else None
        if not ok or h != 10:
            bad += 1
            print('  T1a anomaly', x, y, ok, h)
print('T1a random samples:', 2 * len(P_ok), 'anomalies:', bad)
# (v) T0 samples
bad = 0
for _ in range(50):
    x = Fr(rng.randrange(-3_000_000, 3_000_000), 1_000_037)
    y = Fr(rng.randrange(-3_000_000, 3_000_000), 1_000_039)
    B = A + [x, y]
    ok = is45(B)
    h = max_sidon(B)[0] if ok else None
    if not ok or h != 10:
        bad += 1
        print('  T0 anomaly', x, y, ok, h)
print('T0 random samples: 50 anomalies:', bad, 'time', round(time.time() - t0, 1))
