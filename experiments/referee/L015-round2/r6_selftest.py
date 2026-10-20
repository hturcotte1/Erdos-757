#!/usr/bin/env python3
"""Self-test of the two exact h methods of r4_h.py (frontier DP, SAT) against literal brute force
(all subsets, Sidon by definition), on random integer sets (with 4-point relations present) and on
known sets: A_base (h=8), the data/small_records.json sets, the third 12-point record, Fibonacci sets.
Own code."""
import sys, json, random
sys.path.insert(0, ".")
from r4_h import constraints_from_definition, frontier_dp, sat_h, is_sidon

def brute_h(A):
    n = len(A)
    best = 0
    # enumerate subsets by decreasing size would be faster; plain enumeration is fine for n <= 16
    for mask in range(1 << n):
        k = bin(mask).count("1")
        if k <= best:
            continue
        U = [A[i] for i in range(n) if mask >> i & 1]
        if is_sidon(U):
            best = k
    return best

def h_dp(A):
    cons = constraints_from_definition(A)
    return frontier_dp(len(A), cons)[0]

def h_sat(A, solver="cadical195"):
    cons = constraints_from_definition(A)
    lo = 0
    # find largest t with SAT
    t = 1
    while t <= len(A):
        ok, T = sat_h(A, cons, t, solver)
        if not ok:
            break
        assert is_sidon(T)
        lo = t
        t += 1
    return lo

random.seed(20261020)
bad = 0
for trial in range(300):
    n = random.randint(3, 13)
    span = random.choice([20, 40, 80, 200])
    A = sorted(random.sample(range(span), n))
    b = brute_h(A); d = h_dp(A); s = h_sat(A)
    if not (b == d == s):
        bad += 1
        print("MISMATCH", A, b, d, s)
print("random sets: 300 trials, mismatches:", bad)

known = []
known.append(("A_base", [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056], 8))
known.append(("12pt#3", [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575], 7))
sr = json.load(open("/home/user/Erdos-757/data/small_records.json"))["sets"]
for k, v in sr.items():
    s = v["set"] if isinstance(v, dict) else v
    if isinstance(s, list) and s and isinstance(s[0], list):
        for i, t in enumerate(s):
            known.append(("small_records[%s][%d]" % (k, i), t, None))
    elif isinstance(s, list):
        known.append(("small_records[%s]" % k, s, v.get("h") if isinstance(v, dict) else None))
fib = [2, 3]
while len(fib) < 16:
    fib.append(fib[-1] + fib[-2])
for m in (8, 10, 12, 14, 16):
    known.append(("Fib F3..F%d" % (m + 2), fib[:m], None))
for name, A, hexp in known:
    A = sorted(A)
    d = h_dp(A); s = h_sat(A)
    b = brute_h(A) if len(A) <= 16 else None
    ok = d == s and (b is None or b == d) and (hexp is None or hexp == d)
    bad += 0 if ok else 1
    print("%-24s n=%2d h: DP=%d SAT=%d brute=%s expected=%s %s" % (name, len(A), d, s, b, hexp, "OK" if ok else "FAIL"))
print("ALL SELFTESTS OK" if bad == 0 else "SELFTEST FAILED")
