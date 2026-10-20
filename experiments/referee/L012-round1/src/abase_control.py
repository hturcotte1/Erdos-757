"""Referee control: A_base's AP pattern must be realized by rreal; exact re-verification of every printed realization with Fractions."""
import sys, subprocess, itertools
from fractions import Fraction
A = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
P = 2147483647
n = len(A); idx = {a: i for i, a in enumerate(A)}
edges = sorted(tuple(sorted((idx[a], idx[(a+c)//2], idx[c]))) for a, c in itertools.combinations(A, 2) if (a+c) % 2 == 0 and (a+c)//2 in idx)
print('A_base: n=%d, APs=%d' % (n, len(edges)))
line = 'FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in edges)
out = subprocess.run(['./out/bin/rreal', str(n), 'print'], input=line + '\n', capture_output=True, text=True).stdout.splitlines()
reals = [l for l in out if l.startswith('REAL')]
print([l for l in out if l.startswith('STAT')][0])
m = len(edges); found_self = 0; ok = 0; sets = set()
target = [Fraction(a, 1056) for a in A]
for l in reals:
    parts = dict(kv.split('=') for kv in l.split()[1:])
    u, v = int(parts['u']), int(parts['v']); mu_dfs = list(map(int, parts['mu'].split(',')))
    mu = {m - 1 - k: w for k, w in enumerate(mu_dfs)}          # ord[k] = m-1-k
    # exact solve with Fractions: unknowns all except u, v; x_u = 0, x_v = 1
    var = [w for w in range(n) if w not in (u, v)]; col = {w: i for i, w in enumerate(var)}
    M = []; 
    for e in range(m):
        row = [Fraction(0)] * (len(var) + 1); j = mu[e]; row[col[j]] += 2
        for w in edges[e]:
            if w == j: continue
            if w == v: row[-1] += 1
            elif w != u: row[col[w]] -= 1
        M.append(row)
    N = len(var)
    for c in range(N):
        pr = next(r for r in range(c, N) if M[r][c] != 0); M[c], M[pr] = M[pr], M[c]
        pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(N):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    x = [Fraction(0)] * n; x[v] = Fraction(1)
    for w in var: x[w] = M[col[w]][-1]
    # mod-p agreement with rreal's printed normalised values
    xp = list(map(int, parts['x'].split(',')))
    assert all((xi.numerator * pow(xi.denominator, P - 2, P)) % P == xpi for xi, xpi in zip(x, xp)), 'mod p mismatch'
    assert len(set(x)) == n
    vals = sorted(x); S = set(vals)
    aps = sum(1 for a, c in itertools.combinations(vals, 2) if (a + c) / 2 in S)
    assert aps == m
    ok += 1
    lo, hi = min(x), max(x); xn = tuple(sorted((t - lo) / (hi - lo) for t in x)); sets.add(xn)
    if list(xn) == target or list(xn) == sorted(1 - t for t in target): found_self += 1
print('realizations printed %d, exactly re-verified %d, distinct normalised sets %d, equal to A_base (or reflection): %d' % (len(reals), ok, len(sets), found_self))
