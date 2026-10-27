"""C7 (L019): on stored class-C lists, graphs with all degrees in {2,3} such that
 (6b) at every degree-2 vertex x, any two degree-3 vertices in different x-edges are adjacent in H - x  [Theorem 6(b)], and
 (6c) every fold at every degree-2 vertex leaves C                                                      [Theorem 6(c)].
Counts graphs satisfying (6b), (6c), both.  usage: blocked_and_6b.py cellfile K"""
import sys, itertools, collections
from hg import *
from check_folding import fold
path, K = sys.argv[1], int(sys.argv[2])
cnt = collections.Counter(); both = []
for gi, (n, m, t, E) in enumerate(read_cell(path, K)):
    d = degrees(n, E)
    if min(d) < 2 or max(d) > 3: cnt['deg_not_23'] += 1; continue
    adj = set()
    for e in E:
        for a, b in itertools.permutations(e, 2): adj.add((a, b))
    ok6b = True; ok6c = True
    for x in range(n):
        if d[x] != 2: continue
        e1, e2 = [e for e in E if x in e]
        A = [y for y in e1 if y != x]; B = [y for y in e2 if y != x]
        for y in A:
            for z in B:
                # adjacency in H - x : common edge not containing x
                adjx = any(y in e and z in e for e in E if x not in e)
                if d[y] == 3 and d[z] == 3 and not adjx: ok6b = False
                if not adjx and ok6c:
                    n2, E2 = fold(n, E, x, y, z)
                    if in_C(E2): ok6c = False
    cnt['graphs_deg23'] += 1; cnt['6b'] += ok6b; cnt['6c'] += ok6c; cnt['6b&6c'] += (ok6b and ok6c)
    if ok6b and ok6c: both.append(gi)
print(path.split('/')[-1], dict(cnt), 'both:', both[:20])
