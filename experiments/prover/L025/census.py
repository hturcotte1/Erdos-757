"""L025 census: load the stored near-tight (slack<=1, Delta<=3) classes and the slack-2 classes; verify counts, I11 data,
and list NC pairs / b-configurations by type.  Usage: python3 census.py [slack2]"""
import sys, time, json
from itertools import combinations
from hyp25 import *

NEAR = [(3,1,1),(10,7,4),(14,12,6),(17,13,7),(8,5,3),(12,10,5),(15,11,6),(19,16,8),(22,17,9),(26,22,11)]
SLACK2 = [(6,3,2),(9,4,3),(10,8,4),(13,9,5),(16,10,6),(17,14,7),(20,15,8),(23,16,9)]

def nc_info(h):
    cp = h.co_pairs()
    low = [v for v in h.V if h.deg[v] <= 2]
    nc = [frozenset(p) for p in combinations(low, 2) if frozenset(p) not in cp]
    ncset = set(nc)
    edges = set(frozenset(e) for e in h.E)
    bconf = []
    for t in combinations(low, 3):
        if all(frozenset(p) in ncset for p in combinations(t, 2)):
            bconf.append((t, frozenset(t) in edges))
    return nc, bconf

def main():
    cells = SLACK2 if (len(sys.argv) > 1 and sys.argv[1] == 'slack2') else NEAR
    tot = 0
    summary = {}
    for (n, m, t) in cells:
        L = load_cell(n, m, t)
        cnt = 0; ncnt = {}; bcnt = [0, 0]; b_types = {}
        for (n0, m0, t0, E) in L:
            h = Hyp(E, range(n0))
            if h.maxdeg() > 3:
                continue
            assert h.n == n0 and h.m == m0
            assert h.tau() == t0, (n, m, t, h.tau())
            assert h.connected()
            cnt += 1
            nc, bc = nc_info(h)
            for p in nc:
                x, y = sorted(p)
                key = (h.deg[x], h.deg[y], int(p in h.sig)) if h.deg[x] <= h.deg[y] else (h.deg[y], h.deg[x], int(p in h.sig))
                ncnt[key] = ncnt.get(key, 0) + 1
            for (tr, isedge) in bc:
                bcnt[int(isedge)] += 1
                if not isedge:
                    a, b, c = tr
                    ds = tuple(sorted(h.deg[u] for u in tr))
                    sg = tuple(sorted(int(frozenset(p) in h.sig) for p in combinations(tr, 2)))
                    b_types[str((ds, sg))] = b_types.get(str((ds, sg)), 0) + 1
        tot += cnt
        summary[str((n, m, t))] = dict(classes_D3=cnt, nc_pair_types={str(k): v for k, v in sorted(ncnt.items())},
                                       bconf_nonedge=bcnt[0], bconf_edge=bcnt[1], bconf_nonedge_types=b_types)
        print((n, m, t), 'slack', 3*n+2*m-11*t, 'classes(D<=3)', cnt, 'NC types', dict(sorted(ncnt.items())),
              'b-conf non-edge', bcnt[0], 'edge', bcnt[1], b_types, flush=True)
    print('total classes', tot)
    return summary

if __name__ == '__main__':
    t0 = time.time()
    s = main()
    print('time %.1fs' % (time.time() - t0))
