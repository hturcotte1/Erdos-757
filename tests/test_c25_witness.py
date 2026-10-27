"""The explicit 25-point witness C25 of certificate L023 (f(25) = 15): C25 = A_base u (10^9 + 7919 * B11), with B11 the 11-point
record of data/small_records.json (h = 7), is a (4,5)-set with h(C25) = 15, so f(25) <= 15 [verified-here: frozen judge, claim C007].
(The lower bound f(25) >= 15 is Corollary 5 of results/proofs/L023-f25-equals-15.md, submitted, unrefereed.)"""
import json
from itertools import combinations
from pathlib import Path

from e757.core import alpha, ap_edges, is_45_set

REPO = Path(__file__).resolve().parent.parent
A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B11 = [0, 2009010, 2901878, 3392944, 3459949, 3705482, 3750000, 3794746, 3884010, 4018020, 7500000]
C25 = sorted(A_BASE + [10 ** 9 + 7919 * x for x in B11])


def test_b11_is_the_stored_11_point_record():
    rec = json.loads((REPO / "data" / "small_records.json").read_text())["sets"]["11"]
    assert rec["set"] == B11 and rec["h"] == 7


def test_c25_is_a_45_set_with_h_15():
    assert len(C25) == 25 and len(set(C25)) == 25
    assert is_45_set(C25)
    for B in combinations(C25, 4):
        assert len({abs(x - y) for x, y in combinations(B, 2)}) >= 5
    assert len(ap_edges(C25)) == 20  # 12 + 8: no AP uses points of both parts
    assert alpha(C25) == 15


def test_c25_matches_claim_file():
    claim = json.loads((REPO / "results" / "claims" / "C007-c25-witness-f25.json").read_text())
    assert claim["set"] == C25
    assert claim["claimed_h"] == 15
