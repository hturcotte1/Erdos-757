"""Referee round 2 (L008): connected cells (n,m), n<=NMAX, ceil((n-1)/2) <= m <= n-2, with lo=floor((3n+2m)/11)+1 and
hy=floor((5n+3m)/17).  Prints window cells (lo <= min(hy,m)) and the HY-free cells (lo <= m), plus slack-0/1 cells and the
decompositions of (15,11) with total slack 1 (all multisets of connected types with slack 0/1, plus isolated vertices of slack 3)."""
import sys, itertools
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
win, hyfree = [], []
for n in range(3, NMAX + 1):
    for m in range((n - 1 + 1) // 2, n - 1):
        lo = (3 * n + 2 * m) // 11 + 1; hy = (5 * n + 3 * m) // 17
        if lo <= min(hy, m): win.append((n, m, lo))
        if lo <= m: hyfree.append((n, m, lo))
print('window cells:', win)
print('HY-free cells (lo<=m):', len(hyfree), hyfree)
# slack cells without HY, with tau<=m, n<=15
types = []
for n in range(3, 16):
    for m in range((n) // 2, n - 1):
        if n > 2 * m + 1: continue
        for t in range(0, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if s in (0, 1): types.append((n, m, t, s))
print('slack-0 types:', [x[:3] for x in types if x[3] == 0])
print('slack-1 types:', [x[:3] for x in types if x[3] == 1])
print('  ... those also satisfying HY:', [x[:3] for x in types if 17 * x[2] <= 5 * x[0] + 3 * x[1]])
# decompositions of (n,m,tau)=(15,11,6) into components with slacks summing to 1 (isolated vertex: (1,0,0) slack 3)
allt = [x for x in types] + [(1, 0, 0, 3)]
sols = []
def rec(i, n, m, t, s, chosen):
    if n == 0:
        if m == 0 and t == 0 and s == 0: sols.append(list(chosen))
        return
    if i == len(allt): return
    a = allt[i]
    # use type i k times
    k = 0
    while True:
        rec(i + 1, n - k * a[0], m - k * a[1], t - k * a[2], s - k * a[3], chosen + [a[:3]] * k)
        k += 1
        if k * a[0] > n or k * a[1] > m or k * a[3] > s: break
rec(0, 15, 11, 6, 1, [])
print('decompositions of (15,11,6) with total slack 1:', sols)
