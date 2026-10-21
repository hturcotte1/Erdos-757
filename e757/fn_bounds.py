"""
Provable bounds on f(n) = min { h(A) : A an n-point (4,5)-set }, and where 4/7 can be beaten.

Lower bound (published route, Ma-Tang + Henning-Yeo):
    17 tau <= 5n + 3m,  m <= n - 2   =>   h = n - tau >= n - floor((8n - 6) / 17)   (n >= 2)
    plus f(5) = 4: a linear 3-uniform hypergraph on 5 vertices has a 1-vertex transversal
      (two triples on 5 points always share a point, and a linear 3-uniform hypergraph on 5 points has at most 2 edges).
    plus the certified exact values f(16) = 10, f(18) = 11, f(20) = 12, f(22) = 13, f(23) = 14
      (EXACT_VALUES_VERIFIED below; computer-assisted certificates L008-L011 and L014, K52-K55 and K58, each accepted by
      three referees [verified-here]), which exceed the Henning-Yeo bound (9, 10, 11, 12, 13) at those n.
Upper bound (constructions):
    f(3) <= 2 (a 3-AP), f(8) <= 5, f(10) <= 6 (data/small_records.json, found by e757.ordered_search),
    f(12) <= 7 (12-point sets, omega issue #9804), f(14) <= 8 (A_base, Ma-Tang),
    f(65) <= 37 (KNOWN_UPPER[65] = C003, the depth-6 member of an anonymous reader's self-similar family posted on Erdos Problem
      a Day on 19 Oct 2026: a COMMUNITY construction, NOT this project's discovery; rebuilt exactly, judged PASS NEW-RECORD and
      refereed here, K59).  The whole family f(11+9K) <= 7+5K, i.e. c* <= 5/9, has an independent proof (certificate L015, K60);
      only the judged K = 6 member is tabulated, and it affects fn_bounds(N) only for N >= 65 (the default N = 60 does not see it),
    f(n) <= f(n+1) (delete a point), f(n+1) <= f(n) + 1 (add a generic point),
    f(a+b) <= f(a) + f(b) (gluing, Ma-Tang Lemma 3.6).
Update KNOWN_UPPER when a new verified construction exists.
"""
from __future__ import annotations

import math
from fractions import Fraction

KNOWN_UPPER = {3: 2, 8: 5, 10: 6, 12: 7, 14: 8, 58: 33, 65: 37, 67: 38}  # 8, 10: data/small_records.json; 65: 37 = C003 (results/claims/C003-reader-5-9-K6.json; a COMMUNITY construction, the depth-6 member of an anonymous reader's family posted on Erdős Problem a Day 19 Oct 2026; judged PASS NEW-RECORD and ACCEPTED by two referees here, K59): 37/65 < 4/7; 58: 33 = C004 and 67: 38 = C005 (this project's Lemma-E two-point extensions of S_5 and S_6 at their universal minimum; judged and ACCEPTED x2 each, K62, K63): 33/58 and 38/67 < 4/7
KNOWN_LOWER_EXTRA = {5: 4}
# Exact values proved by computer-assisted, referee-accepted certificates (lower bound beyond Henning-Yeo; the
# matching upper bound is in KNOWN_UPPER or follows by monotonicity/gluing).  Each entry is a certificate accepted by three
# referees (kb/known_results.md K52-K55 and K58, results/LEDGER.md); add a new entry only after its certificate is accepted.
#   16: 10  -- certificate L008 (results/proofs/L008-f16-equals-10.md, K52): f(16) = 10; witness A_base + {-323, 5000}.
#   18: 11  -- certificate L009 (results/proofs/L009-f18-equals-11.md, K53).
#   20: 12  -- certificate L010 (results/proofs/L010-f20-equals-12.md, K54).
#   22: 13  -- certificate L011 (results/proofs/L011-f22-equals-13.md, K55): no (4,5)-set with at most 22 points beats 4/7.
#   23: 14  -- certificate L014 (results/proofs/L014-f23-equals-14.md, K58): f(23) = 14; the lower bound is Theorem 1/2 of L014, the upper bound the
#              witness C23 = B12 u (10^9 + 7919 B11) (B12 = the third 12-point record of kb/00_START_HERE.md section 6, B11 = data/small_records.json
#              sets["11"]; tests/test_c23_witness.py). No (4,5)-set with at most 24 points beats 4/7; the first size at which a (4,5)-set
#              beating 4/7 is not excluded by a certificate is n = 25 (L014 Corollary 3).
EXACT_VALUES_VERIFIED = {16: 10, 18: 11, 20: 12, 22: 13, 23: 14}  # L008/K52, L009/K53, L010/K54, L011/K55, L014/K58 (referee ACCEPT x3 each)


