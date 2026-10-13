import itertools
import json
import random
from fractions import Fraction

import pytest

from e757.core import ap_edges, alpha, is_45_set
from e757.realizability import (order_feasible, verify_certificate, iis, realize_exact,
                                forced_relations, forbidden_core, is_forced)
from e757.saturated import map_of_set, edges_of_map

REC = json.load(open("data/small_records.json"))["sets"]
A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


def labeled(A):
    A = sorted(A)
    idx = {x: i for i, x in enumerate(A)}
    return len(A), [(idx[a], idx[b], idx[c]) for a, b, c in ap_edges(A)]


def edge_set(vals):
    pos = {v: i for i, v in enumerate(vals)}
    return {frozenset((pos[a], pos[b], pos[c])) for a, b, c in ap_edges(vals)}


def test_a_base_roundtrip():
    lo, hi, mid = map_of_set(A_BASE)
    edges = sorted(edges_of_map(mid))
    ok, vals = realize_exact(14, edges)
    assert ok
    assert edge_set(vals) == {frozenset(e) for e in edges}
    assert is_45_set(vals) and alpha(vals) == 8
    # rigid: affinely equivalent to A_base
    norm = lambda s: [Fraction(v - s[0], s[-1] - s[0]) for v in s]
    assert norm(vals) == norm(A_BASE)


@pytest.mark.parametrize("key", sorted(REC))
def test_records_realize(key):
    n, edges = labeled(REC[key]["set"])
    ok, vals = realize_exact(n, edges)
    assert ok
    assert edge_set(vals) == {frozenset(e) for e in edges}
    assert alpha(vals) == REC[key]["h"]


def test_f7_all_labelings_fail():
    F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    rnd = random.Random(7)
    checked = 0
    for lab in itertools.product(range(3), repeat=5):
        for _ in range(12):
            perm = list(range(7))
            while True:
                rnd.shuffle(perm)  # perm[v] = rank of v
                edges = []
                good = True
                for e, k in zip(F7, lab):
                    mid = e[k]
                    ends = [v for v in e if v != mid]
                    lo, hi = sorted((perm[ends[0]], perm[ends[1]]))
                    if not lo < perm[mid] < hi:
                        good = False
                        break
                    edges.append((lo, perm[mid], hi))
                if good:
                    break
            res = realize_exact(7, edges)
            assert res[0] is False, (lab, perm)
            assert res[1] != "inconclusive"
            checked += 1
    assert checked == 243 * 12


def test_f7_labelings_exhaustive_for_identity_like_orders():
    # every labeling, with the vertex numbering itself as the order when it is consistent
    F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    for lab in itertools.product(range(3), repeat=5):
        edges = []
        for e, k in zip(F7, lab):
            mid = e[k]
            ends = sorted(v for v in e if v != mid)
            edges.append((ends[0], mid, ends[1]))
        if all(i < j < k for i, j, k in edges):
            assert realize_exact(7, edges)[0] is False


# Hand-made order-infeasible examples (gap equations g_t = x_{t+1}-x_t):
#  (a) (0,2,3),(1,2,4) share the midpoint 2:  g0+g1 = g2  and  g1 = g2+g3  =>  g0 + g3 = 0.
#  (b) (0,3,4),(1,3,5) share the midpoint 3:  g0+g1+g2 = g3, g1+g2 = g3+g4 => g0 + g4 = 0.
#  (c) (0,1,3),(1,2,4),(0,2,4)?  g0=g1+g2, g1=g2+g3, g0+g1=g2+g3 => from 2nd: g2+g3=g1, so 3rd:
#      g0 = 0.  Verified by the oracle below (it must be infeasible; iis gives a minimal subset).
INFEASIBLE = [
    (5, [(0, 2, 3), (1, 2, 4)]),
    (6, [(0, 3, 4), (1, 3, 5)]),
    (5, [(0, 1, 3), (1, 2, 4), (0, 2, 4)]),
]


@pytest.mark.parametrize("n,edges", INFEASIBLE)
def test_exact_farkas_certificates(n, edges):
    ok, cert = order_feasible(n, edges)
    assert ok is False
    assert verify_certificate(n, edges, False, cert)
    # independent re-check of the certificate with plain Fractions
    gap_rows = []
    for i, j, k in edges:
        r = [0] * (n - 1)
        for t in range(i, j):
            r[t] += 1
        for t in range(j, k):
            r[t] -= 1
        gap_rows.append(r)
    w = [sum(cert["y"][e] * gap_rows[e][t] for e in range(len(edges))) for t in range(n - 1)]
    assert all(x >= 0 for x in w) and any(x > 0 for x in w)
    core = iis(n, edges)
    assert order_feasible(n, core)[0] is False
    for t in range(len(core)):
        assert order_feasible(n, core[:t] + core[t + 1:])[0] is True


def test_feasible_certificate_is_exact_point():
    n, edges = labeled(A_BASE)
    ok, cert = order_feasible(n, edges)
    assert ok is True and verify_certificate(n, edges, True, cert)


def test_forced_relations_and_cores():
    # a pattern with a forced parallelogram: find via library file
    lib = json.load(open("data/forbidden_ordered_n7.json"))
    assert lib["n_cores"] > 0
    for c in lib["cores"]:
        n, edges = c["n"], [tuple(e) for e in c["edges"]]
        rel = ("order",) if c["kind"] == "order" else (c["kind"], tuple(c["relation"]))
        assert is_forced(n, edges, rel)
        # minimality
        for t in range(len(edges)):
            assert not is_forced(n, edges[:t] + edges[t + 1:], rel)
        if c["kind"] != "order":
            r = realize_exact(n, edges)
            assert r[0] is False
