#!/usr/bin/env python3
"""Referee round 3, L015: (i) I_6 (my construction) equals the set of
results/claims/C003-reader-5-9-K6.json; (ii) the stored witness is a Sidon subset of
size 37; (iii) 37/65 < 4/7 exactly; (iv) the claim file parses as integers only;
(v) ratio table (7+5K)/(11+9K) vs 4/7 and 5/9 with Fractions."""
from fractions import Fraction as Fr
from itertools import combinations
import json, sys

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
def N(x, j):
    v = x
    for i in range(1, j + 1):
        v = 101 * 269 ** i + 18 * v
    return v
def integer_set(base, K):
    return sorted({269 ** (K - j) * N(x, j) for j in range(K + 1) for x in base})

fails = []
def chk(c, m):
    print(("OK   " if c else "FAIL ") + m)
    if not c: fails.append(m)

raw = open("/home/user/Erdos-757/results/claims/C003-reader-5-9-K6.json").read()
d = json.loads(raw)
S = d["set"]
chk(all(isinstance(v, int) and not isinstance(v, bool) for v in S), "claim set entries are JSON integers (no floats/strings)")
chk(len(S) == 65 and len(set(S)) == 65, "claim set has 65 distinct entries")
I6 = integer_set(O, 6)
chk(sorted(S) == I6, "claim set == my I_6 = 269^6 S_6 (as a set)")
chk(S == sorted(S), "claim set is sorted")
W = d["witness_sidon_subset"]
chk(set(W) <= set(S) and len(W) == len(set(W)) == 37, "witness: 37 distinct points, subset of the set")
sums = [a + b for a, b in combinations(sorted(W), 2)] + [2 * a for a in W]
chk(len(set(sums)) == len(sums), "witness Sidon by definition (%d distinct sums)" % len(set(sums)))
chk(d["claimed_h"] == 37, "claimed_h = 37")
chk(Fr(37, 65) < Fr(4, 7), "37/65 < 4/7 exactly (37*7=%d < 4*65=%d)" % (37 * 7, 4 * 65))
chk(Fr(d["claimed_h"], len(S)) == Fr(37, 65), "claimed ratio = 37/65")
# scaled-copy check: the set in C003 divided by gcd
from math import gcd
from functools import reduce
g = reduce(gcd, S)
print("gcd of claim set =", g, "(the set is the raw 269^6-scaling; min =", min(S), ", max =", max(S), "= 269^7 ?", max(S) == 269 ** 7, ")")
# ratio table
print("K  n    h    ratio      ratio-5/9        <4/7")
for K in range(0, 12):
    n, h = 11 + 9 * K, 7 + 5 * K
    print("%-2d %-4d %-4d %-10s %-16s %s" % (K, n, h, Fr(h, n), Fr(h, n) - Fr(5, 9), Fr(h, n) < Fr(4, 7)))
chk(Fr(32, 56) == Fr(4, 7), "K=5 ratio equals 4/7 exactly")
chk(all(Fr(7 + 5 * K, 11 + 9 * K) - Fr(5, 9) == Fr(8, 9 * (11 + 9 * K)) for K in range(200)), "ratio - 5/9 = 8/(9(11+9K)) for K<200")
chk(min(K for K in range(100) if Fr(7 + 5 * K, 11 + 9 * K) < Fr(4, 7)) == 6, "smallest K below 4/7 is 6")
print("ALL C003 CHECKS OK" if not fails else "FAILURES: %s" % fails)
sys.exit(1 if fails else 0)
