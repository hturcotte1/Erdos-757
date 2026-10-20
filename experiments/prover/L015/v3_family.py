#!/usr/bin/env python3
"""L015 / C3: S_K in exact integers, compared with the agent's data and with C003; point count, copy
intersections and levels (Step 1); the complete relation census a+b=c+d of S_K for a list of K (a consistency
check of Step 2, not part of the proof); the AP hypergraph, its linearity, and the literal 4-subset test
|B-B| >= 11 (Step 3) for K <= KLIT.
Integers: N_j(x) := 269^j * phi^j(x) satisfies N_0(x) = x, N_j(x) = 101*269^j + 18*N_{j-1}(x); the integer form of S_K is
I_K = { 269^(K-j) N_j(x) : 0 <= j <= K, x in O } = 269^K * S_K.   (Own code; no file of the agent's is imported.)
Run:  python3 -I v3_family.py KLIT K1 K2 ...      (census for K1, K2, ...; 4-subset test for K <= KLIT)
"""
import json
import sys
import time
from fractions import Fraction as Fr
from itertools import combinations

REPO = "/home/user/Erdos-757"
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
OI = [x for x in O if x not in (0, 269)]
E_O = sorted((a, u, c) for a in O for u in O for c in O if a < u < c and a + c == 2 * u)
assert len(E_O) == 9


def ok(cond, label):
    if not cond:
        raise SystemExit("FAILED: " + label)
    print("OK  ", label, flush=True)


def N(j, x):
    v = x
    for i in range(1, j + 1):
        v = 101 * 269 ** i + 18 * v
    return v


def copies(K):
    """copy j of S_K in integer form: dict x -> 269^(K-j) N_j(x)."""
    return [{x: 269 ** (K - j) * N(j, x) for x in O} for j in range(K + 1)]


def phi(x):
    return Fr(101) + Fr(18) * Fr(x) / 269


def S_frac(K):
    s = set()
    cur = [Fr(x) for x in O]
    for j in range(K + 1):
        s |= set(cur)
        cur = [phi(v) for v in cur]
    return s


def main():
    KLIT = int(sys.argv[1])
    KS = [int(a) for a in sys.argv[2:]]
    fam = {m["K"]: m["set"] for m in json.load(open(REPO + "/data/reader_5_9_family.json"))["family"]}
    c003 = json.load(open(REPO + "/results/claims/C003-reader-5-9-K6.json"))
    for K in range(9):
        cps = copies(K)
        IK = sorted(set().union(*[set(c.values()) for c in cps]))
        ok(set(IK) == {v * 269 ** K for v in S_frac(K)}, f"K={K}: integer form = 269^K * S_K (Fractions, phi iterated)")
        ok(IK == sorted(fam[K]), f"K={K}: equals data/reader_5_9_family.json (n={len(IK)})")
    I6 = sorted(set().union(*[set(c.values()) for c in copies(6)]))
    ok(sorted(c003["set"]) == I6, "C003 set = 269^6 * S_6 exactly (65 points)")
    W = sorted(c003["witness_sidon_subset"])
    sw = [a + b for i, a in enumerate(W) for b in W[i:]]
    ok(len(W) == 37 and set(W) <= set(I6) and len(sw) == len(set(sw)), "C003 witness: 37 points of S_6, Sidon by definition (703 distinct sums)")
    out = []
    for K in KS:
        t0 = time.time()
        cps = copies(K)
        pts = sorted(set().union(*[set(c.values()) for c in cps]))
        n = len(pts)
        # levels: minimal j with p in copy j
        lev = {}
        for j, c in enumerate(cps):
            for v in c.values():
                lev.setdefault(v, j)
        cons = [set(cps[j].values()) & set(cps[j + 1].values()) for j in range(K)]
        cons_ok = all(cons[j] == {cps[j][101], cps[j][119]} == {cps[j + 1][0], cps[j + 1][269]} for j in range(K))
        far_ok = all(not (set(cps[i].values()) & set(cps[j].values())) for i in range(K + 1) for j in range(i + 2, K + 1))
        lev_ok = all(lev[cps[j][x]] == j for j in range(K + 1) for x in (O if j == 0 else OI)) and \
            all(lev[cps[j][x]] == j - 1 for j in range(1, K + 1) for x in (0, 269))
        # relation census: all pairs a<=b grouped by sum
        bys = {}
        for i, a in enumerate(pts):
            for b in pts[i:]:
                bys.setdefault(a + b, []).append((a, b))
        rels = [(p, q) for v in bys.values() if len(v) > 1 for i, p in enumerate(v) for q in v[i + 1:]]
        aps = set()
        bad = 0
        for p, q in rels:
            s = set(p) | set(q)
            if len(s) == 3 and (p[0] == p[1] or q[0] == q[1]):
                aps.add(tuple(sorted(s)))
            else:
                bad += 1
        predicted = {tuple(sorted(cps[j][v] for v in e)) for j in range(K + 1) for e in E_O}
        pc = {}
        for e in aps:
            for pr in combinations(e, 2):
                pc[pr] = pc.get(pr, 0) + 1
        r = {"K": K, "n": n, "n_expected": 11 + 9 * K, "relations": len(rels), "non_AP_relations": bad,
             "APs": len(aps), "APs_expected": 9 * (K + 1), "APs_equal_predicted_phi^J(e)": aps == predicted,
             "pairs_in_two_APs": sum(1 for v in pc.values() if v > 1), "consecutive_copies_share_exactly_anchors": cons_ok,
             "nonconsecutive_copies_disjoint": far_ok, "levels_as_in_Step1": lev_ok,
             "max_level_span_of_an_AP": max(max(lev[v] for v in e) - min(lev[v] for v in e) for e in aps)}
        if K <= KLIT:
            mind = 99
            for B in combinations(pts, 4):
                dd = len({u - v for u in B for v in B})          # literal |B - B|
                if dd < mind:
                    mind = dd
            r["min_|B-B|_over_4-subsets"] = mind
            r["number_of_4-subsets"] = n * (n - 1) * (n - 2) * (n - 3) // 24
        r["sec"] = round(time.time() - t0, 1)
        good = (n == 11 + 9 * K and bad == 0 and len(aps) == 9 * (K + 1) and aps == predicted and r["pairs_in_two_APs"] == 0
                and cons_ok and far_ok and lev_ok and r["max_level_span_of_an_AP"] <= 1 and len(rels) == 9 * (K + 1)
                and (K > KLIT or r["min_|B-B|_over_4-subsets"] >= 11))
        r["all_ok"] = good
        print(r, flush=True)
        ok(good, f"K={K}: census as predicted by Steps 1-3")
        out.append(r)
    json.dump(out, open("v3_family_results.json", "w"), indent=1)
    print("ALL FAMILY CHECKS OK")


if __name__ == "__main__":
    main()
