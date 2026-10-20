#!/usr/bin/env python3
"""Referee L015 round 1, script r1: independent recomputation of the finite facts F0-F6 about O
and of the 16-entry table of Step 5.5, plus the hitting-set bounds of the hand proof 5.6.
Written from scratch by the referee; imports nothing from the repository.
Exact integers / Fractions only.   Run:  python3 -I r1_facts_O.py
"""
from fractions import Fraction as F
from itertools import combinations, product

FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
OS = set(O)
OI = [x for x in O if x not in (0, 269)]          # O° (interior)
r = F(18, 269)


def phi(x):
    return 101 + r * x


# ---------------- F0
check(len(OS) == 11 and sorted(O) == O and min(O) == 0 and max(O) == 269, "F0: 11 distinct integers, min 0, max 269")
check(len(OI) == 9 and all(49 <= x <= 159 for x in OI) and min(OI) == 49 and max(OI) == 159, "F0: O° has 9 points in [49,159]")

# ---------------- F1
def is_prime(p):
    if p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True

check(is_prime(269), "F1: 269 is prime (trial division to sqrt)")
check(18 % 269 != 0 and 251 % 269 != 0 and 101 % 269 != 0 and 150 % 269 != 0, "F1: 269 does not divide 18, 251, 101, 150")
check(27169 == 101 * 269, "F1: 27169 = 101*269")
L = F(27169, 251)
check(L.denominator != 1, "F1: L = 27169/251 is not an integer (L = %s)" % L)

# ---------------- F2
check(phi(L) == L, "F2: phi(L) = L")
# phi(x) = L + r (x - L) for all x: both sides affine; compare coefficients exactly
check(r == r and 101 == L - r * L, "F2: phi(x) = L + r(x-L) identically (constant terms agree: L - rL = 101)")
check(phi(0) == 101 and phi(269) == 119, "F2: phi(0)=101, phi(269)=119")

# iterate formula phi^j(x) = L + r^j (x-L): test for many j and x
okit = True
for x in O:
    v = F(x)
    for j in range(1, 25):
        v = phi(v)
        if v != L + r ** j * (x - L):
            okit = False
check(okit, "F2/1.1: phi^j(x) = L + r^j (x - L) for x in O, j <= 24 (iteration vs closed form)")

# ---------------- F3
def y(x):
    return 251 * x - 27169

def v269(n):
    if n == 0:
        return None
    k = 0
    while n % 269 == 0:
        n //= 269
        k += 1
    return k

check(all(F(y(x)) == 251 * (x - L) for x in O), "F3: y(x) = 251 (x - L)")
check(all(y(x) != 0 for x in O), "F3: y(x) != 0 on O")
check(all((y(x) - 251 * x) % 269 == 0 for x in O), "F3: y(x) = 251 x mod 269")
vals = {x: v269(y(x)) for x in O}
print("     269-adic valuations of y(x):", vals)
check(all(vals[x] == 0 for x in OI) and vals[0] == 1 and vals[269] == 1, "F3: v_269(y(x)) = 0 on O°, = 1 at 0 and 269")
check(y(0) == -101 * 269 and y(269) == 150 * 269, "F3: y(0) = -101*269, y(269) = 150*269")

# ---------------- F4: relations in O, enumerated as ORDERED quadruples (not by grouping pair sums)
def canon(q):
    """canonical representative of a relation under the 8 symmetries
    (swap p1<->p2, swap p3<->p4, swap sides)"""
    p1, p2, p3, p4 = q
    a = tuple(sorted((p1, p2)))
    b = tuple(sorted((p3, p4)))
    return tuple(sorted((a, b)))

rels = set()
nord = 0
for q in product(O, repeat=4):
    p1, p2, p3, p4 = q
    if p1 + p2 == p3 + p4 and sorted((p1, p2)) != sorted((p3, p4)):
        nord += 1
        rels.add(canon(q))
