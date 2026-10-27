"""Referee L023 round 1: Q8 without any pruning. All 3^6 = 729 midpoint assignments of the six triples; for each, the exact
solution space V (Fractions) and the generic-point test of realize_generic.py (own code). Also counts the injective assignments
(the prover's 'labellings') and, for those, the dimension of V (2 = unique up to affine maps)."""
import itertools, json
from fractions import Fraction
import realize_generic as R
Q = [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 2, 7)]
n = 8
cnt = dict(total=0, injective=0, good_generic=0, injective_dim2=0)
reasons = {}
for choice in itertools.product(range(3), repeat=6):
    cnt['total'] += 1
    Rv = [tuple(Fraction(int(v == t)) for t in range(n)) for v in range(n)]
    mids = []
    for e, c in zip(Q, choice):
        mid = e[c]; x, y = [v for v in e if v != mid]; mids.append(mid)
        Rv = R.add_eq(Rv, x, mid, y)
    inj = len(set(mids)) == 6
    bad = R.generic_bad(Rv, n)
    if inj:
        cnt['injective'] += 1
        if len(Rv[0]) == 2: cnt['injective_dim2'] += 1
    if bad is None: cnt['good_generic'] += 1
    else: reasons[bad[0]] = reasons.get(bad[0], 0) + 1
print(json.dumps(cnt), json.dumps(reasons))
print('RESULT Q8:', 'NOT-REALIZABLE' if cnt['good_generic'] == 0 else 'REALIZABLE')
