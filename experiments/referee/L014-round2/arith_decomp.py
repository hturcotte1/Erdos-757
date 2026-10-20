"""Referee L014 round 2: own arithmetic for the top cell and own brute-force decompositions (no prover code imported
unless --compare is given, in which case engine.decompositions is only COMPARED against).
Component types of a graph X - w in C: isolated vertex (1,0,0) [slack 3] or connected (n,m,t) with n>=3,
ceil((n-1)/2) <= m <= n-2, 1 <= t <= m, I11 slack s = 3n+2m-11t >= 0 (L011, n <= 22), optionally K8 17t <= 5n+3m."""
import sys, itertools
from math import ceil
def slack(n, m, t): return 3*n + 2*m - 11*t
def types_of_size(n, k8, smax):
    if n == 1: return [(1, 0, 0)]
    if n == 2: return []
    out = []
    for m in range(0, n - 1):           # m <= n-2
        if m < 1 or n > 2*m + 1: continue  # connected with >= 3 vertices needs m >= 1 and n <= 2m+1
        for t in range(1, m + 1):
            s = slack(n, m, t)
            if s < 0 or s > smax: continue
            if k8 and 17*t > 5*n + 3*m: continue
            out.append((n, m, t))
    return out
def partitions(n, maxp):
    if n == 0: yield (); return
    for p in range(min(n, maxp), 0, -1):
        if p == 2: continue
        for r in partitions(n - p, p): yield (p,) + r
def decomps_bf(N, M, S, k8=True):
    sols = set()
    for part in partitions(N, N):
        for combo in itertools.product(*[types_of_size(p, k8, S) for p in part]):
            if sum(c[1] for c in combo) == M and sum(slack(*c) for c in combo) == S:
                sols.add(tuple(sorted(combo)))
    return sorted(sols)
# second method: DP over (n, m, s) building sorted multisets
def decomps_dp(N, M, S, k8=True):
    T = [t for n in range(1, N + 1) for t in types_of_size(n, k8, S)]
    T.sort()
    res = []
    def rec(i, n, m, s, cur):
        if n == N and m == M and s == S: res.append(tuple(cur)); return
        for j in range(i, len(T)):
            a, b, c = T[j]; sl = slack(a, b, c)
            if n + a <= N and m + b <= M and s + sl <= S:
                rec(j, n + a, m + b, s + sl, cur + [T[j]])
    rec(0, 0, 0, 0, [])
    return sorted(set(tuple(sorted(x)) for x in res))
if __name__ == '__main__':
    n, m, t, D = 23, 21, 10, 3
    print('top key', (n, m, t, D), 'sum deg', 3*m, '2n', 2*n, 'ceil(3m/n)', ceil(3*m/n))
    for d in range(1, D + 1):
        for tp in (t - 1, t):
            Sp = 3*(n - 1) + 2*(m - d) - 11*tp
            print('  d=%d tp=%d Sp=%d %s' % (d, tp, Sp, 'feasible' if (Sp >= 0 and d >= ceil(3*m/n)) else 'excluded'))
    for k8 in (True, False):
        a = decomps_bf(22, 18, 3, k8); b = decomps_dp(22, 18, 3, k8)
        print('decompositions of (22,18) slack 3, K8=%s: bf %d dp %d %s' % (k8, len(a), len(b), 'EQUAL' if a == b else 'DIFF'))
        for x in a: print('    ', x, [slack(*c) for c in x])
    # also with smax unrestricted per component (all slacks >= 0 are bounded by total 3 anyway)
    if '--compare' in sys.argv:
        sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L014')
        import engine
        keys = []
        for l in open('/home/user/Erdos-757/experiments/prover/L014/tree_23_21_10_3.txt'):
            if l.startswith('CELL') and ' recurse ' in l:
                keys.append(eval(l.split(' recurse')[0][5:]))
        nb = nd = diff = 0
        for (n, m, t, D) in keys:
            for d in range(max(1, ceil(3*m/n)), D + 1):
                for tp in (t - 1, t):
                    Sp = 3*(n-1) + 2*(m-d) - 11*tp
                    if Sp < 0 or tp < 0: continue
                    e = sorted(tuple(sorted(x)) for x in engine.decompositions(n-1, m-d, Sp))
                    a = decomps_bf(n-1, m-d, Sp, True); a2 = decomps_bf(n-1, m-d, Sp, False); b = decomps_dp(n-1, m-d, Sp, True)
                    nb += 1; nd += len(a)
                    ok = (e == a == b)
                    if not ok: diff += 1
                    print('BRANCH', (n, m, t, D), 'd=%d tp=%d Sp=%d' % (d, tp, Sp), 'engine', len(e), 'bf', len(a), 'dp', len(b), 'bf_noK8', len(a2), 'OK' if ok else 'DIFF', '' if a == a2 else 'K8-MATTERS')
        print('SUMMARY recursion keys', len(keys), 'branches', nb, 'decompositions', nd, 'differences', diff)
