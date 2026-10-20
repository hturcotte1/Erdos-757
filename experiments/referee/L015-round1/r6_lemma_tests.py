#!/usr/bin/env python3
"""Referee L015 round 1, script r6: numerical tests of the GENERAL lemmas the certificate uses, on the
repository data and on random / glued sets, plus the exact ratio arithmetic of Step 7.
 (L4)  Step 4: for a finite set X of reals,  X is a (4,5)-set (literal: every 4-subset has >= 5 distinct distances)
       <=>  X has no relation on 4 distinct points  AND  its 3-AP hypergraph is linear.
       (The certificate uses '<='; both directions are tested.)
 (L5)  Step 5.1: if X has no relation on 4 distinct points, then Sidon subsets = 3-AP-free subsets, so
       h(X) = alpha(AP hypergraph)  (brute force, n <= 16).
 (R7)  Step 7: exact Fractions for (7+5K)/(11+9K).
Imports nothing from the repository; reads data/ as data.  Run: python3 -I r6_lemma_tests.py
"""
import gzip
import json
import random
import time
from fractions import Fraction as F
from itertools import combinations

FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


def is45(X):
    return all(len({abs(a - b) for a, b in combinations(B, 2)}) >= 5 for B in combinations(X, 4))


def no4rel(X):
    sums = {}
    for a, b in combinations(sorted(X), 2):
        s = a + b
        if s in sums:
            return False
        sums[s] = 1
    return True


def aps_exact(X):
    S = set(X)
    out = []
    for a, c in combinations(sorted(X), 2):
        m = F(a + c, 2) if not isinstance(a, F) else (a + c) / 2
        if m in S and m != a and m != c:
            out.append((a, m, c))
    return out


def linear(E):
    return all(len(set(e) & set(f)) <= 1 for e, f in combinations(E, 2))


def h_brute(X):
    Xs = sorted(X)
    n = len(Xs)
    best = 0
    for mask in range(1 << n):
        U = [Xs[i] for i in range(n) if mask >> i & 1]
        if len(U) <= best:
            continue
        ds = [b - a for a, b in combinations(U, 2)]
        if len(ds) == len(set(ds)):
            best = len(U)
    return best


def alpha_brute(X, E):
    Xs = sorted(X)
    n = len(Xs)
    idx = {x: i for i, x in enumerate(Xs)}
    em = [sum(1 << idx[v] for v in e) for e in E]
    best = 0
    for mask in range(1 << n):
        c = bin(mask).count("1")
        if c <= best:
            continue
        if all(mask & m != m for m in em):
            best = c
    return best


t0 = time.time()
ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
rec = json.load(open("/home/user/Erdos-757/data/small_records.json"))["sets"]
sets = {"A_base": ABASE}
for k, v in rec.items():
    sets["small_records[%s]" % k] = v["set"]
fib = [2, 3]
while len(fib) < 18:
    fib.append(fib[-1] + fib[-2])
sets["Fibonacci F3..F20"] = fib
sets["{1,2,3,5,...} (negative)"] = [1, 2, 3, 5, 8, 13, 21]
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
sets["O"] = O

# (L4) on named sets and ALL induced subsets of A_base and of the 12-point sets
tot = 0
okL4 = True
for name, X in sets.items():
    a = is45(X)
    b = no4rel(X) and linear(aps_exact(X))
    tot += 1
    if a != b:
        okL4 = False
        print("   L4 mismatch on", name, a, b)
    print("     %s: n=%d (4,5)=%s  no4rel&linear=%s" % (name, len(X), a, b))
for name in ["A_base", "small_records[12]", "small_records[12b]", "small_records[12c]"]:
    X = sorted(sets[name])
    for k in range(4, len(X) + 1):
        for Y in combinations(X, k):
            tot += 1
            if is45(Y) != (no4rel(Y) and linear(aps_exact(Y))):
                okL4 = False
check(okL4, "L4 on named sets and all induced subsets of A_base and the three 12-point sets (%d sets; %.1fs)" % (tot, time.time() - t0))

