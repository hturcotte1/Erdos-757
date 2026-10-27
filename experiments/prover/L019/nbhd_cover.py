"""C8 (L019): for the uncoverable linear triples of a cell (pairs not inside an F-edge, no minimum transversal of F meets all
three), the transversal number of the set of edges of H = F + v meeting Z = {v} u W (Proposition 10 quantity) and k = number
of F-edges meeting W.  usage: nbhd_cover.py cellfile K"""
import sys, itertools, collections
from hg import *
path, K = sys.argv[1], int(sys.argv[2])
hist = collections.Counter()
for (n, m, t, E) in read_cell(path, K):
    tt, Ts = all_min_transversals(n, E, t)
    inE = set()
    for e in E:
        for x, y in itertools.permutations(e, 2): inE.add((x, y))
    pairs = [(x, y) for x in range(n) for y in range(x+1, n) if (x, y) not in inE]
    mb = {p: sum(1 << i for i, T in enumerate(Ts) if (T >> p[0] & 1) or (T >> p[1] & 1)) for p in pairs}
    for p1, p2, p3 in itertools.combinations(pairs, 3):
        W = set(p1) | set(p2) | set(p3)
        if len(W) < 6 or (mb[p1] & mb[p2] & mb[p3]): continue
        v = n
        near = [e for e in E if set(e) & W] + [(v,) + p1, (v,) + p2, (v,) + p3]
        k = len(near) - 3
        hist[(k, tau(n + 1, near))] += 1
print(path.split('/')[-1], '(k, tau of edges meeting N[v]) : count', dict(sorted(hist.items())))
