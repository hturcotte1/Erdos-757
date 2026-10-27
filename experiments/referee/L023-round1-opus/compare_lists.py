"""Referee L023 round 1: compare my recomputed cell lists (CELLDIR given) with (U1)'s stored lists, as sets of FOUND lines
(canonical forms), plus SHA-256 of the sorted FOUND lines. usage: compare_lists.py MYCELLDIR key1 key2 ..."""
import sys, os, hashlib
U1 = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
mine = sys.argv[1]; allok = True
for k in sys.argv[2:]:
    n, m, t, D = map(int, k.split(','))
    name = 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D)
    def found(p):
        if not os.path.exists(p): return None, False
        L = open(p).read().splitlines()
        return set(l.strip() for l in L if l.startswith('FOUND:')), any(l.startswith('INFO ') for l in L)
    a, ia = found(os.path.join(mine, name)); b, ib = found(os.path.join(U1, name))
    if a is None or not ia: print(k, 'MINE MISSING/INCOMPLETE'); allok = False; continue
    h = lambda S: hashlib.sha256('\n'.join(sorted(S)).encode()).hexdigest()[:16]
    eq = a == b
    print('(%s) mine %d classes (sha256 sorted %s) | U1 %d classes (%s) | %s' % (k, len(a), h(a), len(b), h(b), 'EQUAL' if eq else 'DIFFERENT: only mine %d, only U1 %d' % (len(a - b), len(b - a))))
    allok &= eq
print('SUMMARY', 'ALL EQUAL' if allok else 'NOT ALL EQUAL')
