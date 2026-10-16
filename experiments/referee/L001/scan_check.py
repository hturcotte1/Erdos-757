"""Referee L001: scan-based re-derivation (no AP-partner formula) with numpy integer arithmetic.
Part A: scan half-integers covering all of P; Part B: for each x in P_ok scan all quarter-integers
covering Q(x); Part C: reproduce the authors' half-integer grid counts in [-60,1120], computing h
for every pair with both new points in APs."""
import json, sys, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001')
from rcore import A_BASE, max_sidon, is45

t0 = time.time()
A = np.array(A_BASE, dtype=np.int64)
TRI = np.array(list(combinations(range(14), 3)))
PAIR = np.array(list(combinations(range(14), 2)))

def single45(vals, As):
    """vals: int array (scaled), As: scaled A. Returns bool array: A u {v} is (4,5) (all 4-sets with v)."""
    out = np.ones(len(vals), bool)
    a, b, c = As[TRI[:, 0]], As[TRI[:, 1]], As[TRI[:, 2]]
    fixed = np.stack([np.abs(a - b), np.abs(a - c), np.abs(b - c)], axis=1)  # (364,3)
    for s in range(0, len(vals), 2000):
        v = vals[s:s + 2000][:, None]
        D = np.concatenate([np.abs(v - a)[:, :, None], np.abs(v - b)[:, :, None], np.abs(v - c)[:, :, None],
                            np.broadcast_to(fixed, (v.shape[0], 364, 3))], axis=2)
        D.sort(axis=2)
        eq = (np.diff(D, axis=2) == 0).sum(axis=2)
        out[s:s + 2000] = (eq <= 1).all(axis=1)
    return out

def pair45(x, ys, As):
    """bool array over ys: all 4-sets {x,y,a,b} have >= 5 distinct distances."""
    a, b = As[PAIR[:, 0]], As[PAIR[:, 1]]
    out = np.ones(len(ys), bool)
    for s in range(0, len(ys), 4000):
        y = ys[s:s + 4000][:, None]
        n = y.shape[0]
        D = np.stack([np.broadcast_to(np.abs(x - y), (n, 91)), np.broadcast_to(np.abs(x - a), (n, 91)),
                      np.broadcast_to(np.abs(x - b), (n, 91)), np.abs(y - a), np.abs(y - b),
                      np.broadcast_to(np.abs(a - b), (n, 91))], axis=2)
        D.sort(axis=2)
        eq = (np.diff(D, axis=2) == 0).sum(axis=2)
        out[s:s + 4000] = (eq <= 1).all(axis=1)
    return out

def in_ap_with(vals, S):
    """bool array: v forms a 3-AP with two distinct points of S (v not in S assumed)."""
    S = np.array(sorted(S), dtype=np.int64)
    twoS = set((2 * S).tolist())
    sums = set()
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            sums.add(int(S[i] + S[j]))
    mid = np.isin(2 * vals, np.array(sorted(sums)))                      # v midpoint
    end = np.isin(vals[:, None] + S[None, :], np.array(sorted(twoS))).any(axis=1)  # v + w = 2u
    return mid | end

# ---------- Part A: half-integers (scale 2) in [-1100, 2200] contain every element of P
A2 = 2 * A
G = np.arange(-2200, 4401, dtype=np.int64)
G = G[~np.isin(G, A2)]
inP = in_ap_with(G, A2.tolist())
ok1 = single45(G, A2)
P_scan = {Fr(int(v), 2) for v in G[inP]}
Pok_scan = {Fr(int(v), 2) for v in G[inP & ok1]}
D = json.load(open('/home/user/Erdos-757/experiments/referee/L001/t1_out.json'))
P_form = {Fr(s) for s in D['P']}
Pok_form = {Fr(s) for s in D['P_ok']}
print('A: |P_scan|', len(P_scan), '|P_ok_scan|', len(Pok_scan), 'equal to formula sets:',
      P_scan == P_form, Pok_scan == Pok_form, 'range of P', min(P_form), max(P_form), 't', round(time.time() - t0, 1), flush=True)

