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
