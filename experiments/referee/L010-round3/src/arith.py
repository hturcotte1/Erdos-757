"""Referee L010 round 3: exact arithmetic re-derivation (written from scratch).
(a) window cells for n<=20: connected cells (n>=3, n<=2m+1, m<=n-2), lo=floor((3n+2m)/11)+1 (least tau violating I11),
    hy=min(floor((5n+3m)/17), m); window iff lo<=hy.  Also the cells that would appear WITHOUT the connectivity bound n<=2m+1.
(b) degree bounds from the inequality itself (no closed formula): for each d, test 11*(tau-1) <= 3(N-1)+2(m-d) and that tau(H-v)=tau is impossible.
(c) connected cells of slack 0..3 with n<=19, with and without the HY filter.
(d) decompositions of (N,M) with total slack S into multisets of pieces = connected cells of slack <= S plus the isolated vertex (1,0,0) of slack 3."""
import sys
def conn_cells(nmax):
    for n in range(3, nmax + 1):
        for m in range(0, n - 1):           # m <= n-2 by (P3); n <= 2m+1 for connected graphs with m>=1
            if m >= 1 and n <= 2 * m + 1: yield n, m
def window(nmax, need_conn=True):
    out = []
    for n in range(2, nmax + 1):
        for m in range(0, n - 1):
            if need_conn and (m == 0 or n > 2 * m + 1): continue
            lo = (3 * n + 2 * m) // 11 + 1; hy = min((5 * n + 3 * m) // 17, m)
            if lo <= hy: out.append((n, m, lo, hy, 3 * n + 2 * m - 11 * lo))
    return out
print('(a) window cells, connected cells only, n<=20:')
W = window(20)
for w in W: print('    (n,m)=(%d,%d) tau in [%d,%d] slack at lo = %d' % w)
print('    count:', len(W))
print('(a2) window cells n=19,20 WITHOUT the connectivity bound (these need 0.3):')
for w in window(20, need_conn=False):
    if w[0] >= 19 and w not in W: print('    ', w)
print('(b) degree bounds for n=19,20 window cells, from the inequality 11*tau(H-v) <= 3(N-1)+2(m-d):')
for (n, m, lo, hy, s) in W:
    if n < 19: continue
    t = lo
    assert lo == hy, 'more than one admissible tau'
    # tau(H-v) in {t-1, t}; tau(H-v)=t requires 11t <= 3(n-1)+2(m-d) for some d>=0:
    forced = 11 * t > 3 * (n - 1) + 2 * m
    dmax = max(d for d in range(0, m + 1) if 11 * (t - 1) <= 3 * (n - 1) + 2 * (m - d))
    hy_tau = (5 * n + 3 * m) // 17
    print('    (%d,%d,%d): s=%d, tau(H-v)=%d forced: %s, d <= %d, HY gives tau <= %d, sum deg = %d vs 2n = %d -> %s' % (
        n, m, t, s, t - 1, forced, dmax, hy_tau, 3 * m, 2 * n, 'IMPOSSIBLE by counting' if dmax <= 2 and 3 * m > dmax * n else 'ok'))
def slack_cells(nmax, smax, hy=True):
    out = []
    for n, m in conn_cells(nmax):
        for t in range(0, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if 0 <= s <= smax and (not hy or 17 * t <= 5 * n + 3 * m): out.append((n, m, t, s))
    return out
for hy in (True, False):
    sc = slack_cells(19, 3, hy)
    print('(c) connected cells n<=19 by slack, HY filter =', hy)
    for s in range(4): print('    slack %d:' % s, [c[:3] for c in sc if c[3] == s])
sc = slack_cells(19, 3, True)
def decomps(N, M, S, pieces):
    pieces = sorted(set(pieces))
    sols = []
    def rec(i, n, m, s, chosen):
        if (n, m, s) == (N, M, S): sols.append(tuple(chosen)); return
        if i == len(pieces) or n > N or m > M or s > S: return
        pn, pm, pt, ps = pieces[i]
        k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, chosen + [(pn, pm, pt)] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sols
pieces = sc + [(1, 0, 0, 3)]
for (N, M, S) in [(18, 12, 1), (17, 9, 3), (19, 10, 0), (16, 9, 0), (16, 10, 2), (13, 9, 2), (17, 13, 0)]:
    D = decomps(N, M, S, pieces)
    print('(d) decompositions of (%d,%d) with total slack %d: %d' % (N, M, S, len(D)))
    for d in D: print('      ', list(d))
# the same without HY: must be identical lists
pieces2 = slack_cells(19, 3, False) + [(1, 0, 0, 3)]
for (N, M, S) in [(18, 12, 1), (17, 9, 3), (19, 10, 0)]:
    assert decomps(N, M, S, pieces) == decomps(N, M, S, pieces2), 'HY matters for decompositions'
print('(d2) decompositions identical with and without HY: ok')
