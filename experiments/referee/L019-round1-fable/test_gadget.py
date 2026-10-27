"""Theorem 2(i) on data (N = 27 by L016; every stored graph has n <= 26 <= N-1).
mode pairs: for stored K with s(K) <= 3: every two disjoint pairs Q1,Q2 (not inside an edge of K, so that the gadget is
   linear) with K + w(Q1,Q2) in C must be met by a minimum transversal (Theorem 2(i), k = 2).  We report for the
   UNCOVERED pairs of pairs whether the gadget is in C (must never be).
mode triples: for stored K with s(K) <= 1: every three disjoint pairs with K + v(Q1,Q2,Q3) in C must be met by a
   minimum transversal (k = 3; this is C1 on data, Theorem 4(c)).  For uncovered triples we check the gadget is not in C.
usage: test_gadget.py pairs|triples <path> <K>"""
import sys, itertools, collections
from ref import *

mode, path, K = sys.argv[1], sys.argv[2], int(sys.argv[3])
st = collections.Counter()
for (n, m, t0, E) in read_cell(path, K):
    V = set(range(n))
    t, Ts, co = cotransversal_vertices(E)
    s = 3 * n + 2 * m - 11 * t
    Ts = list(Ts)
    st['graphs'] += 1
    pairs = [frozenset(p) for p in itertools.combinations(range(n), 2) if not adjacent(E, *p)]
    mask = {p: sum(1 << i for i, T in enumerate(Ts) if T & p) for p in pairs}
    w = n
    if mode == 'pairs':
        if s > 3:
            continue
        for p1, p2 in itertools.combinations(pairs, 2):
            if p1 & p2:
                continue
            st['pairs_of_pairs'] += 1
            if mask[p1] & mask[p2]:
                continue
            st['uncovered'] += 1
            E2 = E + [p1 | {w}, p2 | {w}]
            if in_C(V | {w}, E2):
                st['UNCOVERED_GADGET_IN_C'] += 1
            else:
                st['uncovered_gadget_notC'] += 1
                if not is_linear(E2): st['reason_nonlinear'] += 1
                elif has_f7(E2): st['reason_f7'] += 1
                else: st['reason_p3'] += 1
    else:
        if s > 1:
            continue
        for p1, p2, p3 in itertools.combinations(pairs, 3):
            if (p1 & p2) or (p1 & p3) or (p2 & p3):
                continue
            st['triples'] += 1
            if mask[p1] & mask[p2] & mask[p3]:
                continue
            st['uncovered'] += 1
            # pair-pair coverage (Theorem 3 on data: needs F+v(Pi,Pj) in C)
            for a, b in ((p1, p2), (p1, p3), (p2, p3)):
                if not (mask[a] & mask[b]):
                    E2 = E + [a | {w}, b | {w}]
                    if in_C(V | {w}, E2): st['UNCOVERED_PAIRPAIR_GADGET_IN_C'] += 1
            E3 = E + [p1 | {w}, p2 | {w}, p3 | {w}]
            if in_C(V | {w}, E3):
                st['UNCOVERED_TRIPLE_GADGET_IN_C'] += 1
            else:
                st['uncovered_gadget_notC'] += 1
                if not is_linear(E3): st['reason_nonlinear'] += 1
                elif has_f7(E3): st['reason_f7'] += 1
                else: st['reason_p3'] += 1
print(mode, path.split('/')[-1], K, dict(st))
