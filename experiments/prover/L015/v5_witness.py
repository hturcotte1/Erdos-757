#!/usr/bin/env python3
"""L015 / C5: the explicit Sidon subsets T_K = U* u phi(U*) u ... u phi^K(U*), U* = {0,98,101,117,119,159,269} (Step 6).
For each K in the list: |T_K| = 7+5K (as computed, not assumed), T_K is a subset of S_K, T_K is Sidon BY DEFINITION
(all sums x+y, x<=y, distinct), T_K contains no 3-term AP, and T_K = U* u phi(T_{K-1}) (self-similar form).
Integer form as in v3_family.py.   Run:  python3 -I v5_witness.py K1 K2 ...
"""
import sys
from itertools import combinations

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
USTAR = [0, 98, 101, 117, 119, 159, 269]


def N(j, x):
    v = x
    for i in range(1, j + 1):
        v = 101 * 269 ** i + 18 * v
    return v


def S_int(K, base):
    return sorted({269 ** (K - j) * N(j, x) for j in range(K + 1) for x in base})


def main():
    for K in [int(a) for a in sys.argv[1:]]:
        S = S_int(K, O)
        T = S_int(K, USTAR)
        sums = [a + b for i, a in enumerate(T) for b in T[i:]]
        sidon = len(sums) == len(set(sums))
        Tset = set(T)
        ap_free = not any((a + c) % 2 == 0 and (a + c) // 2 in Tset for a, c in combinations(T, 2))
        if K >= 1:   # T_K = 269^K U*  u  { 101*269^K + 18 t : t in T_{K-1} }   (phi applied, then scaled)
            rec = sorted({269 ** K * u for u in USTAR} | {101 * 269 ** K + 18 * t for t in S_int(K - 1, USTAR)})
            rec_ok = rec == T
        else:
            rec_ok = T == USTAR
        good = len(T) == 7 + 5 * K and Tset <= set(S) and sidon and ap_free and rec_ok
        print(f"K={K}: n={len(S)} |T_K|={len(T)} (7+5K={7+5*K}) subset={Tset <= set(S)} Sidon_by_definition={sidon} "
              f"({len(sums)} sums) AP_free={ap_free} self_similar={rec_ok} -> {'OK' if good else 'FAIL'}", flush=True)
        if not good:
            raise SystemExit("FAILED")
    print("ALL WITNESS CHECKS OK")


if __name__ == "__main__":
    main()
