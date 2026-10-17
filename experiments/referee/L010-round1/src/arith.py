"""Referee L010 r1: all arithmetic of the certificate from scratch (exact integers).
(a) window cells n <= 20 (connected range ceil((n-1)/2) <= m <= n-2, lo = floor((3n+2m)/11)+1 <= min(hy, m), hy = floor((5n+3m)/17));
(b) degree bound for every window cell with n in {19, 20} from I11 at n-1: for every vertex v, 11*tau(H-v) <= 3(n-1)+2(m-d),
    tau(H-v) >= tau-1;  we compute directly the largest d compatible, without the closed formula;
(c) slack-k cells (connected range, tau <= m, with and without Henning-Yeo) and the isolated vertex (1,0,0) of slack 3;
(d) every multiset of components (cells of slack >= 0, isolated vertices allowed) with prescribed (n, m, total slack),
    by brute-force recursion over all candidate cells; reported with and without the HY filter on component cells."""
import math, itertools, json, sys
def cells(nmax, kmax, hy=True):
    out = [(1, 0, 0)]  # isolated vertex
    for n in range(3, nmax + 1):
        for m in range(math.ceil((n - 1) / 2), n - 1):
            for t in range(0, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= kmax and (not hy or 17 * t <= 5 * n + 3 * m):
                    out.append((n, m, t))
    return out
def slack(c): n, m, t = c; return 3 * n + 2 * m - 11 * t
def decomps(N, M, S, hy=True):
    cand = sorted(c for c in cells(N, S, hy) if c[0] <= N and c[1] <= M)
    res = []
    def rec(i, n, m, s, cur):
        if n == N and m == M and s == S: res.append(tuple(cur)); return
        if n >= N or i >= len(cand): return
        for j in range(i, len(cand)):
            c = cand[j]
            if n + c[0] <= N and m + c[1] <= M and s + slack(c) <= S:
                cur.append(c); rec(j, n + c[0], m + c[1], s + slack(c), cur); cur.pop()
    rec(0, 0, 0, 0, [])
    return res
print('(a) window cells n<=20:')
W = []
for n in range(3, 21):
    for m in range(math.ceil((n - 1) / 2), n - 1):
        lo = (3 * n + 2 * m) // 11 + 1; hy = (5 * n + 3 * m) // 17
        if lo <= min(hy, m): W.append((n, m, list(range(lo, min(hy, m) + 1))))
for w in W: print('  ', w, 'slack', [3 * w[0] + 2 * w[1] - 11 * t for t in w[2]])
print('  count', len(W))
print('(b) degree bounds for n in {19,20}:')
for n, m, ts in W:
    if n < 19: continue
    for t in ts:
        # largest d such that some value tau(H-v) in {t-1, t} satisfies 11*tau(H-v) <= 3(n-1)+2(m-d)
        ok = [d for d in range(0, m + 1) if any(11 * tv <= 3 * (n - 1) + 2 * (m - d) for tv in (t - 1, t))]
        dmax = max(ok) if ok else None
        forced = all(11 * t > 3 * (n - 1) + 2 * (m - d) for d in range(0, m + 1))
        print('   (%d,%d,%d) s=%d: d<=%s; tau(H-v)=tau-1 forced for every d: %s; 3m=%d vs 2n=%d' % (n, m, t, 3*n+2*m-11*t, dmax, forced, 3*m, 2*n))
for k in range(4):
    print('(c) slack-%d cells n<=19 (HY):' % k, [c for c in cells(19, k) if slack(c) == k])
    print('    without HY extra:', sorted(set(c for c in cells(19, k, False) if slack(c) == k) - set(cells(19, k))))
for (N, M, S) in [(18, 12, 1), (17, 9, 3), (19, 10, 0), (16, 9, 0), (17, 13, 0), (16, 10, 2), (13, 9, 2)]:
    D = decomps(N, M, S); D2 = decomps(N, M, S, False)
    print('(d) (%d,%d) slack %d: %d decompositions (HY)%s' % (N, M, S, len(D), '' if set(D) == set(D2) else ' ; without HY: %d, extra %s' % (len(D2), sorted(set(D2) - set(D)))))
    for d in D: print('     ', list(d))
