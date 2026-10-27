"""(L023) Independent brute force of the component decompositions of the two top branches of (25,23,11,4), compared with
engine.decompositions, and the input counts recomputed from the stored list sizes.
A decomposition of (N, M) with total slack S: multiset of types (n_K, m_K, tau_K): the isolated vertex (1,0,0) (slack 3) or a connected
type with n_K >= 3, ceil((n_K-1)/2) <= m_K <= n_K - 2, 1 <= tau_K <= m_K, 17 tau_K <= 5 n_K + 3 m_K, s_K = 3n_K + 2m_K - 11tau_K >= 0;
sum n_K = N, sum m_K = M, sum s_K = S.   usage: python3 decomp_bf.py CELLDIR"""
import sys, os, math, itertools, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'topcell'))
os.environ.setdefault('CELLDIR', sys.argv[1]); os.environ.setdefault('ENGINELOG', '/dev/null')
import engine
def types(nk, S):
    if nk == 1: return [(1, 0, 0)] if S >= 3 else []
    out = []
    for mk in range(math.ceil((nk - 1) / 2), nk - 1):
        for tk in range(1, mk + 1):
            s = 3 * nk + 2 * mk - 11 * tk
            if 17 * tk <= 5 * nk + 3 * mk and 0 <= s <= S: out.append((nk, mk, tk))
    return out
def partitions(N, maxpart):
    if N == 0: yield []; return
    for p in range(min(N, maxpart), 0, -1):
        if p == 2: continue
        for rest in partitions(N - p, p): yield [p] + rest
def bf(N, M, S):
    res = set()
    for P in partitions(N, N):
        choices = [types(p, S) for p in P]
        for combo in itertools.product(*choices):
            if sum(c[1] for c in combo) == M and sum(3 * c[0] + 2 * c[1] - 11 * c[2] for c in combo) == S:
                res.add(tuple(sorted(combo, reverse=True)))
    return res
def size(typ, d):
    if typ == (1, 0, 0): return 1
    fn = os.path.join(sys.argv[1], 'cell_%d_%d_%d_D%d.txt' % (typ + (d,)))
    return sum(1 for l in open(fn) if l.startswith('FOUND:'))
n, m, t, D = 25, 23, 11, 4
tot_all = 0
for d in range(math.ceil(3 * m / n), D + 1):
    for tp in (t - 1, t):
        S = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if S < 0: print('branch d=%d tp=%d S=%d < 0: none' % (d, tp, S)); continue
        mine = bf(n - 1, m - d, S)
        eng = set(tuple(sorted(dec, reverse=True)) for dec in engine.decompositions(n - 1, m - d, S))
        print('branch d=%d tp=%d S=%d: brute force %d decompositions, engine %d, %s' % (d, tp, S, len(mine), len(eng), 'EQUAL' if mine == eng else 'DIFFERENT'))
        tot = 0
        for dec in sorted(mine):
            cnt = 1
            for typ in sorted(set(dec)):
                k = dec.count(typ); c = size(typ, d); cnt *= math.comb(c + k - 1, k)
            print('   ', list(dec), 'inputs', cnt); tot += cnt
        print('   branch inputs', tot); tot_all += tot
print('TOTAL inputs', tot_all)