# ---------- Part B: for x in P_ok scan quarter-integers (scale 4) covering every possible y in an AP of A u {x}
A4 = 4 * A
lo = min(2 * min(A_BASE + [x]) - max(A_BASE + [x]) for x in Pok_form)
hi = max(2 * max(A_BASE + [x]) - min(A_BASE + [x]) for x in Pok_form)
Y = np.arange(int(4 * lo) - 8, int(4 * hi) + 9, dtype=np.int64)
Y = Y[~np.isin(Y, A4)]
okY = single45(Y, A4)
print('B: y-range', lo, hi, 'grid size', len(Y), 'singles (4,5):', int(okY.sum()), 't', round(time.time() - t0, 1), flush=True)
found = set()
t1a = 0
for x in sorted(Pok_form):
    x4 = int(4 * x)
    ys = Y[(Y != x4) & okY]
    pk = pair45(x4, ys, A4)
    inap = in_ap_with(ys, A4.tolist() + [x4])
    for y in ys[pk & inap]:
        found.add(frozenset((x, Fr(int(y), 4))))
    t1a += int((pk & ~inap).sum())
T1b_mine = {frozenset((Fr(a), Fr(b))) for a, b, h, W in D['good']}
R = json.load(open('/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/results.json'))
stored = {frozenset((Fr(a), Fr(b))) for a, b, h in R['stored']}
print('B: (4,5) pairs with x in P_ok and y in an AP of B:', len(found), '; equal to my T1b set:', found == T1b_mine,
      '; equal to stored:', found == stored, '; grid y isolated (T1a-type, (4,5)):', t1a, 't', round(time.time() - t0, 1), flush=True)

# ---------- Part C: authors' grid, half-integers in [-60,1120]
Gc = np.arange(-120, 2241, dtype=np.int64)
Gc = Gc[~np.isin(Gc, A2)]
okc = single45(Gc, A2)
V = Gc[okc]
print('C: valid singles', len(V), flush=True)
Vin = in_ap_with(V, A2.tolist())   # v in P
Pset2 = set(V[Vin].tolist())
n45 = 0; ap_pairs = []; nline = []
twoA = set(A2.tolist())
Aset2 = set(A2.tolist())
for i in range(len(V) - 1):
    x = int(V[i]); ys = V[i + 1:]
    pk = pair45(x, ys, A2)
    n45 += int(pk.sum())
    ys = ys[pk]
    if len(ys) == 0:
        continue
    # APs {a,x,y}: 2x = a + y, 2y = a + x, 2a = x + y
    c1 = np.isin(2 * x - ys, A2).astype(int)
    c2 = np.zeros(len(ys), int); m = ((ys * 2 - x) )
    c2 = np.isin(2 * ys - x, A2).astype(int)
    s = x + ys
    c3 = ((s % 2 == 0) & np.isin(s // 2, A2)).astype(int)
    nxy = c1 + c2 + c3
    xin = (x in Pset2) | (nxy > 0)
    yin = np.isin(ys, np.array(sorted(Pset2))) | (nxy > 0)
    both = xin & yin
    ypin = np.isin(ys, np.array(sorted(Pset2)))
    linegen = both & (x not in Pset2) & (~ypin) & (nxy == 1)
    for y in ys[both & ~linegen]:
        ap_pairs.append((x, int(y)))
    for y in ys[linegen]:
        nline.append((x, int(y)))
print('C: (4,5) pairs', n45, '; both-in-AP non-line-generic', len(ap_pairs), '; line-generic', len(nline),
      't', round(time.time() - t0, 1), flush=True)
miss = [p for p in ap_pairs if frozenset((Fr(p[0], 2), Fr(p[1], 2))) not in stored]
print('C: non-line-generic pairs missing from stored:', len(miss))
hd = {}
for x, y in ap_pairs + nline:
    S = A_BASE + [Fr(x, 2), Fr(y, 2)]
    h = max_sidon(S)[0]
    hd[h] = hd.get(h, 0) + 1
print('C: direct h over all', len(ap_pairs) + len(nline), 'both-in-AP (4,5) grid pairs:', hd)
# spot-check numpy (4,5) decisions against the full pure-Python check
import random
rng = random.Random(5)
smp = rng.sample(ap_pairs, 200) + rng.sample(nline, 200)
assert all(is45(A_BASE + [Fr(x, 2), Fr(y, 2)]) for x, y in smp)
print('C: 400 sampled numpy (4,5) decisions confirmed by full check; done t', round(time.time() - t0, 1))
