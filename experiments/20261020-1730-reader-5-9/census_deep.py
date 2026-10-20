#!/usr/bin/env python3
"""Exact relation census of S_K for larger K (pure Python ints, scale 269^K).

Integer recursion: A_K = 269^K * O  u  { 101*269^K + 18*a : a in A_{K-1} }  (a already scaled by 269^(K-1)),
which is phi applied to A_{K-1} followed by scaling by 269.  Checked equal to data/reader_5_9_family.json for K <= 8.
For each K in the list we enumerate ALL pair sums a+b (a<=b), group equal sums, and verify:
  * |S_K| = 11 + 9K;
  * every coincidence of two different pairs is a 3-term AP (no parallelogram a+b=c+d on 4 distinct points);
  * #APs = 9(K+1) and each AP lies inside a single copy phi^j(O);
  * no two APs share two points.
From these: S_K is a (4,5)-set (no parallelogram + linear AP hypergraph; see README for the 3-line reduction).
Usage: python3 census_deep.py 9 10 11 12 15 20 30 40 60 80 100
"""
import itertools
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]


def build(K):
    A = list(O)
    for k in range(1, K + 1):
        A = sorted(set(269 ** k * o for o in O) | {101 * 269 ** k + 18 * a for a in A})
    return A


def copy_sets(K):
    """phi^j(O) scaled by 269^K, as integer sets, j = 0..K:  269^(K-j) * (copy j at its own scale) ."""
    # direct: phi^j(x) = L + r^j (x-L); at scale 269^K * 251 : 
    from fractions import Fraction as F
    L = F(27169, 251)
    res = []
    for j in range(K + 1):
        s = set()
        for x in O:
            v = (L + F(18, 269) ** j * (F(x) - L)) * 269 ** K
            assert v.denominator == 1
            s.add(int(v))
        res.append(s)
    return res


def census(K):
    t0 = time.time()
    A = build(K)
    n = len(A)
    by_sum = defaultdict(list)
    for i, a in enumerate(A):
        for b in A[i:]:
            by_sum[a + b].append((a, b))
    aps, bad = set(), 0
    for prs in by_sum.values():
        if len(prs) < 2:
            continue
        for p, q in itertools.combinations(prs, 2):
            pts = set(p) | set(q)
            if len(pts) == 3:
                aps.add(tuple(sorted(pts)))
            else:
                bad += 1
    copies = copy_sets(K)
    inside = sum(1 for e in aps if any(set(e) <= c for c in copies))
    # minimal level of each point = smallest j with the point in copy j
    minlev = {}
    for j, c in enumerate(copies):
        for v in c:
            minlev.setdefault(v, j)
    spans = [max(minlev[v] for v in e) - min(minlev[v] for v in e) for e in aps]
    # copies: consecutive intersections of size 2, others empty
    cons = [len(copies[j] & copies[j + 1]) for j in range(K)]
    noncons = max([len(copies[i] & copies[j]) for i in range(K + 1) for j in range(i + 2, K + 1)] or [0])
    share2 = 0
    # APs sharing two points: index by pairs
    pair_cnt = defaultdict(int)
    for e in aps:
        for pr in itertools.combinations(e, 2):
            pair_cnt[pr] += 1
    share2 = sum(1 for v in pair_cnt.values() if v > 1)
    return {"K": K, "n": n, "n_ok": n == 11 + 9 * K, "n_aps": len(aps), "n_aps_expected": 9 * (K + 1),
            "non_AP_coincidences_(parallelograms/other)": bad, "aps_inside_one_copy": inside,
            "point_pairs_in_two_APs": share2, "max_span_of_APs_in_minimal_levels": max(spans) if spans else 0,
            "consecutive_copies_intersections": sorted(set(cons)), "max_nonconsecutive_intersection": noncons, "copies_union_equals_set": set().union(*copies) == set(A),
            "sec": round(time.time() - t0, 1)}


if __name__ == "__main__":
    fam = {m["K"]: m["set"] for m in json.loads((REPO / "data" / "reader_5_9_family.json").read_text())["family"]}
    for K in fam:
        assert build(K) == sorted(fam[K]), f"integer recursion != json at K={K}"
    print("integer recursion matches data/reader_5_9_family.json for K<=8", flush=True)
    out = []
    for K in [int(x) for x in sys.argv[1:]]:
        r = census(K)
        out.append(r)
        print(r, flush=True)
        (Path(__file__).resolve().parent / "census_deep_results.json").write_text(json.dumps(out, indent=1))
