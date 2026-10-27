"""Referee L023 (opus-b): own generator of the component-type decompositions (necessary conditions only) compared with the engine's
engine.decompositions (the code under test, imported from the worker's src/ only for the comparison), for the branches of the top key
and of the five GAP keys.  A component type is the isolated vertex (1,0,0) (slack 3) or (n,m,t) with n >= 3, ceil((n-1)/2) <= m <= n-2,
1 <= t <= m, 17t <= 5n+3m (K8) and slack 3n+2m-11t >= 0 (I11, L013 Thm 1, n <= 26)."""
import sys, math
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/src')
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
import engine
keys = [(25, 23, 11, 4), (25, 23, 11, 3), (24, 20, 10, 3), (23, 17, 9, 3), (21, 19, 9, 3), (20, 16, 8, 3), (17, 15, 7, 3)]
for (n, m, t, D) in keys:
    for d in range(1, D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if d < math.ceil(3 * m / n) or Sp < 0: continue
            a = own(n - 1, m - d, Sp); b = sorted(set(tuple(sorted(x)) for x in engine.decompositions(n - 1, m - d, Sp)))
            print('key %s branch d=%d tp=%d S=%d: own %d engine %d %s' % ((n, m, t, D), d, tp, Sp, len(a), len(b), 'EQUAL' if a == b else 'DIFFERENT'))
            if (n, m, t) == (25, 23, 11) or a != b:
                for x in a: print('     ', list(x))
