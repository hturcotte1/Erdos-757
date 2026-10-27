"""Spot check of L019 Theorem 5 (folding lemma) with ref2.py (independent code).
For every vertex x of degree 2 (edges {x,u,u'}, {x,w,w'}) and y in {u,u'}, z in {w,w'} non-adjacent:
 (a) n-2 vertices, m-2 distinct 3-edges, d(zeta) = d(y)+d(z)-2, Delta bound;
 (b) tau(K) <= tau(K°)+1;  (c) x co-transversal => tau(K°) = tau-1 and s(K°) = s+1;
 (d) for K in C: K° linear <=> no common neighbour of y,z in K-x; every F7 copy of K° contains zeta;
     K° satisfies (P3) <=> no saturated S of K with y,z in S, x not in S; such S has |S| >= 6.
usage: spot_thm5.py cells | ap | random N seed"""
import sys, random, itertools, json, collections
from ref2 import *

D = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'


def check_graph(V, E, st):
    V = sorted(V)
    t, Ts = all_min_T(V, E)
    s = slack(len(V), len(E), t)
    co = set().union(*Ts)
    d = degrees(V, E)
    Delta = max(d.values()) if d else 0
    inC = in_C(V, E)
    st['graphs'] += 1
    st['graphs_inC'] += inC
    for x in V:
        if d[x] != 2:
            continue
        e1, e2 = [e for e in E if x in e]
        for y in sorted(e1 - {x}):
            for z in sorted(e2 - {x}):
                if adjacent(E, y, z):
                    st['adjacent_pairs'] += 1
                    continue
                V2, E2, zeta = fold(V, E, x, y, z)
                st['folds'] += 1
                ok = (all(len(e) == 3 for e in E2) and len(set(E2)) == len(E2) == len(E) - 2
                      and len(V2) == len(V) - 2)
                d2 = degrees(V2, E2)
                ok = ok and d2[zeta] == d[y] + d[z] - 2 and max(d2.values()) <= max(Delta, d[y] + d[z] - 2)
                if not ok:
                    st['FAIL_a'] += 1
                t2, _ = all_min_T(V2, E2)
                s2 = slack(len(V2), len(E2), t2)
                if not t <= t2 + 1:
                    st['FAIL_b'] += 1
                if x in co:
                    st['folds_cotrans'] += 1
                    if t2 != t - 1 or s2 != s + 1:
                        st['FAIL_c'] += 1
                else:
                    st['folds_noncotrans_dtau%+d' % (t2 - t)] += 1
                if not inC:
                    continue
                st['folds_hostC'] += 1
                Ex = [e for e in E if x not in e]
                Ny = set().union(*[e for e in Ex if y in e] or [set()]) - {y}
                Nz = set().union(*[e for e in Ex if z in e] or [set()]) - {z}
                cn = bool(Ny & Nz)
                lin2 = is_linear(E2)
                if lin2 != (not cn):
                    st['FAIL_d_lin'] += 1
                cps = f7_copies(E2)
                if any(zeta not in set().union(*cp) for cp in cps):
                    st['FAIL_d_f7'] += 1
                st['folds_with_F7'] += bool(cps)
                p3 = p3_ok(V2, E2)
                Vx = [v for v in V if v != x]
                Vs, idx, f = edge_counts(Vx, Ex)
                by, bz = 1 << idx[y], 1 << idx[z]
                sizes = set()
                for S in range(1 << len(Vs)):
                    if S & by and S & bz:
                        k = bin(S).count('1')
                        if k >= 3 and f[S] == k - 2:
                            sizes.add(k)
                if p3 != (not sizes):
                    st['FAIL_d_p3'] += 1
                if sizes:
                    st['p3_blocked'] += 1
                    st['min_blocking_sat_size_%d' % min(sizes)] += 1
                    if min(sizes) < 6:
                        st['FAIL_d_size'] += 1
                    for k in sizes:
                        st['some_blocking_sat_of_size_%d' % k] += 1
                if lin2 and not cps and p3:
                    st['fold_inC'] += 1
                    if s2 < 0:
                        st['fold_inC_negative_slack'] += 1


def report(name, st):
    fails = {k: v for k, v in st.items() if k.startswith('FAIL') and v}
    print(name, dict(sorted(st.items())), 'FAILURES:', fails or 0, flush=True)


def random_linear(n, rng, tries=200):
    E = []
    pairs = set()
    for _ in range(tries):
        e = frozenset(rng.sample(range(n), 3))
        ps = set(itertools.combinations(sorted(e), 2))
        if ps & pairs:
            continue
        E.append(e)
        pairs |= ps
        if rng.random() < 0.08:
            break
    return E


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'cells':
        for c, K in [('8_5_3', None), ('10_7_4', None), ('10_8_4', None), ('14_12_6', None),
                     ('12_10_5', 40), ('13_9_5', 30), ('17_13_7', None)]:
            st = collections.Counter()
            for (n, E, t) in read_cell(D + 'cell_%s.txt' % c, K):
                tt, _ = all_min_T(range(n), E)
                assert tt == t, ('stored tau wrong', c)
                check_graph(range(n), E, st)
            report('cell_' + c, st)
    elif mode == 'ap':
        R = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
        st = collections.Counter()
        sets = {k: v['set'] for k, v in R.items()}
        fib = [2, 3]
        while len(fib) < 12:
            fib.append(fib[-1] + fib[-2])
        sets['fib12'] = fib
        # generic gluing of the 8-point and the 10-point records: A u (q B + t)
        A8, B10 = R['8']['set'], R['10']['set']
        glue = sorted(A8 + [1000003 * b + 10 ** 12 for b in B10])
        sets['glue_8_10'] = glue
        rng = random.Random(20261027)
        base = R['14']['set']
        for i in range(150):
            k = rng.randint(6, 13)
            sets['Abase_sub%d' % i] = sorted(rng.sample(base, k))
        for name, A in sets.items():
            assert len(set(A)) == len(A)
            assert is_45(A), name
            E = ap_hypergraph(A)
            if not E:
                continue
            s1 = collections.Counter()
            check_graph(A, E, s1)
            assert s1['graphs_inC'] == 1, ('AP hypergraph not in C', name)
            st.update(s1)
            if not name.startswith('Abase_sub'):
                report('ap_' + name, s1)
        report('ap_TOTAL', st)
    elif mode == 'random':
        N, seed = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        st = collections.Counter()
        for _ in range(N):
            n = rng.randint(7, 12)
            E = random_linear(n, rng)
            if E:
                check_graph(range(n), E, st)
        report('random', st)
