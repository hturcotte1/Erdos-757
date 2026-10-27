"""Referee L019: independent re-computation of C4-C7 (per-graph blocked folds, Theorem 6(b) pattern) with refhg.
For each graph: degree sequence; for each degree-2 vertex x and each (y,z) in different x-edges: 'adj' (adjacent in K),
else the fold's membership in C (N = non-linear, F = F7, P = (P3) fails); flags:
  allblocked = no degree-2 vertex has a fold in C;  six_b = Theorem 6(b) holds at every degree-2 vertex;
  deg23 = all degrees in {2,3}.  Prints indices (0-based, as in the certificate) of allblocked graphs and of
  deg23 & six_b & allblocked graphs, and for those the multiset of blocking reasons.
usage: test_blocked.py cellpath K"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import *


def fold_status(n, E, x, y, z):
    n2, imgs, zeta = fold(n, E, x, y, z)
    E2 = [tuple(sorted(g)) for g in imgs]
    if not linear(E2):
        return 'N'
    if f7_copies(E2):
        return 'F'
    ok = p3_ok_table(n2, E2) if n2 <= 22 else p3_ok_flow(E2)
    return 'inC' if ok else 'P'


def main(path, K):
    allb = []; both = []; reasons = {}
    cnt = collections.Counter()
    for gi, (n, m, t, E) in enumerate(read_cell(path, K)):
        d = degrees(n, E)
        deg23 = min(d) >= 2 and max(d) <= 3
        six_b = True
        any_good = False
        rs = collections.Counter()
        for x in range(n):
            if d[x] != 2:
                continue
            ex = [g for g in E if x in g]
            A = [u for u in ex[0] if u != x]; B = [u for u in ex[1] if u != x]
            for y in A:
                for z in B:
                    adjx = adjacent(E, y, z, avoid=x)
                    if d[y] == 3 and d[z] == 3 and not adjx:
                        six_b = False
                    if adjacent(E, y, z):
                        rs['adj'] += 1
                        continue
                    st = fold_status(n, E, x, y, z)
                    rs[st] += 1
                    if st == 'inC':
                        any_good = True
        cnt['graphs'] += 1
        cnt['deg23'] += deg23
        if not any_good:
            allb.append(gi); reasons[gi] = (dict(rs), sorted(collections.Counter(d).items()), m == n - 2)
        if deg23 and six_b and not any_good:
            both.append(gi)
    print(os.path.basename(path), dict(cnt), 'all-blocked graphs:', allb, 'deg23&6b&all-blocked:', both)
    for gi in allb:
        print('   #%d reasons %s degree counts %s m=n-2 %s' % (gi, reasons[gi][0], reasons[gi][1], reasons[gi][2]))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
