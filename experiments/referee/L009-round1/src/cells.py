"""Referee L009: my own arithmetic for the window cells, slack cells and decompositions (exact integers).
Window cell: connected (n,m) with ceil((n-1)/2) <= m <= n-2 and some tau with 11 tau > 3n+2m, 17 tau <= 5n+3m, tau <= m.
Slack cells: connected (n,m,tau) with s = 3n+2m-11tau in [0,S], tau <= m, 17tau <= 5n+3m (and, separately, WITHOUT HY).
Decompositions: multisets of connected slack cells and isolated vertices (1,0,0; s=3) with given total (n,m,s)."""
from functools import lru_cache
def conn(n): return range(-(-(n - 1) // 2), n - 1)   # ceil((n-1)/2) .. n-2
def window(n):
    out = []
    for m in conn(n):
        taus = [t for t in range(m + 1) if 11 * t > 3 * n + 2 * m and 17 * t <= 5 * n + 3 * m]
        if taus: out.append((n, m, taus))
    return out
def slack(nmax, smax, hy=True):
    return [(n, m, t, 3*n+2*m-11*t) for n in range(3, nmax + 1) for m in conn(n) for t in range(m + 1)
            if 0 <= 3*n+2*m-11*t <= smax and (not hy or 17*t <= 5*n+3*m)]
for n in range(3, 19): 
    w = window(n)
    if w: print('window n=%d:' % n, w)
for hy in (True, False):
    sc = slack(17, 2, hy)
    for s in (0, 1, 2): print('HY' if hy else 'noHY', 'slack', s, [c[:3] for c in sc if c[3] == s])
def decomp(N, M, S, pieces):
    pieces = sorted(set(pieces)); res = []
    def rec(i, n, m, s, ch):
        if (n, m, s) == (N, M, S): res.append(tuple(ch)); return
        if i == len(pieces) or n > N or m > M or s > S: return
        p = pieces[i]; k = 0
        while n + k*p[0] <= N and m + k*p[1] <= M and s + k*p[3] <= S:
            rec(i + 1, n + k*p[0], m + k*p[1], s + k*p[3], ch + [p[:3]] * k); k += 1
    rec(0, 0, 0, 0, []); return res
for hy in (True, False):
    P = slack(17, 2, hy) + [(1, 0, 0, 3)]
    for (N, M, S) in [(16, 9, 0), (17, 13, 0), (16, 10, 2), (13, 9, 2), (13, 8, 0), (15, 11, 1)]:
        print('HY' if hy else 'noHY', 'decomp', (N, M, S), decomp(N, M, S, P))
# degree bounds
for (n, m, t, nprev, name) in [(17, 12, 7, 16, 'Lemma17'), (18, 16, 8, 17, 'Thm1'), (17, 13, 7, 16, 'LemmaR17'), (14, 12, 6, 13, 'LemmaR14'), (18, 11, 7, 17, 'Step3.2')]:
    # tau(H-v) >= t-1 and 11 tau(H-v) <= 3(n-1) + 2(m-d)  ->  max d
    dmax = max(d for d in range(0, m + 1) if 11 * (t - 1) <= 3 * (n - 1) + 2 * (m - d))
    tv_le_t = all(11 * t > 3 * (n - 1) + 2 * (m - d) for d in range(0, m + 1))
    # with all degrees <= dmax: sum d = 3m <= dmax*d_top + (dmax-1)*(n-d_top)
    dtop = min(k for k in range(n + 1) if 3 * m <= dmax * k + (dmax - 1) * (n - k))
    print(name, (n, m, t), 'max degree', dmax, '| tau(H-v)=t-1 for all v:', tv_le_t, '| at least', dtop, 'vertices of degree', dmax,
          '| slack of H-v at max degree:', 3*(n-1) + 2*(m-dmax) - 11*(t-1))
