"""Stress test of the combinatorial core of L022 Theorem 1(b): for random ORDERED MIDPOINT PATTERNS (vertices 0..n-1 in
their order, triples (a,b,c) with a<b<c and pairwise distinct midpoints b; not required to be linear or realizable), the
forms X_a + X_c - 2 X_b are linearly independent (exact rank over Q equals the number of triples).
usage: python3 independence_stress.py seed trials"""
import sys, random
from fractions import Fraction as Fr

def rank_Q(rows, n):
    M = [list(map(Fr, r)) for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = 1 / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r

seed, T = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed); bad = 0; tot = 0
for t in range(T):
    n = rnd.randint(4, 30)
    mids = rnd.sample(range(1, n - 1), rnd.randint(1, n - 2))
    rows = []
    for b in mids:
        a = rnd.randrange(0, b); c = rnd.randrange(b + 1, n)
        r = [0] * n; r[a] += 1; r[c] += 1; r[b] -= 2; rows.append(r)
    tot += 1
    if rank_Q(rows, n) != len(rows): bad += 1; print('DEPENDENT', n, rows)
print({'patterns': tot, 'dependent': bad})
