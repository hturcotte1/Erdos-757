"""S6: my own recount of the numbers that the proof quotes from bruteforce_check.py
(half-integers in [-300, 1699.5]; doubled coordinates v in [-600, 3400)). numpy int64, own code.
Quoted: 3,305 valid singles; 5,185,660 (4,5) pairs; 15,800 line-generic and 766 non-line-generic pairs
with both points in 3-APs; all 766 stored (exact), stored-in-window = 766.
(h for these pairs is not recomputed here: s4_arrangement.py proves h = 10 for EVERY valid pair in R^2.)"""
import itertools, json, sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
import numpy as np
from r3lib import A_BASE, third_points

t0 = time.time()
A2 = np.array([2 * a for a in A_BASE], dtype=np.int64)
A2s = set(int(a) for a in A2)
LO, HI = -600, 3400
# valid singles: A u {v} is (4,5): all 4-sets {v,a,b,c}
trip = np.array(list(itertools.combinations(range(14), 3)), dtype=np.int64)
cand = np.array([v for v in range(LO, HI) if v not in A2s], dtype=np.int64)
ok = np.ones(len(cand), dtype=bool)
for t in trip:
    a, b, c = A2[t]
    V = cand
    d = np.stack([np.abs(V - a), np.abs(V - b), np.abs(V - c),
                  np.full_like(V, abs(a - b)), np.full_like(V, abs(a - c)), np.full_like(V, abs(b - c))], axis=1)
    d.sort(axis=1)
    ok &= (1 + (np.diff(d, axis=1) != 0).sum(axis=1)) >= 5
vals = cand[ok]
print('valid singles:', len(vals))
# P in doubled coordinates
Pd = {int(v) for v in third_points([int(a) for a in A2])}
assert all(isinstance(v, int) or F(v).denominator == 1 for v in Pd)
OFF = 10000
isP = np.zeros(3 * OFF, dtype=bool)
for v in Pd:
    isP[int(v) + OFF] = True
isA = np.zeros(6 * OFF, dtype=bool)
for a in A2s:
    isA[a + 2 * OFF] = True
two_A = np.zeros(6 * OFF, dtype=bool)
for a in A2s:
    two_A[2 * a + 2 * OFF] = True
IJ = np.array(list(itertools.combinations(range(14), 2)), dtype=np.int64)
Ai, Aj = A2[IJ[:, 0]], A2[IJ[:, 1]]
dab = np.abs(Ai - Aj)
total = nline = nnon = 0
nonlg = []
for k in range(len(vals) - 1):
    x = vals[k]
    Y = vals[k + 1:]
    m = len(Y)
    d = np.empty((m, 91, 6), dtype=np.int64)
    d[:, :, 0] = np.abs(x - Y)[:, None]
    d[:, :, 1] = np.abs(x - Ai)[None, :]
    d[:, :, 2] = np.abs(x - Aj)[None, :]
    d[:, :, 3] = np.abs(Y[:, None] - Ai[None, :])
    d[:, :, 4] = np.abs(Y[:, None] - Aj[None, :])
    d[:, :, 5] = dab[None, :]
    d.sort(axis=2)
    nd = 1 + (np.diff(d, axis=2) != 0).sum(axis=2)
    good = (nd >= 5).all(axis=1)
    Yg = Y[good]
    total += len(Yg)
    if not len(Yg):
        continue
    cross = (two_A[x + Yg + 2 * OFF].astype(int) + isA[2 * x - Yg + 2 * OFF].astype(int)
             + isA[2 * Yg - x + 2 * OFF].astype(int))
    px = bool(isP[x + OFF]); py = isP[Yg + OFF]
    inx = px | (cross > 0); iny = py | (cross > 0)
    both = inx & iny
    lg = both & (~py) & (cross == 1) & (not px)
    nl = both & ~lg
    nline += int(lg.sum()); nnon += int(nl.sum())
    nonlg.extend((int(x), int(y)) for y in Yg[nl])
print('(4,5) pairs:', total, '| both points in 3-APs:', nline + nnon, '| line-generic:', nline, '| non-line-generic:', nnon)
R = json.load(open('/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/results.json'))
stored = {frozenset((F(a), F(b))) for a, b, h in R['stored']}
inwin = {s for s in stored if all((2 * q).denominator == 1 and LO <= 2 * q < HI for q in s)}
mine = {frozenset((F(x, 2), F(y, 2))) for x, y in nonlg}
print('stored pairs in window:', len(inwin), '| non-line-generic == stored-in-window:', mine == inwin)
print('time %.1fs' % (time.time() - t0))
