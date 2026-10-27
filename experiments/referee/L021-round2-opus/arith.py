"""Exact arithmetic checks of the edited passages of L021 (round 2) and of the
case split 4.3. Fractions / ints only."""
from fractions import Fraction as Fr
from itertools import combinations_with_replacement
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rlib import A_of, s_of

ok = True


def check(cond, msg):
    global ok
    print(("OK   " if cond else "FAIL ") + msg)
    ok = ok and cond


# identity A = 12 s - 9 n + 11 m  and  A = 12(s + n/6 - 11(n-m)/12)
good = all(A_of(n, m, t) == 12 * s_of(n, m, t) - 9 * n + 11 * m and
           Fr(A_of(n, m, t)) == 12 * (s_of(n, m, t) + Fr(n, 6) - Fr(11, 12) * (n - m))
           for n in range(0, 60) for m in range(0, 60) for t in range(0, 30))
check(good, "A = 27n+35m-132tau = 12s-9n+11m = 12(s+n/6-11(n-m)/12) on a grid")

# piece types: weights and slacks
types = {(3, 1, 1): (16, 0), (8, 5, 3): (5, 1), (10, 7, 4): (13, 0), (15, 11, 6): (2, 1), (17, 13, 7): (10, 0)}
for (n, m, t), (W, s) in types.items():
    check(-A_of(n, m, t) == W and s_of(n, m, t) == s,
          f"piece type {(n, m, t)}: W = {-A_of(n, m, t)} (claimed {W}), s = {s_of(n, m, t)} (claimed {s})")
    # J_{1/6}: 66 tau <= 19 n + 12 m  <=>  W <= 11(n-m)
    check(66 * t <= 19 * n + 12 * m and W <= 11 * (n - m), f"  J_1/6 and W <= 11(n-m) = {11*(n-m)}")
    # disconnected case of 7.6: B = F + v + 3 edges, tau(B) = tau(F)+1
    nB, mB, tB = n + 1, m + 3, t + 1
    check(s_of(nB, mB, tB) == s - 2 and s_of(nB, mB, tB) < 0 and nB <= 18,
          f"  7.6 disconnected case: B = {(nB, mB, tB)}, s(B) = {s_of(nB, mB, tB)} = s(F)-2 < 0, n(B) <= 18")

# (14,12,6): A = +6 ; A_base and 12-point sanity values
check(A_of(14, 12, 6) == 6, "A(14,12,6) = +6")
check(A_of(12, 10, 5) == 14 and 19 * 12 + 12 * 10 - 66 * 5 == 18, "12-point records: A = 14, J slack 18")
check(19 * 14 + 12 * 12 - 66 * 6 == 14, "A_base J_{1/6} slack 14")

# KT* remark examples
for (n, m, t), (s, A) in {(21, 10, 7): (6, -7), (27, 13, 9): (8, -4)}.items():
    check(s_of(n, m, t) == s and A_of(n, m, t) == A and 11 * m < 9 * n,
          f"remark cell {(n, m, t)}: s = {s_of(n, m, t)}, A = {A_of(n, m, t)}, sparse (11m < 9n: {11*m} < {9*n})")

# hypertrees with a perfect matching: n = 6k+3, m = 3k+1, tau = 2k+1
for k in range(0, 12):
    n, m, t = 6 * k + 3, 3 * k + 1, 2 * k + 1
    A = A_of(n, m, t)
    defM = 16 * t - 35 * (m - t)          # matching family: 2k+1 copies of E_1, E* = the k other edges
    check(A == 3 * k - 16 and defM == 16 - 3 * k and A + defM == 0,
          f"hypertree k={k}: A = {A} = 3k-16, DEF_H(M) = {defM} = 16-3k, A + DEF_H(M) = 0")
# general perfect matching identity: A + DEF_H(M) = (35m-17n) + (17n-35m) = 0 (tau = n/3)
check(all(A_of(3 * q, m, q) + (16 * q - 35 * (m - q)) == 0 for q in range(1, 40) for m in range(q, 4 * q)),
      "any H with perfect matching M and tau = |M|: A + DEF_H(M) = 0")

# saturated remark: m = n-2 gives A = 12 s + 2 n - 22 ; HY bound gives s >= (m-4n)/17 = -(3n+2)/17
check(all(A_of(n, n - 2, t) == 12 * s_of(n, n - 2, t) + 2 * n - 22 for n in range(2, 80) for t in range(0, 40)),
      "m = n-2: A = 12s + 2n - 22")
