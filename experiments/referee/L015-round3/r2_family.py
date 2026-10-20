#!/usr/bin/env python3
"""Referee round 3, L015: build S_K exactly (Fractions) for K <= KMAX, and check
Theorem 1(a)-(c) by direct computation: point count, copy intersections, the full
relation census from pair sums (no AP assumption), linearity, midpoint saturation,
integer form I_K by the recursion of 1.6 vs 269^K S_K.  Usage: r2_family.py KMAX"""
from fractions import Fraction as Fr
from itertools import combinations
import sys, json

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
Oin = [x for x in O if x not in (0, 269)]
E = [frozenset(e) for e in [(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121),
                            (75, 117, 159), (83, 101, 119), (83, 121, 159), (117, 119, 121)]]
r = Fr(18, 269)
def phi_pow(x, j):
    v = Fr(x)
    for _ in range(j):
        v = 101 + r * v
    return v

fails = []
def chk(cond, msg):
    if not cond:
        fails.append(msg)
        print("FAIL " + msg)

summary = {}
for K in range(0, KMAX + 1):
    copies = [[phi_pow(x, j) for x in O] for j in range(K + 1)]
    S = set()
    for c in copies:
        S |= set(c)
    n = len(S)
    chk(n == 11 + 9 * K, "K=%d |S_K|=%d != %d" % (K, n, 11 + 9 * K))
    # copy intersections
    for j in range(K + 1):
        for jp in range(j + 1, K + 1):
            inter = set(copies[j]) & set(copies[jp])
            if jp == j + 1:
                chk(inter == {phi_pow(101, j), phi_pow(119, j)} == {phi_pow(0, jp), phi_pow(269, jp)},
                    "K=%d copies %d,%d intersection wrong" % (K, j, jp))
            else:
                chk(not inter, "K=%d copies %d,%d not disjoint" % (K, j, jp))
    # levels
    lev = {}
    for j in range(K + 1):
        for x in O:
            p = phi_pow(x, j)
            if p not in lev:
                lev[p] = (j, x)
    chk(all(lev[p][1] in Oin for p in lev if lev[p][0] >= 1), "K=%d level>=1 points have interior x" % K)
    chk(sum(1 for p in lev if lev[p][0] == 0) == 11 and all(sum(1 for p in lev if lev[p][0] == j) == 9 for j in range(1, K + 1)),
        "K=%d level counts 11, 9, 9, ..." % K)
    # full relation census from pair sums (a <= b), no AP assumption
    Sl = sorted(S)
    sums = {}
    for a, b in combinations(Sl, 2):
        sums.setdefault(a + b, []).append((a, b))
    for a in Sl:
        sums.setdefault(2 * a, []).append((a, a))
    rep = {s: v for s, v in sums.items() if len(v) >= 2}
    expected_edges = {frozenset(phi_pow(x, J) for x in e) for J in range(K + 1) for e in E}
    chk(len(expected_edges) == 9 * (K + 1), "K=%d expected edges not distinct" % K)
    found_edges = set()
    cross = 0
    for s, v in rep.items():
        if len(v) != 2:
            fails.append("K=%d sum %s repeated %d times" % (K, s, len(v))); continue
        (a, b), (c, d) = v
        pts = frozenset((a, b, c, d))
        if len(pts) == 4 or not (a == b or c == d):
            cross += 1
            fails.append("K=%d non-AP relation %s" % (K, v)); continue
        found_edges.add(pts)
    chk(len(rep) == 9 * (K + 1), "K=%d relation count %d != %d" % (K, len(rep), 9 * (K + 1)))
    chk(found_edges == expected_edges, "K=%d AP set != {phi^J(e)}" % K)
    # 3-APs directly from triples (independent of sums grouping), for K <= 8 (cost n^3/6)
    if K <= 8:
        aps = {frozenset((a, u, c)) for a, u, c in combinations(Sl, 3) if a + c == 2 * u}
        chk(aps == expected_edges, "K=%d AP triples != expected" % K)
    # linearity, middles, degrees, level span
    el = list(found_edges)
    chk(all(len(e & f) <= 1 for e, f in combinations(el, 2)), "K=%d not linear" % K)
    mids = sorted(sorted(e)[1] for e in el)
    chk(mids == sorted(p for p in Sl if p not in (min(Sl), max(Sl))), "K=%d middles != non-extreme points" % K)
    chk(min(Sl) == 0 and max(Sl) == 269, "K=%d extremes" % K)
    deg = {p: 0 for p in Sl}
    for e in el:
        for p in e:
            deg[p] += 1
    chk(max(deg.values()) == 4, "K=%d max degree %d" % (K, max(deg.values())))
    spans = {max(lev[p][0] for p in e) - min(lev[p][0] for p in e) for e in el}
    chk(spans <= {0, 1}, "K=%d level spans %s" % (K, spans))
    # integer form by recursion 1.6 and equality with 269^K S_K
    N = {x: x for x in O}
    I = set(269 ** K * N[x] for x in O)
    Nj = dict(N)
    for j in range(1, K + 1):
        Nj = {x: 101 * 269 ** j + 18 * Nj[x] for x in O}
        I |= set(269 ** (K - j) * Nj[x] for x in O)
    chk(I == set(269 ** K * p for p in S) and all(isinstance(v, int) for v in I), "K=%d integer form" % K)
    chk(all((269 ** K * p).denominator == 1 for p in S), "K=%d 269^K S_K integral" % K)
    summary[K] = dict(n=n, relations=len(rep), cross=cross, maxdeg=max(deg.values()))
    print("K=%2d n=%3d relations=%3d (9(K+1)=%3d) all AP, cross-copy=%d, linear, saturated, maxdeg=%d, integer form OK"
          % (K, n, len(rep), 9 * (K + 1), cross, max(deg.values())))
json.dump(summary, open("r2_family_results.json", "w"), indent=1)
print("ALL FAMILY CHECKS OK (K<=%d)" % KMAX if not fails else "FAILURES %d" % len(fails))
sys.exit(1 if fails else 0)
