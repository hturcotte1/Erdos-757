#!/usr/bin/env python3
"""Exact constants used in the hand proof of the span lemma (see README, Lemma 2).
y(x) = 251 x - 27169 = 251 (x - L), L = 27169/251 the fixed point of phi."""
import itertools
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
Oint = [x for x in O if x not in (0, 269)]
y = {x: 251 * x - 27169 for x in O}
assert 27169 == 101 * 269 and 251 * 108 < 27169 < 251 * 109            # L = 27169/251 not an integer
assert all(v != 0 for v in y.values())                                  # no point of O equals L
assert min(y.values()) == -27169 and max(y.values()) == 40350
assert all(abs(v) <= 40350 for v in y.values())
assert 18 ** 3 <= 40350 < 18 ** 4
assert 269 ** 2 > 13181 == 49 * 269
# phi(x) = L + (18/269)(x - L) = 101 + 18 x / 269
from fractions import Fraction as F
L = F(27169, 251)
assert all(L + F(18, 269) * (F(x) - L) == F(101) + F(18 * x, 269) for x in range(0, 300))
# mod 269: y = 251 x (mod 269), 251 invertible
assert all((y[x] - 251 * x) % 269 == 0 for x in O)
assert all(y[x] % 269 != 0 for x in Oint)           # interior points never vanish mod 269
assert [x for x in O if y[x] % 269 == 0] == [0, 269]
# deepest level with exactly two points of the same sign:  x1 + x2 = 0 (mod 269)
pairs = [(a, b) for a, b in itertools.combinations_with_replacement(Oint, 2) if (a + b) % 269 == 0]
print("pairs x1<=x2 in O-interior with x1+x2 = 0 mod 269:", pairs)
# v_18-type divisibility of y: largest d with 18^d | y(x)
def d18(v):
    d = 0
    while v % (18 ** (d + 1)) == 0:
        d += 1
    return d
print("y(x) and largest d with 18^d | y(x):", {x: (y[x], d18(y[x])) for x in O})
print("max over O of d18:", max(d18(y[x]) for x in O))
# deepest level with exactly three points: x1 + x2 - x3 = 0 mod 269 (signs ++-) or 2 x1 - x3 (a=b)
triples = [(a, b, c) for a, b in itertools.combinations_with_replacement(Oint, 2) for c in Oint if (a + b - c) % 269 == 0]
print("(x1,x2,x3) interior with x1+x2 = x3 mod 269:", triples)
print("all constants OK")

# ---- finite facts about O used in the hand proof (README, Lemmas 1-3) ----
from collections import defaultdict
sums = defaultdict(list)
for i, a in enumerate(O):
    for b in O[i:]:
        sums[a + b].append((a, b))
rels = [prs for prs in sums.values() if len(prs) > 1]
aps_O = []
for prs in rels:
    assert len(prs) == 2
    pts = set(prs[0]) | set(prs[1])
    assert len(pts) == 3, "a relation on 4 distinct points exists in O (parallelogram)"
    aps_O.append(tuple(sorted(pts)))
assert len(aps_O) == 9, aps_O
print("APs of O (the only relations a+b=c+d in O):", sorted(aps_O))
assert all(len(set(e) & set(f)) <= 1 for e, f in itertools.combinations(aps_O, 2)), "two APs of O share two points"
assert not any(0 in e and 269 in e for e in aps_O), "an AP of O contains both 0 and 269"
# every AP is centred at a distinct interior point (one AP per interior point)
assert sorted(e[1] for e in aps_O) == sorted(Oint)
# m = 3 case: the two mod-269 solutions force the 4th point 2 x_a - x_c in {0, 269} (an anchor), i.e. an AP of O
for (a, b, c) in triples:
    assert a == b and (2 * a - c) in (0, 269) and tuple(sorted((2 * a - c, a, c))) in aps_O
print("m=3 solutions are exactly the APs {0,49,98} and {49,159,269}: OK")
# phi(0)=101 and phi(269)=119 (the shared points), both interior points of O
assert F(101) + F(18 * 0, 269) == 101 and F(101) + F(18 * 269, 269) == 119
print("finite facts about O OK")
