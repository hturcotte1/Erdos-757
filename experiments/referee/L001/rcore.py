"""Referee L001: independent primitives. No imports from e757/ or judge/.
All decisions exact: Fractions are scaled to integers by the lcm of denominators."""
from fractions import Fraction as Fr
from itertools import combinations
from math import lcm

A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


def to_int(S):
    """Scale a list of Fractions/ints to distinct integers (positive scaling preserves every property)."""
    S = [Fr(s) for s in S]
    L = 1
    for s in S:
        L = lcm(L, s.denominator)
    T = [int(s * L) for s in S]
    assert all(Fr(t, L) == s for t, s in zip(T, S))
    return T, L


def is45(S):
    """Definition: every 4 distinct points determine >= 5 distinct absolute differences. Full check, no shortcuts."""
    T, _ = to_int(S)
    if len(set(T)) != len(T):
        raise ValueError('repeated points')
    T.sort()
    n = len(T)
    D = [[abs(T[i] - T[j]) for j in range(n)] for i in range(n)]
    for i, j, k, l in combinations(range(n), 4):
        if len({D[i][j], D[i][k], D[i][l], D[j][k], D[j][l], D[k][l]}) < 5:
            return False
    return True


def three_aps(S):
    """All 3-term APs (as sorted triples) in S, found by brute force over triples."""
    T = sorted(Fr(s) for s in S)
    return [(p, q, r) for p, q, r in combinations(T, 3) if q - p == r - q]


def is_sidon_def(S):
    """Definition via positive differences: all pairwise positive differences distinct."""
    T, _ = to_int(S)
    d = [abs(u - v) for u, v in combinations(T, 2)]
    return len(d) == len(set(d))


def max_sidon(S, count_all=False):
    """Largest Sidon subset by branch and bound over points in increasing order, maintaining the
    set of positive differences used so far (no use of AP hypergraphs).
    Returns (h, witness as Fractions[, number of maximum Sidon subsets])."""
    T, L = to_int(S)
    order = sorted(range(len(T)), key=lambda i: T[i])
    T = [T[i] for i in order]
    n = len(T)
    best = [0, None]
    cnt = [0]

    def rec(i, chosen, diffs):
        k = len(chosen)
        if count_all:
            if k + (n - i) < best[0]:
                return
        elif k + (n - i) <= best[0]:
            return
        if i == n:
            if k > best[0]:
                best[0], best[1], cnt[0] = k, list(chosen), 1
            elif k == best[0]:
                cnt[0] += 1
            return
        z = T[i]
        nd = [z - c for c in chosen]
        ok = len(set(nd)) == len(nd) and not any(d in diffs for d in nd)
        if ok:
            chosen.append(z)
            rec(i + 1, chosen, diffs | set(nd))
            chosen.pop()
        rec(i + 1, chosen, diffs)

    rec(0, [], frozenset())
    W = [Fr(w, L) for w in best[1]]
    assert is_sidon_def(W) and len(W) == best[0]
    if count_all:
        return best[0], W, cnt[0]
    return best[0], W


def ap_partners(S):
    """All values v (not in S) such that {v, s, t} is a 3-AP for some distinct s, t in S:
    v midpoint (s+t)/2, or v endpoint 2s - t (s the midpoint)."""
    S = [Fr(s) for s in S]
    out = set()
    for s in S:
        for t in S:
            if s != t:
                out.add((s + t) / 2)
                out.add(2 * s - t)
    return out - set(S)
