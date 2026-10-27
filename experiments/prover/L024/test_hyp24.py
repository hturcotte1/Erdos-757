"""L024: self-tests of hyp24.py against brute force on random small 3-graphs and on the 32 pieces.
Run: timeout 900 nice -n 10 python3 test_hyp24.py > test_hyp24_output.txt"""
import random, itertools, sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
from hyp24 import *
random.seed(24)
bad = 0; cnt = 0; inc3 = 0
for trial in range(3000):
    n = random.randint(4, 11)
    m = random.randint(1, n)
    E = set()
    while len(E) < m:
        E.add(tuple(sorted(random.sample(range(n), 3))))
    E = list(E)
    a = p3_ok(n, E); b = p3_ok_slow(n, E); c = p3_brute(n, E)
    cnt += 1
    if not (a == b == c): bad += 1; print('P3 MISMATCH', n, E, a, b, c)
    # tau vs brute force
    t = tau(n, E)
    em = emasks(E)
    tb = min(k for k in range(n + 1) if any(all(e & sum(1 << x for x in T) for e in em) for T in itertools.combinations(range(n), k)))
    if t != tb: bad += 1; print('TAU MISMATCH', n, E, t, tb)
    mts = min_transversals(n, E, t)
    mb = sorted(sum(1 << x for x in T) for T in itertools.combinations(range(n), t) if all(e & sum(1 << x for x in T) for e in em))
    if sorted(mts) != mb: bad += 1; print('MT MISMATCH', n, E)
    # F7 vs brute force over 7-subsets of edges... check by subsets of 5 edges
    f7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
    def has_f7():
        for S in itertools.combinations(E, 5):
            V = sorted(set(x for e in S for x in e))
            if len(V) != 7: continue
            Ss = set(S)
            for perm in itertools.permutations(V):
                if all(tuple(sorted(perm[x] for x in e)) in Ss for e in f7): return True
        return False
    if m >= 5 and n >= 7 and trial % 10 == 0:
        if f7_free(n, E) == has_f7(): bad += 1; print('F7 MISMATCH', n, E)
print('random tests', cnt, 'mismatches', bad)
# F7 itself
print('F7 detected:', not f7_free(7, [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]))
pieces = load_pieces()
print('pieces in C_3:', sum(1 for P in pieces if in_C3(P['n'], P['edges'])), 'of', len(pieces))
print('pieces with Delta <= 2:', [P['name'] for P in pieces if max(P['deg']) <= 2])
