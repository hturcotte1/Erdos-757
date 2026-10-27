"""Print the local structure of uncoverable linear triples (pairs not inside an F-edge) in a cell file.
usage: unc_detail.py cell_file K maxprint"""
import sys, itertools, collections
from hg import *
path, K, maxp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
cnt = 0
for (n, m, t, E) in read_cell(path, K):
    tt, Ts = all_min_transversals(n, E, t)
    assert tt == t
    d = degrees(n, E)
    inE = set()
    for e in E:
        for x, y in itertools.permutations(e, 2): inE.add((x, y))
    pairs = [(x, y) for x in range(n) for y in range(x+1, n) if (x, y) not in inE]
    mb = {p: sum(1 << i for i, T in enumerate(Ts) if (T >> p[0] & 1) or (T >> p[1] & 1)) for p in pairs}
    for p1, p2, p3_ in itertools.combinations(pairs, 3):
        W = set(p1) | set(p2) | set(p3_)
        if len(W) < 6: continue
        if mb[p1] & mb[p2] & mb[p3_]: continue
        cnt += 1
        if cnt > maxp: continue
        v = n
        H = list(E) + [(v,) + p1, (v,) + p2, (v,) + p3_]
        cps = f7_copies(H)
        # F-edges meeting W
        near = [e for e in E if set(e) & W]
        print('F', (n, m, t), 'pairs', p1, p2, p3_, 'dF', [d[x] for x in p1], [d[x] for x in p2], [d[x] for x in p3_])
        print('  F-edges meeting W:', near)
        print('  #F7 copies', len(cps), [sorted(tuple(sorted(e)) for e in cp) for cp in list(cps)[:3]])
        # traces of min transversals on W
        tr = collections.Counter(tuple(sorted(x for x in W if T >> x & 1)) for T in Ts)
        print('  traces on W (count):', dict(sorted(tr.items(), key=lambda z: (len(z[0]), z[0]))))
print('total uncoverable linear triples', cnt)
