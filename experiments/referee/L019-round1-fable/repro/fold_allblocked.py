"""C4 (L019): degree-2 vertices all of whose four folds leave C (on stored lists), and whether they lie in a Pasch
configuration {x u u', x w w', u w t, u' w' t} (then all four folds are blocked by adjacency / a common neighbour)."""
import sys, itertools, collections
from hg import *
from check_folding import fold
path, K = sys.argv[1], int(sys.argv[2])
tot = collections.Counter(); ex = None
for (n, m, t, E) in read_cell(path, K):
    d = degrees(n, E); Es = set(frozenset(e) for e in E)
    inE = set()
    for e in E:
        for a, b in itertools.permutations(e, 2): inE.add((a, b))
    for x in range(n):
        if d[x] != 2: continue
        e1, e2 = [e for e in E if x in e]
        A = [y for y in e1 if y != x]; B = [y for y in e2 if y != x]
        good = 0
        for u in A:
            for w in B:
                if (u, w) in inE: continue
                n2, E2 = fold(n, E, x, u, w)
                if in_C(E2): good += 1
        # Pasch through x: two edges {u,w,t},{u',w',t} or {u,w',t},{u',w,t}
        pasch = False
        for (u, u2) in (A, A[::-1]):
            for tt in range(n):
                if tt in (x,) + tuple(A) + tuple(B): continue
                if frozenset((u, B[0], tt)) in Es and frozenset((u2, B[1], tt)) in Es: pasch = True
        tot[('unblocked folds', good, 'pasch', pasch)] += 1
        if good == 0 and ex is None: ex = (n, E, x, e1, e2, pasch)
print(path.split('/')[-1], K, dict(tot))
if ex: print('example all-blocked:', ex)