print("     ordered relation quadruples in O:", nord, " classes:", len(rels))
check(len(rels) == 9, "F4: exactly 9 relation classes in O")
E_cert = [(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121),
          (75, 117, 159), (83, 101, 119), (83, 121, 159), (117, 119, 121)]
pts = []
allap = True
for (a, b) in rels:
    S = sorted(set(a) | set(b))
    # must be (u,u) vs (v,w) with v<u<w
    if a[0] == a[1]:
        u, (v, w) = a[0], b
    elif b[0] == b[1]:
        u, (v, w) = b[0], a
    else:
        allap = False
        continue
    if not (v < u < w and v + w == 2 * u and len(S) == 3):
        allap = False
    pts.append(tuple(S))
check(allap, "F4: every relation of O is of the form (u,u,v,w) with v<u<w a 3-AP")
check(sorted(pts) == sorted(E_cert), "F4: the point sets are exactly e1..e9 of the certificate")
# each ordered-quadruple class has exactly 8 ordered representatives? (u,u,v,w): orbit size 4
check(nord == 9 * 4, "F4: 36 ordered quadruples = 9 classes x 4 (orbit of (u,u,v,w))")
mids = sorted(e[1] for e in E_cert)
check(mids == OI, "F4: middles of e1..e9 are the nine points of O°, one each")
check(all(len(set(e) & set(f)) <= 1 for e, f in combinations(E_cert, 2)), "F4: linear (two edges share <= 1 point)")
check(not any(0 in e and 269 in e for e in E_cert), "F4: no edge contains both 0 and 269")
# the certificate's list of repeated sums
sums = {}
for i, a in enumerate(O):
    for b in O[i:]:
        sums.setdefault(a + b, []).append((a, b))
rep = {s: v for s, v in sums.items() if len(v) > 1}
cert_rep = {98: [(0, 98), (49, 49)], 150: [(49, 101), (75, 75)], 166: [(49, 117), (83, 83)], 318: [(49, 269), (159, 159)],
            196: [(75, 121), (98, 98)], 234: [(75, 159), (117, 117)], 202: [(83, 119), (101, 101)], 242: [(83, 159), (121, 121)],
            238: [(117, 121), (119, 119)]}
check(len(sums) + sum(len(v) - 1 for v in sums.values()) == 66 and sum(len(v) for v in sums.values()) == 66, "F4: 66 sums x+y, x<=y")
check({s: sorted(v) for s, v in rep.items()} == {s: sorted(v) for s, v in cert_rep.items()}, "F4: repeated sums exactly as listed in 0.4, each exactly twice")
# literal (4,5) property of O
mind = min(len({abs(a - b) for a, b in combinations(B, 2)}) for B in combinations(O, 4))
check(mind >= 5, "O itself: every 4-subset has >= 5 distinct distances (min = %d)" % mind)
# degrees in O
deg = {x: sum(x in e for e in E_cert) for x in O}
print("     degrees in O:", deg)

# ---------------- F5: residues over O°, all position subsets T of {1,2,3,4} with |T| <= 3
eps = (1, 1, -1, -1)
sol = {}
for m in (1, 2, 3):
    for T in combinations(range(4), m):
        for xs in product(OI, repeat=m):
            if sum(eps[i] * x for i, x in zip(T, xs)) % 269 == 0:
                sol.setdefault((m, T), []).append(xs)
# m = 1: none
check(not any(k[0] == 1 for k in sol), "F5(i): m=1 has no solution")
# m = 2: only opposite-side equal values
ok2 = True
for (m, T), L2 in sol.items():
    if m != 2:
        continue
    same_side = (eps[T[0]] == eps[T[1]])
    for xs in L2:
        if same_side or xs[0] != xs[1]:
            ok2 = False
