"""Referee #2 (L021): independent recomputation of the role counts of Theorem 7(v) / 7.6 for the 32 pieces.
Co-transversality of a pair decided by SAT (min transversal containing both), not by enumerating transversals.
Definitions from L017 Theorem 4(iv) with attachable vertices = piece-degree <= 2, trace pairs not inside a piece edge."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L021')
from ref_lib import *
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
tot = {'b': [], 'c': [], 'e': [], 'f1': []}
for p in R['pieces']:
    P = Piece(p['edges'], p['name'])
    assert P.tau == p['tau'] and P.W == p['W']
    deg = degrees(P.n, P.edges)
    att = [x for x in range(P.n) if deg[x] <= 2]
    co_cache = {}
    def co(x, y):
        k = (min(x, y), max(x, y))
        if k not in co_cache: co_cache[k] = sat_transversal(P.n, P.edges, P.tau, with_vertices=k)
        return co_cache[k]
    inside = lambda a, b: any(a in e and b in e for e in P.edges)
    pairs = [(a, b) for a, b in itertools.combinations(att, 2) if not inside(a, b)]
    rb = sum(1 for x, y, z in itertools.combinations(att, 3) if not co(x, y) and not co(x, z) and not co(y, z))
    rc = sum(1 for (a, b), (c, d) in itertools.combinations(pairs, 2) if len({a, b, c, d}) == 4 and not any(co(x, y) for x in (a, b) for y in (c, d)))
    re_ = sum(1 for (a, b) in pairs for e in att if e not in (a, b) and not co(a, e) and not co(b, e))
    rf = sum(1 for (a, b) in pairs for c, e in itertools.combinations([x for x in att if x not in (a, b)], 2) if not any(co(x, y) for x in (a, b) for y in (c, e)))
    ncp = sum(1 for (x, y) in itertools.combinations(range(P.n), 2) if not co(x, y))
    for k, v in (('b', rb), ('c', rc), ('e', re_), ('f1', rf)):
        if v: tot[k].append(P.name)
    print(P.name, 'tau', P.tau, 'W', P.W, 'role_b', rb, 'role_c', rc, 'role_e', re_, 'role_f1', rf, 'non-co-transversal pairs (all vertices)', ncp)
print('role_b>0:', tot['b']); print('role_c>0:', tot['c']); print('role_e>0:', tot['e']); print('role_f1>0:', tot['f1'])
