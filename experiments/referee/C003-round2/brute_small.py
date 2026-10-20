#!/usr/bin/env python3
"""Brute-force cross-checks (definition only) of my SAT and DP tools on instances with n <= 22:
S_0 (n=11), S_1 (n=20) of the family, A_base (n=14), the three 12-point record sets, and random
induced subsets of the claimed 65-point set with 16 <= n <= 22."""
import itertools
import json
import random
import sys
import time
sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/C003-round2")
from reflib import *

A65, raw = load_claim_set()
cases = []
for K in (0, 1):
    ints, levels, anc = rebuild_family(K)
    cases.append((f"S_{K} (n={len(ints)})", ints))
cases.append(("A_base (n=14, h=8 published)", [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]))
cases.append(("12-pt #3 (n=12, h=7)", [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]))
rng = random.Random(20261020)
_, lev65, anc65 = rebuild_family(6)
def copy_points(j):
    """indices of the 11 points of copy j = phi^j(O): minimal level j, plus the two anchors (level j-1)"""
    pts = set(i for i in range(65) if lev65[i] == j) | set(i for i in range(65) if lev65[i] == j-1 and anc65[i])
    return sorted(pts)
for j in range(7):
    assert len(copy_points(j)) == 11, (j, len(copy_points(j)))
# conflict-rich induced subsets: one full copy (11 points, 9 APs) plus random extra points
for n, j in ((16, 0), (18, 3), (20, 6), (21, 2), (22, 4), (22, 5), (22, 1)):
    base = copy_points(j)
    extra = rng.sample([i for i in range(65) if i not in base], n - 11)
    idx = sorted(base + extra)
    cases.append((f"copy {j} + {n-11} random points (n={n})", [A65[i] for i in idx]))
# two consecutive copies (20 points) plus 2 random extra points (n=22)
for j in (0, 2, 5):
    base = sorted(set(copy_points(j)) | set(copy_points(j+1)))
    extra = rng.sample([i for i in range(65) if i not in base], 2)
    idx = sorted(base + extra)
    cases.append((f"copies {j},{j+1} + 2 random points (n={len(idx)})", [A65[i] for i in idx]))
# unions of two consecutive copies (20 points each)
for j in range(6):
    idx = sorted(set(copy_points(j)) | set(copy_points(j+1)))
    cases.append((f"copies {j},{j+1} of C003 (n={len(idx)})", [A65[i] for i in idx]))
allok = True
out = []
for name, B in cases:
    B = sorted(B)
    n = len(B)
    conf = conflicts_from_definition(B)
    t = time.time()
    hb, Tb = brute_force_h(B)
    tb = time.time() - t
    # is this a (4,5)-set?  (induced subsets of a (4,5)-set are (4,5)-sets)
    is45 = all(len({b - a, c - a, d - a, c - b, d - b, d - c}) >= 5 for a, b, c, d in itertools.combinations(B, 4))
    best, mask, peak = frontier_dp(n, conf, list(range(n)))
    sat_h, _ = sat_atleast(n, conf, hb)
    sat_h1, _ = sat_atleast(n, conf, hb + 1)
    ok = (best == hb) and sat_h and (not sat_h1) and is_sidon(Tb)
    allok &= ok
    print(f"{name:60s} (4,5)={is45} brute h={hb} ({tb:.1f}s)  DP h={best}  SAT>={hb}:{sat_h} SAT>={hb+1}:{sat_h1}  conflicts={len(conf)} sizes={sorted(set(map(len,conf)))}  agree={ok}")
    out.append({"case": name, "n": n, "is45": is45, "brute_h": hb, "dp_h": best, "sat_ge_h": sat_h, "sat_ge_h1": sat_h1, "agree": ok})
json.dump(out, open("/home/user/Erdos-757/experiments/referee/C003-round2/brute_small.json", "w"), indent=1)
print("ALL AGREE:", allok)
