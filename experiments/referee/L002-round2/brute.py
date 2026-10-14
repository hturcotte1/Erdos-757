"""Referee round 2: plain brute force over ordered midpoint patterns for small n (validation of enum.c).
For each interior j choose None or (i,k), i<j<k. Keep linear + K30 (pairwise, from the definition).
alpha by exhaustive subset scan; F7 by explicit isomorphism test (all bijections onto F7's vertex set).
Prints counts[(m, T_alpha_max, f7flag)] as 'alpha<=T' counts for every T."""
import sys, itertools
from collections import Counter

F7 = [frozenset(e) for e in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]]
F7set = set(F7)

def contains_f7(edges):
    E = [frozenset(e) for e in edges]
    Eset = set(E)
    for five in itertools.combinations(E, 5):
        verts = sorted(set().union(*five))
        if len(verts) != 7:
            continue
        fs = set(five)
        for perm in itertools.permutations(range(7)):
            mp = dict(zip(verts, perm))
            if all(frozenset(mp[v] for v in e) in F7set for e in five):
                return True
    return False

def alpha(n, edges):
    masks = [(1 << a) | (1 << b) | (1 << c) for a, b, c in edges]
    best = 0
    for S in range(1 << n):
        pc = bin(S).count("1")
        if pc <= best:
            continue
        if all((S & e) != e for e in masks):
            best = pc
    return best

def run(n):
    cnt = Counter()
    edges = []
    def ok_new(i, j, k):
        for (a, b, c) in edges:
            s = {a, b, c}
            if len(s & {i, j, k}) >= 2:
                return False
            # K30 both directions (from the definition): if a<=i, c<=k, (a,c)!=(i,k) then b<j ; and symmetric
            if a <= i and c <= k and (a, c) != (i, k) and not (b < j):
                return False
            if i <= a and k <= c and (a, c) != (i, k) and not (j < b):
                return False
        return True
    def rec(j):
        if j == n - 1:
            a = alpha(n, edges)
            f = contains_f7(edges) if len(edges) >= 5 else False
            cnt[(len(edges), a, int(f))] += 1
            return
        rec(j + 1)  # none
        for i in range(j):
            for k in range(j + 1, n):
                if ok_new(i, j, k):
                    edges.append((i, j, k))
                    rec(j + 1)
                    edges.pop()
    rec(1)
    return cnt

if __name__ == "__main__":
    n = int(sys.argv[1])
    cnt = run(n)
    # cumulative: number with alpha <= T for each (m, T, f7)
    ms = sorted(set(k[0] for k in cnt))
    for m in ms:
        for T in range(1, n + 1):
            f0 = sum(v for (mm, a, f), v in cnt.items() if mm == m and a <= T and f == 0)
            f1 = sum(v for (mm, a, f), v in cnt.items() if mm == m and a <= T and f == 1)
            if f0 or f1:
                print(f"n={n} m={m} T={T} f7free={f0} f7={f1}")
