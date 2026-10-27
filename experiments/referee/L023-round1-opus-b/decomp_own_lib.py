"""Referee L023 (opus-b): own generator of the component-type decompositions (necessary conditions only) compared with the engine's
engine.decompositions (the code under test, imported from the worker's src/ only for the comparison), for the branches of the top key
and of the five GAP keys.  A component type is the isolated vertex (1,0,0) (slack 3) or (n,m,t) with n >= 3, ceil((n-1)/2) <= m <= n-2,
1 <= t <= m, 17t <= 5n+3m (K8) and slack 3n+2m-11t >= 0 (I11, L013 Thm 1, n <= 26)."""
import sys, math
def types(nmax):
    T = [(1, 0, 0)]
    for n in range(3, nmax + 1):
        for m in range(-(-(n - 1) // 2), n - 1):
            for t in range(1, m + 1):
                if 17 * t <= 5 * n + 3 * m and 3 * n + 2 * m - 11 * t >= 0: T.append((n, m, t))
    return T
def own(N, M, S):
    T = sorted(types(N), reverse=True); out = []
    sl = lambda p: 3 * p[0] + 2 * p[1] - 11 * p[2]
    def rec(start, n, m, s, ch):
        if n == N:
            if m == M and s == S: out.append(tuple(sorted(ch)))
            return
        for i in range(start, len(T)):
            p = T[i]
            if n + p[0] <= N and m + p[1] <= M and s + sl(p) <= S: rec(i, n + p[0], m + p[1], s + sl(p), ch + [p])
    rec(0, 0, 0, 0, [])
    return sorted(set(out))
