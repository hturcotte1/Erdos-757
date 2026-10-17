"""Referee (L013 round 2): brute-force decompositions, written from scratch.
A decomposition of (N, M) with total slack S: a multiset of component types summing to (N, M, T), T = (3N+2M-S)/11, every type
either the isolated vertex (1,0,0) or a connected type (n,m,tau) with n >= 3, n <= 2m+1, m <= n-2, 1 <= tau <= m, 17tau <= 5n+3m,
and slack 3n+2m-11tau >= 0 (I11 below the current n).  Generated part by part over ALL integer partitions of N (parts of every
size 1..N, including 2, which then simply has no type), with (m, tau) ranging over 0..n and 0..m before filtering."""
import sys, json, os, math, itertools
from functools import lru_cache
def types_of(n):
    out = []
    for m in range(0, n + 1):
        for t in range(0, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if s < 0: continue
            if n == 1 and m == 0 and t == 0: out.append((n, m, t)); continue
            if n >= 3 and m >= 1 and n <= 2 * m + 1 and m <= n - 2 and 1 <= t <= m and 17 * t <= 5 * n + 3 * m:
                out.append((n, m, t))
    return out
def decomps(N, M, S):
    if (3 * N + 2 * M - S) % 11 != 0: return []
    T = (3 * N + 2 * M - S) // 11
    alltypes = sorted([ty for n in range(1, N + 1) for ty in types_of(n)], reverse=True)
    res = []
    def rec(i, n, m, t, cur):
        if n == N:
            if m == M and t == T: res.append(tuple(cur))
            return
        for j in range(i, len(alltypes)):
            ty = alltypes[j]
            if n + ty[0] <= N and m + ty[1] <= M and t + ty[2] <= T:
                cur.append(ty); rec(j, n + ty[0], m + ty[1], t + ty[2], cur); cur.pop()
    rec(0, 0, 0, 0, [])
    return [tuple(sorted(r)) for r in res]
if __name__ == '__main__':
    N, M, S = map(int, sys.argv[1:4])
    for d in decomps(N, M, S): print(list(d))
