"""Referee L003: (a) for every midpoint map at n<=8 (all maps, no pruning) the system 2x_j = x_l + x_r (x_0=0, x_{n-1}=1)
is nonsingular with 0 < det <= 2^(n-2) (M-matrix bound used by the float pre-filter of satenum.c);
(b) for weak Sidon sets, 3-APs have distinct midpoints (checked on random integer sets)."""
import itertools, random
from fractions import Fraction as Fr
def det_int(M):
    M = [[Fr(x) for x in r] for r in M]; n = len(M); d = Fr(1)
    for k in range(n):
        p = next((i for i in range(k, n) if M[i][k] != 0), None)
        if p is None: return 0
        if p != k: M[k], M[p] = M[p], M[k]; d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            M[i] = [a - f * b for a, b in zip(M[i], M[k])]
    return d
for n in range(4, 9):
    N2 = n - 2; choices = [[(l, r) for l in range(j) for r in range(j + 1, n)] for j in range(1, n - 1)]
    cnt = 0; mn = None; mx = None
    for mp in itertools.product(*choices):
        M = [[0] * N2 for _ in range(N2)]
        for j, (l, r) in enumerate(mp, start=1):
            M[j - 1][j - 1] += 2
            if l >= 1: M[j - 1][l - 1] -= 1
            if r <= n - 2: M[j - 1][r - 1] -= 1
        d = det_int(M); cnt += 1
        mn = d if mn is None else min(mn, d); mx = d if mx is None else max(mx, d)
        if n == 8 and cnt >= 200000: break
    print('n=%d maps checked=%d det range [%s, %s], bound 2^(n-2)=%d' % (n, cnt, mn, mx, 2 ** (n - 2)))
random.seed(1); bad = 0; tested = 0
for _ in range(20000):
    A = sorted(random.sample(range(200), 8))
    sums = [a + b for a, b in itertools.combinations(A, 2)]
    if len(sums) != len(set(sums)): continue
    tested += 1
    mids = [b for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b]
    if len(mids) != len(set(mids)): bad += 1
print('weak Sidon random sets tested=%d, with a repeated AP midpoint=%d' % (tested, bad))
