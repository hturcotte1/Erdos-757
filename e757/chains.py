"""
Exact independence densities of periodic "chain" hypergraphs.

Chain model: vertex j (of class c = j mod p) is the midpoint of the AP {j - a_c, j, j + b_c}.
Fibonacci is the single-class chain (a, b) = (2, 1); tribonacci is (3, 1).
The largest density of a vertex set containing no edge is computed exactly as a maximum mean
cycle (Karp) on states (phase, last L bits), L = max(a_c + b_c).

Result recorded in kb/dead_ends.md: every linear single-class chain with a + b <= 11, every
2-class chain with span <= 8 and every 3-class chain with span <= 6 has density >= 3/5,
so these constructions cannot beat 4/7. Long-range structure is needed.
"""
from __future__ import annotations

import itertools
from fractions import Fraction


def chain_density(offsets):
    """offsets: list of (a_c, b_c) per class (period p = len(offsets)). Returns a Fraction."""
    p = len(offsets)
    L = max(a + b for a, b in offsets)
    n_states = p * (1 << L)
    edges = []
    for ph in range(p):
        for s in range(1 << L):
            for bit in (0, 1):
                t1 = ph + 1
                win = (s << 1) | bit  # bit k of win = position (t+1) - k
                bad = False
                for c, (a, b) in enumerate(offsets):
                    if ((t1 - b) - c) % p == 0:
                        if (win & 1) and (win >> b) & 1 and (win >> (a + b)) & 1:
                            bad = True
                            break
                if not bad:
                    edges.append((ph * (1 << L) + s, (t1 % p) * (1 << L) + (win & ((1 << L) - 1)), bit))
    NEG = -(10 ** 9)
    D = [[NEG] * n_states for _ in range(n_states + 1)]
    for v in range(n_states):
        D[0][v] = 0
    for k in range(1, n_states + 1):
        Dk, Dp = D[k], D[k - 1]
        for u, v, w in edges:
            if Dp[u] != NEG and Dp[u] + w > Dk[v]:
                Dk[v] = Dp[u] + w
    best = Fraction(-1)
    for v in range(n_states):
        if D[n_states][v] == NEG:
            continue
        worst = None
        for k in range(n_states):
            if D[k][v] != NEG:
                r = Fraction(D[n_states][v] - D[k][v], n_states - k)
                if worst is None or r < worst:
                    worst = r
        if worst is not None and worst > best:
            best = worst
    return best


def chain_is_linear(offsets, n=60):
    p = len(offsets)
    E = []
    for j in range(n):
        a, b = offsets[j % p]
        if j - a >= 0 and j + b < n:
            E.append(frozenset((j - a, j, j + b)))
    return all(len(e & f) <= 1 for e, f in itertools.combinations(E, 2))
