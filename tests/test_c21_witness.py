"""The explicit 21-point witness A21 of claim C006 (K66): a (4,5)-set with h(A21) = 12, so f(21) <= 12 [verified-here: frozen judge
+ referee]. With the Henning-Yeo lower bound (K8) h >= 12, f(21) = 12 [derived-here]; 12/21 = 4/7 exactly (not a record)."""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from e757.core import alpha, ap_edges, is_45_set

A21 = [0, 210, 396, 420, 444, 792, 888, 1374, 1566, 1581, 1596, 1758, 1935, 1941, 2231, 2301, 2304, 2375, 2449, 2521, 2667]


def test_a21_is_a_45_set_with_h_12():
    assert len(A21) == 21 and len(set(A21)) == 21
    assert is_45_set(A21)
    for B in combinations(A21, 4):
        assert len({abs(x - y) for x, y in combinations(B, 2)}) >= 5
    assert len(ap_edges(A21)) == 19
    assert alpha(A21) == 12
    assert Fraction(12, 21) == Fraction(4, 7)


def test_a21_matches_claim_file():
    claim = json.loads((Path(__file__).resolve().parent.parent / "results" / "claims" / "C006-tight-21pt-h12.json").read_text())
    assert claim["set"] == A21