# (L4) on random integer sets (most are NOT (4,5)): tests both directions
random.seed(20261020)
cnt = {True: 0, False: 0}
okR = True
for trial in range(20000):
    n = random.randint(4, 9)
    X = random.sample(range(0, random.choice([20, 40, 80, 200])), n)
    a = is45(X)
    b = no4rel(X) and linear(aps_exact(X))
    cnt[a] += 1
    if a != b:
        okR = False
        print("   L4 mismatch", sorted(X), a, b)
check(okR, "L4 on 20000 random integer sets: (4,5) %d, not (4,5) %d, equivalence holds in all (%.1fs)" % (cnt[True], cnt[False], time.time() - t0))

# (L4) generic and non-generic gluings A_base u (q O + t)
okG = True
ng = 0
for trial in range(60):
    if trial % 2 == 0:
        q = F(random.randint(1, 10 ** 6), random.randint(1, 10 ** 6))          # generic-ish rational scale
    else:
        q = F(random.choice([1, 2, 3, 4]))                                 # integer scales (often parallelograms)
    t = F(2000) + F(random.randint(0, 50))
    X = sorted(set([F(x) for x in ABASE] + [q * x + t for x in O]))
    if len(X) != 25:
        continue
    ng += 1
    a = is45(X)
    b = no4rel(X) and linear(aps_exact(X))
    if a != b:
        okG = False
check(okG, "L4 on %d gluings A_base u (qO+t), generic and integer q (%.1fs)" % (ng, time.time() - t0))

# (L4) the census data: 2910 saturated extremal 14-point classes and the 15-point sets
okD = True
nd = 0
for fn in ["/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz", "/home/user/Erdos-757/data/ext15_sets.jsonl.gz"]:
    with gzip.open(fn, "rt") as f:
        for i, line in enumerate(f):
            if i % 7:            # every 7th record, to bound the CPU time
                continue
            r = json.loads(line)
            X = r["set"]
            nd += 1
            a = is45(X)
            b = no4rel(X) and linear(aps_exact(X))
            if a != b or not a:
                okD = False
check(okD, "L4 on %d census sets from data/ (every 7th of census_n14_m12_classes and ext15_sets): all (4,5), all weak Sidon & linear (%.1fs)" % (nd, time.time() - t0))

# (L5) h = alpha(AP) for weak Sidon sets, brute force (n <= 16)
okL5 = True
nl5 = 0
cand = [ABASE, rec["12"]["set"], rec["12b"]["set"], rec["12c"]["set"], O, fib[:14]]
for trial in range(300):
    X = sorted(random.sample(range(0, 300), random.randint(5, 12)))
    if no4rel(X):
        cand.append(X)
for X in cand:
    if not no4rel(X):
        continue
    nl5 += 1
    hb = h_brute(X)
    al = alpha_brute(X, aps_exact(X))
    if hb != al:
        okL5 = False
        print("   L5 mismatch", X, hb, al)
check(okL5, "L5 (Sidon = AP-free in weak Sidon sets): h = alpha(AP) on %d weak Sidon sets incl. A_base (h=%d), O (h=%d) (%.1fs)" %
      (nl5, h_brute(ABASE), h_brute(O), time.time() - t0))

# (R7) exact ratios
r = [F(7 + 5 * K, 11 + 9 * K) for K in range(0, 101)]
check(all(r[K] == F(5, 9) + F(8, 9 * (11 + 9 * K)) for K in range(101)), "7.2: (7+5K)/(11+9K) = 5/9 + 8/(9(11+9K)) for K <= 100")
check(all(r[K] > r[K + 1] > F(5, 9) for K in range(100)), "7.2: strictly decreasing, > 5/9")
check([K for K in range(101) if r[K] < F(4, 7)] == list(range(6, 101)) and r[5] == F(4, 7), "7.5: below 4/7 iff K >= 6; K = 5 gives exactly 4/7")
check(r[6] == F(37, 65) and F(37, 65) < F(4, 7), "7.5: K=6 ratio 37/65 < 4/7 (exact)")
print("     K=0..6 ratios:", [str(x) for x in r[:7]])
print("SUMMARY: %d failures" % len(FAILS))
for f in FAILS:
    print("  FAILED:", f)
