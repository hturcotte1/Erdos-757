"""(L012) Brute-force reference for ext_d: for each input G on NG vertices, every d-set of pairwise disjoint admissible pairs
({a,b} not inside an edge of G, G-degrees <= EP), H = G + {NG,a,b}; tau(H) by brute force over vertex subsets; prints HIT lines for
tau(H) >= T.  Usage: bf_ext.py NG T d EP < input"""
import sys, itertools
NG, T, d, EP = map(int, sys.argv[1:5])
def tau_ge(es, nv, t):   # True iff no (t-1)-subset of the nv vertices meets every edge
    if t <= 0: return True
    sets = [frozenset(e) for e in es]
    for k in range(t):
        for S in itertools.combinations(range(nv), k):
            s = set(S)
            if all(s & e for e in sets): return False
    return True
cnt = 0
for line in sys.stdin:
    t = list(map(int, line.split()));
    if not t: continue
    m = t[0]; es = [tuple(t[1 + 3 * i: 4 + 3 * i]) for i in range(m)]
    deg = [sum(v in e for e in es) for v in range(NG)]
    pairs = [(a, b) for a in range(NG) for b in range(a + 1, NG) if deg[a] <= EP and deg[b] <= EP and not any(a in e and b in e for e in es)]
    for S in itertools.combinations(pairs, d):
        if len({v for p in S for v in p}) != 2 * d: continue
        H = es + [(a, b, NG) for a, b in S]
        if tau_ge(H, NG + 1, T):
            cnt += 1; print('HIT: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in H))
print('SUMMARY bf hits', cnt)
