"""Brute force (n <= 22) on the family members S_0, S_1 and their Lemma-E extensions E1(S_0), E1(S_1)."""
import sys
from fractions import Fraction
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
def S_K(K):
    pts = set(Fraction(x) for x in O); cur = [Fraction(x) for x in O]
    for _ in range(K):
        cur = [Fraction(101) + Fraction(18, 269) * x for x in cur]; pts |= set(cur)
    return sorted(int(x * 269 ** K) for x in pts)
for K in (0, 1):
    S = S_K(K); span = S[-1] - S[0]; t = 3 * span + 1000003
    E = sorted([S[0] - t, S[0] + t] + S); E = [x - E[0] for x in E]
    for name, X in (('S_%d' % K, S), ('E1(S_%d)' % K, E)):
        forb, census = R.forbidden_sets(X)
        ve = R.ve_max_independent(len(X), forb)[0]
        bm, cnt = R.brute_max(len(X), forb)
        bd = R.brute_max_by_definition(X) if len(X) <= 13 else None
        print(name, 'n', len(X), 'is45', R.is45_literal(X)[0], 'census', census, 'VE', ve, 'brute', bm,
              '#max', cnt, 'brute-by-definition', bd)
