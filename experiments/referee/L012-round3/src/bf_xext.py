"""Referee L012 round 3: brute-force validation of xext on small inputs.
For G (n vertices, edge list), d, EP, T: enumerate ALL d-sets of pairwise disjoint admissible pairs (not inside an edge, both of
degree <= EP), build H = G + {w,a,b}, compute tau(H) by brute force, keep tau(H) >= T; then apply the same filters as xext
(F7 centre test, P3 brute force) and report (hits, contain_F7, F7free_P3_violated, survivors).  Compare with xext's SUMMARY.
Usage: python3 bf_xext.py NG T d EP < inputs (one or more lines "m a b c ...")"""
import sys, subprocess
from itertools import combinations
NG, T, d, EP = map(int, sys.argv[1:5])
def tau(n, masks):
    for k in range(0, n + 1):
        for S in combinations(range(n), k):
            sm = sum(1 << v for v in S)
            if all(mk & sm for mk in masks): return k
def has_f7(edges):
    es = set(frozenset(e) for e in edges); verts = set(v for e in edges for v in e)
    for p in verts:
        at = [e for e in edges if p in e]
        if len(at) < 3: continue
        for tr in combinations(at, 3):
            prs = [tuple(v for v in e if v != p) for e in tr]
            for s2 in (0, 1):
                for s3 in (0, 1):
                    t1 = frozenset([prs[0][0], prs[1][s2], prs[2][s3]]); t2 = frozenset([prs[0][1], prs[1][1 - s2], prs[2][1 - s3]])
                    if t1 in es and t2 in es: return True
    return False
def p3_ok(edges):
    for k in range(1, len(edges) + 1):
        for F in combinations(edges, k):
            if len(set(v for e in F for v in e)) < k + 2: return False
    return True
lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
tot = dict(hits=0, contain_F7=0, F7free_P3_violated=0, survivors=0)
for l in lines:
    a = list(map(int, l.split())); m = a[0]; edges = [tuple(a[1 + 3 * i:4 + 3 * i]) for i in range(m)]
    deg = [0] * NG
    for e in edges:
        for v in e: deg[v] += 1
    inedge = set(frozenset(p) for e in edges for p in combinations(e, 2))
    pairs = [(x, y) for x in range(NG) for y in range(x + 1, NG) if deg[x] <= EP and deg[y] <= EP and frozenset((x, y)) not in inedge]
    for S in combinations(pairs, d):
        vs = [v for p in S for v in p]
        if len(set(vs)) < 2 * d: continue
        H = edges + [(NG, x, y) for (x, y) in S]
        masks = [sum(1 << v for v in e) for e in H]
        if tau(NG + 1, masks) < T: continue
        tot['hits'] += 1
        if has_f7(H): tot['contain_F7'] += 1; continue
        if not p3_ok(H): tot['F7free_P3_violated'] += 1; continue
        tot['survivors'] += 1
print('BF', ' '.join('%s=%d' % kv for kv in tot.items()))
