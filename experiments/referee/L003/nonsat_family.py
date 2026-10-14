"""Referee L003: independent check of the non-saturated part.
For each n = 6..11 take realized NON-saturated extremal sets from the census output files (read as data only),
re-verify from the definitions ((4,5) on all 4-subsets, 3-APs, h = largest Sidon subset by brute force over subsets),
then build the exact solution space V of the AP equations (Fractions), and exhibit K perturbed sets x + e*v
(v in V, independent of x and 1) that are again (4,5)-sets with the same AP pattern and h = f(n), with pairwise
distinct affine normal forms.  Also f(n) >= ceil((9n+6)/17) (Ma-Tang via Henning-Yeo) for each n.
No e757 / judge imports."""
import sys, json, gzip, math, itertools, random
from fractions import Fraction as Fr
F = {6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7}
R = '/home/user/Erdos-757/experiments/20261014-1430-small-counts/results/'

def is45(A):
    for q in itertools.combinations(sorted(A), 4):
        if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5: return False
    return True

def aps(A):
    A = sorted(A); S = set(A); pos = {v: i for i, v in enumerate(A)}
    out = []
    for i in range(len(A)):
        for k in range(i + 2, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 if isinstance(s, int) else True:
                mid = s / 2 if not isinstance(s, int) else (s // 2 if s % 2 == 0 else None)
                if mid is not None and mid in S: out.append((i, pos[mid], k))
    return out

def sidon(B):
    d = set()
    for a, b in itertools.combinations(sorted(B), 2):
        if b - a in d: return False
        d.add(b - a)
    return True

def h_of(A):
    A = sorted(A); n = len(A)
    for size in range(n, 0, -1):
        for B in itertools.combinations(A, size):
            if sidon(B): return size
    return 0

def nf(vals):
    v = sorted(Fr(x) for x in vals); lo = v[0]; v = [x - lo for x in v]
    den = 1
    for x in v: den = den * x.denominator // math.gcd(den, x.denominator)
    w = [int(x * den) for x in v]; g = 0
    for x in w: g = math.gcd(g, x)
    w = [x // g for x in w]
    return tuple(min(w, sorted(w[-1] - x for x in w)))

def nullspace(rows, n):
    M = [list(r) for r in rows]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = 1 / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [Fr(0)] * n; v[fc] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        basis.append(v)
    return basis, len(piv)

def rank(vecs):
    M = [list(v) for v in vecs]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r

random.seed(2026)
for n in range(6, 12):
    T = F[n]
    lb = -(-(9 * n + 6) // 17)
    files = [f for f in [R + 'n%d_m%d_real.json.gz' % (n, m) for m in range(1, n - 2)] + [R + 'n11_m%d_sample_real.json.gz' % m for m in (6, 7, 8) if n == 11]]
    pool = []
    for fn in files:
        try: pool += json.load(gzip.open(fn, 'rt'))
        except FileNotFoundError: pass
    pool = [r for r in pool if len(r['edges']) < n - 2]
    picks = random.sample(pool, min(3, len(pool)))
    for r in picks:
        A = sorted(r['set']); assert len(set(A)) == n
        ok45 = is45(A); E = aps(A); m = len(E); h = h_of(A)
        assert ok45 and h == T and m < n - 2 and sorted(map(tuple, r['edges'])) == sorted(E), (n, A)
        rows = []
        for (i, j, k) in E:
            row = [Fr(0)] * n; row[i] += 1; row[k] += 1; row[j] -= 2; rows.append(row)
        basis, rk = nullspace(rows, n)
        x = [Fr(a) for a in A]; one = [Fr(1)] * n
        # a direction of V independent of x and 1
        v = next(b for b in basis if rank([x, one, b]) == 3)
        fam = set(); tries = 0
        for e in [Fr(1, 1000 * t) for t in range(1, 40)]:
            y = [a + e * b for a, b in zip(x, v)]
            if any(y[i] >= y[i + 1] for i in range(n - 1)): continue
            tries += 1
            if is45(y) and len(aps(y)) == m and sorted(aps(y)) == sorted(E) and h_of(y) == T:
                fam.add(nf(y))
            if len(fam) >= 5: break
        print('n=%d f=%d HY-lb=%d | set m=%d dimV=%d (n-rank=%d) h=%d (4,5)=%s | perturbations tested=%d, distinct extremal classes found=%d'
              % (n, T, lb, m, len(basis), n - rk, h, ok45, tries, len(fam)))
