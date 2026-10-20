"""Certificate L009, Steps 1, 2, 3 (exact integer arithmetic; written for L009, not derived from windows.py / parts_g.py).
(a) window cells (n,m) for n <= 18: connected cells (n>=3, ceil((n-1)/2) <= m <= n-2) admitting tau with 11 tau > 3n+2m,
    17 tau <= 5n+3m (Henning-Yeo) and tau <= m; printed with the admissible tau and the slack at the least violating tau.
(b) connected cells (n,m,tau) with slack s = 3n+2m-11tau in {0,1,2}, n <= 17 (every tau in 0..m is tried; tau <= m and HY imposed).
(c) decompositions of a target (N,M) with total slack S into a multiset of component types: connected cells of slack <= S
    and the isolated vertex (1,0,0) of slack 3; no other restriction."""
import sys
def conn_cells(nmax):
    for n in range(3, nmax + 1):
        for m in range((n - 1 + 1) // 2, n - 1):
            yield n, m
def window(nmax):
    out = []
    for n, m in conn_cells(nmax):
        lo = (3 * n + 2 * m) // 11 + 1; hi = min((5 * n + 3 * m) // 17, m)
        if lo <= hi: out.append((n, m, list(range(lo, hi + 1)), 3 * n + 2 * m - 11 * lo))
    return out
def slack_cells(nmax, smax):
    out = []
    for n, m in conn_cells(nmax):
        for t in range(0, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if 0 <= s <= smax and 17 * t <= 5 * n + 3 * m: out.append((n, m, t, s))
    return out
def decompositions(N, M, S, pieces):
    sols = []
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S: sols.append(list(chosen)); return
        if i == len(pieces): return
        pn, pm, pt, ps = pieces[i]; k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, chosen + [pieces[i]] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sols
W = window(18)
print('(a) window cells n<=18 (n,m,admissible taus,slack at least violating tau):')
for w in W: print('   ', w)
sc = slack_cells(17, 2)
for s in (0, 1, 2): print('(b) connected cells n<=17 with slack %d:' % s, [c[:3] for c in sc if c[3] == s])
pieces = sc + [(1, 0, 0, 3)]
for (N, M, S, why) in [(16, 9, 0, 'G = H-v for H in (17,12,7)'), (17, 13, 0, 'G = H-v for H in (18,16,8)'),
                       (16, 10, 2, "G' = T-w for T in (17,13,7)"), (13, 9, 2, "G' = T-w for T in (14,12,6)"),
                       (13, 8, 0, 'L007 check'), (15, 11, 1, 'L008 check')]:
    print('(c) decompositions of (%d,%d) with total slack %d [%s]:' % (N, M, S, why), [[p[:3] for p in d] for d in decompositions(N, M, S, pieces)])
