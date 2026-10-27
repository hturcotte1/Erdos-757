"""The explicit 19-point witness A19 of claim C008 (K70): a (4,5)-set with h(A19) = 11, so f(19) <= 11 [verified-here: frozen judge
+ referee]. With the Henning-Yeo lower bound (K8) h >= 11, f(19) = 11 [derived-here]; 11/19 > 4/7 (not a record)."""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from e757.core import alpha, ap_edges, is_45_set

A19 = [0, 14756207, 18236662, 22551504, 26866346, 29512414, 31669835, 35323160, 36473324, 37256612, 37818662, 38021000,
       38290784, 38380712, 38740424, 38762906, 38785388, 38976485, 39190064]


def test_a19_is_a_45_set_with_h_11():
    assert len(A19) == 19 and len(set(A19)) == 19
    assert is_45_set(A19)
    for B in combinations(A19, 4):
        assert len({abs(x - y) for x, y in combinations(B, 2)}) >= 5
    assert len(ap_edges(A19)) == 16
    assert alpha(A19) == 11
    assert Fraction(11, 19) > Fraction(4, 7)


def test_a19_matches_claim_file():
    claim = json.loads((Path(__file__).resolve().parent.parent / "results" / "claims" / "C008-f19-h11.json").read_text())
    assert claim["set"] == A19
    assert claim["claimed_h"] == 11
