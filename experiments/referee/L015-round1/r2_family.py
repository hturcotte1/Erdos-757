#!/usr/bin/env python3
"""Referee L015 round 1, script r2: the family S_K built from scratch with exact Fractions.
 (1) points: |S_K| = 11+9K, copy intersections (Theorem 1(a)) for K <= KPTS;
 (2) integer form I_K = 269^K S_K (denominators checked), and the recursion of Step 1.6;
 (3) relation census for K <= KCEN by grouping pair SUMS and, separately, pair DIFFERENCES;
     every relation must be a 3-AP relation and the AP set must equal {phi^J(e)};
 (4) literal (4,5)-test (>= 5 distinct distances in every 4-subset) for K <= K45;
 (5) T_K = U_j phi^j(U*) for K <= KT: subset of S_K, size 7+5K, Sidon by definition;
 (6) the set of results/claims/C003-reader-5-9-K6.json equals I_6.
Imports nothing from the repository (reads the C003 JSON as data).  Run: python3 -I r2_family.py
"""
import json
import sys
import time
from fractions import Fraction as F
from itertools import combinations

KPTS, KCEN, K45, KT = 40, 20, 8, 30
if len(sys.argv) > 1:
    K45 = int(sys.argv[1])

FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
OI = [x for x in O if x not in (0, 269)]
E = [(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121),
     (75, 117, 159), (83, 101, 119), (83, 121, 159), (117, 119, 121)]
Ustar = [0, 98, 101, 117, 119, 159, 269]
r = F(18, 269)


def phi(x):
    return 101 + r * x


def phij(x, j):
    v = F(x)
    for _ in range(j):
        v = phi(v)
    return v


KMAX = max(KPTS, KCEN, K45, KT)
P = [[phij(x, j) for x in O] for j in range(KMAX + 1)]   # P[j][i] = phi^j(O[i])


def copies(K):
    return [set(P[j]) for j in range(K + 1)]


def S(K):
    s = set()
    for j in range(K + 1):
        s |= set(P[j])
    return s


def to_int(K, X):
    out = []
    sc = 269 ** K
    for v in X:
        w = v * sc
        if w.denominator != 1:
            return None
        out.append(int(w))
    return sorted(out)


# ---------------- (1) points and intersections
t0 = time.time()
ok_pts = True
for K in range(KPTS + 1):
    C = copies(K)
    if len(S(K)) != 11 + 9 * K:
        ok_pts = False
        print("   |S_%d| = %d" % (K, len(S(K))))
    for j in range(K + 1):
        if len(C[j]) != 11:
            ok_pts = False
        for jj in range(j + 1, K + 1):
            inter = C[j] & C[jj]
            if jj == j + 1:
                exp = {phij(101, j), phij(119, j)}
                if inter != exp or exp != {P[j + 1][0], P[j + 1][10]}:
                    ok_pts = False
            elif inter:
                ok_pts = False
    # no point in three copies
    cnt = {}
    for j in range(K + 1):
        for v in C[j]:
            cnt[v] = cnt.get(v, 0) + 1
    if max(cnt.values()) > 2:
        ok_pts = False
check(ok_pts, "Thm 1(a): |S_K| = 11+9K, consecutive copies meet exactly in {phi^j(101),phi^j(119)} = {phi^(j+1)(0),phi^(j+1)(269)}, others disjoint, no point in 3 copies (K <= %d)" % KPTS)
check(all(min(S(K)) == 0 and max(S(K)) == 269 for K in (0, 5, KPTS)), "S_K subset [0,269] with extremes 0, 269")

# ---------------- (2) integer form and recursion 1.6
ok_int = True
for K in range(KPTS + 1):
    I = to_int(K, S(K))
    if I is None or len(I) != 11 + 9 * K:
        ok_int = False
        continue
    # recursion: N_0(x) = x, N_j(x) = 101*269^j + 18 N_{j-1}(x); I_K = {269^(K-j) N_j(x)}
    I2 = set()
    for x in O:
        N = x
        I2.add(269 ** K * N)
        for j in range(1, K + 1):
            N = 101 * 269 ** j + 18 * N
            I2.add(269 ** (K - j) * N)
    if sorted(I2) != I:
        ok_int = False
check(ok_int, "Thm 1(a)/1.6: I_K = 269^K S_K is a set of integers and equals the recursion of 1.6 (K <= %d)" % KPTS)

# ---------------- (6) C003
c003 = json.load(open("/home/user/Erdos-757/results/claims/C003-reader-5-9-K6.json"))
A = c003["set"]
check(all(isinstance(v, int) for v in A), "C003: all entries are JSON integers (no rational/float parsing issue)")
check(len(A) == len(set(A)) == 65, "C003: 65 distinct entries")
check(sorted(A) == to_int(6, S(6)), "C003: set equals I_6 = 269^6 S_6 exactly")
print("     C003 keys:", sorted(c003.keys()), " claimed_h:", c003.get("claimed_h"), " witness size:", len(c003.get("witness_sidon_subset", []) or []))
if c003.get("witness_sidon_subset"):
    W = c003["witness_sidon_subset"]
    sm = [a + b for i, a in enumerate(W) for b in W[i:]]
    check(set(W) <= set(A) and len(sm) == len(set(sm)) and len(W) == 37, "C003: stored witness is a Sidon subset of size 37 (sums x<=y distinct)")