check(ok2, "F5(ii),(iii): m=2 solutions only on opposite sides with equal x (=> same point on both sides, excluded by 0.2)")
# m = 3
ok3 = True
for T in combinations(range(4), 3):
    L3 = sol.get((3, T), [])
    q = [i for i in range(4) if i not in T][0]
    # the two positions of T with the same sign, and the odd one
    sg = [eps[i] for i in T]
    odd = [i for i in T if sg.count(eps[i]) == 1][0]
    pair = [i for i in T if i != odd]
    got = sorted((dict(zip(T, xs))[pair[0]], dict(zip(T, xs))[pair[1]], dict(zip(T, xs))[odd]) for xs in L3)
    if got != [(49, 49, 98), (159, 159, 49)]:
        ok3 = False
        print("     m=3 T=%s solutions %s" % (T, got))
    # the fourth point: p_q = combination of the others; must be phi^J(2u - v) with 2u - v in {0, 269}
    for (u1, u2, v) in got:
        d = 2 * u1 - v
        if not (u1 == u2 and d in (0, 269) and tuple(sorted((d, u1, v))) in E_cert):
            ok3 = False
check(ok3, "F5(iv): m=3, every T: only (u,u,v) = (49,49,98) or (159,159,49); 4th point 0 resp. 269; point set e1 resp. e4")

# ---------------- F6 / Lemma 1.2 (direct, d <= 30)
hits = []
for xp in O:
    v = F(xp)
    for d in range(1, 31):
        v = phi(v)
        if v in OS:
            hits.append((xp, d, int(v)))
check(hits == [(0, 1, 101), (269, 1, 119)], "F6: phi^d(x') in O (x' in O, 1<=d<=30) only phi(0)=101, phi(269)=119; got %s" % hits)

# ---------------- Table of Step 5.5, computed by Sidon-by-DIFFERENCES (no AP list, no sums)
def sidon_diff(U):
    ds = [b - a for a, b in combinations(sorted(U), 2)]
    return len(ds) == len(set(ds))

E_mask = []
idx = {x: i for i, x in enumerate(O)}
for e in E_cert:
    E_mask.append(sum(1 << idx[x] for x in e))

ST = [(0, 0), (1, 0), (0, 1), (1, 1)]
best = {}
best_ap = {}
nsid = 0
agree = True
for mask in range(1 << 11):
    U = [O[i] for i in range(11) if mask >> i & 1]
    s1 = sidon_diff(U)
    s2 = not any(mask & em == em for em in E_mask)
    if s1 != s2:
        agree = False
    if s1:
        nsid += 1
        a = (int(0 in U), int(269 in U))
        b = (int(101 in U), int(119 in U))
        best[(a, b)] = max(best.get((a, b), -1), len(U))
check(agree, "Table: Sidon-by-differences == E(O)-free for all 2048 subsets of O")
check(len(best) == 16, "Table: all 16 state pairs realised")
print("     Sidon subsets of O incl. empty set:", nsid)
B = [[best[(s, t)] for t in ST] for s in ST]
print("     best =", B)
M = [[B[i][k] - sum(ST[i]) for k in range(4)] for i in range(4)]
R0 = [max(B[i][k] for i in range(4)) for k in range(4)]
print("     M =", M, " R0 =", R0)
check(B == [[5, 6, 6, 6], [5, 6, 6, 6], [5, 6, 6, 6], [6, 7, 7, 7]], "Table: best as in Step 5.5")
check(M == [[5, 6, 6, 6], [4, 5, 5, 5], [4, 5, 5, 5], [4, 5, 5, 5]], "Table: M as in Step 5.5")
check(R0 == [6, 7, 7, 7], "Table: R0 = (6,7,7,7)")


def mp(R, M):
    return [max(R[i] + M[i][k] for i in range(4)) for k in range(4)]

check(mp(R0, M) == [x + 5 for x in R0], "Table: R0 (x) M = R0 + 5 = %s" % mp(R0, M))
check(all(sidon_diff(sorted(set(S))) for S in [[0, 101, 119, 269]]) and all(
    not any(set(e) <= set(S) for e in E_cert) for k in range(5) for S in combinations([0, 101, 119, 269], k)),
    "5.4: every subset of {0,101,119,269} is admissible")

