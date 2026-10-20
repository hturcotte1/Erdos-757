"""Referee (L014 round 3): own brute-force decompositions of (N, M) into component types with total I11 slack S.
Component types: isolated vertex (1,0,0) [slack 3] or connected type (n,m,t): n>=3, ceil((n-1)/2) <= m <= n-2, 1 <= t <= m,
17t <= 5n+3m (K8), slack s = 3n+2m-11t >= 0 (I11, valid for n <= 22 by L011).  Partition-first: integer partitions of N into
parts 1 or >= 3, every assignment of types to parts, kept iff sum m = M and sum slack = S.  Returns sorted multisets."""
import itertools, sys
def types(n, S):
    if n == 1: return [(1, 0, 0)]
    out = []
    for m in range((n - 1 + 1) // 2, n - 1):
        for t in range(1, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if 0 <= s <= S and 17 * t <= 5 * n + 3 * m: out.append((n, m, t))
    return out
def partitions(n, maxpart):
    if n == 0: yield []; return
    for p in range(min(n, maxpart), 0, -1):
        if p == 2: continue
        for rest in partitions(n - p, p): yield [p] + rest
def decompositions_bf(N, M, S):
    sols = set()
    for part in partitions(N, N):
        if sum(1 for p in part if p == 1) * 3 > S: continue
        for combo in itertools.product(*[types(p, S) for p in part]):
            if sum(c[1] for c in combo) == M and sum(3 * c[0] + 2 * c[1] - 11 * c[2] for c in combo) == S:
                sols.add(tuple(sorted(combo)))
    return sorted(sols)
if __name__ == '__main__':
    N, M, S = map(int, sys.argv[1:4])
    for d in decompositions_bf(N, M, S): print(list(d))
