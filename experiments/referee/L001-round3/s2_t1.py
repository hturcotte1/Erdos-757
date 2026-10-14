"""S2: Case T1 (x in P) re-derived independently, compared with the authors' results.json / witnesses.json.
Run: python3 -I s2_t1.py  (from this directory). Writes s2_t1_out.json (my (4,5) T1b pairs + SAT witnesses)."""
import itertools, json, math, random, sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
import numpy as np
from r3lib import (A_BASE, is45_py, is45_np, is_sidon, h_sat, h_brute, ap_triples, third_points, to_ints)

t0 = time.time()
EXP = '/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/'
A = [F(a) for a in A_BASE]
AS = set(A)


def scan_third_points(base, step_den, lo, hi):
    """definition-level grid scan: all v in (1/step_den)Z, lo<=v<=hi, v not in base, such that the sorted
    triple {v,p,q} is equally spaced for some distinct p,q in base."""
    D = step_den
    ints, Db = to_ints(base)
    L = math.lcm(D, Db)
    bi = np.array([int(F(b) * L) for b in base], dtype=np.int64)
    grid = np.arange(math.ceil(F(lo) * D), math.floor(F(hi) * D) + 1, dtype=np.int64) * (L // D)
    hit = np.zeros(len(grid), dtype=bool)
    for i, j in itertools.combinations(range(len(bi)), 2):
        p, q = bi[i], bi[j]
        T = np.stack([grid, np.full_like(grid, p), np.full_like(grid, q)], axis=1)
        T.sort(axis=1)
        hit |= (T[:, 1] - T[:, 0] == T[:, 2] - T[:, 1])
    inb = np.isin(grid, bi)
    return {F(int(g), L) for g in grid[hit & ~inb]}


# ---- P and P_ok
P = third_points(A)
literal = {(a + b) / 2 for a, b in itertools.permutations(A, 2)} | {2 * b - a for a, b in itertools.permutations(A, 2)}
print('|P| (excluding A) =', len(P), '| literal set {(a+b)/2, 2b-a : a != b} =', len(literal),
      '(of which in A:', len(literal & AS), ')')
assert all(v.denominator in (1, 2) for v in P) and min(P) >= -1056 and max(P) <= 2112
Pscan = scan_third_points(A, 2, -1100, 2200)
print('grid scan (1/2)Z in [-1100,2200] equals P:', Pscan == P)
Pok = sorted(x for x in P if is45_np(A + [x]))
assert all(is45_py(A + [x]) == (x in Pok) for x in P), 'np/py disagreement on singles'
print('|P_ok| =', len(Pok))

# ---- h(A u {x})
hAx = {}
for x in Pok:
    hs, W = h_sat(A + [x], start=9)
    hb, _ = h_brute(A + [x])
    assert hs == hb
    hAx[x] = hs
print('h(A u {x}) distribution (sat == brute):', {h: list(hAx.values()).count(h) for h in set(hAx.values())})

# ---- T1b candidates
single = {}


def single_ok(v):
    if v not in single:
        single[v] = (v not in AS) and is45_np(A + [v])
    return single[v]


pairs = set()
nscan_ok = 0
for x in Pok:
    Ax = A + [x]
    Q = third_points(Ax)
    lo = 2 * min(Ax) - max(Ax); hi = 2 * max(Ax) - min(Ax)
    assert all(v.denominator in (1, 2, 4) and lo <= v <= hi for v in Q)
    Qs = scan_third_points(Ax, 4, lo, hi)
    nscan_ok += (Qs == Q)
    for y in Q:
        pairs.add(frozenset((x, y)))
print('Q(x) scan==formula for', nscan_ok, 'of', len(Pok), 'x;  T1b unordered candidate pairs:', len(pairs))

good = []
nrej_single = nrej_pair = 0
for pr in sorted(pairs, key=lambda s: sorted(s)):
    x, y = sorted(pr)
    if not (single_ok(x) and single_ok(y)):
        nrej_single += 1
        continue
    B = A + [x, y]
    ok = is45_np(B)
    if not ok:
        nrej_pair += 1
        continue
    good.append((x, y))
print('(4,5) T1b pairs:', len(good), '| rejected by a single A u {v}:', nrej_single, '| rejected as pair:', nrej_pair)
# pure-python double check of every accepted pair and every pair-level rejection
pyok = all(is45_py(A + [x, y]) for x, y in good)
print('pure-python is45 confirms all accepted:', pyok)

hdist = {}
out = []
for x, y in good:
    B = A + [x, y]
    hs, W = h_sat(B, start=10)
    hb, cnt = h_brute(B)
    assert hs == hb, (x, y, hs, hb)
    hdist[hs] = hdist.get(hs, 0) + 1
    out.append({'x': str(x), 'y': str(y), 'h': hs, 'W': [str(w) for w in W], 'nmax': cnt})
print('h distribution over (4,5) T1b pairs (sat == brute):', hdist)
nboth = sum(1 for x, y in good if x in P and y in P)
print('pairs with both points in P:', nboth)

# ---- compare with the authors' files (exact Fractions)
R = json.load(open(EXP + 'results.json'))
stored = {frozenset((F(a), F(b))) for a, b, h in R['stored']}
print('results.json: stored', len(R['stored']), 'distinct', len(stored), 'all h=10:', all(h == 10 for _, _, h in R['stored']))
mine = {frozenset(p) for p in good}
print('mine', len(mine), '| mine - stored', len(mine - stored), '| stored - mine', len(stored - mine))
print('authors summary fields:', {k: R[k] for k in ('Px_size', 'Px_45', 'type1_pairs', 'type1_45', 'type1_generic_y',
                                                  'type2_isect_pts', 'type2_isect_45', 'witness_certified', 'n_stored')})
Wj = json.load(open(EXP + 'witnesses.json'))
wpairs = {frozenset((F(w['x']), F(w['y']))) for w in Wj['pairs']}
print('witnesses.json pairs', len(Wj['pairs']), 'distinct', len(wpairs), '== mine:', wpairs == mine)
bad = 0
for w in Wj['pairs']:
    x, y = F(w['x']), F(w['y'])
    S = [F(v) for v in w['S']]
    B = set(A) | {x, y}
    if not (len(S) == 10 and len(set(S)) == 10 and set(S) <= B and x not in AS and y not in AS and x != y
            and is_sidon(S) and is45_np(sorted(B))):
        bad += 1
print('witnesses.json pair witnesses failing (Sidon 10-subset of a (4,5) B):', bad)
bad9 = 0
gx = set()
for w in Wj['generic_y']:
    x = F(w['x']); gx.add(x)
    S = [F(v) for v in w['S9']]
    if not (len(set(S)) == 9 and set(S) <= set(A) | {x} and is_sidon(S) and is45_np(A + [x])):
        bad9 += 1
print('witnesses.json generic_y: entries', len(Wj['generic_y']), 'x-set == P_ok:', gx == set(Pok), 'failures:', bad9)

# ---- T1a: random y in no AP of A u {x,y}
rng = random.Random(20261014)
t1a = {}
for x in Pok:
    Q = third_points(A + [x])
    for _ in range(3):
        y = F(rng.randint(-3_000_000, 6_000_000), 1_000_003)
        assert y not in Q and y not in AS and y != x
        B = A + [x, y]
        aps = [t for t in ap_triples(B) if y in t]
        assert not aps
        if is45_np(B):
            h = h_sat(B, start=10)[0]
            t1a[h] = t1a.get(h, 0) + 1
        else:
            t1a['not45'] = t1a.get('not45', 0) + 1
print('T1a random generic y (3 per x):', t1a)
json.dump({'pairs': out, 'Pok': [str(x) for x in Pok]}, open('s2_t1_out.json', 'w'))
print('time %.1fs' % (time.time() - t0))
