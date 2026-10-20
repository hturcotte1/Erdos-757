#!/usr/bin/env python3
"""Exact structural route to h(C003) <= 37 (human-checkable), independent of e757/judge.

1. Rebuild S_6 = O u phi(O) u ... u phi^6(O), phi(x) = 101 + 18x/269, with Fractions;
   scale by 269^6; compare with the claim set as exact sets.
2. Copy structure: C_j = phi^j(O); |C_j| = 11; C_{j-1} n C_j = a_j := phi^j({0,269}) = phi^{j-1}({101,119});
   C_j n C_j' = empty for |j-j'| >= 2.
3. APs of O (computed); every relation of the claim set (sum census, from the definition) is a
   3-AP lying inside one copy C_j and is phi^j of an AP of O; all 7*9 such images occur.
4. Finite facts on O (all 2^11 subsets): for every AP-free T in O, with s = T n {0,269},
   s' = T n {101,119}:   (F2) |T \\ {0,269}| <= 5 + [s' != 0] - [s != 0],
                          (F1) |T| <= 6 + [s' != 0].
5. Telescoping: |T| = |T n C_0| + sum_{j>=1} |T n (C_j \\ a_j)|
                    <= 6 + [T n b_0] + sum_{j=1..6} (5 + [T n b_j] - [T n a_j]),  b_j := a_{j+1},
                    = 6 + 5*6 + [T n b_6] <= 37.
   Also an exact max-plus evaluation of the same chain (own code) and the per-copy table.
"""
import itertools
import json
import sys
from collections import defaultdict
from fractions import Fraction

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
R = Fraction(18, 269)


def phi(x):
    return Fraction(101) + R * x


def phij(x, j):
    for _ in range(j):
        x = phi(x)
    return x


def aps_of(P):
    P = sorted(P)
    S = set(P)
    out = []
    for i in range(len(P)):
        for k in range(i + 1, len(P)):
            mid = (P[i] + P[k]) / 2
            if mid in S:
                out.append((P[i], mid, P[k]))
    return out


def main():
    claim = json.load(open(sys.argv[1]))
    A = sorted(int(x) for x in claim["set"])
    K = 6
    copies = [[phij(Fraction(x), j) for x in O] for j in range(K + 1)]
    S = sorted(set().union(*map(set, copies)))
    scale = 269 ** K
    Sint = [x * scale for x in S]
    assert all(x.denominator == 1 for x in Sint)
    Sint = [int(x) for x in Sint]
    print(f"1. rebuilt S_6: {len(S)} points; equals claim set exactly: {Sint == A}; "
          f"scale 269^6 = {scale}; max = {Sint[-1]} (= 269^7: {Sint[-1] == 269 ** 7})")

    # 2. copy structure
    ok = True
    for j in range(K + 1):
        ok &= len(set(copies[j])) == 11
    for j in range(1, K + 1):
        inter = set(copies[j - 1]) & set(copies[j])
        aj = {phij(Fraction(0), j), phij(Fraction(269), j)}
        bj1 = {phij(Fraction(101), j - 1), phij(Fraction(119), j - 1)}
        ok &= inter == aj == bj1
    for j, jj in itertools.combinations(range(K + 1), 2):
        if jj - j >= 2:
            ok &= not (set(copies[j]) & set(copies[jj]))
    print(f"2. copy structure (|C_j|=11, C_(j-1) n C_j = phi^j{{0,269}} = phi^(j-1){{101,119}}, "
          f"far copies disjoint): {ok};  65 = 7*11 - 6*2: {7 * 11 - 6 * 2 == len(S)}")

    # 3. APs and census
    apO = aps_of([Fraction(x) for x in O])
    print(f"3. APs of O: {len(apO)}: {[tuple(int(v) for v in e) for e in apO]}")
    # all relations of the claim set from the definition
    n = len(A)
    by_sum = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            by_sum[A[i] + A[j]].append((i, j))
    unions = set()
    for lst in by_sum.values():
        for p, q in itertools.combinations(lst, 2):
            unions.add(frozenset(A[v] for v in set(p) | set(q)))
    assert all(len(u) == 3 for u in unions)
    copy_sets = [set(int(x * scale) for x in c) for c in copies]
    images = set()
    for j in range(K + 1):
        for e in apO:
            images.add(frozenset(int(phij(v, j) * scale) for v in e))
    in_one_copy = all(any(u <= cs for cs in copy_sets) for u in unions)
    print(f"   claim-set relations: {len(unions)} (all 3-sets); each inside one copy: {in_one_copy}; "
          f"set of relations == {{phi^j(AP of O)}} ({len(images)} images): {unions == images}")

    # 4. finite facts on O, exhaustively
    idx = {x: i for i, x in enumerate(O)}
    E = [tuple(idx[int(v)] for v in e) for e in apO]
    a = {idx[0], idx[269]}
    b = {idx[101], idx[119]}
    best = defaultdict(lambda: -1)   # (s, s') -> max |T|
    F1 = F2 = True
    nfree = 0
    for mask in range(1 << 11):
        T = {i for i in range(11) if mask >> i & 1}
        if any(set(e) <= T for e in E):
            continue
        nfree += 1
        s = frozenset(T & a)
        sp = frozenset(T & b)
        best[(s, sp)] = max(best[(s, sp)], len(T))
        F2 &= len(T - a) <= 5 + (1 if sp else 0) - (1 if s else 0)
        F1 &= len(T) <= 6 + (1 if sp else 0)
    alphaO = max(best.values())
    print(f"4. O: {nfree} AP-free subsets, alpha(O) = {alphaO}; (F2) holds: {F2}; (F1) holds: {F1}")
    states = [frozenset(), frozenset({idx[0]}), frozenset({idx[269]}), frozenset({idx[0], idx[269]})]
    outs = [frozenset(), frozenset({idx[101]}), frozenset({idx[119]}), frozenset({idx[101], idx[119]})]
    M = [[best[(s, sp)] - len(s) for sp in outs] for s in states]
    R0 = [max(best[(s, sp)] for s in states) for sp in outs]
    print(f"   per-copy table M[s][s'] = max|T| - |s| (rows s = T n {{0,269}}: none, 0, 269, both; "
          f"cols s' = T n {{101,119}}): {M};  R_0 = {R0}")

    # 5. telescoping bound and exact max-plus evaluation
    bound = 6 + 5 * K + 1
    Rv = R0[:]
    for _ in range(K):
        # copy j: anchors a_j = phi^j{0,269} carry the state of the previous copy's outs b_(j-1);
        # the pairing (0 <-> 101, 269 <-> 119) is phi(0) = 101, phi(269) = 119
        Rv = [max(Rv[t] + M[t][u] for t in range(4)) for u in range(4)]
    print(f"5. telescoping bound 6 + 5K + 1 = {bound} for K = {K}; exact max-plus chain value = {max(Rv)}; "
          f"phi(0) = {phi(Fraction(0))}, phi(269) = {phi(Fraction(269))}")


if __name__ == "__main__":
    main()
