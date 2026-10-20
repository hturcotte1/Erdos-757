#!/usr/bin/env python3
"""L015 / C1: every finite fact about O, phi and the residues mod 269 used in Steps 1-3 of
results/proofs/L015-reader-family-c-le-5-9.md.  Written for L015 (no code shared with
experiments/20261020-1730-reader-5-9/).  Exact integers and Fractions only.
Run:  python3 -I v1_facts_O.py
"""
from fractions import Fraction as Fr
from itertools import product

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
OI = [x for x in O if x not in (0, 269)]          # O-interior, written O° in the proof
L = Fr(27169, 251)


def phi(x):
    return Fr(101) + Fr(18) * Fr(x) / 269


def ok(cond, label):
    if not cond:
        raise SystemExit("FAILED: " + label)
    print("OK  ", label)


# ---- F0: O itself
ok(O == sorted(set(O)) and len(O) == 11 and O[0] == 0 and O[-1] == 269, "F0 O has 11 distinct integers, min 0, max 269")
ok(len(OI) == 9 and min(OI) == 49 and max(OI) == 159, "F0 O° = O minus {0,269} has 9 points, all in [49,159]")

# ---- F1: arithmetic of 269, 18, 251
ok(all(269 % p for p in range(2, 17)) and 17 * 17 > 269, "F1 269 is prime (no divisor in 2..16, 17^2 > 269)")
ok(18 % 269 != 0 and 251 % 269 != 0, "F1 269 divides neither 18 nor 251 (so both are units mod 269)")
ok(27169 == 101 * 269, "F1 27169 = 101*269")
ok(251 * 108 < 27169 < 251 * 109, "F1 L = 27169/251 is not an integer (251*108 < 27169 < 251*109)")

# ---- F2: phi and its fixed point; phi^j(x) - L = (18/269)^j (x - L)
ok(L == Fr(101) + Fr(18) * L / 269, "F2 L = 27169/251 is the fixed point of phi")
# both sides of phi(x) = L + (18/269)(x - L) are affine in x, so agreement at x = 0 and x = 1 is an identity
ok(all(phi(x) == L + Fr(18, 269) * (x - L) for x in (0, 1)), "F2 phi(x) = L + (18/269)(x - L) identically")
ok(phi(0) == 101 and phi(269) == 119, "F2 phi(0) = 101 and phi(269) = 119, both in O°")
ok(all(phi(x) not in set(O) for x in OI), "F2 phi(x) is not in O for x in O° (direct check)")

# ---- F3: y(x) = 251 x - 27169 = 251 (x - L)
y = {x: 251 * x - 27169 for x in O}
ok(all(y[x] == 251 * (x - L) for x in O), "F3 y(x) = 251 (x - L)")
ok(all(y[x] != 0 for x in O), "F3 y(x) != 0 for all x in O")
ok(all((y[x] - 251 * x) % 269 == 0 for x in O), "F3 y(x) = 251 x (mod 269)")
ok([x for x in O if y[x] % 269 == 0] == [0, 269], "F3 269 | y(x) iff x in {0,269}")
ok([x for x in O if x % 269 == 0] == [0, 269], "F3 the multiples of 269 in O are exactly 0 and 269")
ok(y[0] == -101 * 269 and y[269] == 150 * 269 and y[0] % 269 ** 2 != 0 and y[269] % 269 ** 2 != 0,
   "F3 y(0) = -101*269, y(269) = 150*269, neither divisible by 269^2")
print("     y values:", y)

# ---- F4: all relations a+b = c+d inside O (pairs a<=b, c<=d, distinct pairs)
pairs = [(a, b) for i, a in enumerate(O) for b in O[i:]]
bysum = {}
for p in pairs:
    bysum.setdefault(p[0] + p[1], []).append(p)
