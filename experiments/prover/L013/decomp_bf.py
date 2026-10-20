"""(L013, prover) Independent decomposition generator (partition-first; written from scratch, imports nothing from the engine).
A decomposition of (N, M) with total slack S is a multiset of component types whose vertex counts, edge counts and I11 slacks add up to
N, M and S, where a type is either the isolated vertex (1,0,0) (slack 3) or a connected type (p, m, t) with p >= 3,
p <= 2m+1 (connected), m <= p-2 (P3), 1 <= t <= m, 17t <= 5p+3m (K8) and slack 3p+2m-11t >= 0 (I11 below the current size).
Method: every integer partition of N into parts 1 or >= 3 (non-increasing), then every choice of a type for each part (pruned only by the
facts that partial edge sums cannot exceed M and partial slack sums cannot exceed S, both implied by non-negativity), kept iff the edge
sum is M and the slack sum is S.  Output: set of sorted tuples of types."""
from functools import lru_cache
@lru_cache(maxsize=None)
def types_of(p):
    if p == 1: return ((1, 0, 0),)
    out = []
    for m in range(0, p - 1):
        if p > 2 * m + 1: continue
        for t in range(1, m + 1):
            if 17 * t <= 5 * p + 3 * m and 3 * p + 2 * m - 11 * t >= 0: out.append((p, m, t))
    return tuple(out)
def partitions(n, maxp):
    if n == 0: yield (); return
    for p in range(min(n, maxp), 0, -1):
        if p == 2: continue
        for rest in partitions(n - p, p): yield (p,) + rest
def bf_decomps(N, M, S):
    sols = set()
    for part in partitions(N, N):
        def rec(i, msum, ssum, chosen):
            if msum > M or ssum > S: return
            if i == len(part):
                if msum == M and ssum == S: sols.add(tuple(sorted(chosen)))
                return
            for ty in types_of(part[i]):
                rec(i + 1, msum + ty[1], ssum + 3 * ty[0] + 2 * ty[1] - 11 * ty[2], chosen + [ty])
        rec(0, 0, 0, [])
    return sols
if __name__ == '__main__':
    import sys
    N, M, S = map(int, sys.argv[1:4])
    for d in sorted(bf_decomps(N, M, S)): print(list(d))
