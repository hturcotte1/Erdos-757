#!/usr/bin/env python3
"""Referee L016 round 1 (own code): component-type decompositions of X - w by brute force.
A type is (1,0,0) (isolated vertex, slack 3) or a connected type (n,m,t) with n >= 3, ceil((n-1)/2) <= m <= n-2,
1 <= t <= m and slack 3n+2m-11t >= 0 (I11 below 27 vertices, L013).  Optional extra necessary conditions:
K8 (17t <= 5n+3m) and the degree bound t >= ceil(m/D).  decomps(N, M, T) = all multisets of types with sums N, M, T."""
import sys
from functools import lru_cache

def types(maxn, k8=False, D=None):
    out = [(1, 0, 0)]
    for n in range(3, maxn + 1):
        for m in range((n - 1 + 1) // 2, n - 1):
            for t in range(1, m + 1):
                if 3 * n + 2 * m - 11 * t < 0:
                    continue
                if k8 and 17 * t > 5 * n + 3 * m:
                    continue
                if D is not None and t * D < m:
                    continue
                out.append((n, m, t))
    return sorted(out)

def decomps(N, M, T, k8=False, D=None):
    ty = types(N, k8, D)
    res = []
    def rec(i, n, m, t, cur):
        if n == 0:
            if m == 0 and t == 0:
                res.append(tuple(cur))
            return
        for j in range(i, len(ty)):
            a, b, c = ty[j]
            if a <= n and b <= m and c <= t:
                cur.append(ty[j]); rec(j, n - a, m - b, t - c, cur); cur.pop()
    rec(0, N, M, T, [])
    return res

if __name__ == '__main__':
    N, M, T = map(int, sys.argv[1:4])
    for flag in ('plain', 'K8', 'K8+deg3'):
        ds = decomps(N, M, T, k8=(flag != 'plain'), D=(3 if flag == 'K8+deg3' else None))
        print(flag, len(ds))
        for d in ds:
            print('  ', d)