print("     time so far %.1fs" % (time.time() - t0), flush=True)

# ---------------- (3) relation census
def predicted_aps(K):
    sc = 269 ** K
    out = set()
    for J in range(K + 1):
        for e in E:
            out.add(tuple(sorted(int(phij(x, J) * sc) for x in e)))
    return out


ok_cen = True
for K in range(KCEN + 1):
    I = to_int(K, S(K))
    n = len(I)
    bysum = {}
    for i in range(n):
        a = I[i]
        for k in range(i, n):
            bysum.setdefault(a + I[k], []).append((a, I[k]))
    nrel = 0
    aps = set()
    bad = 0
    for s, L in bysum.items():
        if len(L) < 2:
            continue
        for p, q in combinations(L, 2):
            nrel += 1
            pts = set(p) | set(q)
            dbl = [t for t in (p, q) if t[0] == t[1]]
            if len(pts) != 3 or len(dbl) != 1:
                bad += 1
                continue
            u = dbl[0][0]
            o = q if dbl[0] == p else p
            if not (o[0] < u < o[1]):
                bad += 1
            aps.add(tuple(sorted(pts)))
    # difference census
    bydiff = {}
    for i in range(n):
        for k in range(i + 1, n):
            bydiff.setdefault(I[k] - I[i], []).append((I[i], I[k]))
    ndc = 0
    bad_d = 0
    aps_d = set()
    for d, L in bydiff.items():
        if len(L) < 2:
            continue
        for p, q in combinations(L, 2):
            ndc += 1
            pts = set(p) | set(q)
            if len(pts) != 3:
                bad_d += 1
            else:
                aps_d.add(tuple(sorted(pts)))
    pred = predicted_aps(K)
    good = (nrel == 9 * (K + 1) and bad == 0 and aps == pred and ndc == 9 * (K + 1) and bad_d == 0 and aps_d == pred
            and max(len(L) for L in bysum.values()) == 2 and max(len(L) for L in bydiff.values()) == 2)
    # linearity
    lin = all(len(set(a) & set(b)) <= 1 for a, b in combinations(sorted(aps), 2))
    good = good and lin
    if not good or K % 5 == 0 or K == KCEN:
        print("   K=%2d n=%3d sum-relations=%d (non-AP %d) diff-coincidences=%d (4-point %d) APs==pred:%s linear:%s" %
              (K, n, nrel, bad, ndc, bad_d, aps == pred and aps_d == pred, lin), flush=True)
    ok_cen = ok_cen and good
check(ok_cen, "Thm 1(b),(c): for every K <= %d all relations are 3-AP relations, exactly 9(K+1), AP set = {phi^J(e)}, linear; same by differences" % KCEN)
print("     time so far %.1fs" % (time.time() - t0), flush=True)

# ---------------- (5) T_K
ok_T = True
for K in range(KT + 1):
    T = set()
    for j in range(K + 1):
        T |= {phij(x, j) for x in Ustar}
    TI = to_int(K, T)
    I = set(to_int(K, S(K)))
    sm = [a + b for i, a in enumerate(TI) for b in TI[i:]]
    ap = any((a + c) % 2 == 0 and (a + c) // 2 in set(TI) for a, c in combinations(TI, 2))
    good = (len(TI) == 7 + 5 * K and set(TI) <= I and len(sm) == len(set(sm)) and not ap)
    if not good:
        print("   T_%d bad: size %d" % (K, len(TI)))
    ok_T = ok_T and good
check(ok_T, "Thm 1(e)/Step 6: T_K subset S_K, |T_K| = 7+5K, Sidon (all sums x<=y distinct), no 3-AP, for every K <= %d" % KT)
print("     time so far %.1fs" % (time.time() - t0), flush=True)

# ---------------- (4) literal (4,5)-test
for K in range(K45 + 1):
    I = to_int(K, S(K))
    n = len(I)
    did = {}
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(i + 1, n):
            d = I[k] - I[i]
            if d not in did:
                did[d] = len(did)
            D[i][k] = D[k][i] = did[d]
    mn = 6
    cnt = 0
    hist = {}
    for i in range(n):
        Di = D[i]
        for j in range(i + 1, n):
            Dj = D[j]
            dij = Di[j]
            for k in range(j + 1, n):
                Dk = D[k]
                dik, djk = Di[k], Dj[k]
                for l in range(k + 1, n):
                    c = len({dij, dik, Di[l], djk, Dj[l], Dk[l]})
                    cnt += 1
                    hist[c] = hist.get(c, 0) + 1
                    if c < mn:
                        mn = c
    check(hist.get(5, 0) == 9 * (K + 1) * (n - 3) and set(hist) <= {5, 6},
          "Thm 1(d): K=%d: #4-subsets with exactly 5 distances = 9(K+1)(n-3) = %d (each contains exactly one AP)" % (K, 9 * (K + 1) * (n - 3)))
    check(mn >= 5 and cnt == n * (n - 1) * (n - 2) * (n - 3) // 24,
          "Thm 1(d): K=%d n=%d: all %d 4-subsets have >= 5 distinct distances (min %d; histogram %s; %.1fs)" %
          (K, n, cnt, mn, dict(sorted(hist.items())), time.time() - t0))

print("SUMMARY: %d failures" % len(FAILS))
for f in FAILS:
    print("  FAILED:", f)
