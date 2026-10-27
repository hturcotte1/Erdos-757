#!/usr/bin/env python3
"""redfree.py -- exact (Red) test for a 3-uniform hypergraph (independent pure-Python implementation, used to validate bin/redfree).

(Red): a pair (Z, T), Z a proper nonempty vertex subset, T a vertex set meeting every edge that meets Z, with 11|T| <= 3|Z| + 2 e(Z),
e(Z) = number of edges meeting Z.  For fixed Z the best T is a minimum transversal of E_Z, so
    value(Z) = 3|Z| + 2 e(Z) - 11 tau(E_Z),   (Red) holds for Z  iff  value(Z) >= 0.
API: red_report(edges) -> dict(redfree, best_value, best_Z, best_T, e_Z, n, m, tau, slack, red_pairs(count), ...).
Vertices are arbitrary hashables; isolated vertices must be passed via `vertices=`."""
import itertools, sys
from fractions import Fraction

def min_transversal(edge_sets, verts):
    """smallest set of vertices (from verts) meeting every edge in edge_sets; brute force over sizes (exact)."""
    edge_sets = [frozenset(e) for e in edge_sets]
    if not edge_sets: return frozenset()
    verts = sorted(set().union(*edge_sets))
    for k in range(1, len(verts) + 1):
        for T in itertools.combinations(verts, k):
            Ts = set(T)
            if all(Ts & e for e in edge_sets): return frozenset(T)
    raise AssertionError

def red_report(edges, vertices=None, want_all=False):
    edges = [tuple(e) for e in edges]
    V = sorted(set(vertices) if vertices is not None else set(x for e in edges for x in e))
    n, m = len(V), len(edges)
    tau = len(min_transversal(edges, V))
    best = None; cnt = 0; pairs = []
    for k in range(1, n):
        for Z in itertools.combinations(V, k):
            Zs = set(Z)
            EZ = [e for e in edges if Zs & set(e)]
            T = min_transversal(EZ, V)
            val = 3 * k + 2 * len(EZ) - 11 * len(T)
            if val >= 0:
                cnt += 1
                if want_all: pairs.append((Z, tuple(sorted(T))))
            if best is None or val > best[0] or (val == best[0] and k < len(best[1])):
                best = (val, Z, T, len(EZ))
    return dict(n=n, m=m, tau=tau, slack=3 * n + 2 * m - 11 * tau, redfree=(best is None or best[0] < 0),
                best_value=None if best is None else best[0], best_Z=None if best is None else best[1],
                best_T=None if best is None else tuple(sorted(best[2])), e_Z=None if best is None else best[3],
                num_red_Z=cnt, red_pairs=pairs)

if __name__ == '__main__':
    import json
    sys.path.insert(0, __file__.rsplit('/experiments/', 1)[0])
    from e757.core import ap_edges
    d = json.load(open(__file__.rsplit('/experiments/', 1)[0] + '/data/small_records.json'))
    A = d['sets']['14']['set']
    E = ap_edges(A)
    idx = {a: i for i, a in enumerate(sorted(A))}
    EE = [tuple(sorted(idx[x] for x in e)) for e in E]
    print('A_base: n=14 m=%d edges (index in sorted order): %s' % (len(EE), EE))
    r = red_report(EE); print({k: v for k, v in r.items() if k != 'red_pairs'})
