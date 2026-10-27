"""C3 (L019): folds of the three small linear vertex-critical violators (F7, s=-2; two (9,8,4), s=-1; list from L017 C3).
Folding lemma predicts: for x co-transversal, tau(H°)=tau(H)-1, s(H°)=s(H)+1; for F7 (all linear 3-graphs with <=6 vertices
satisfy I11, L017 C3) every non-degenerate fold must be non-linear."""
import itertools
from hg import *
from check_folding import fold
G = {'F7': (7, [(0,1,6),(0,4,5),(1,2,3),(2,4,6),(3,5,6)]),
     '984a': (9, [(0,1,2),(0,3,4),(1,6,7),(2,5,8),(3,5,7),(3,6,8),(4,5,6),(4,7,8)]),
     '984b': (9, [(0,1,4),(0,2,3),(1,7,8),(2,5,6),(3,5,8),(3,6,7),(4,5,7),(4,6,8)])}
for name, (n, E) in G.items():
    t = tau(n, E); s = 3*n + 2*len(E) - 11*t; d = degrees(n, E)
    inE = set()
    for e in E:
        for a, b in itertools.permutations(e, 2): inE.add((a, b))
    res = []
    for x in range(n):
        if d[x] != 2: continue
        e1, e2 = [e for e in E if x in e]
        for u in [y for y in e1 if y != x]:
            for w in [y for y in e2 if y != x]:
                if (u, w) in inE: res.append('adj'); continue
                n2, E2 = fold(n, E, x, u, w); t2 = tau(n2, E2)
                res.append(('lin' if linear(E2) else 'nonlin') + ' s=%d' % (3*n2 + 2*len(E2) - 11*t2))
    import collections
    print(name, 'n m tau s =', n, len(E), t, s, 'folds:', dict(collections.Counter(res)))
