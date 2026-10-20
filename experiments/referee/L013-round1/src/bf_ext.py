"""Brute force for validating myext: all d-sets of pairwise disjoint pairs {a,b} (not inside an edge, deg <= d-1), tau(X) by
exhaustive subset search; prints the sets with tau(X) >= t, one per line 'SET: line=i a-b ...' (sorted)."""
import sys, itertools
NG, T, d = map(int, sys.argv[1:4])
def tau(nv, es):
    em = [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in es]
    for k in range(0, len(es) + 1):
        for S in itertools.combinations(range(nv), k):
            s = 0
            for v in S: s |= 1 << v
            if all(s & e for e in em): return k
for li, l in enumerate(sys.stdin, 1):
    a = list(map(int, l.split()))
    if not a: continue
    k = a[0]; es = [tuple(a[1 + 3 * i: 4 + 3 * i]) for i in range(k)]
    deg = [0] * NG
    for e in es:
        for v in e: deg[v] += 1
    if tau(NG, es) != T - 1: print('BADTAU line', li); continue
    pairs = [(x, y) for x in range(NG) for y in range(x + 1, NG) if deg[x] <= d - 1 and deg[y] <= d - 1 and not any(x in e and y in e for e in es)]
    for P in itertools.combinations(pairs, d):
        vs = [v for p in P for v in p]
        if len(set(vs)) < 2 * d: continue
        X = es + [(NG, x, y) for (x, y) in P]
        if tau(NG + 1, X) >= T:
            print('SET: line=%d ' % li + ' '.join('%d-%d' % p for p in sorted(P)))
