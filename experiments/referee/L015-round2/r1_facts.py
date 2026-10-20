#!/usr/bin/env python3
"""Referee round 2 for L015: independent check of the finite facts F0-F6 about O, the 16-entry
table best(s,s'), M, R_0, R_0 (x) M, and the hand transversal bounds of Step 5.6 (a)-(d').
Own code; exact integers and Fractions; standard library only.
"""
from fractions import Fraction as Fr
from itertools import combinations, product

FAIL = []
def check(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond:
        FAIL.append(msg)

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
OI = [x for x in O if x not in (0, 269)]
r = Fr(18, 269)
L = Fr(27169, 251)
def phi(x):
    return 101 + r * x
def y(x):
    return 251 * x - 27169

# ---------- F0
check(len(set(O)) == 11 and all(isinstance(x, int) for x in O), "F0: 11 distinct integers")
check(min(O) == 0 and max(O) == 269 and all(0 <= x <= 269 for x in O), "F0: min 0, max 269")
check(len(OI) == 9 and min(OI) == 49 and max(OI) == 159, "F0: interior has 9 points in [49,159]")

# ---------- F1
def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True
check(is_prime(269), "F1: 269 prime")
check(18 % 269 != 0 and 251 % 269 != 0, "F1: 269 does not divide 18 or 251")
check(27169 == 101 * 269, "F1: 27169 = 101*269")
check(L.denominator != 1, "F1: L not an integer (L = %s)" % L)

# ---------- F2 (phi is affine: compare at two points suffices; also check at all of O and L)
check(phi(L) == L, "F2: phi(L) = L")
check(all(phi(x) == L + r * (x - L) for x in O + [Fr(1, 3), Fr(-7, 2), L]), "F2: phi(x) = L + r(x-L) at test points (affine, so identity)")
# identity of affine maps: same value at 0 and at 1
check(phi(0) == L + r * (0 - L) and phi(1) == L + r * (1 - L), "F2: affine identity (two points)")
check(phi(0) == 101 and phi(269) == 119, "F2: phi(0)=101, phi(269)=119")

# ---------- F3
check(all(y(x) == 251 * (x - L) for x in O), "F3: y(x) = 251(x-L) on O")
check(all(y(x) != 0 for x in O), "F3: y(x) != 0 on O")
check(all((y(x) - 251 * x) % 269 == 0 for x in O), "F3: y(x) = 251x mod 269 on O")
check([x for x in O if y(x) % 269 == 0] == [0, 269], "F3: 269 | y(x) iff x in {0,269}")
check(y(0) == -101 * 269 and y(269) == 150 * 269, "F3: y(0) = -101*269, y(269) = 150*269")
check(y(0) % (269 * 269) != 0 and y(269) % (269 * 269) != 0, "F3: 269^2 divides neither")

# ---------- F4: relations in O by brute force over ordered quadruples
Oset = set(O)
quads = []
for p1, p2, p3 in product(O, repeat=3):
    p4 = p1 + p2 - p3
    if p4 in Oset and sorted((p1, p2)) != sorted((p3, p4)):
        quads.append((p1, p2, p3, p4))
classes = set()
for q in quads:
    a = tuple(sorted(q[:2])); b = tuple(sorted(q[2:]))
    classes.add(tuple(sorted((a, b))))
check(len(quads) == 36, "F4: 36 ordered relation quadruples in O (= 4 per AP relation), got %d" % len(quads))
check(len(classes) == 9, "F4: 9 relation classes, got %d" % len(classes))
E = []
for (a, b) in classes:
    pts = set(a) | set(b)
    # exactly one side doubled
    dbl = [s for s in (a, b) if s[0] == s[1]]
    check(len(pts) == 3 and len(dbl) == 1, "F4: class %s has 3 points with a doubled middle" % ((a, b),))
    E.append(tuple(sorted(pts)))
E = sorted(E)
E_claim = sorted([(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121), (75, 117, 159),
                  (83, 101, 119), (83, 121, 159), (117, 119, 121)])
check(E == E_claim, "F4: the 9 point sets are exactly e1..e9")
# APs by the triple definition
aps = sorted(t for t in combinations(sorted(O), 3) if t[0] + t[2] == 2 * t[1])
check(aps == E_claim, "F4: all 3-APs of O (triples a<u<c, a+c=2u) are exactly e1..e9")
# repeated sums
from collections import Counter
sums = Counter(x + z for x, z in combinations(sorted(O), 2))
for x in O:
    sums[2 * x] += 1
check(sum(sums.values()) == 66, "F4: 66 sums x+y with x<=y")
rep = sorted((s, c) for s, c in sums.items() if c > 1)
check(rep == sorted([(98, 2), (150, 2), (166, 2), (318, 2), (196, 2), (234, 2), (202, 2), (242, 2), (238, 2)]),
      "F4: repeated sums are exactly 98,150,166,318,196,234,202,242,238, each twice: %s" % rep)
mids = sorted(e[1] for e in E)
check(mids == sorted(OI), "F4: middles are the 9 interior points, one each")
check(all(len(set(e) & set(f)) <= 1 for e, f in combinations(E, 2)), "F4: pairwise intersections <= 1")
check(not any(0 in e and 269 in e for e in E), "F4: no AP contains both 0 and 269")

# ---------- F5 (mod 269 over O°, tuples not necessarily distinct)
check(all(x % 269 != 0 for x in OI), "F5(i)")
check(all((a + b) % 269 != 0 for a, b in product(OI, repeat=2)), "F5(ii)")
check(all(a == b for a, b in product(OI, repeat=2) if (a - b) % 269 == 0), "F5(iii)")
sol = sorted(t for t in product(OI, repeat=3) if (t[0] + t[1] - t[2]) % 269 == 0)
check(sol == [(49, 49, 98), (159, 159, 49)], "F5(iv): solutions %s" % sol)
# also check the hand range claims
check(min(a + b - c for a, b, c in product(OI, repeat=3)) == -61 and max(a + b - c for a, b, c in product(OI, repeat=3)) == 269,
      "F5(iv) hand range [-61,269]")
check(sorted(269 - x for x in OI) == sorted([220, 194, 186, 171, 168, 152, 150, 148, 110]), "F5(ii) hand list 269-x")
small = sorted(a + b for a, b in combinations(OI + [], 2) if a + b <= 159) + sorted(2 * a for a in OI if 2 * a <= 159)
check(sorted(small) == sorted([98, 124, 132, 147, 150, 150, 158]), "F5(iv) hand list of sums <= 159: %s" % sorted(small))
# also: all sign patterns for m=3 (two same side, one opposite): +,+,- and -,-,+ equivalent
sol2 = sorted(t for t in product(OI, repeat=3) if (-t[0] - t[1] + t[2]) % 269 == 0)
check(sol2 == sol, "F5(iv) negated pattern same solutions")
# fourth point
check(all(2 * a - c in (0, 269) for a, b, c in sol), "F5: 2x1-x3 in {0,269} for the solutions")

# ---------- F6 / Lemma 1.2 for d <= 40 (exact Fractions)
hits = []
for x0 in O:
    v = Fr(x0)
    for d in range(1, 41):
        v = phi(v)
        if v.denominator == 1 and int(v) in Oset:
            hits.append((x0, d, int(v)))
check(sorted(hits) == [(0, 1, 101), (269, 1, 119)], "F6/Lemma 1.2 (d<=40): hits %s" % hits)

# ---------- Table best(s,s'), by the Sidon definition (no AP list used)
def is_sidon(U):
    U = sorted(U)
    seen = set()
    for i in range(len(U)):
        for j in range(i, len(U)):
            s = U[i] + U[j]
            if s in seen:
                return False
            seen.add(s)
    return True
states = [(0, 0), (1, 0), (0, 1), (1, 1)]
best = {(s, t): None for s in states for t in states}
nsidon = 0
adm = []
for mask in range(1 << 11):
    U = [O[i] for i in range(11) if mask >> i & 1]
    if not is_sidon(U):
        continue
    nsidon += 1
    adm.append(frozenset(U))
    s = (int(0 in U), int(269 in U)); t = (int(101 in U), int(119 in U))
    if best[(s, t)] is None or len(U) > best[(s, t)]:
        best[(s, t)] = len(U)
# cross-check: Sidon <=> contains no e in E (F4 consequence)
adm2 = set()
for mask in range(1 << 11):
    U = frozenset(O[i] for i in range(11) if mask >> i & 1)
    if not any(set(e) <= U for e in E):
        adm2.add(U)
check(set(adm) == adm2, "table: Sidon subsets of O = E(O)-free subsets (%d)" % nsidon)
B = [[best[(s, t)] for t in states] for s in states]
print("best =", B)
check(B == [[5, 6, 6, 6], [5, 6, 6, 6], [5, 6, 6, 6], [6, 7, 7, 7]], "table best matches certificate")
M = [[B[i][j] - sum(states[i]) for j in range(4)] for i in range(4)]
R0 = [max(B[i][j] for i in range(4)) for j in range(4)]
print("M =", M, " R0 =", R0)
check(M == [[5, 6, 6, 6], [4, 5, 5, 5], [4, 5, 5, 5], [4, 5, 5, 5]], "M matches")
check(R0 == [6, 7, 7, 7], "R0 matches")
def mp(R, M):
    return [max(R[i] + M[i][j] for i in range(4)) for j in range(4)]
R1 = mp(R0, M)
check(R1 == [x + 5 for x in R0], "R0 (x) M = R0 + 5: %s" % R1)

# ---------- Hand transversal bounds of Step 5.6: max admissible |U| inside W, and tau_W
def tau(W):
    edges = [e for e in E if set(e) <= set(W)]
    for k in range(0, len(W) + 1):
        for X in combinations(W, k):
            if all(set(e) & set(X) for e in edges):
                return k, edges
cases = {
    "(a) W=O": (O, 4, 7),
    "(b) no 101,119": ([x for x in O if x not in (101, 119)], 3, 6),
    "(c) no 0": ([x for x in O if x != 0], 4, 6),
    "(c') no 269": ([x for x in O if x != 269], 4, 6),
    "(d) no 0,101,119": ([x for x in O if x not in (0, 101, 119)], 3, 5),
    "(d') no 101,119,269": ([x for x in O if x not in (101, 119, 269)], 3, 5),
}
for name, (W, tclaim, uclaim) in cases.items():
    t, edges = tau(W)
    mx = max(len(U) for U in adm if U <= set(W))
    check(t >= tclaim and mx <= uclaim and mx == len(W) - t,
          "5.6 %s: |W|=%d, edges=%d, tau_W=%d (claim >= %d), max admissible |U| in W = %d (claim <= %d)"
          % (name, len(W), len(edges), t, tclaim, mx, uclaim))
# degree claims in (b), (d), (d')
def degs(W):
    edges = [e for e in E if set(e) <= set(W)]
    return {x: sum(1 for e in edges if x in e) for x in W}
db = degs(cases["(b) no 101,119"][0])
check(db == {0: 1, 49: 3, 75: 2, 83: 2, 98: 2, 117: 2, 121: 2, 159: 3, 269: 1}, "5.6(b) degrees %s" % db)
dd = degs(cases["(d) no 0,101,119"][0])
check(dd == {49: 2, 75: 2, 83: 2, 98: 1, 117: 2, 121: 2, 159: 3, 269: 1}, "5.6(d) degrees %s" % dd)
ddp = degs(cases["(d') no 101,119,269"][0])
check(max(ddp.values()) <= 2 and len([e for e in E if set(e) <= set(cases["(d') no 101,119,269"][0])]) == 5, "5.6(d') all degrees <= 2, 5 edges")
# U* admissible
Ustar = {0, 98, 101, 117, 119, 159, 269}
check(is_sidon(Ustar) and len(Ustar) == 7, "U* Sidon, size 7")
# the 16 entries are realised by subsets of {0,101,119,269}
check(all(is_sidon(U) for U in [set(c) for k in range(5) for c in combinations([0, 101, 119, 269], k)]),
      "every subset of {0,101,119,269} is Sidon (all 16 entries finite)")
# degrees in O (sanity section: max degree 4 at 49)
dO = degs(O)
check(dO[49] == 4 and max(dO.values()) == 4 and dO[101] == 2 and dO[119] == 2 and dO[0] == 1 and dO[269] == 1,
      "degrees in O: deg(49)=4 max, deg(101)=deg(119)=2, deg(0)=deg(269)=1: %s" % dO)
print("FAILURES:", len(FAIL))
print("ALL R1 FACTS OK" if not FAIL else "R1 FAILED")
