"""L021: independent recomputation, for the 32 pieces of L*, of the role counts of L017 C5 used in Theorem 7(v)
(conditions of L017 Theorem 4(iv) on one component; attachable vertices = piece-degree <= 2; a pair used as a trace of a
hub edge must not lie inside an edge of the piece):
 role_b : three attachable vertices, pairwise in no common minimum transversal;
 role_c : two disjoint attachable pairs (not inside edges), all four cross pairs in no common minimum transversal;
 role_e : an attachable pair {a,b} (not inside an edge) and an attachable vertex e, {a,e} and {b,e} in no common min. transversal;
 role_f1: an attachable pair {a,b} (not inside an edge) and two further attachable vertices c, e, all four cross pairs
          {a,c},{a,e},{b,c},{b,e} in no common minimum transversal.
Exact (all minimum transversals enumerated)."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
tot = {'b': [], 'c': [], 'e': [], 'f1': []}
for p in R['pieces']:
    P = Piece(p['edges'], p['name']); T = min_transversals(masks(P.edges), P.tau)
    att = [x for x in range(P.n) if P.deg[x] <= 2]
    co = lambda x, y: any((t >> x) & 1 and (t >> y) & 1 for t in T)
    inside = lambda a, b: any(a in e and b in e for e in P.edges)
    pairs = [(a, b) for a, b in itertools.combinations(att, 2) if not inside(a, b)]
    rb = sum(1 for x, y, z in itertools.combinations(att, 3) if not co(x, y) and not co(x, z) and not co(y, z))
    rc = sum(1 for (a, b), (c, d) in itertools.combinations(pairs, 2) if len({a, b, c, d}) == 4 and not any(co(x, y) for x in (a, b) for y in (c, d)))
    re_ = sum(1 for (a, b) in pairs for e in att if e not in (a, b) and not co(a, e) and not co(b, e))
    rf = sum(1 for (a, b) in pairs for c, e in itertools.combinations([x for x in att if x not in (a, b)], 2)
             if not any(co(x, y) for x in (a, b) for y in (c, e)))
    for k, v in (('b', rb), ('c', rc), ('e', re_), ('f1', rf)):
        if v: tot[k].append(P.name)
    print(P.name, 'role_b', rb, 'role_c', rc, 'role_e', re_, 'role_f1', rf)
print('pieces with role_b > 0:', tot['b']); print('pieces with role_c > 0:', tot['c'])
print('pieces with role_e > 0:', tot['e']); print('pieces with role_f1 > 0:', tot['f1'])
