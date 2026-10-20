#!/usr/bin/env python3
"""(1) The explicit Sidon subsets T_K = U phi^j(U*), U* = {0,98,101,117,119,159,269}, for K <= 30:
    T_K subset of S_K, |T_K| = 7+5K, Sidon by definition (all sums x+y, x<=y, distinct), no 3-AP,
    and T_K = U* u phi(T_{K-1}).
(2) The C003 identity: results/claims/C003-reader-5-9-K6.json 'set' equals I_6 = 269^6 S_6 exactly;
    artifact checks on the raw JSON (types, duplicates), witness check, and the exact ratio test with Fractions;
    h of the raw JSON set recomputed by the r4 DP and SAT (from the Sidon definition).
Own code; standard library + pysat (via r4_h).
"""
import sys, json
sys.path.insert(0, ".")
from fractions import Fraction as Fr
from itertools import combinations
from r2_family import build, phij
from r4_h import constraints_from_definition, frontier_dp, sat_h, is_sidon

Ustar = [0, 98, 101, 117, 119, 159, 269]
allok = True
prevT = None
for K in range(0, 31):
    copies, S, I = build(K)
    Sset = set(S)
    T = sorted(set(phij(x, j) for j in range(K + 1) for x in Ustar))
    scale = 269 ** K
    TI = [int(v * scale) for v in T]
    assert all((v * scale).denominator == 1 for v in T)
    sid = is_sidon(TI)
    noap = not any(a + c == 2 * b for a, b, c in combinations(TI, 3))
    sub = set(T) <= Sset
    selfsim = True
    if prevT is not None:
        selfsim = set(T) == set(Fr(x) for x in Ustar) | set(101 + Fr(18, 269) * v for v in prevT)
    ok = sid and noap and sub and len(T) == 7 + 5 * K and selfsim
    allok &= ok
    if K <= 10 or K % 5 == 0:
        print("K=%d |T_K|=%d (7+5K=%d) subset=%s Sidon=%s noAP=%s selfsimilar=%s -> %s"
              % (K, len(T), 7 + 5 * K, sub, sid, noap, selfsim, "OK" if ok else "FAIL"), flush=True)
    prevT = T
print("ALL WITNESS T_K (K<=30) OK" if allok else "WITNESS FAILED")

# ---------- C003
raw = json.load(open("/home/user/Erdos-757/results/claims/C003-reader-5-9-K6.json"))
st = raw["set"]
types_ok = all(type(v) is int for v in st)        # excludes bool, float, str
dup_ok = len(set(st)) == len(st)
copies, S, I6 = build(6)
eq = sorted(st) == I6
print("C003: n=%d all-int=%s distinct=%s equals I_6=%s claimed_h=%r" % (len(st), types_ok, dup_ok, eq, raw.get("claimed_h")))
w = raw.get("witness_sidon_subset", [])
w_ok = all(type(v) is int for v in w) and len(set(w)) == len(w) == 37 and set(w) <= set(st) and is_sidon(w)
print("C003 witness: size=%d subset=%s Sidon=%s" % (len(w), set(w) <= set(st), is_sidon(w)))
A = sorted(st)
cons = constraints_from_definition(A)
hdp, wdt, ms = frontier_dp(len(A), cons)
r37, T37 = sat_h(A, cons, 37, "cadical195")
r38, _ = sat_h(A, cons, 38, "cadical195")
print("C003 raw set: h by DP = %d; SAT >=37 %s, >=38 %s" % (hdp, "SAT" if r37 else "UNSAT", "SAT" if r38 else "UNSAT"))
# (4,5) on the raw set, literally
mn = min(len({a - b for a in B for b in B}) for B in combinations(A, 4))
print("C003 raw set: min |B-B| over all 4-subsets = %d" % mn)
ratio = Fr(hdp, len(A))
print("C003 ratio h/n = %s ; < 4/7: %s ; 7*37=%d vs 4*65=%d" % (ratio, ratio < Fr(4, 7), 7 * 37, 4 * 65))
c_ok = types_ok and dup_ok and eq and raw.get("claimed_h") == 37 and w_ok and hdp == 37 and r37 and not r38 and mn >= 11 and ratio < Fr(4, 7)
# records: K=5 ratio, smallest K below 4/7
recs = [(K, Fr(7 + 5 * K, 11 + 9 * K)) for K in range(0, 12)]
first = min(K for K, q in recs if q < Fr(4, 7))
print("ratios:", [(K, str(q)) for K, q in recs], " K=5 ratio == 4/7:", recs[5][1] == Fr(4, 7), " first K below 4/7:", first)
print("difference formula (7+5K)/(11+9K) - 5/9 == 8/(9(11+9K)) for K<=1000:",
      all(Fr(7 + 5 * K, 11 + 9 * K) - Fr(5, 9) == Fr(8, 9 * (11 + 9 * K)) for K in range(1001)))
c_ok = c_ok and recs[5][1] == Fr(4, 7) and first == 6
print("ALL C003 CHECKS OK" if c_ok else "C003 CHECKS FAILED")
