"""The explicit 23-point witness C23 of certificate L014 (results/proofs/L014-f23-equals-14.md, Step 5.3, C10):
C23 = B12 u (10^9 + 7919 * B11) is a (4,5)-set with h(C23) = 14, so f(23) <= 14 [verified-here].
(The lower bound f(23) >= 14 is Theorem 2 of L014 (with Theorem 1 there and L012 Theorem 1); L014 is ACCEPTED x3, K58, and
e757.fn_bounds.EXACT_VALUES_VERIFIED[23] = 14.  This test pins only the upper-bound witness.)"""
from fractions import Fraction
from itertools import combinations
from e757.core import alpha, ap_edges, is_45_set

C23 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575, 1000000000, 16909350190, 23979971882,
       27868723536, 28399336131, 30343711958, 30696250000, 31050593574, 31757475190, 32818700380, 60392500000]


def test_c23_is_a_45_set_with_h_14():
    assert len(set(C23)) == 23
    assert is_45_set(C23)
    # every 4-subset determines at least 5 distinct absolute differences (exact integers)
    for B in combinations(C23, 4):
        assert len({abs(x - y) for x, y in combinations(B, 2)}) >= 5
    edges = ap_edges(C23)
    assert len(edges) == 18
    assert alpha(C23) == 14
