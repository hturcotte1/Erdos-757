"""The explicit 27-point witness C27 of certificate L016 (f(27) = 16, K61): C27 = A_base u (10^9 + 7919 * (A_base minus {1056}))
is a (4,5)-set with h(C27) = 16, so f(27) <= 16 [verified-here]. (The lower bound f(27) >= 16 is Theorem 1 of L016.)"""
from itertools import combinations
from e757.core import alpha, ap_edges, is_45_set

A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
C27 = sorted(A_BASE + [10 ** 9 + 7919 * x for x in A_BASE if x != 1056])


def test_c27_is_a_45_set_with_h_16():
    assert len(C27) == 27 and len(set(C27)) == 27
    assert is_45_set(C27)
    for B in combinations(C27, 4):
        assert len({abs(x - y) for x, y in combinations(B, 2)}) >= 5
    assert len(ap_edges(C27)) == 22
    assert alpha(C27) == 16
