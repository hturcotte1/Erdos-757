#!/usr/bin/env python3
"""Validate the referee's exact tools (frontier DP of dp2.py, SAT of sat_check.py, HiGHS MILP of
sat_check.py) against a brute force that uses ONLY the Sidon definition, on instances with n <= 22:
  - A_base and the small record sets in data/small_records.json (known h values);
  - structured induced subsets of the C005 set (sizes 14..22) chosen to contain many 3-APs:
    zigzag-order prefixes (outer layers + the two new points), centre blocks (inner copies), and
    unions of AP vertex sets.  Induced subsets of a (4,5)-set are (4,5)-sets.
Brute force: for s = n, n-1, ...: test every s-subset for 'all positive differences distinct';
the first s with a Sidon s-subset is h.  No e757, no judge.
"""
import itertools
import json
import random
import sys
import time

sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/C005-round2")
import dp2  # noqa: E402
import sat_check  # noqa: E402


def brute_h(A):
    n = len(A)
    for s in range(n, 0, -1):
        for sub in itertools.combinations(A, s):
            d = set()
            ok = True
            for x, y in itertools.combinations(sub, 2):
                t = y - x
                if t in d:
                    ok = False
                    break
                d.add(t)
            if ok:
                return s
    return 0


def dp_h(A):
    n = len(A)
    edges = dp2.aps_of(A)
    vals = []
    for order in (dp2.zigzag(n), list(range(n)), dp2.greedy_order(n, edges)):
        fs, _, _ = dp2.frontier_profile(n, edges, order)
        if max(fs) <= 22:
            h, _ = dp2.dp(n, edges, order, max_frontier=22, verbose=False)
            vals.append(h)
    assert vals and all(v == vals[0] for v in vals), ("DP orders disagree!", vals)
    return vals[0], len(edges)


def sat_h(A, h):
    cons = sat_check.conflicts(A)
    n = len(A)
    r1, _, _ = sat_check.sat_method(A, cons, h) if h >= 1 else (True, None, 0)
    r2 = False if h + 1 > n else sat_check.sat_method(A, cons, h + 1)[0]
    return r1, r2


def milp_h(A):
    cons = sat_check.conflicts(A)
    st, msg, val, bnd, dt = sat_check.milp_method(A, cons, 60)
    return val if st == 0 else None


def check(name, A, expected=None):
    t0 = time.time()
    hb = brute_h(A)
    tb = time.time() - t0
    hd, m = dp_h(A)
    r1, r2 = sat_h(A, hb)
    hm = milp_h(A)
    ok = (hd == hb) and r1 and (not r2) and (hm == hb) and (expected is None or expected == hb)
    print(f"{name}: n={len(A)} m={m} brute h={hb} ({tb:.1f}s) DP h={hd} SAT(>=h)={r1} SAT(>=h+1)={r2} MILP h={hm}"
          + (f" expected={expected}" if expected is not None else "") + (" OK" if ok else " MISMATCH!!"))
    sys.stdout.flush()
    return ok


def main():
    allok = True
    A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    allok &= check("A_base", A_base, 8)
    try:
        rec = json.load(open("/home/user/Erdos-757/data/small_records.json"))
        cnt = 0

        def walk(obj, key=""):
            nonlocal cnt, allok
            if isinstance(obj, dict):
                for k, v in obj.items():
                    walk(v, f"{key}/{k}")
            elif isinstance(obj, list):
                if obj and all(isinstance(x, int) for x in obj) and 6 <= len(obj) <= 22 and cnt < 12:
                    cnt += 1
                    allok &= check(f"small_records{key}", sorted(obj))
                else:
                    for i, v in enumerate(obj):
                        walk(v, f"{key}[{i}]")
        walk(rec)
    except Exception as e:
        print("small_records.json not usable:", e)
    C = dp2.load("/home/user/Erdos-757/results/claims/C005-lemmaE-SK6-E1.json")
    n = len(C)
    edges = dp2.aps_of(C)
    zz = dp2.zigzag(n)
    # zigzag prefixes: outer layers plus the two new points
    for s in (14, 16, 18, 20, 22):
        idx = sorted(zz[:s])
        allok &= check(f"C005 zigzag prefix n={s}", [C[i] for i in idx])
    # centre blocks (inner copies)
    for lo, s in ((27, 14), (26, 18), (24, 20), (23, 22), (30, 16)):
        idx = list(range(lo, lo + s))
        allok &= check(f"C005 centre block [{lo},{lo+s}) n={s}", [C[i] for i in idx])
    # unions of AP vertex sets (random), padded to the target size with random vertices
    random.seed(20261021)
    for s in (16, 18, 20, 22, 22, 20):
        verts = set()
        es = edges[:]
        random.shuffle(es)
        for e in es:
            if len(verts | set(e)) <= s:
                verts |= set(e)
        while len(verts) < s:
            verts.add(random.randrange(n))
        idx = sorted(verts)
        allok &= check(f"C005 AP-union n={s}", [C[i] for i in idx])
    print("ALL OK" if allok else "SOME MISMATCH")


if __name__ == "__main__":
    main()