rel = [(p, q) for v in bysum.values() for i, p in enumerate(v) for q in v[i + 1:]]
ok(len(rel) == 9, "F4 O has exactly 9 relations a+b=c+d with {a,b} != {c,d}")
E = []
for p, q in rel:
    pts = set(p) | set(q)
    # one pair must be (u,u): a relation on 3 distinct points with a doubled middle
    dbl = [r for r in (p, q) if r[0] == r[1]]
    ok(len(pts) == 3 and len(dbl) == 1, f"F4 relation {p}~{q} is a 3-AP (one pair doubled, 3 distinct points)")
    u = dbl[0][0]
    other = q if dbl[0] == p else p
    ok(other[0] < u < other[1] and other[0] + other[1] == 2 * u, f"F4   ... with middle {u}")
    E.append(tuple(sorted(pts)))
E = sorted(set(E))
expected = [(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121), (75, 117, 159),
            (83, 101, 119), (83, 121, 159), (117, 119, 121)]
ok(E == expected, "F4 the 3-APs of O are exactly the page's nine: " + str(E))
ok(sorted(e[1] for e in E) == OI, "F4 one AP centred at each of the 9 interior points (middles = O°, each once)")
ok(all(len(set(e) & set(f)) <= 1 for i, e in enumerate(E) for f in E[i + 1:]), "F4 no two APs of O share two points")
ok(not any(0 in e and 269 in e for e in E), "F4 no AP of O contains both 0 and 269")
# a direct second derivation of the APs: triples a<u<c in O with a+c = 2u
E2 = sorted((a, u, c) for a in O for u in O for c in O if a < u < c and a + c == 2 * u)
ok(E2 == E, "F4 second derivation (all triples a<u<c, a+c=2u) gives the same 9 APs")

# ---- F5: the deepest-level congruences, over O°, every sign pattern, ordered tuples
# m = 1:  x = 0 (mod 269)
ok([x for x in OI if x % 269 == 0] == [], "F5 m=1: no x in O° with x = 0 (mod 269)")
# m = 2, same side: x1 + x2 = 0 (mod 269), x1 = x2 allowed
ok([(a, b) for a, b in product(OI, OI) if (a + b) % 269 == 0] == [], "F5 m=2 same side: no x1+x2 = 0 (mod 269) in O° (incl. x1 = x2)")
# m = 2, opposite sides: x1 - x2 = 0 (mod 269) only if x1 = x2
ok(all(a == b for a, b in product(OI, OI) if (a - b) % 269 == 0), "F5 m=2 opposite sides: x1 = x2 (mod 269) forces x1 = x2")
# m = 3, two on one side (x_a, x_b), one on the other (x_c): x_a + x_b - x_c = 0 (mod 269)
sol3 = sorted((a, b, c) for a, b, c in product(OI, OI, OI) if (a + b - c) % 269 == 0)
ok(sol3 == [(49, 49, 98), (159, 159, 49)], "F5 m=3: the only solutions are (49,49,98) and (159,159,49): " + str(sol3))
for a, b, c in sol3:
    d = 2 * a - c
    ok(a == b and d in (0, 269) and tuple(sorted((d, a, c))) in E, f"F5   ({a},{a},{c}): 4th point 2*{a}-{c} = {d}, and {{{d},{a},{c}}} is an AP of O")
# all four sign patterns of m = 3 reduce to this one (the relation is symmetric); check that directly too:
for signs in product((1, -1), repeat=3):
    if abs(sum(signs)) != 1:
        continue          # (+,+,+) and (-,-,-) cannot occur: 3 positions of a 4-term relation with signs (+,+,-,-)
    s3 = sorted(t for t in product(OI, OI, OI) if sum(e * v for e, v in zip(signs, t)) % 269 == 0)
    ok(len(s3) == 2, f"F5 m=3 sign pattern {signs}: exactly 2 ordered solutions (the two above, reordered)")

# ---- F6: phi^d(x') in O with x' in O and d >= 1 only for d = 1, x' in {0,269}  (direct, d <= 6; the proof handles all d)
hits = []
for xp in O:
    v = Fr(xp)
    for d in range(1, 7):
        v = phi(v)
        if v in set(Fr(x) for x in O):
            hits.append((xp, d, v))
ok(hits == [(0, 1, 101), (269, 1, 119)], "F6 phi^d(x') in O (x' in O, 1 <= d <= 6) only for (0,1)->101 and (269,1)->119")
print("ALL FACTS OK")
