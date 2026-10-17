"""Certificate L011 (exact integer arithmetic; prover's own script, extending L010's decomp20.py).
(a) window cells n <= 22 (slack at the least violating tau, degree bound floor((s+8)/2), 3m vs 2n);
(b) connected cells with slack 0..3 for n <= 21;
(c) decompositions of the graphs met in the proof, by TWO independent generators that must agree:
    G1 (slack-sum): multisets of piece types (connected cells of slack <= S, and the isolated vertex (1,0,0) of slack 3)
        with sum n = N, sum m = M and total slack exactly S;
    G2 (partition-first): integer partitions of N into parts that are 1 or >= 3; for every part every (m_i, tau_i) with
        m_i <= n_i-2, n_i <= 2m_i+1, tau_i <= m_i, 17 tau_i <= 5n_i+3m_i and slack in [0, 3] (part 1: (0,0)), kept iff
        sum m_i = M and sum tau_i = T (T = (3N+2M-S)/11);
(d) record cells (n,m,tau): m <= n-2, tau <= m, HY, I11 slack >= 0, h = n-tau <= ceil(4n/7)-1, for n <= 40."""
import sys, math, itertools
from collections import Counter
def conn_cells(nmax):
    for n in range(3, nmax + 1):
        for m in range((n - 1 + 1) // 2, n - 1):
            yield n, m
def window(nmax):
    out = []
    for n, m in conn_cells(nmax):
        lo = (3 * n + 2 * m) // 11 + 1; hi = min((5 * n + 3 * m) // 17, m)
        if lo <= hi:
            s = 3 * n + 2 * m - 11 * lo; out.append((n, m, lo, s, (s + 8) // 2, 3 * m, 2 * n))
    return out
def slack_cells(nmax, smax):
    out = []
    for n, m in conn_cells(nmax):
        for t in range(0, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if 0 <= s <= smax and 17 * t <= 5 * n + 3 * m: out.append((n, m, t, s))
    return out
def gen1(N, M, S):
    pieces = slack_cells(N, S) + [(1, 0, 0, 3)]; sols = []
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S: sols.append(tuple(sorted(chosen))); return
        if i == len(pieces): return
        pn, pm, pt, ps = pieces[i]; k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, chosen + [(pn, pm, pt)] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sorted(set(sols))
def gen2(N, M, S):
    if (3 * N + 2 * M - S) % 11: return []
    T = (3 * N + 2 * M - S) // 11
    def types(n):
        if n == 1: return [(1, 0, 0)]
        out = []
        for m in range(0, n - 1):
            if n > 2 * m + 1: continue
            for t in range(0, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= 3 and 17 * t <= 5 * n + 3 * m: out.append((n, m, t))
        return out
    def partitions(n, maxpart):
        if n == 0: yield []; return
        for p in range(min(n, maxpart), 0, -1):
            if p == 2: continue
            for rest in partitions(n - p, p): yield [p] + rest
    sols = set()
    for part in partitions(N, N):
        for combo in itertools.product(*[types(p) for p in part]):
            if sum(c[1] for c in combo) == M and sum(c[2] for c in combo) == T:
                sols.add(tuple(sorted(combo)))
    return sorted(sols)
if __name__ == '__main__':
    print('(a) window cells n in {21,22} (n, m, least violating tau, slack, degree bound, 3m, 2n):')
    for w in window(22):
        if w[0] >= 21: print('   ', w)
    print('    number of window cells n<=22:', len(window(22)))
    sc = slack_cells(21, 3)
    for s in (0, 1, 2, 3): print('(b) connected cells n<=21 with slack %d:' % s, [c[:3] for c in sc if c[3] == s])
    jobs = [(20, 9, 1, 'G for (21,12,8)'), (20, 14, 0, 'G for (21,17,9)'), (19, 11, 2, "G' for connected (20,14,8)"),
            (21, 13, 1, 'G for (22,16,9)'), (20, 10, 3, "G' for connected (21,13,8)"),
            (17, 9, 3, 'L010 check'), (18, 12, 1, 'L010 check'), (19, 10, 0, 'L010 check'), (16, 10, 2, 'L009 check'), (13, 9, 2, 'L009 check')]
    for N, M, S, why in jobs:
        a, b = gen1(N, M, S), gen2(N, M, S)
        print('(c) (%d,%d) total slack %d [%s]: G1 %d, G2 %d, %s' % (N, M, S, why, len(a), len(b), 'EQUAL' if a == b else 'DIFFERENT'))
        for x in a: print('       ', list(x))
    print('(d) record cells (n, m, tau, slack) with I11 slack >= 0, n <= 40:')
    for n in range(3, 41):
        hmax = math.ceil(4 * n / 7) - 1; tmin = n - hmax
        cells = [(n, m, t, 3 * n + 2 * m - 11 * t) for m in range(0, n - 1) for t in range(tmin, m + 1)
                 if 17 * t <= 5 * n + 3 * m and 11 * t <= 3 * n + 2 * m]
        hy = [(m, t) for m in range(0, n - 1) for t in range(tmin, m + 1) if 17 * t <= 5 * n + 3 * m]
        if hy or cells: print('    n=%d h<=%d: HY-feasible (m,tau): %s; I11-allowed: %s' % (n, hmax, hy, cells))
