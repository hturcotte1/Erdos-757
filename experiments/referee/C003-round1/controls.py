#!/usr/bin/env python3
"""Positive and negative controls for the referee verifier (own code only; no e757/judge).

Positive: A_base (n=14, h=8), the three 12-point sets (h=7), all sets of data/small_records.json,
          Fibonacci {2,3,5,...,F_k}: (4,5) and h by DP == h by definition-level brute force.
Negative: {1,2,3,5} and {1,2,3,6} must fail; the claim set with one point replaced so that a
          parallelogram or an AP sharing two points appears must fail the (4,5) test; a
          witness with one extra point must fail the Sidon test.
"""
import json
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from verify_c003 import bfs_order, check_45, frontier_dp, is_sidon_diffs, is_sidon_sums, sum_census  # noqa
from bruteforce_crosscheck import brute_definition  # noqa: E402


def forb_of(B):
    rels, _ = sum_census(B)
    return sorted({tuple(sorted(set(p) | set(q))) for p, q in rels})


def h_dp(B):
    F = forb_of(B)
    return frontier_dp(len(B), F, bfs_order(len(B), F, 0))[0]


def main():
    repo = sys.argv[1]
    A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    twelve3 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]
    recs = json.load(open(f"{repo}/data/small_records.json"))["sets"]
    tests = [("A_base", A_base, 8), ("12-pt third set", twelve3, 7)]
    for k, v in recs.items():
        if isinstance(v, dict) and "set" in v:
            tests.append((f"small_records[{k}]", v["set"], v.get("h")))
        elif isinstance(v, list):
            for i, w in enumerate(v):
                tests.append((f"small_records[{k}][{i}]", w["set"], w.get("h")))
    fib = [2, 3]
    while len(fib) < 16:
        fib.append(fib[-1] + fib[-2])
    tests.append(("Fibonacci 2..F_17 (16 pts)", fib, None))
    for name, S, hexp in tests:
        S = sorted(int(x) for x in S)
        ok45 = check_45(S)[0]
        d = h_dp(S)
        bf = brute_definition(S) if len(S) <= 22 else None
        print(f"{name}: n={len(S)} (4,5)={ok45} h_DP={d} h_brute={bf} expected={hexp} "
              f"{'OK' if (bf is None or bf == d) and (hexp is None or hexp == d) else 'MISMATCH'}")

    # negative controls
    print(f"negative [1,2,3,5]: (4,5) = {check_45([1, 2, 3, 5])[0]} (must be False: diffs {{1,2,3,4}})")
    print(f"control [1,2,3,6]: (4,5) = {check_45([1, 2, 3, 6])[0]} (must be True: diffs {{1,..,5}}; "
          f"it is (4,5) but not Sidon, K3), Sidon = {is_sidon_sums([1, 2, 3, 6])} (must be False)")
    claim = json.load(open(f"{repo}/results/claims/C003-reader-5-9-K6.json"))
    A = sorted(int(x) for x in claim["set"])
    rng = random.Random(7)
    caught = 0
    for t in range(20):
        a, b, c = rng.sample(A, 3)
        x = a + b - c   # creates a+b = c+x (parallelogram or AP)
        if x in A:
            continue
        B = sorted(set(A) | {x})
        ok = check_45(B)[0]
        caught += (not ok)
    print(f"negative: claim set + one point x = a+b-c, 20 trials: (4,5) rejected in {caught} of the trials "
          f"with x new")
    W = sorted(int(x) for x in claim["witness_sidon_subset"])
    rest = [x for x in A if x not in W]
    extra_ok = [x for x in rest if is_sidon_sums(W + [x])]
    print(f"negative: witness + any one of the {len(rest)} other points is Sidon for {len(extra_ok)} of them "
          f"(0 expected: the witness is maximal); diff/sum tests agree: "
          f"{all(is_sidon_sums(W + [x]) == is_sidon_diffs(W + [x]) for x in rest)}")


if __name__ == "__main__":
    main()