# brute-force h(S_K) via chaining per-copy choices is NOT done here (that is the proof's method); see r3.

# ---------------- hitting-set bounds of 5.6
def tau(W):
    Es = [e for e in E_cert if set(e) <= set(W)]
    for k in range(len(W) + 1):
        for X in combinations(W, k):
            Xs = set(X)
            if all(Xs & set(e) for e in Es):
                return k, Es
    return None, Es

cases = {
    "(a) W=O": (O, 4, None),
    "(b) W=O-{101,119}": ([x for x in O if x not in (101, 119)], 3, [1, 3, 4, 5, 6, 8]),
    "(c) W=O-{0}": ([x for x in O if x != 0], 4, [2, 3, 4, 5, 6, 7, 8, 9]),
    "(c') W=O-{269}": ([x for x in O if x != 269], 4, [1, 2, 3, 5, 6, 7, 8, 9]),
    "(d) W=O-{0,101,119}": ([x for x in O if x not in (0, 101, 119)], 3, [3, 4, 5, 6, 8]),
    "(d') W=O-{101,119,269}": ([x for x in O if x not in (101, 119, 269)], 3, [1, 3, 5, 6, 8]),
}
for name, (W, tclaim, elist) in cases.items():
    t, Es = tau(W)
    lab = sorted(E_cert.index(e) + 1 for e in Es)
    alpha = max(len(U) for k in range(len(W) + 1) for U in combinations(W, k) if not any(set(e) <= set(U) for e in Es)) if len(W) <= 11 else None
    okc = (t == tclaim) and (elist is None or lab == elist) and alpha == len(W) - t
    check(okc, "5.6 %s: edges %s, tau_W = %s (claimed >= %d), max admissible = %s = |W| - tau_W" % (name, lab, t, tclaim, alpha))
# the degrees claimed in (b), (d), (d')
def degs(W):
    Es = [e for e in E_cert if set(e) <= set(W)]
    return {x: sum(x in e for e in Es) for x in W}
check(degs(cases["(b) W=O-{101,119}"][0]) == {0: 1, 49: 3, 75: 2, 83: 2, 98: 2, 117: 2, 121: 2, 159: 3, 269: 1}, "5.6(b) degrees as stated")
check(degs(cases["(d) W=O-{0,101,119}"][0]) == {49: 2, 75: 2, 83: 2, 98: 1, 117: 2, 121: 2, 159: 3, 269: 1}, "5.6(d) degrees as stated")
check(max(degs(cases["(d') W=O-{101,119,269}"][0]).values()) <= 2, "5.6(d') all degrees <= 2")
# pairwise-disjoint triples used in (a), (c), (c')
check(not (set(E_cert[0]) & set(E_cert[5])) and not (set(E_cert[0]) & set(E_cert[6])) and not (set(E_cert[5]) & set(E_cert[6])), "5.6(a)/(c'): e1, e6, e7 pairwise disjoint")
check(not (set(E_cert[3]) & set(E_cert[4])) and not (set(E_cert[3]) & set(E_cert[6])) and not (set(E_cert[4]) & set(E_cert[6])), "5.6(c): e4, e5, e7 pairwise disjoint")

# ---------------- U*
Us = [0, 98, 101, 117, 119, 159, 269]
check(sidon_diff(Us) and not any(set(e) <= set(Us) for e in E_cert) and len(Us) == 7, "6.1: U* Sidon (differences), E(O)-free, |U*| = 7")
check((int(0 in Us), int(269 in Us)) == (1, 1) and (int(101 in Us), int(119 in Us)) == (1, 1), "6.1: a(U*) = b(U*) = (1,1)")

print("SUMMARY: %d failures" % len(FAILS))
for f in FAILS:
    print("  FAILED:", f)
