#!/usr/bin/env python3
"""Independent check of L022 Theorem 5's claim that Q10 = (10,7,4) class 0
{012,034,157,268,379,489,569} is in C, tight, Delta = 3, and NOT contained in the AP hypergraph of
any (4,5)-set, and that every 6-edge subset is realizable. Own code: exact RREF over Q.
A labelled system (one midpoint per edge, injective) is realizable as a sub-hypergraph iff the generic
point of its solution space V is weak Sidon (no difference form and no form x_i+x_j-x_k-x_l with
{i,j},{k,l} disjoint vanishes on V) and the AP forms vanishing on V form a linear 3-graph.
"""
import itertools
from fractions import Fraction

Q10 = [(0,1,2),(0,3,4),(1,5,7),(2,6,8),(3,7,9),(4,8,9),(5,6,9)]

def rref(rows, n):
    rows = [list(map(Fraction, r)) for r in rows]
    piv = []
    r = 0
    for c in range(n):
        p = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0: p = i; break
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        inv = 1 / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c); r += 1
        if r == len(rows): break
    return rows[:r], piv

def in_rowspace(R, piv, v):
    v = list(map(Fraction, v))
    for row, c in zip(R, piv):
        if v[c] != 0:
            f = v[c]
            v = [a - f * b for a, b in zip(v, row)]
    return all(x == 0 for x in v)

def realizable(E, n):
    for mids in itertools.product(*[range(3) for _ in E]):
        M = [e[k] for e, k in zip(E, mids)]
        if len(set(M)) < len(M): continue
        rows = []
        for e, k in zip(E, mids):
            r = [0]*n
            for j, x in enumerate(e):
                r[x] += (-2 if j == k else 1)
            rows.append(r)
        R, piv = rref(rows, n)
        bad = False
        for i, j in itertools.combinations(range(n), 2):
            v = [0]*n; v[i] = 1; v[j] = -1
            if in_rowspace(R, piv, v): bad = True; break
        if bad: continue
        for a, b, c, d in itertools.permutations(range(n), 4):
            if a < b and c < d and a < c:
                v = [0]*n; v[a] += 1; v[b] += 1; v[c] -= 1; v[d] -= 1
                if in_rowspace(R, piv, v): bad = True; break
        if bad: continue
        forced = []
        for j in range(n):
            for i, k in itertools.combinations([x for x in range(n) if x != j], 2):
                v = [0]*n; v[i] += 1; v[k] += 1; v[j] -= 2
                if in_rowspace(R, piv, v): forced.append(frozenset((i, j, k)))
        if any(len(e & f) >= 2 for e, f in itertools.combinations(set(forced), 2)): continue
        return True, M
    return False, None

def tau(E):
    Es = [frozenset(e) for e in E]; best = [len(E)]
    def rec(ch, k):
        if k >= best[0]: return
        unc = [e for e in Es if not (e & ch)]
        if not unc: best[0] = k; return
        for u in sorted(unc[0]): rec(ch | {u}, k + 1)
    rec(frozenset(), 0); return best[0]

if __name__ == "__main__":
    n = 10
    deg = [sum(x in e for e in Q10) for x in range(n)]
    t = tau(Q10)
    print("degrees", sorted(deg), "tau", t, "slack", 3*n + 2*len(Q10) - 11*t)
    ok, M = realizable(Q10, n)
    print("Q10 realizable as sub-hypergraph of a (4,5)-set:", ok)
    allsub = True
    for S in itertools.combinations(Q10, 6):
        used = sorted(set().union(*S))
        idx = {x: i for i, x in enumerate(used)}
        S2 = [tuple(idx[x] for x in e) for e in S]
        r, _ = realizable(S2, len(used))
        if not r: allsub = False; print("non-realizable 6-subset", S)
    print("all 6-edge subsets realizable:", allsub)