check(all(Fr(s_of(n, n - 2, 0) * 17 - 11 * (5 * n + 3 * (n - 2)), 17) == Fr(-(3 * n + 2), 17)
          for n in range(2, 80)),
      "HY (17 tau <= 5n+3m) with m = n-2 gives exactly s >= -(3n+2)/17")
# n >= 28 saturated: HY admits negative A? smallest n with 12*floor-bound + 2n - 22 < 0
neg = [n for n in range(11, 80) if 12 * Fr(-(3 * n + 2), 17) + 2 * n - 22 < 0]
print("     (info) n >= 11 where the HY floor alone would allow A < 0 for saturated graphs:", neg[:5], "...")

# Theorem 1(b) numbers
check(Fr(6) - Fr(1, 6) == Fr(35, 6) and (Fr(6) - Fr(1, 6)) / 11 == Fr(35, 66) and Fr(35, 66) > Fr(9, 17),
      "35/66 > 9/17")
check(all(((6 - e) / 11 > Fr(9, 17)) == (e < Fr(3, 17)) for e in [Fr(3, 17) - Fr(1, 1000), Fr(3, 17), Fr(3, 17) + Fr(1, 1000), Fr(0), Fr(1, 6)]),
      "(6-eps)/11 > 9/17 iff eps < 3/17")
check(27 + 3 * 35 == 132 and 27 + 2 * 35 - 132 == -35 and 27 + 35 - 132 == -70, "hub balances 0, -35, -70")

# 4.3 case split: brute force over j, e_v, k_v and weight multisets from the five W values
Ws = [16, 13, 10, 5, 2]
feasible = set()
for j in range(1, 9):
    for ev in range(0, 25):
        for kv in range(0, 4):
            if not (ev + kv >= j + 1):         # (ii), from (E)
                continue
            for ws in combinations_with_replacement(Ws, j):
                if sum(ws) - 35 * ev >= 1:     # (i)
                    feasible.add((j, ev, kv, sum(ws) >= 36))
print("     (info) feasible (j, e_v, k_v, sumW>=36):", sorted(feasible))
exp = {(1, 0, 2), (1, 0, 3), (2, 0, 3), (3, 1, 3)}
check({(j, ev, kv) for (j, ev, kv, _) in feasible} == exp and all(b for (j, ev, kv, b) in feasible if j == 3),
      "4.3: only (D1) j=1,e=0,k in {2,3}; (D2) j=2,e=0,k=3; (D3) j=3,e=1,k=3 with sum W >= 36")
# also with arbitrary integer weights 1..16 (only W <= 16 used in the proof)
feasible2 = set()
for j in range(1, 9):
    for ev in range(0, 25):
        for kv in range(0, 4):
            if ev + kv >= j + 1 and 16 * j - 35 * ev >= 1:
                feasible2.add((j, ev, kv))
check(feasible2 == exp, "4.3 with any weights <= 16: same three cases")
# max of sum W - 35 e_v over the cases (bound A(H) >= -32)
mx = max([16, 16 + 16, 16 * 3 - 35])
check(mx == 32, "largest sum W - 35 e_v is 32 (D2 with two E_1)")

# Theorem 6 theta table: theta = 50c - 27e - 66[c odd], e <= min(C(c,2), floor(3c/2)), connected e >= c-1
negs = []
for c in range(1, 200):
    emax = min(c * (c - 1) // 2, (3 * c) // 2)
    for e in range(max(0, c - 1), emax + 1):
        th = 50 * c - 27 * e - 66 * (c % 2)
        if th < 0:
            negs.append((c, e, th))
check(negs == [(1, 0, -16), (5, 7, -5)], f"theta < 0 only for (c,e) = (1,0): -16 and (5,7): -5; found {negs}")
# 6.2 algebra: 66(N+|U|-o) - 16N - 27M with N = |U| + sum c, M <= 3|U| + sum e
# A >= 35|U| + sum theta  <=>  identity 66N+66U-66o-16N-81U-27 sum e = 35U + sum(50c - 27e) - 66 o
check(all(66 * (U + sc + U) - 66 * o - 16 * (U + sc) - 27 * (3 * U + se) == 35 * U + 50 * sc - 27 * se - 66 * o
          for U in range(6) for sc in range(10) for se in range(12) for o in range(5)),
      "6.2 algebra")
print("ALL OK" if ok else "SOME FAILURE")
