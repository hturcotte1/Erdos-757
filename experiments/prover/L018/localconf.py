"""localconf.py -- exhaustive local-configuration analysis for Conjecture RU (certificate L018).

A configuration around a root vertex r is built in BFS order: every vertex at distance <= R from r is PROCESSED,
i.e. its degree d in {1,2,3} is chosen and ALL its edges are listed.  Vertices at distance R+1 (the boundary) are
created fresh, one per edge slot (no identifications among boundary vertices: the worst case, see the certificate,
Lemma 3), and are treated as INCOMPLETE (they may have further unknown edges).
For Z a nonempty set of processed vertices, every edge meeting Z is listed, so
    value(Z) = 3|Z| + 2 e(Z) - 11 tau(E_Z)
is computed EXACTLY (tau over all vertices of the configuration).  If value(Z) >= 0 and some vertex is outside Z,
(Z, T) is a (Red) pair in every hypergraph containing the configuration in this way.
Pruning: after each processed vertex q, all Z containing q (and processed vertices only) are tested; a configuration
in which a (Red) pair is found is 'reducible' and is not extended.
Output: counts and the list of irreducible configurations at radius R (with their best value).
Usage: python3 localconf.py ROOTDEG R [--rootdeg-neighbours ...]
"""
import sys, itertools, json
from hg import TauCache, in_class_C

class Conf:
    __slots__ = ('edges', 'inc', 'dist', 'nproc', 'deg')
    def __init__(self):
        self.edges = []      # list of tuples
        self.inc = []        # per vertex: list of edge indices
        self.dist = []
        self.nproc = 0       # vertices 0..nproc-1 are processed
        self.deg = []        # chosen degree for processed vertices (None otherwise)
    def copy(self):
        c = Conf()
        c.edges = list(self.edges); c.inc = [list(x) for x in self.inc]; c.dist = list(self.dist)
        c.nproc = self.nproc; c.deg = list(self.deg)
        return c
    def newv(self, d):
        self.inc.append([]); self.dist.append(d); self.deg.append(None)
        return len(self.inc) - 1
    def add_edge(self, e):
        i = len(self.edges); self.edges.append(tuple(sorted(e)))
        for v in e:
            self.inc[v].append(i)

def shares_edge(c, u, v):
    return any(v in c.edges[i] for i in c.inc[u])

def best_value_with(c, q, tc, closed):
    """max over Z subset of processed vertices (ids < c.nproc), q in Z, of value(Z). Returns (value, Z, T-size)."""
    P = [v for v in range(c.nproc) if v != q]
    nV = len(c.inc)
    best = (-10**9, None, None)
    # E_Z masks
    em = [0] * nV
    for v in range(nV):
        for i in c.inc[v]:
            em[v] |= 1 << i
    for k in range(len(P) + 1):
        for S in itertools.combinations(P, k):
            Z = (q,) + S
            if closed and len(Z) == nV:
                continue
            F = 0
            for z in Z:
                F |= em[z]
            ez = bin(F).count('1')
            t = tc.tau(F)
            val = 3 * len(Z) + 2 * ez - 11 * t
            if val > best[0]:
                best = (val, Z, t)
    return best

def gen(c, R, out, stats, depth_limit_vertices=60):
    """process vertices in id order until the next unprocessed vertex has dist > R."""
    q = c.nproc
    if q >= len(c.inc) or c.dist[q] > R:
        # leaf: irreducible configuration at radius R
        closed = (q >= len(c.inc))
        stats['leaves'] += 1
        out.append(c.copy())
        return
    k = len(c.inc[q])
    dq = c.dist[q]
    # candidates: unprocessed existing vertices w != q, deg < 3, not sharing an edge with q,
    # with dist in {dq, dq+1}, and (if dq == R) dist == R only (no boundary merges)
    cands = []
    for w in range(q + 1, len(c.inc)):
        if len(c.inc[w]) >= 3:
            continue
        if shares_edge(c, q, w):
            continue
        if c.dist[w] == dq or (c.dist[w] == dq + 1 and dq + 1 <= R):
            cands.append(w)
    NEW = -1
    types = [(NEW, NEW)] + [(w, NEW) for w in cands] + [(u, w) for u, w in itertools.combinations(cands, 2) if not shares_edge(c, u, w)]
    lo = max(k, 1)
    for D in range(lo, 4):
        r = D - k
        for combo in itertools.combinations_with_replacement(range(len(types)), r):
            used = []
            ok = True
            for ti in combo:
                for x in types[ti]:
                    if x != NEW:
                        used.append(x)
            if len(used) != len(set(used)):
                continue
            # degree check: each used w gets +1
            if any(len(c.inc[w]) + 1 > 3 for w in used):
                continue
            # pairs (u,w) used in two different new edges? impossible since each w used once
            c2 = c.copy()
            for ti in combo:
                a, b = types[ti]
                if a == NEW:
                    a = c2.newv(dq + 1)
                if b == NEW:
                    b = c2.newv(dq + 1)
                c2.add_edge((q, a, b))
            c2.deg[q] = D
            c2.nproc = q + 1
            stats['nodes'] += 1
            closed = (c2.nproc >= len(c2.inc))
            tc = TauCache(c2.edges)
            val, Z, t = best_value_with(c2, q, tc, closed)
            if val >= 0:
                stats['reducible'] += 1
                key = (len(Z), val)
                stats['redZ'][key] = stats['redZ'].get(key, 0) + 1
                continue
            gen(c2, R, out, stats)

def root_conf(rootdeg):
    c = Conf()
    r = c.newv(0)
    return c

def run(rootdeg, R, extra=None):
    c = Conf()
    r = c.newv(0)
    # process the root with fixed degree rootdeg: its edges contain new vertices only (dist 1)
    for _ in range(rootdeg):
        a = c.newv(1); b = c.newv(1)
        c.add_edge((r, a, b))
    c.deg[r] = rootdeg
    c.nproc = 1
    out = []
    stats = {'nodes': 0, 'reducible': 0, 'leaves': 0, 'redZ': {}}
    gen(c, R, out, stats)
    return out, stats

def best_value_all(c, closed=False):
    tc = TauCache(c.edges)
    P = list(range(c.nproc))
    nV = len(c.inc)
    em = [0] * nV
    for v in range(nV):
        for i in c.inc[v]:
            em[v] |= 1 << i
    best = (-10**9, None)
    for k in range(1, len(P) + 1):
        for Z in itertools.combinations(P, k):
            if closed and len(Z) == nV:
                continue
            F = 0
            for z in Z:
                F |= em[z]
            val = 3 * len(Z) + 2 * bin(F).count('1') - 11 * tc.tau(F)
            if val > best[0]:
                best = (val, Z)
    return best

if __name__ == '__main__':
    rootdeg = int(sys.argv[1]); R = int(sys.argv[2])
    out, stats = run(rootdeg, R)
    print('root degree', rootdeg, 'radius', R, 'nodes', stats['nodes'], 'reducible', stats['reducible'], 'irreducible leaves', stats['leaves'])
    print('reducing Z (|Z|, value) counts:', sorted(stats['redZ'].items()))
    inC = 0
    summary = {}
    for c in out:
        okC = in_class_C(c.edges)
        inC += okC
        degs = tuple(c.deg[v] for v in range(c.nproc))
        summary[(okC, degs)] = summary.get((okC, degs), 0) + 1
    print('irreducible leaves in class C:', inC)
    for k, v in sorted(summary.items()):
        print('  inC=%s processed-degrees=%s : %d' % (k[0], k[1], v))
