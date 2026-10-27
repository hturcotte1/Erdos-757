"""Numerical test of the E1-hub identities used in L024 4.5-4.6 (they hold for every 3-graph G'):
tau(G' + hub(a,b,c)) = tau(G') + 2 if no minimum transversal of G' contains two of a,b,c, and tau(G') + 1 otherwise;
and {a,b,c} in E(G') makes the hub contain F7.  Random G' plus the stored small cells."""
import random, sys, glob
from itertools import combinations
from rlib import min_transversals, tau_bb, has_F7, load_cell

random.seed(5)
ok = bad = 0; f7ok = 0; n_b = 0
inst = []
for it in range(1500):
    n = random.randint(4, 11)
    m = random.randint(1, n)
    E = set()
    while len(E) < m:
        E.add(tuple(sorted(random.sample(range(n), 3))))
    inst.append((n, sorted(E)))
for fn in sorted(glob.glob('/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_*.txt')):
    L = load_cell(fn)
    if L and L[0][0] <= 15:
        for (n, m, t, E) in L[:40]:
            inst.append((n, E))
for (n, E) in inst:
    t, mts = min_transversals(n, E)
    for _ in range(3):
        a, b, c = random.sample(range(n), 3)
        v, x, y, z = n, n + 1, n + 2, n + 3
        EH = list(E) + [(x, y, z), tuple(sorted((v, x, a))), tuple(sorted((v, y, b))), tuple(sorted((v, z, c)))]
        tH = tau_bb(n + 4, EH)
        two = any(bin(T & ((1 << a) | (1 << b) | (1 << c))).count('1') >= 2 for T in mts)
        pred = t + 1 if two else t + 2
        n_b += (not two)
        if tH == pred:
            ok += 1
        else:
            bad += 1
            print('MISMATCH', n, E, a, b, c, t, tH)
        if tuple(sorted((a, b, c))) in set(E):
            f7ok += has_F7(n + 4, EH)
print('hub identity tests', ok + bad, 'mismatches', bad, 'b-config cases', n_b)
# F7 claim: hub over an edge {a,b,c}
cnt = 0; hit = 0
for (n, E) in inst[:500]:
    for e in E[:2]:
        a, b, c = e
        v, x, y, z = n, n + 1, n + 2, n + 3
        EH = list(E) + [(x, y, z), tuple(sorted((v, x, a))), tuple(sorted((v, y, b))), tuple(sorted((v, z, c)))]
        cnt += 1; hit += has_F7(n + 4, EH)
print('hub over an existing edge: F7 present in', hit, 'of', cnt)
