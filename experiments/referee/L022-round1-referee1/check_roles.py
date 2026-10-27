# Referee recomputation of the data D2, D3 used in L022 Corollary 3' (Step 3.4), independent code.
# For every Delta<=3 class of the stored connected slack-0 and slack-1 lists with n<=26:
#   att      = vertices of degree <= 2 (possible co-vertices, L017 Thm 4(i))
#   noncot   = pairs of att lying in no common minimum transversal
#   role_b   = three att vertices, pairwise noncot                         (pattern (b))
#   role_f1  = pair {a,b} of att not inside an edge + two further att vertices c != e,
#              all four cross pairs noncot                                  (pattern (f), F1 side)
#   role_e   = pair {a,b} of att not inside an edge + att vertex e, {a,e},{b,e} noncot (pattern (e))
#   pendants = number of degree-1 vertices (tight classes)
# Also enumerates the connected cells (n,m,tau) of slack 0/1 with n<=26 (L017 Thm 6(i) rules).
import sys, time
from itertools import combinations
from rlib import all_min_transversals, degree

INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'


def load_cell(cell):
    out = []
    for line in open(INP + 'cell_%s.txt' % cell):
        a = list(map(int, line.split()))
        if not a:
            continue
        n, m, t = a[:3]
        out.append((n, m, t, [tuple(sorted(a[3 + 3 * i:6 + 3 * i])) for i in range(m)]))
    return out


def roles(n, m, t, E):
    V = list(range(n))
    tt, Ts, VV = all_min_transversals(E, V)
    assert tt == t, (tt, t)
    deg = [degree(E, x) for x in V]
    att = [x for x in V if deg[x] <= 2]
    cot = set()
    for T in Ts:
        mem = [x for x in V if T >> x & 1]
        for p in combinations(mem, 2):
            cot.add(p)
    inedge = set()
    for e in E:
        for p in combinations(e, 2):
            inedge.add(p)
    nc = lambda x, y: (min(x, y), max(x, y)) not in cot
    rb = sum(1 for a, b, c in combinations(att, 3) if nc(a, b) and nc(a, c) and nc(b, c))
    rf = 0
    re_ = 0
    for a, b in combinations(att, 2):
        if (a, b) in inedge:
            continue
        rest = [x for x in att if x not in (a, b)]
        good = [x for x in rest if nc(a, x) and nc(b, x)]
        re_ += len(good)
        rf += len(good) * (len(good) - 1) // 2
    pend = sum(1 for x in V if deg[x] == 1)
    ncpairs = sum(1 for x, y in combinations(att, 2) if nc(x, y))
    return rb, rf, re_, pend, ncpairs, len(Ts)


def main():
    cells = sys.argv[1:] or ['3_1_1', '10_7_4', '14_12_6', '17_13_7', '8_5_3', '12_10_5', '15_11_6', '22_17_9', '26_22_11', '19_16_8']
    for cell in cells:
        L = load_cell(cell)
        t0 = time.time()
        agg = {'classes_D3': 0, 'role_b>0': [], 'role_f1>0': [], 'role_e>0': [], 'pendants_hist': {}, 'noncot_pairs': 0}
        for i, (n, m, t, E) in enumerate(L):
            if max(degree(E, x) for x in range(n)) > 3:
                continue
            agg['classes_D3'] += 1
            rb, rf, re_, pend, ncp, nT = roles(n, m, t, E)
            if rb:
                agg['role_b>0'].append(i)
            if rf:
                agg['role_f1>0'].append(i)
            if re_:
                agg['role_e>0'].append(i)
            agg['pendants_hist'][pend] = agg['pendants_hist'].get(pend, 0) + 1
            agg['noncot_pairs'] += ncp
        s = 3 * L[0][0] + 2 * L[0][1] - 11 * L[0][2]
        print(cell, 'slack', s, agg, '%.0fs' % (time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
