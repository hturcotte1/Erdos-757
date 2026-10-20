#!/usr/bin/env python3
"""Rebuild the reader's self-similar family (erdosproblemaday.com/day/757-reader-five-ninths-refereed).

O = {0,49,75,83,98,101,117,119,121,159,269},  phi(x) = 101 + 18x/269.
Three readings of S_K, all in exact Fractions:
  (R1) recursion  A_0 = O,  A_K = O u phi(A_{K-1})            (the scout's reading)
  (R2) union      S_K = O u phi(O) u ... u phi^K(O)           (the page's definition)
  (R3) closed form phi^j(x) = L + (18/269)^j (x - L), L = 27169/251 (fixed point of phi)
They must coincide as sets.  Then scale by the lcm of the denominators to get integers and write
data/reader_5_9_family.json.   Run:  python3 build_family.py
"""
import json
import sys
from fractions import Fraction as F
from math import gcd, lcm
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
KMAX = 8
L = F(27169, 251)


def phi(x):
    return F(101) + F(18) * F(x) / 269


def phi_pow(x, j):
    for _ in range(j):
        x = phi(x)
    return x


def S_recursive(K):
    A = sorted(F(x) for x in O)
    for _ in range(K):
        A = sorted(set(F(x) for x in O) | {phi(x) for x in A})
    return A


def S_union(K):
    s = set()
    for j in range(K + 1):
        s |= {phi_pow(F(x), j) for x in O}
    return sorted(s)


def S_closed(K):
    s = set()
    for j in range(K + 1):
        s |= {L + F(18, 269) ** j * (F(x) - L) for x in O}
    return sorted(s)


def to_ints(A):
    den = 1
    for a in A:
        den = lcm(den, a.denominator)
    ints = [int(a * den) for a in A]
    assert all(F(i, den) == a for i, a in zip(ints, A))
    return den, ints


def main():
    assert phi(0) == 101 and phi(269) == 119
    fam = []
    for K in range(KMAX + 1):
        r1, r2, r3 = S_recursive(K), S_union(K), S_closed(K)
        assert r1 == r2 == r3, f"readings differ at K={K}"
        assert len(r1) == 11 + 9 * K, f"K={K}: |S_K|={len(r1)} != {11 + 9 * K}"
        den, ints = to_ints(r1)
        g = 0
        for v in ints:
            g = gcd(g, v)
        fam.append({"K": K, "n": len(ints), "scale": den, "gcd_of_integers": g,
                    "scale_is_269_pow_K": den == 269 ** K, "set": ints})
        print(f"K={K} n={len(ints)} scale={den} (=269^K: {den == 269 ** K}) gcd={g} max={ints[-1]}")
    out = REPO / "data" / "reader_5_9_family.json"
    out.write_text(json.dumps({
        "source": "reader's 5/9 family, https://erdosproblemaday.com/day/757-reader-five-ninths-refereed [community]; rebuilt here by experiments/20261020-1730-reader-5-9/build_family.py",
        "definition": "O={0,49,75,83,98,101,117,119,121,159,269}, phi(x)=101+18x/269, S_K=O u phi(O) u ... u phi^K(O), integers = scale * S_K with scale = lcm of denominators",
        "readings_checked_equal": ["A_K = O u phi(A_{K-1})", "O u phi(O) u ... u phi^K(O)", "closed form L+(18/269)^j (x-L), L=27169/251"],
        "family": fam}, indent=1))
    print("wrote", out.relative_to(REPO))


if __name__ == "__main__":
    sys.exit(main())
