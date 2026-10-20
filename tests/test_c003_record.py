"""C003: the 65-point (4,5)-set with h = 37 (37/65 < 4/7), the depth-6 member of an anonymous reader's self-similar family
(Erdős Problem a Day, 19 Oct 2026; a COMMUNITY construction, not this project's). Judged PASS NEW-RECORD by judge/judge.py and
ACCEPTED by two independent referees (results/reviews/C003-reader-5-9-K6__referee__*.md); K59 [verified-here].
This test pins the cheap half: the set is a (4,5)-set, the stored witness is a 37-point 3-AP-free (Sidon) subset, 37*7 < 4*65,
and the set equals the exact rebuild of 269^6 * (O u phi(O) u ... u phi^6(O)).  The upper bound h <= 37 is the judge's and the referees'."""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from e757.core import ap_edges, is_45_set

CLAIM = Path(__file__).resolve().parents[1] / "results" / "claims" / "C003-reader-5-9-K6.json"
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]


def phi(x):
    return Fraction(101) + Fraction(18) * x / 269


def rebuild(K):
    S = set(Fraction(x) for x in O)
    cur = set(Fraction(x) for x in O)
    for _ in range(K):
        cur = {phi(x) for x in cur}
        S |= cur
    scale = 269 ** K
    out = sorted(int(x * scale) for x in S)
    assert all(x * scale == int(x * scale) for x in S)
    return out


def test_c003_record_set():
    d = json.loads(CLAIM.read_text())
    A = [int(x) for x in d["set"]]
    assert len(A) == 65 and len(set(A)) == 65
    assert A == rebuild(6)
    assert is_45_set(A)
    W = [int(x) for x in d["witness_sidon_subset"]]
    assert len(W) == 37 and set(W) <= set(A)
    Ws = set(W)
    for a, b in combinations(sorted(W), 2):  # no 3-term AP inside the witness
        if (a + b) % 2 == 0:
            assert (a + b) // 2 not in Ws or (a + b) // 2 in (a, b)
    assert 37 * 7 < 4 * 65  # ratio 37/65 is below 4/7
    assert len(ap_edges(A)) == 63  # exactly 9 APs per copy, 7 copies
