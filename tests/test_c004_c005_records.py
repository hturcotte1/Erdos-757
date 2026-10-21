"""C004 (58 points, h = 33) and C005 (67 points, h = 38): this project's Lemma-E two-point extensions, at the universal
minimum, of the community sets S_5 and S_6 (an anonymous reader's family, Erdős Problem a Day, 19 Oct 2026). Judged PASS
NEW-RECORD by judge/judge.py and ACCEPTED by two independent referees each (results/reviews/C004-*, C005-*); K62, K63.
This test pins the cheap half: each set is a (4,5)-set, equals S_K u {a - t, a + t} with a = min S_K (translated to start at 0),
the stored witness is a Sidon subset of the claimed size, and 7h < 4n.  The upper bound on h is the judge's and the referees'."""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from e757.core import ap_edges, is_45_set

ROOT = Path(__file__).resolve().parents[1]
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]


def family(K):
    S = set(Fraction(x) for x in O); cur = set(S)
    for _ in range(K):
        cur = {Fraction(101) + Fraction(18) * x / 269 for x in cur}; S |= cur
    return sorted(int(x * 269 ** K) for x in S)


def check(claim, K, t, n, h, m):
    d = json.loads((ROOT / "results" / "claims" / claim).read_text())
    A = [int(x) for x in d["set"]]
    assert len(A) == n and len(set(A)) == n
    S = family(K)
    E = sorted([S[0] - t, S[0] + t] + S)
    assert A == [x - E[0] for x in E]  # the Lemma-E extension at the minimum, translated to start at 0
    assert is_45_set(A)
    assert len(ap_edges(A)) == m
    W = [int(x) for x in d["witness_sidon_subset"]]
    assert len(W) == h and set(W) <= set(A)
    Ws = set(W)
    for a, b in combinations(sorted(W), 2):
        if (a + b) % 2 == 0 and (a + b) // 2 not in (a, b):
            assert (a + b) // 2 not in Ws
    assert 7 * h < 4 * n


def test_c004():
    check("C004-lemmaE-SK5-E1.json", 5, 3 * 269 ** 6 + 1000003, 58, 33, 55)


def test_c005():
    check("C005-lemmaE-SK6-E1.json", 6, 3 * 269 ** 7 + 1000003, 67, 38, 64)
