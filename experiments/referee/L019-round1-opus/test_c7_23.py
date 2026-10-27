"""Referee L019: C7 on the slack-1 cell (23,21,10) omitted by the certificate: classes with all degrees in {2,3},
Theorem 6(b) at every degree-2 vertex, and every fold blocked in C (refhg)."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import *
from test_blocked import fold_status
path = sys.argv[1]
cnt = collections.Counter(); both = []
for gi, (n, m, t, E) in enumerate(read_cell(path)):
    d = degrees(n, E)
    cnt['graphs'] += 1
    if min(d) < 2 or max(d) > 3:
        cnt['deg_not_23'] += 1; continue
    cnt['deg23'] += 1
    six_b = True
    folds = []
    for x in range(n):
        if d[x] != 2: continue
        ex = [g for g in E if x in g]
        A = [u for u in ex[0] if u != x]; B = [u for u in ex[1] if u != x]
        for y in A:
            for z in B:
                if d[y] == 3 and d[z] == 3 and not adjacent(E, y, z, avoid=x): six_b = False
                if not adjacent(E, y, z): folds.append((x, y, z))
    if not six_b: continue
    cnt['6b'] += 1
    if all(fold_status(n, E, x, y, z) != 'inC' for (x, y, z) in folds):
        both.append(gi)
print(os.path.basename(path), dict(cnt), 'deg23 & 6b & all folds blocked:', both)
