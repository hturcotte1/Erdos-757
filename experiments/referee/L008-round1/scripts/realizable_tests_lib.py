"""Referee numerical tests on genuine (4,5)-sets (exact integers, own code, no e757/judge imports):
 (1) witness C16: distinct, (4,5) from the definition, number of 3-APs, h by brute force over all 2^16 subsets (Sidon = all sums
     x+y, x<=y, distinct) and by CP-SAT (different method); h/n vs 4/7 with Fractions;
 (2) for every induced subset S of A_base (2^14), both 12-point omega sets and the third 12-point set, C16 (2^16) and the
     Fibonacci set {F3..F18} (2^16): H(S) is linear, F7-free and satisfies (P3) [membership in O+], I11 11 tau <= 3|S|+2m
     (Corollary 3 range |S|<=16), tau(H(S)) <= 6 when |S| = 16 (Theorem 1), and h(S) = |S| - tau(H(S)) on a random sample;
 (3) 16-point (4,5)-sets obtained by two-point extensions of census 14-point classes (points in new 3-APs), the same checks,
     and h >= 10 (Theorem 2)."""
import itertools, json, gzip, random, sys
from fractions import Fraction
def is45(A):
    for q in itertools.combinations(A, 4):
        if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5: return False
    return True
def aps(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(idx[a], idx[(a + c) // 2], idx[c]) for a, c in itertools.combinations(A, 2) if (a + c) % 2 == 0 and (a + c) // 2 in idx]
def is_sidon(S):
    s = set()
    for i in range(len(S)):
        for j in range(i, len(S)):
            t = S[i] + S[j]
            if t in s: return False
            s.add(t)
    return True
def h_brute(A):
    A = sorted(A); n = len(A); best = 0
    # iterate subsets by decreasing size would be faster; simple: check all subsets of size k from high to low
    for k in range(n, 0, -1):
        for S in itertools.combinations(A, k):
            if is_sidon(S): return k
    return 0
def h_cpsat(A):
    from ortools.sat.python import cp_model
    A = sorted(A); n = len(A); M = cp_model.CpModel(); x = [M.NewBoolVar('x%d' % i) for i in range(n)]
    # forbid every pair of distinct multisets {a,b} != {c,d} with a+b = c+d
    sums = {}
    for i in range(n):
        for j in range(i, n): sums.setdefault(A[i] + A[j], []).append((i, j))
    for s, prs in sums.items():
        for (i, j), (k, l) in itertools.combinations(prs, 2):
            inv = sorted({i, j, k, l}); M.Add(sum(x[t] for t in inv) <= len(inv) - 1)
    M.Maximize(sum(x)); S = cp_model.CpSolver(); S.parameters.num_workers = 1; st = S.Solve(M)
    assert st == cp_model.OPTIMAL; return int(S.ObjectiveValue())
def tau(edges, verts):
    edges = [frozenset(e) for e in edges]
    def rec(es, k):
        if not es: return True
        if k == 0: return False
        e = next(iter(es))
        return any(rec([f for f in es if v not in f], k - 1) for v in e)
    for k in range(0, len(verts) + 1):
        if rec(edges, k): return k
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def has_f7(edges):
    es = set(frozenset(e) for e in edges)
    for five in itertools.combinations(list(es), 5):
        U = sorted(set().union(*five))
        if len(U) != 7: continue
        for p in itertools.permutations(U):
            if all(frozenset((p[a], p[b], p[c])) in es for a, b, c in F7): return True
    return False
def linear(edges): return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(edges, 2))
def p3(edges, verts):
    verts = list(verts)
    for k in range(2, len(verts) + 1):
        pass
    vs = sorted(verts); pos = {v: i for i, v in enumerate(vs)}; ms = [sum(1 << pos[v] for v in e) for e in edges]
    for S in range(1 << len(vs)):
        c = bin(S).count('1')
        if c < 2: continue
        if sum(1 for m in ms if m & S == m) > c - 2: return False
    return True
