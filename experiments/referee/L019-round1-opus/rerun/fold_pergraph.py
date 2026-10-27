"""C5 (L019): per graph, the number of degree-2 vertices having at least one fold that stays in C
(a minimal counterexample with slack -2 would need this number to be 0)."""
import sys, itertools, collections
from hg import *
from check_folding import fold
path, K = sys.argv[1], int(sys.argv[2])
hist = collections.Counter(); zero = []
for gi, (n, m, t, E) in enumerate(read_cell(path, K)):
    d = degrees(n, E)
    inE = set()
    for e in E:
        for a, b in itertools.permutations(e, 2): inE.add((a, b))
    goodv = 0; n2v = 0
    for x in range(n):
        if d[x] != 2: continue
        n2v += 1
        e1, e2 = [e for e in E if x in e]
        ok = False
        for u in [y for y in e1 if y != x]:
            for w in [y for y in e2 if y != x]:
                if (u, w) in inE: continue
                n2, E2 = fold(n, E, x, u, w)
                if in_C(E2): ok = True; break
            if ok: break
        goodv += ok
    hist[(n2v, goodv)] += 1
    if goodv == 0: zero.append(gi)
print(path.split('/')[-1], 'graphs', K, '(#deg-2 vertices, #with an unblocked fold): count', dict(sorted(hist.items())), 'graphs with none:', zero[:10])
