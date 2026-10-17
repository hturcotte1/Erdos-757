"""Certificate L010, Steps 1-6 (exact integer arithmetic; prover's own script, generalising L009's decomp18.py).
(a) window cells for n <= 20 with the admissible tau and the slack at the least violating tau, and the degree bound floor((s+8)/2);
(b) connected cells (n,m,tau) with slack s in {0,1,2,3}, n <= 19 (every tau in 0..m is tried; tau <= m and HY imposed);
(c) decompositions of a target (N,M) with total slack S into a multiset of component types: connected cells of slack <= S and the
    isolated vertex (1,0,0) of slack 3 (included explicitly: it matters as soon as S >= 3)."""
import sys
def conn_cells(nmax):
    for n in range(3, nmax + 1):
        for m in range((n - 1 + 1) // 2, n - 1):
            yield n, m
def window(nmax):
    out = []
    for n, m in conn_cells(nmax):
        lo = (3 * n + 2 * m) // 11 + 1; hi = min((5 * n + 3 * m) // 17, m)
        if lo <= hi:
            s = 3 * n + 2 * m - 11 * lo
            out.append((n, m, list(range(lo, hi + 1)), s, (s + 8) // 2))
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
print('(a) window cells n<=20 (n, m, admissible taus, slack at least violating tau, degree bound floor((s+8)/2)):')
for w in window(20):
    if w[0] >= 17: print('   ', w)
print('    all window cells n<=20:', [(w[0], w[1], w[2][0]) for w in window(20)])
sc = slack_cells(19, 3)
for s in (0, 1, 2, 3): print('(b) connected cells n<=19 with slack %d:' % s, [c[:3] for c in sc if c[3] == s])
pieces = sc + [(1, 0, 0, 3)]
for (N, M, S, why) in [(18, 12, 1, 'G = H-v for H in (19,15,8)'), (17, 9, 3, "X-w for X connected (18,12,7) with a degree-3 vertex w"),
                       (19, 10, 0, 'G = H-v for H in (20,13,8)'), (16, 10, 2, 'L009 check'), (13, 9, 2, 'L009 check'), (17, 13, 0, 'L009 check')]:
    d = decompositions(N, M, S, pieces)
    print('(c) decompositions of (%d,%d) with total slack %d [%s]: %d' % (N, M, S, why, len(d)))
    for x in d: print('      ', [p[:3] for p in x])
