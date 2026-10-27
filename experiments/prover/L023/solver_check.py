"""(L023) Cross-check of the exact sparse solver of realize_sdr.py against sympy's exact linear algebra (Matrix.LUsolve over Q)
on a seeded random sample of injective labellings of X_0 and of Q8: identical solutions and identical classification."""
import sys, random, re, itertools
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from realize_sdr import labellings, solve, classify
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def sympy_solve(E, n, mids):
    M = set(mids); u, w = [v for v in range(n) if v not in M]
    unk = sorted(M); col = {v: i for i, v in enumerate(unk)}
    A = sp.zeros(len(E), len(unk)); b = sp.zeros(len(E), 1)
    for r, (e, m) in enumerate(zip(E, mids)):
        a, c = [v for v in e if v != m]
        A[r, col[m]] += 2
        for v in (a, c):
            if v == w: b[r] += 1
            elif v != u: A[r, col[v]] -= 1
    if A.det() == 0: return None
    x = A.LUsolve(b)
    out = [None] * n; out[u] = Fr(0); out[w] = Fr(1)
    for v in unk: out[v] = Fr(int(sp.fraction(x[col[v]])[0]), int(sp.fraction(x[col[v]])[1]))
    return out
X0 = parse([l for l in open('cell_25_23_11_D4.txt') if l.startswith('FOUND:')][0])
Q8 = [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 7, 2)]
rnd = random.Random(2310)
for name, E, n, k in (('X_0', X0, 25, 120), ('Q8', Q8, 8, 95)):
    L = list(labellings(E, n)); S = L if k >= len(L) else rnd.sample(L, k)
    same = 0
    for mids in S:
        x1 = solve(E, n, mids); x2 = sympy_solve(E, n, mids)
        assert x1 == x2, (name, mids)
        assert classify(x1, E, n) == classify(x2, E, n)
        same += 1
    print('%s: %d labellings (of %d) solved by both, identical solutions and classifications' % (name, same, len(L)), flush=True)
# second sample (added): classes X_3 and X_5, 60 labellings each, seed 77
G = [parse(l) for l in open('cell_25_23_11_D4.txt') if l.startswith('FOUND:')]
rnd2 = random.Random(77)
for gi in (3, 5):
    E = G[gi]; L = list(labellings(E, 25)); S = rnd2.sample(L, 60); ok = 0
    for mids in S:
        x1 = solve(E, 25, mids); x2 = sympy_solve(E, 25, mids); assert x1 == x2; assert classify(x1, E, 25) == classify(x2, E, 25); ok += 1
    print('X_%d: %d labellings (of %d) solved by both, identical solutions and classifications' % (gi, ok, len(L)), flush=True)
