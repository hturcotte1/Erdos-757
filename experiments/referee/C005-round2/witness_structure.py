#!/usr/bin/env python3
"""Witness check, exact ratio, and structural check that C005 = (C003 shifted by t1) U {0, 2 t1}
with t1 = 3*span(C003) + 1000003 as stated in experiments/20261021-0225-lemmaE-extensions/README.md.
Pure Python ints / Fractions; no e757, no judge."""
import itertools
import json
from fractions import Fraction

c5 = json.load(open("/home/user/Erdos-757/results/claims/C005-lemmaE-SK6-E1.json"))
c3 = json.load(open("/home/user/Erdos-757/results/claims/C003-reader-5-9-K6.json"))
A = sorted(Fraction(str(x)) for x in c5["set"])
assert all(v.denominator == 1 for v in A)
A = [int(v) for v in A]
n = len(A)
W = sorted(Fraction(str(x)) for x in c5["witness_sidon_subset"])
assert all(v.denominator == 1 for v in W)
W = [int(v) for v in W]
print("n =", n, "; witness size", len(W), "; distinct", len(set(W)) == len(W), "; subset", set(W) <= set(A))
d = [y - x for x, y in itertools.combinations(W, 2)]
print("witness Sidon by definition (all positive differences distinct):", len(d) == len(set(d)))
s = [x + y for x, y in itertools.combinations(W, 2)]
print("witness: all sums x+y (x<y) distinct:", len(s) == len(set(s)), "; also 2x vs x+y collisions:",
      any((2 * x) in set(s) for x in W))
h = int(c5["claimed_h"])
print("claimed_h", h, "== |witness|:", h == len(W))
r = Fraction(h, n)
print(f"h/n = {r}; 4/7 - h/n = {Fraction(4,7) - r}; h/n < 4/7: {r < Fraction(4,7)}; 7h={7*h} < 4n={4*n}: {7*h < 4*n}")
print(f"compare C003: 37/65 = {Fraction(37,65)}; 38/67 < 37/65: {Fraction(38,67) < Fraction(37,65)}; D = 17h - 9n = {17*h - 9*n}; D/n = {Fraction(17*h-9*n, n)} vs 5/7")
# structure
B = sorted(int(Fraction(str(x))) for x in c3["set"])
span = B[-1] - B[0]
t1 = 3 * span + 1000003
shifted = [b - B[0] + t1 for b in B]
E1 = sorted(shifted + [0, 2 * t1])
print("C003 n =", len(B), "span =", span, "t1 =", t1)
print("C005 == shift(C003) U {0, 2*t1}:", E1 == A)
print("new points: 0 and", 2 * t1, "; old min now at", t1, "; AP {0, t1, 2 t1}:", A[0] + 2 * t1 == 2 * t1 and t1 in set(A))
# differences of the old set vs the new differences (genericity, as an explicit check)
oldd = set(y - x for x, y in itertools.combinations(shifted, 2))
newd = set()
for p in (0, 2 * t1):
    for b in shifted:
        newd.add(abs(b - p))
newd.add(2 * t1)
print("new differences colliding with old differences:", len(oldd & newd), "; among themselves duplicates:",
      2 * 65 + 1 - len(newd))
