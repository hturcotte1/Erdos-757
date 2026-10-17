"""Certificate L008, Steps 1 and 4 (exact integer arithmetic).
(a) Window cells (n,m) with n <= NMAX: connected cells (n>=3, ceil((n-1)/2) <= m <= n-2) admitting tau with
    11 tau > 3n+2m (I11 violated), 17 tau <= 5n+3m (Henning-Yeo), tau <= m.
(b) All connected cells (n,m,tau) with n <= 15 and slack s = 3n+2m-11tau in {0,1} (plus tau <= m and HY).
(c) All multisets of component types (n_i,m_i,tau_i), each a connected cell of slack 0 or 1 or an isolated vertex (1,0,0) of
    slack 3, with sum n_i = 15, sum m_i = 11 and total slack exactly 1 (no a-priori restriction on the number of slack-1 pieces).
(d) Same as (c) for (n,m) = (13,8) with total slack 0 (the L007 decomposition, as a check)."""
import sys
def conn_cells(nmax):
    for n in range(3, nmax + 1):
        for m in range((n - 1 + 1) // 2, n - 1):
            yield n, m
def window(nmax):
    out = []
    for n, m in conn_cells(nmax):
        lo = (3 * n + 2 * m) // 11 + 1; hi = min((5 * n + 3 * m) // 17, m)
        if lo <= hi: out.append((n, m, lo, hi))
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
        pn, pm, pt, ps = pieces[i]
        # choose how many copies of piece i
        k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, chosen + [pieces[i]] * k)
            k += 1
    rec(0, 0, 0, 0, [])
    return sols
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
print('(a) window cells n<=%d (n,m,lo,hi):' % NMAX, window(NMAX))
sc = slack_cells(15, 1)
print('(b) connected cells n<=15 with slack 0:', [c[:3] for c in sc if c[3] == 0])
print('    connected cells n<=15 with slack 1:', [c[:3] for c in sc if c[3] == 1])
pieces = sc + [(1, 0, 0, 3)]
print('(c) decompositions of (15,11) with total slack 1:', [[p[:3] for p in d] for d in decompositions(15, 11, 1, pieces)])
print('(d) decompositions of (13,8) with total slack 0:', [[p[:3] for p in d] for d in decompositions(13, 8, 0, pieces)])
