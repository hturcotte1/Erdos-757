"""
Provable bounds on f(n) = min { h(A) : A an n-point (4,5)-set }, and where 4/7 can be beaten.

Lower bound (published route, Ma-Tang + Henning-Yeo):
    17 tau <= 5n + 3m,  m <= n - 2   =>   h = n - tau >= n - floor((8n - 6) / 17)   (n >= 2)
    plus f(5) = 4: a linear 3-uniform hypergraph on 5 vertices has a 1-vertex transversal
    (three pairwise-intersecting triples on 5 points must share a point).
Upper bound (constructions):
    f(3) <= 2 (a 3-AP), f(8) <= 5, f(10) <= 6 (data/small_records.json, found by e757.ordered_search),
    f(12) <= 7 (12-point sets, omega issue #9804), f(14) <= 8 (A_base, Ma-Tang),
    f(n) <= f(n+1) (delete a point), f(n+1) <= f(n) + 1 (add a generic point),
    f(a+b) <= f(a) + f(b) (gluing, Ma-Tang Lemma 3.6).
Update KNOWN_UPPER when a new verified construction exists.
"""
from __future__ import annotations

import math
from fractions import Fraction

KNOWN_UPPER = {3: 2, 8: 5, 10: 6, 12: 7, 14: 8}  # 8, 10: data/small_records.json
KNOWN_LOWER_EXTRA = {5: 4}
# Exact values proved by computer-assisted, referee-accepted certificates (lower bound beyond Henning-Yeo; the
# matching upper bound is in KNOWN_UPPER or follows by monotonicity/gluing).  Add 18 and 20 only after L009/L010 are accepted.
#   16: 10  -- certificate L008 (results/proofs/L008-f16-equals-10.md, K52): f(16) = 10; witness A_base + {-323, 5000}.
EXACT_VALUES_VERIFIED = {16: 10}


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
    """True if f(n) is known exactly by a verified certificate (EXACT_VALUES_VERIFIED); such n cannot host a record
    beating 4/7 beyond what the exact value allows."""
    return n in EXACT_VALUES_VERIFIED


def beat_feasibility(n):
    """Can an n-point (4,5)-set have h/n < 4/7 without contradicting Henning-Yeo?
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
            note = f"  [f({n}) = {EXACT_VALUES_VERIFIED[n]} exactly, L008: h<={h} impossible]"
        print(f"n={n:2d}: {status}  need h<={h} tau>={tau} m>={m} (max {n-2}){note}")
