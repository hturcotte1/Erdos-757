"""Theorem 5 (folding lemma) tested with independent code.
usage: test_fold.py cell <path> <K> [p3brute_limit]   |   test_fold.py random <N> <seed>
For every stored graph K (in C), every degree-2 vertex x with edges {x,u,u'},{x,w,w'}, every y in {u,u'}, z in {w,w'}
not adjacent in K: build K° and check
 (a) m(K°) = m-2 with all image edges distinct 3-sets; n(K°) = n-2; deg(zeta) = d(y)+d(z)-2; Delta(K°) <= max(Delta, d(y)+d(z)-2)
 (b) tau(K) <= tau(K°)+1  [also tau(K°) <= tau(K)]
 (c) x co-transversal => tau(K°) = tau(K)-1 and s(K°) = s(K)+1
 (d) K° linear <=> y,z have no common neighbour in K-x; every F7 copy of K° contains zeta;
     (P3 of K°) <=> no saturated S of K with x notin S, y,z in S (brute force, n <= limit); such S has |S| >= 6
 (e') if K° in C then s(K°) >= 0 (I11 below 27 vertices, L016) and, when K° in C and x co-transversal, s(K°) = s(K)+1.
"""
import sys, itertools, random, collections
from ref import *

def check_graph(n, E, st, inC_known, brute_limit):
    V = set(range(n))
    t, Ts, co = cotransversal_vertices(E)
    s = 3 * n + 2 * len(E) - 11 * t
    d = degrees(V, E)
    Delta = max(d.values())
    st['graphs'] += 1
    sat_cache = None
    for x in range(n):
        if d[x] != 2:
            continue
        e1, e2 = [e for e in E if x in e]
        A = sorted(e1 - {x}); B = sorted(e2 - {x})
        assert not (e1 & e2) - {x}
        for y in A:
            for z in B:
                if adjacent(E, y, z):
                    st['adjacent'] += 1
                    continue
                V2, E2 = fold(V, E, x, y, z)
                st['folds'] += 1
                # (a)
                ok_a = (len(E2) == len(E) - 2 and all(len(f) == 3 for f in E2) and len(set(E2)) == len(E2)
                        and len(V2) == n - 2)
                d2 = degrees(V2, E2)
                if d2[y] != d[y] + d[z] - 2: ok_a = False
                if max(d2.values()) > max(Delta, d[y] + d[z] - 2): ok_a = False
                if any(d2[v] > d[v] for v in V2 if v != y): ok_a = False
                if not ok_a:
                    st['a_fail'] += 1
                t2 = tau(E2)
                # (b)
                if not (t <= t2 + 1): st['b_fail'] += 1
                if not (t2 <= t): st['b2_fail'] += 1
                # (c)
                if x in co:
                    st['folds_cotrans'] += 1
                    s2 = 3 * (n - 2) + 2 * len(E2) - 11 * t2
                    if t2 != t - 1 or s2 != s + 1: st['c_fail'] += 1
                if not inC_known:
                    continue
                # (d) linearity <=> common neighbour in K-x
                Ex = [e for e in E if x not in e]
                nb_y = set().union(*[e for e in Ex if y in e]) - {y} if any(y in e for e in Ex) else set()
                nb_z = set().union(*[e for e in Ex if z in e]) - {z} if any(z in e for e in Ex) else set()
                common = (nb_y & nb_z) - {y, z}
                lin2 = is_linear(E2)
                if lin2 != (len(common) == 0): st['d_lin_fail'] += 1
                # F7 copies all contain zeta
                if lin2:
                    cps = f7_copies(E2)
                    for cp in cps:
                        if not any(y in e for e in cp): st['d_f7_fail'] += 1
                    if cps: st['f7_blocked'] += 1
                # P3 criterion
                if n <= brute_limit:
                    p3ok = p3_brute(V2, E2)[0]
                    if sat_cache is None:
                        sat_cache = saturated_sets(V, E)
                    S_block = [S for S in sat_cache if x not in S and y in S and z in S]
                    if p3ok != (len(S_block) == 0): st['d_p3_fail'] += 1
                    for S in S_block:
                        if len(S) < 6: st['d_size_fail'] += 1
                        st['block_sizes'][len(S)] += 1
                    if not p3ok: st['p3_blocked'] += 1
                else:
                    p3ok = p3_hall(V2, E2)
                    if not p3ok: st['p3_blocked'] += 1
                if not lin2: st['nonlinear'] += 1
                inC2 = lin2 and (not cps if lin2 else False) and p3ok
                if inC2:
                    st['fold_inC'] += 1
                    s2 = 3 * (n - 2) + 2 * len(E2) - 11 * t2
                    if s2 < 0: st['I11_fail_inC'] += 1
                    if x in co and s2 != s + 1: st['c_fail_inC'] += 1

if __name__ == '__main__':
    st = collections.Counter(); st['block_sizes'] = collections.Counter()
    if sys.argv[1] == 'cell':
        path, K = sys.argv[2], int(sys.argv[3])
        lim = int(sys.argv[4]) if len(sys.argv) > 4 else 17
        for (n, m, t, E) in read_cell(path, K):
            check_graph(n, E, st, True, lim)
        print(path.split('/')[-1], K, dict(st))
    else:
        N, seed = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        for _ in range(N):
            n = rng.randint(6, 12); m = rng.randint(2, n + 1)
            E = random_linear(n, m, rng)
            if len(set().union(*E)) < n if E else True:
                continue
            inC = in_C(range(n), E)
            check_graph(n, E, st, inC, 13)
            st['inC_graphs'] += int(inC)
        print('random', N, seed, dict(st))
