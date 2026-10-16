"""Exact counts of extremal (4,5)-sets (h = f(n)) for small n: re-derive n=8 and n=10 (saturated, m = n-2) and check that the
record sets of data/small_records.json are among the affine classes.  Pipeline: experiments/20261014-1430-small-counts/counts.py
(C DFS over class O with alpha <= f(n), exact realization of every pattern, is_45_set/alpha re-check).
Expected (see the experiment README): n=8: 260 labelled / 130 up to reflection / 66 realizable;
n=10: 79488 / 39765 / 6644."""
import json
import os
import sys

import pytest

from e757.core import alpha, is_45_set
from e757.ordered_dfs_c import available

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments", "20261014-1430-small-counts"))
sys.path.insert(0, os.path.join(ROOT, "experiments", "20261014-1005-census-dfs"))
pytestmark = pytest.mark.skipif(not available(), reason="C binary unavailable")


def derive(n, m):
    import counts as c
    pats, stats, _ = c.enum(n, m)
    cs = sorted(set(c.canon(n, p) for p in pats))
    real, reasons, fb = c.realize_all(n, m, cs)
    return c, pats, cs, real


def record_pattern(c, vals):
    from e757.core import ap_edges
    vals = sorted(vals)
    pos = {v: i for i, v in enumerate(vals)}
    edges = [(pos[a], pos[b], pos[d]) for a, b, d in ap_edges(vals)]
    return len(vals), len(edges), c.canon(len(vals), edges)


@pytest.mark.parametrize("n,lab,refl,nreal", [(8, 260, 130, 66), (10, 79488, 39765, 6644)])
def test_saturated_counts(n, lab, refl, nreal):
    c, pats, cs, real = derive(n, n - 2)
    classes = {c.normalize(r["set"]) for r in real}
    assert (len(pats), len(cs), len(real), len(classes)) == (lab, refl, nreal, nreal)
    for r in real:
        assert r["h"] == c.F[n] and r["is_45"] and r["dim"] == 2
        assert is_45_set(r["set"]) and alpha(sorted(r["set"])) == c.F[n]


@pytest.mark.parametrize("key", ["8", "10"])
def test_record_sets_are_among_the_extremal_patterns(key):
    """The n=8 record has m=5 APs (non-saturated: lies in a 1-parameter family), the n=10 record m=8 (saturated: a single class)."""
    import counts as c
    rec = json.load(open(os.path.join(ROOT, "data", "small_records.json")))["sets"][key]["set"]
    n, m, pat = record_pattern(c, rec)
    assert (n, m) == {"8": (8, 5), "10": (10, 8)}[key]
    c, pats, cs, real = derive(n, m)
    assert pat in {c.canon(n, r["edges"]) for r in real}
    if m == n - 2:
        assert c.normalize(rec) in {c.normalize(r["set"]) for r in real}
