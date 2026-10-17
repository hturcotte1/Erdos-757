"""(L012) Independent check of engine.decompositions on every (N, M, S) used by the engine (BRANCH lines of out/engine.log and the two
final routes): brute force over all multisets of component types (n_i, m_i, tau_i) -- connected types (n >= 3,
ceil((n-1)/2) <= m <= n-2, 1 <= tau <= m, 17 tau <= 5n + 3m, slack >= 0) and the isolated vertex (1,0,0) -- with
sum n_i = N, sum m_i = M and sum tau_i = (3N + 2M - S)/11 (so the slacks add to S)."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import decompositions
def types(N):
    U = [(1, 0, 0)]
    for n in range(3, N + 1):
        for m in range((n) // 2, n - 1):
            if n > 2 * m + 1: continue
            for t in range(1, m + 1):
                if 17 * t <= 5 * n + 3 * m and 3 * n + 2 * m - 11 * t >= 0: U.append((n, m, t))
    return U
def bf(N, M, S):
    if (3 * N + 2 * M - S) % 11: return set()
    T = (3 * N + 2 * M - S) // 11; U = types(N); sols = set()
    def rec(i, n, m, t, ch):
        if n == N and m == M and t == T: sols.add(tuple(sorted(ch))); return
        for j in range(i, len(U)):
            a, b, c = U[j]
            if n + a <= N and m + b <= M and t + c <= T: rec(j, n + a, m + b, t + c, ch + [U[j]])
    rec(0, 0, 0, 0, []); return sols
jobs = set([(22, 17, 1), (22, 18, 3)])
for l in open('out/engine.log'):
    mm = re.match(r"\s*BRANCH \((\d+), (\d+), (\d+), (\d+)\) d=(\d+) tp=(\d+) S'=(\d+)", l)
    if mm:
        n, m, t, D, d, tp, S = map(int, mm.groups()); jobs.add((n - 1, m - d, S))
bad = []
for N, M, S in sorted(jobs):
    a = set(tuple(sorted(x)) for x in decompositions(N, M, S)); b = bf(N, M, S)
    if a != b: bad.append((N, M, S, len(a), len(b)))
print('checked', len(jobs), '(N, M, S) triples; differences:', bad)
