"""
Provable bounds on f(n) = min { h(A) : A an n-point (4,5)-set }, and where 4/7 can be beaten.

Lower bound (published route, Ma-Tang + Henning-Yeo):
    17 tau <= 5n + 3m,  m <= n - 2   =>   h = n - tau >= n - floor((8n - 6) / 17)   (n >= 2)
    plus f(5) = 4: a linear 3-uniform hypergraph on 5 vertices has a 1-vertex transversal
    (three pairwise-intersecting triples on 5 points must share a point).
Upper bound (constructions):
    f(3) <= 2 (a 3-AP), f(12) <= 7 (12-point sets, omega issue #9804), f(14) <= 8 (A_base, Ma-Tang),
    f(n) <= f(n+1) (delete a point), f(n+1) <= f(n) + 1 (add a generic point),
    f(a+b) <= f(a) + f(b) (gluing, Ma-Tang Lemma 3.6).
Update KNOWN_UPPER when a new verified construction exists.
"""
from __future__ import annotations

import math
from fractions import Fraction

KNOWN_UPPER = {3: 2, 12: 7, 14: 8}
KNOWN_LOWER_EXTRA = {5: 4}


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
    U = {n: n for n in range(1, N + 1)}
    for n, v in KNOWN_UPPER.items():
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
        print(f"n={n:2d}: {'possible' if ok else 'EXCLUDED'}  need h<={h} tau>={tau} m>={m} (max {n-2})")
