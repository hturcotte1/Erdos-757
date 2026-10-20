#!/usr/bin/env python3
"""Referee round 3, L015: independent check of the finite facts F0-F6, the 16-entry
transfer table, the hitting-set numbers of Step 5.6, U*, and R_0 (x) M = R_0 + 5.
Written from the certificate statement only; no code imported from anywhere."""
from fractions import Fraction as Fr
from itertools import combinations, product
import sys

fails = []
def chk(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
Oset = set(O)
Oin = [x for x in O if x not in (0, 269)]
r = Fr(18, 269)
phi = lambda x: 101 + r * x
L = Fr(27169, 251)
y = lambda x: 251 * x - 27169

# ---- F0
chk(len(O) == 11 and len(Oset) == 11 and O == sorted(O), "F0 11 distinct sorted integers")
chk(min(O) == 0 and max(O) == 269, "F0 min 0 max 269")
chk(len(Oin) == 9 and all(49 <= x <= 159 for x in Oin), "F0 interior in [49,159], 9 points")

# ---- F1
def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
chk(is_prime(269), "F1 269 prime")
chk(18 % 269 and 251 % 269, "F1 269 does not divide 18, 251")
chk(27169 == 101 * 269, "F1 27169 = 101*269")
chk(L.denominator != 1, "F1 L not an integer")
chk(L == Fr(101 * 269, 269 - 18), "F1 L = 101/(1-r)")

# ---- F2
chk(phi(L) == L, "F2 phi(L) = L")
chk(all(phi(Fr(x)) == L + r * (x - L) for x in range(-300, 600)), "F2 phi(x) = L + r(x-L) (integers -300..599)")
chk(phi(0) == 101 and phi(269) == 119, "F2 phi(0)=101, phi(269)=119")

# ---- F3
chk(all(y(x) == 251 * (x - L) for x in O), "F3 y(x) = 251(x-L)")
chk(all(y(x) != 0 for x in O), "F3 y(x) != 0 on O")
chk(all((y(x) - 251 * x) % 269 == 0 for x in O), "F3 y(x) = 251x mod 269")
chk(all((y(x) % 269 == 0) == (x in (0, 269)) for x in O), "F3 269 | y(x) iff x in {0,269}")
chk(y(0) == -101 * 269 and y(269) == 150 * 269, "F3 y(0), y(269)")
chk(y(0) % (269 ** 2) != 0 and y(269) % (269 ** 2) != 0, "F3 269^2 divides neither")

# ---- F4: relations in O, via all 66 sums and via all AP triples
sums = {}
for a, b in combinations(O, 2):
    sums.setdefault(a + b, []).append((a, b))
for a in O:
    sums.setdefault(2 * a, []).append((a, a))
chk(sum(len(v) for v in sums.values()) == 66, "F4 66 sums x+y with x<=y")
rep = {s: v for s, v in sums.items() if len(v) >= 2}
chk(len(rep) == 9 and all(len(v) == 2 for v in rep.values()), "F4 exactly 9 repeated sums, each exactly twice")
E_from_sums = set()
for s, v in rep.items():
    (a, b), (c, d) = v
    pts = {a, b, c, d}
    chk(len(pts) == 3 and (a == b or c == d), "F4 repeated sum %d is a doubled middle: %s" % (s, v))
    E_from_sums.add(frozenset(pts))
E_claimed = [frozenset(e) for e in [(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121),
                                    (75, 117, 159), (83, 101, 119), (83, 121, 159), (117, 119, 121)]]
E_triples = {frozenset((a, u, c)) for a, u, c in combinations(O, 3) if a + c == 2 * u}
chk(E_from_sums == set(E_claimed) == E_triples, "F4 E(O) = the nine listed APs (from sums and from triples)")
expected_rep = {98: [(0, 98), (49, 49)], 150: [(49, 101), (75, 75)], 166: [(49, 117), (83, 83)], 318: [(49, 269), (159, 159)],
                196: [(75, 121), (98, 98)], 234: [(75, 159), (117, 117)], 202: [(83, 119), (101, 101)],
                242: [(83, 159), (121, 121)], 238: [(117, 121), (119, 119)]}
chk({s: sorted(v) for s, v in rep.items()} == {s: sorted(v) for s, v in expected_rep.items()}, "F4 the nine repeated sums as listed")
mids = sorted(sorted(e)[1] for e in E_claimed)
chk(mids == Oin, "F4 middles = interior points, one each")
chk(all(len(e & f) <= 1 for e, f in combinations(E_claimed, 2)), "F4 pairwise intersections <= 1")
chk(all(not ({0, 269} <= e) for e in E_claimed), "F4 no edge contains both 0 and 269")
# every relation in O (4-tuples) is an AP relation
nrel = 0
for p in product(O, repeat=4):
    if p[0] + p[1] == p[2] + p[3] and sorted(p[:2]) != sorted(p[2:]):
        nrel += 1
        pts = frozenset(p)
        chk_ok = pts in set(E_claimed) and (p[0] == p[1] or p[2] == p[3])
        if not chk_ok:
            fails.append("F4 relation not AP: %s" % (p,))
chk(nrel == 9 * 4, "F4 exactly 36 ordered relation tuples in O (9 relations x 4 symmetries), all AP relations")

# ---- F5 (mod 269 over interior points, exhaustive)
chk(all(x % 269 != 0 for x in Oin), "F5(i)")
chk(all((a + b) % 269 != 0 for a in Oin for b in Oin), "F5(ii) (a=b allowed)")
chk(all(((a - b) % 269 == 0) == (a == b) for a in Oin for b in Oin), "F5(iii)")
sol = sorted((a, b, c) for a in Oin for b in Oin for c in Oin if (a + b - c) % 269 == 0)
chk(sol == [(49, 49, 98), (159, 159, 49)], "F5(iv) solutions = {(49,49,98),(159,159,49)}: %s" % sol)
chk(all(2 * a - c in (0, 269) for a, b, c in sol), "F5(iv) fourth point 2x1-x3 in {0,269}")
# also all sign patterns with one sign opposite to the other two (positions of T in the m=3 case)
for signs in [(1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]:
    s2 = sorted((a, b, c) for a in Oin for b in Oin for c in Oin if (signs[0] * a + signs[1] * b + signs[2] * c) % 269 == 0)
    chk(len(s2) == 2 and all(sorted(t) in ([49, 49, 98], [49, 159, 159]) for t in s2), "F5(iv) sign pattern %s -> 2 solutions" % (signs,))

# ---- F6: phi^d(x') in O for 1<=d<=6
hits = []
for d in range(1, 7):
    for xp in O:
        v = Fr(xp)
        for _ in range(d):
            v = phi(v)
        if v.denominator == 1 and int(v) in Oset:
            hits.append((d, xp, int(v)))
chk(hits == [(1, 0, 101), (1, 269, 119)], "F6 hits = %s" % hits)

# ---- Lemma 1.2 directly for d <= 40 (consistency)
hits2 = []
for d in range(1, 41):
    for xp in O:
        v = L + r ** d * (xp - L)
        if v.denominator == 1 and int(v) in Oset:
            hits2.append((d, xp, int(v)))
chk(hits2 == [(1, 0, 101), (1, 269, 119)], "Lemma 1.2 numerically for d<=40")

# ---- Step 5.4/5.5: table best(s,s') by brute force over all subsets, Sidon by definition
def is_sidon(S):
    seen = set()
    for a, b in combinations(S, 2):
        if a + b in seen:
            return False
        seen.add(a + b)
    for a in S:
        if 2 * a in seen:
            return False
        seen.add(2 * a)
    return True
states = [(0, 0), (1, 0), (0, 1), (1, 1)]
best = {(s, t): -1 for s in states for t in states}
nsidon = 0
for mask in range(1 << 11):
    U = [O[i] for i in range(11) if mask >> i & 1]
    if is_sidon(U):
        nsidon += 1
        Us = set(U)
        s = (int(0 in Us), int(269 in Us)); t = (int(101 in Us), int(119 in Us))
        best[(s, t)] = max(best[(s, t)], len(U))
# admissible (AP-free) == Sidon on O
adm_eq = all(is_sidon([O[i] for i in range(11) if m >> i & 1]) == all(not (e <= {O[i] for i in range(11) if m >> i & 1}) for e in E_claimed) for m in range(1 << 11))
chk(adm_eq, "5.2 admissible (E(O)-free) == Sidon for every subset of O")
chk(nsidon == 831, "831 Sidon subsets of O (incl. empty): %d" % nsidon)
B = [[best[(s, t)] for t in states] for s in states]
print("best =", B)
chk(B == [[5, 6, 6, 6], [5, 6, 6, 6], [5, 6, 6, 6], [6, 7, 7, 7]], "5.5 best table")
M = [[B[i][j] - sum(states[i]) for j in range(4)] for i in range(4)]
R0 = [max(B[i][j] for i in range(4)) for j in range(4)]
print("M =", M, "R0 =", R0)
chk(M == [[5, 6, 6, 6], [4, 5, 5, 5], [4, 5, 5, 5], [4, 5, 5, 5]], "5.5 M")
chk(R0 == [6, 7, 7, 7], "5.5 R0")
RM = [max(R0[i] + M[i][j] for i in range(4)) for j in range(4)]
chk(RM == [x + 5 for x in R0], "5.5 R0 (x) M = R0 + 5: %s" % RM)
# iterate to K = 200 (consistency): R_K = R0 + 5K
R = R0[:]
ok = True
for k in range(1, 201):
    R = [max(R[i] + M[i][j] for i in range(4)) for j in range(4)]
    ok &= (R == [x + 5 * k for x in R0])
chk(ok, "R_K = R0 + 5K for K <= 200 (max R_K = 7+5K)")

# ---- Step 5.6 hand bounds: minimum hitting set of the edges inside W
def tau(W):
    Wl = sorted(W)
    edges = [e for e in E_claimed if e <= set(W)]
    for k in range(0, len(Wl) + 1):
        for X in combinations(Wl, k):
            Xs = set(X)
            if all(e & Xs for e in edges):
                return k, edges
    return None
cases = {"(a) W=O": (set(O), 4), "(b) W=O\\{101,119}": (set(O) - {101, 119}, 3), "(c) W=O\\{0}": (set(O) - {0}, 4),
         "(c') W=O\\{269}": (set(O) - {269}, 4), "(d) W=O\\{0,101,119}": (set(O) - {0, 101, 119}, 3),
         "(d') W=O\\{101,119,269}": (set(O) - {101, 119, 269}, 3)}
for name, (W, claimed) in cases.items():
    t, edges = tau(W)
    chk(t == claimed, "5.6 %s: tau_W = %d (claimed >= %d), edges inside W = %d, so |U| <= %d" % (name, t, claimed, len(edges), len(W) - t))
# the edge lists quoted in 5.6
names = {e: "e%d" % (i + 1) for i, e in enumerate(E_claimed)}
quoted = {"(b) W=O\\{101,119}": "e1 e3 e4 e5 e6 e8", "(c) W=O\\{0}": "e2 e3 e4 e5 e6 e7 e8 e9", "(c') W=O\\{269}": "e1 e2 e3 e5 e6 e7 e8 e9",
          "(d) W=O\\{0,101,119}": "e3 e4 e5 e6 e8", "(d') W=O\\{101,119,269}": "e1 e3 e5 e6 e8"}
for name, q in quoted.items():
    W = cases[name][0]
    inside = " ".join(sorted((names[e] for e in E_claimed if e <= W), key=lambda s: int(s[1:])))
    chk(inside == q, "5.6 %s edge list %s" % (name, inside))
# the max |U| over admissible U under each hypothesis (direct, from best table semantics)
def maxU(pred):
    return max(len([O[i] for i in range(11) if m >> i & 1]) for m in range(1 << 11)
               if is_sidon([O[i] for i in range(11) if m >> i & 1]) and pred({O[i] for i in range(11) if m >> i & 1}))
chk(maxU(lambda U: True) == 7, "(a) max admissible |U| = 7")
chk(maxU(lambda U: 101 not in U and 119 not in U) == 6, "(b) max |U| with 101,119 not in U = 6")
chk(maxU(lambda U: 0 not in U) == 6, "(c) max |U| with 0 not in U = 6")
chk(maxU(lambda U: 269 not in U) == 6, "(c') max |U| with 269 not in U = 6")
chk(maxU(lambda U: 0 not in U and 101 not in U and 119 not in U) == 5, "(d) = 5")
chk(maxU(lambda U: 269 not in U and 101 not in U and 119 not in U) == 5, "(d') = 5")
# finiteness remark in 5.4: every subset of {0,101,119,269} admissible
chk(all(is_sidon(list(S)) for k in range(5) for S in combinations([0, 101, 119, 269], k)), "5.4 all subsets of {0,101,119,269} admissible")
chk([e for e in E_claimed if len(e & {0, 101, 119, 269}) >= 2] == [frozenset((83, 101, 119))], "5.4 only e7 meets {0,101,119,269} twice")

# ---- Step 6: U*
Ustar = {0, 98, 101, 117, 119, 159, 269}
chk(is_sidon(sorted(Ustar)) and all(not (e <= Ustar) for e in E_claimed), "6.1 U* admissible / Sidon")
chk(len(Ustar) == 7 and {0, 269} <= Ustar and {101, 119} <= Ustar, "6.1 |U*|=7, a=b=(1,1)")
miss = {names[e]: sorted(e - Ustar) for e in E_claimed}
print("6.1 points of each edge missing from U*:", miss)

print()
print("ALL FACTS OK" if not fails else "FAILURES: %d\n%s" % (len(fails), "\n".join(fails)))
sys.exit(1 if fails else 0)
