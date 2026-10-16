"""Step 6: reproduce the numbers quoted from bruteforce_check.py with my own numpy code, and redo its
'contained in results.json' test with EXACT comparison (the authors' script truncates quarter-integers with int()).
Window: half-integers in [-300, 1699.5]  (doubled coordinates: integers in [-600, 3399])."""
import itertools, json, sys, time
import numpy as np
from fractions import Fraction as F
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import ABASE, is45

t0 = time.time()
A2 = np.array([2 * a for a in ABASE], dtype=np.int64)
A2set = set(int(a) for a in A2)
V = np.array([v for v in range(-600, 3400) if v not in A2set], dtype=np.int64)
# valid singles: every triple of A with v has >= 5 distinct distances (<= 1 equal pair among 6)
ok = np.ones(len(V), dtype=bool)
for a, b, c in itertools.combinations(A2.tolist(), 3):
    s = [abs(a - b), abs(a - c), abs(b - c)]
    va, vb, vc = np.abs(V - a), np.abs(V - b), np.abs(V - c)
    eq = (s[0] == s[1]) + (s[0] == s[2]) + (s[1] == s[2]) + sum((w == t).astype(int) for w in (va, vb, vc) for t in s) \
        + (va == vb).astype(int) + (va == vc).astype(int) + (vb == vc).astype(int)
    ok &= eq <= 1
vals = V[ok]
print('valid singles:', len(vals), flush=True)
# P in doubled coordinates
P2 = set()
for a, b in itertools.combinations(A2.tolist(), 2):
    for v in ((a + b) // 2 if (a + b) % 2 == 0 else None, 2 * a - b, 2 * b - a):
        if v is not None and v not in A2set:
            P2.add(v)
IJ = list(itertools.combinations(range(14), 2))
total = 0
nline = 0
nonline = []
for k, x in enumerate(vals.tolist()):
    Y = vals[k + 1:]
    if len(Y) == 0:
        break
    good = np.ones(len(Y), dtype=bool)
    d1 = np.abs(x - Y)
    for i, j in IJ:
        ai, aj = int(A2[i]), int(A2[j])
        d2, d3, d6 = abs(x - ai), abs(x - aj), abs(ai - aj)
        d4, d5 = np.abs(Y - ai), np.abs(Y - aj)
        eq = int(d2 == d3) + int(d2 == d6) + int(d3 == d6) \
            + (d1 == d2).astype(np.int8) + (d1 == d3) + (d1 == d4) + (d1 == d5) + (d1 == d6) \
            + (d4 == d2) + (d4 == d3) + (d4 == d5) + (d4 == d6) + (d5 == d2) + (d5 == d3) + (d5 == d6)
        good &= eq <= 1
    Yg = Y[good]
    total += len(Yg)
    if len(Yg) == 0:
        continue
    kx = x in P2
    ky = np.array([int(y) in P2 for y in Yg], dtype=bool)
    cross = np.zeros(len(Yg), dtype=np.int64)
    for a in A2.tolist():
        cross += (2 * a == x + Yg) + (2 * x == a + Yg) + (2 * Yg == a + x)
    inx = kx | (cross > 0)
    iny = ky | (cross > 0)
    both = inx & iny
    lg = both & (~ky) & (not kx) & (cross == 1)
    nline += int(lg.sum())
    for y in Yg[both & ~lg].tolist():
        nonline.append((x, int(y)))
    if k % 500 == 0:
        print('  x index', k, 'total so far', total, 't=%.0f' % (time.time() - t0), flush=True)
print('(4,5) pairs total:', total, '| line-generic:', nline, '| non-line-generic both-in-AP:', len(nonline))
R = json.load(open('/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/results.json'))
stored_exact = {frozenset((F(a), F(b))) for a, b, h in R['stored']}
miss = [p for p in nonline if frozenset((F(p[0], 2), F(p[1], 2))) not in stored_exact]
print('non-line-generic both-in-AP pairs missing from results.json (exact comparison):', len(miss), miss[:5])
# how many entries does the authors' truncated set have, and would truncation create spurious matches?
trunc = {frozenset((int(2 * F(a)), int(2 * F(b)))) for a, b, h in R['stored']}
exact_int = {frozenset((int(2 * F(a)), int(2 * F(b)))) for a, b, h in R['stored']
             if (2 * F(a)).denominator == 1 and (2 * F(b)).denominator == 1}
print('authors truncated set size', len(trunc), '| exactly-half-integral stored pairs', len(exact_int),
      '| spurious truncated keys', len(trunc - exact_int))
# full (4,5) re-check of the 766 with the pure-Python definition
print('pure-Python is45 on all non-line-generic pairs:', all(is45([F(a) for a in ABASE] + [F(x, 2), F(y, 2)]) for x, y in nonline))
print('time %.1fs' % (time.time() - t0))