def hy_max_tau(n, m=None):
    """Largest transversal number allowed by Henning-Yeo for n points and m APs (default m = n-2)."""
    if m is None:
        m = max(n - 2, 0)
    return (5 * n + 3 * m) // 17


def fn_bounds(N=60):
    """Return {n: (lower, upper)} for 1 <= n <= N."""
    L = {1: 1, 2: 2}
    for n in range(3, N + 1):
        L[n] = n - hy_max_tau(n)
    for n, v in KNOWN_LOWER_EXTRA.items():
        L[n] = max(L[n], v)
    for n, v in EXACT_VALUES_VERIFIED.items():
        if n <= N:
            L[n] = max(L[n], v)
    U = {n: n for n in range(1, N + 1)}
    for n, v in KNOWN_UPPER.items():
        if n <= N:
            U[n] = min(U[n], v)
    for n, v in EXACT_VALUES_VERIFIED.items():
        if n <= N:
            U[n] = min(U[n], v)
    changed = True
    while changed:
        changed = False
        for n in range(1, N + 1):
            best = U[n]
            if n + 1 <= N:
                best = min(best, U[n + 1])
            if n > 1:
                best = min(best, U[n - 1] + 1)
            for a in range(1, n):
                best = min(best, U[a] + U[n - a])
            if best < U[n]:
                U[n] = best
                changed = True
    return {n: (L[n], U[n]) for n in range(1, N + 1)}


def f_lower(n):
    """Best known lower bound on f(n) (Henning-Yeo plus the verified exact values)."""
    return fn_bounds(max(n, 2))[n][0]


def is_closed(n):
    """True if f(n) is known exactly by a verified certificate (EXACT_VALUES_VERIFIED).  For every current entry
    (n = 16, 18, 20, 22, 23) f(n) = ceil(4n/7) = 10, 11, 12, 13, 14, so no n-point (4,5)-set has h/n < 4/7 there."""
    return n in EXACT_VALUES_VERIFIED


def beat_feasibility(n):
    """Can an n-point (4,5)-set have h/n < 4/7 without contradicting Henning-Yeo?
    Henning-Yeo only: EXACT_VALUES_VERIFIED is not consulted, so n = 16, 18, 20, 22, 23 still report possible = True although
      they are closed by the certificates L008-L011 and L014 (use is_closed(n); the __main__ table prints CLOSED for them).
    Returns (possible, h_needed, tau_needed, min_m_needed)."""
    h = math.ceil(Fraction(4 * n, 7)) - 1
    tau = n - h
    m_need = max(0, math.ceil(Fraction(17 * tau - 5 * n, 3)))
    return m_need <= n - 2, h, tau, m_need


if __name__ == "__main__":
    b = fn_bounds(40)
    print("exact:", {n: lu[0] for n, lu in b.items() if lu[0] == lu[1]})
    print("open :", {n: lu for n, lu in b.items() if lu[0] < lu[1]})
    for n in range(12, 41):
        ok, h, tau, m = beat_feasibility(n)
        status = 'possible' if ok else 'EXCLUDED'
        note = ""
        if ok and is_closed(n):
            status = 'CLOSED'
            note = f"  [f({n}) = {EXACT_VALUES_VERIFIED[n]} exactly, verified exact value (kb/known_results.md K52-K55, K58): h<={h} impossible]"
        print(f"n={n:2d}: {status}  need h<={h} tau>={tau} m>={m} (max {n-2}){note}")
