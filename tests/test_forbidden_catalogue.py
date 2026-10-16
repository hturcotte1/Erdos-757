"""Regression test for experiments/20261014-0005-forbidden-n8/README.md (triangle and Pasch verdicts).

Everything is recomputed with e757.realizability.realize_exact; only the expected verdicts are
hard-coded.  Patterns are rank-form edge sets (i,j,k), i<j<k, 2x_j = x_i+x_k, identified up to
reflection (so also up to the automorphisms of the configuration).
"""
import itertools
from collections import Counter

from e757.core import ap_edges, is_45_set
from e757.realizability import realize_exact

TRIANGLE = ((0, 1, 2), (0, 3, 4), (1, 3, 5))                  # corners 0,1,3; edge-private 2,4,5
PASCH = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
TWO_EDGES = ((0, 1, 2), (0, 3, 4))


def reflect(n, rf):
    return tuple(sorted((n - 1 - k, n - 1 - j, n - 1 - i) for i, j, k in rf))


def verdicts(edges):
    """{rank_form: (mids, verdict)} over all vertex orders, rank forms up to reflection."""
    n = max(v for e in edges for v in e) + 1
    res = {}
    for perm in itertools.permutations(range(n)):
        rf, mids = [], []
        for e in edges:
            a, b, c = sorted(e, key=lambda v: perm[v])
            rf.append((perm[a], perm[b], perm[c]))
            mids.append(b)
        rf = tuple(sorted(rf))
        rf = min(rf, reflect(n, rf))
        if rf in res:
            continue
        r = realize_exact(n, list(rf))
        if r[0]:
            vals = r[1]
            pos = {v: i for i, v in enumerate(vals)}
            assert {frozenset((pos[a], pos[b], pos[c])) for a, b, c in ap_edges(vals)} == {frozenset(e) for e in rf}
            assert is_45_set(vals)
            v = "R"
        else:
            v = {"order-infeasible": "O", "forced extra AP": "E", "forced repeated difference": "D"}[r[1]]
        res[rf] = (tuple(mids), v)
    return res


def test_two_edge_labelings():
    res = verdicts(TWO_EDGES)
    # vertex 0 is the shared vertex.  Types: shared midpoint (both mids == 0), mid at shared vertex for one
    # edge only, no mid at the shared vertex.
    by = Counter()
    for mids, v in res.values():
        t = "shared" if mids[0] == mids[1] else ("one" if 0 in mids else "none")
        by[(t, v)] += 1
    assert dict(by) == {("shared", "O"): 1, ("shared", "D"): 1, ("one", "R"): 3, ("none", "R"): 3, ("none", "O"): 1}


def test_triangle_verdicts():
    res = verdicts(TRIANGLE)
    private = {2, 4, 5}
    by = Counter()
    for mids, v in res.values():
        injective = len(set(mids)) == 3
        medial = set(mids) == private
        by[(injective, medial, v)] += 1
        if v == "R":
            assert injective and not medial
    # whole census: 60 ordered patterns = 22 realizable + 28 order-infeasible + 10 forced repeated difference
    assert len(res) == 60
    assert dict(Counter(v for _, v in res.values())) == {"R": 22, "O": 28, "D": 10}
    # the medial triangle (all three midpoints edge-private) is forbidden in every order (K31)
    assert dict((k, c) for k, c in by.items() if k[1]) == {(True, True, "O"): 1, (True, True, "D"): 1}
    # shared midpoint (non-injective) labelings are forbidden in every order
    assert all(k[2] != "R" for k in by if not k[0])
    # every other injective labeling is realizable in at least one order
    realizable_labelings = {mids for mids, v in res.values() if v == "R"}
    all_injective = {mids for mids, v in res.values() if len(set(mids)) == 3 and set(mids) != private}
    assert realizable_labelings == all_injective


def test_pasch_verdicts():
    res = verdicts(PASCH)
    assert len(res) == 15
    assert dict(Counter(v for _, v in res.values())) == {"R": 1, "O": 13, "E": 1}
    realizable = [rf for rf, (_, v) in res.items() if v == "R"]
    # Pasch is realizable in exactly one ordered pattern (up to reflection)
    want = min(((0, 1, 3), (0, 2, 5), (1, 4, 5), (2, 3, 4)),
               reflect(6, ((0, 1, 3), (0, 2, 5), (1, 4, 5), (2, 3, 4))))
    assert realizable == [want]
    # e.g. the integer point 0,4,7,8,9,14 realizes it
    pts = [0, 4, 7, 8, 9, 14]
    assert is_45_set(pts)
    assert {frozenset(pts.index(x) for x in t) for t in ap_edges(pts)} == {frozenset(e) for e in want} or \
        {frozenset(pts.index(x) for x in t) for t in ap_edges(pts)} == {frozenset(e) for e in reflect(6, want)}
