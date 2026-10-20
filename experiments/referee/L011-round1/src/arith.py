"""Referee L011 round 1: all arithmetic of the certificate, from scratch (exact integers only).
(1) window cells n<=22 (every violating tau, not only the least), with and without K8;
(2) degree bounds by the direct inequality (no closed formula), and the forced value tau(H-v)=tau-1;
(3) counting impossibilities;
(4) connected component types with slack in [0,S] (n<=21), with and without K8, incl. the isolated vertex;
(5) decompositions by brute force over multisets of component types (each component: connected => n<=2m+1 or (n,m)=(1,0);
    (P3) => m<=n-2 for n>=2; tau<=m; slack>=0 (I11 below N)); total slack exactly S; with and without K8;
(6) record cells / Corollary 3 / Remarks 4,5."""
import math, itertools, sys

def comp_types(nmax, smax, use_k8=True):
    out = [(1, 0, 0)]                       # isolated vertex: slack 3
    for n in range(3, nmax + 1):
        for m in range(1, n - 1):           # m <= n-2
            if n > 2 * m + 1: continue      # connected
            for t in range(0, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if s < 0 or s > smax: continue
                if use_k8 and 17 * t > 5 * n + 3 * m: continue
                out.append((n, m, t))
    return [c for c in out if 3 * c[0] + 2 * c[1] - 11 * c[2] <= smax]

def slack(c): return 3 * c[0] + 2 * c[1] - 11 * c[2]

def decomps(N, M, S, use_k8=True):
    types = sorted(comp_types(N, S, use_k8))
    res = []
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S:
            res.append(tuple(chosen)); return
        if i >= len(types): return
        c = types[i]
        # choose multiplicity k of type i
        k = 0
        while n + k * c[0] <= N and m + k * c[1] <= M and s + k * slack(c) <= S:
            rec(i + 1, n + k * c[0], m + k * c[1], s + k * slack(c), chosen + [c] * k)
            k += 1
            if c[0] == 0: break
    rec(0, 0, 0, 0, [])
    return sorted(set(res))

def window_cells(n, use_k8=True):
    out = []
    for m in range(1, n - 1):
        if n > 2 * m + 1: continue          # violator is connected (component argument)
        for t in range(0, m + 1):
            if 11 * t <= 3 * n + 2 * m: continue
            if use_k8 and 17 * t > 5 * n + 3 * m: continue
            out.append((n, m, t))
    return out

def degree_bound(n, m, t):
    """largest d such that a vertex of degree d is consistent: H-v has n-1 vertices, m-d edges, tau(H-v) in {t-1,t},
    and I11 holds on n-1 vertices. Returns (dmax, forced tau(H-v) values)."""
    ok = []
    forced = set()
    for d in range(0, m + 1):
        poss = [tv for tv in (t - 1, t) if 11 * tv <= 3 * (n - 1) + 2 * (m - d)]
        if poss: ok.append(d); forced |= set(poss)
    return (max(ok) if ok else None), sorted(forced)

if __name__ == '__main__':
    print('== (1) window cells (connected, m<=n-2, tau<=m, I11 violated) ==')
    allw = []
    for n in range(3, 23):
        w = window_cells(n); allw += w
        w0 = window_cells(n, use_k8=False)
        if n >= 19: print(' n=%d with K8:' % n, w, '| without K8 (count):', len(w0))
    print(' number of window cells n<=22 with K8:', len(allw))
    print('== (2) degree bounds and forced tau(H-v) ==')
    for c in window_cells(21) + window_cells(22):
        n, m, t = c; s = 3 * n + 2 * m - 11 * t
        dmax, forced = degree_bound(n, m, t)
        print(' cell', c, 'slack', s, 'dmax', dmax, 'tau(H-v) possible', forced, '3m', 3 * m, '2n', 2 * n,
              'count-impossible(dmax<=2 and 3m>2n):', dmax <= 2 and 3 * m > 2 * n,
              'K8 tau max', (5 * n + 3 * m) // 17)
    print('== (4) component types with slack <= 3, n <= 21 ==')
    for use in (True, False):
        ct = comp_types(21, 3, use)
        for s in range(4):
            print(' K8=%s slack %d:' % (use, s), [c for c in ct if slack(c) == s])
    print('== (5) decompositions ==')
    jobs = [(20, 9, 1), (19, 11, 2), (20, 14, 0), (20, 10, 3), (21, 13, 1)]
    for N, M, S in jobs:
        a = decomps(N, M, S, True); b = decomps(N, M, S, False)
        print(' (%d,%d) slack %d: %d decompositions; without K8: %d; equal: %s' % (N, M, S, len(a), len(b), a == b))
        for x in a:
            print('    ', ' + '.join('(%d,%d,%d)' % c for c in x))
    # an extra robustness check: decompositions with each component only required to have slack >= 0 (no cap 3)
    print('== (6) Corollary 3 / Remark 5 record cells ==')
    for n in range(3, 41):
        hmax = math.ceil(4 * n / 7) - 1
        if 7 * hmax >= 4 * n: hmax -= 1
        assert 7 * hmax < 4 * n and 7 * (hmax + 1) >= 4 * n
        tmin = n - hmax
        hy = [(m, t) for m in range(0, n - 1) for t in range(tmin, m + 1) if 17 * t <= 5 * n + 3 * m]
        i11 = [(m, t, 3 * n + 2 * m - 11 * t) for (m, t) in hy if 11 * t <= 3 * n + 2 * m]
        if hy: print(' n=%d h<=%d HY-feasible %s I11-allowed %s' % (n, hmax, hy, i11))
    print('== Remark 4 ==')
    n = 21
    for m in range(0, 20):
        for t in range(0, m + 1):
            if 11 * t <= 3 * n + 2 * m and 17 * t <= 5 * n + 3 * m and t >= 9:
                print(' n=21 allowed (m,tau) with tau>=9:', (m, t), 'slack', 3 * n + 2 * m - 11 * t, 'K8 rhs', 5 * n + 3 * m)
    print(' f(22) lower bound from Theorem 1: tau <= floor((66+2*20)/11) =', (66 + 40) // 11, '-> h >=', 22 - (66 + 40) // 11)
    print(' HY alone at n=22: tau <= floor((110+60)/17) =', (110 + 60) // 17, '-> h >=', 22 - (110 + 60) // 17)
    print(' ceil(4*22/7) =', -(-88 // 7))
    print('== (7) robustness: window cells WITHOUT K8 at n=21,22 that K8 excludes are impossible by the degree lemma alone ==')
    for n in (21, 22):
        extra = [c for c in window_cells(n, use_k8=False) if c not in window_cells(n)]
        worst = max(degree_bound(*c)[0] if degree_bound(*c)[0] is not None else -1 for c in extra)
        print(' n=%d: %d extra cells; max degree bound over them = %d (<= 1 is impossible for a connected violator with n > 3)' % (n, len(extra), worst))
