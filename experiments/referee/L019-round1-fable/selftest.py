"""Self-test of ref.py against brute force / CP-SAT / known graphs."""
import random, itertools, sys
from ref import *

F7 = [frozenset(e) for e in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]]
fano = [frozenset(e) for e in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
grid = [frozenset(e) for e in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]]
print('F7: linear', is_linear(F7), 'copies', len(f7_copies(F7)), 'p3', p3_brute(range(7), F7)[0], 'tau', tau(F7), 'slack', slack(7, F7))
print('Fano: copies of F7', len(f7_copies(fano)), '(expected 7*... = 21 = choose 2 disjoint lines? Fano has no disjoint lines -> 0)')
print('grid: in_C', in_C(range(9), grid), 'tau', tau(grid))
# relabelled F7 plus pendant
rel = [frozenset(e) for e in [(6,5,4),(6,3,2),(6,1,0),(5,3,1),(4,2,0),(0,7,8)]]
print('relabelled F7 + pendant: has_f7', has_f7(rel))
# F7 brute-force check: count copies by testing all 7-subsets x 5-edge subsets isomorphism, on random linear graphs
def f7_brute(E):
    """count F7 copies by brute force: every 5-subset of edges spanning 7 vertices, isomorphism via degree-3 centre."""
    res = set()
    for five in itertools.combinations(E, 5):
        Vs = set().union(*five)
        if len(Vs) != 7: continue
        d = degrees(Vs, five)
        centres = [v for v in Vs if d[v] == 3]
        if len(centres) != 1 or any(d[v] != 2 for v in Vs if v != centres[0]): continue
        c = centres[0]
        at_c = [e for e in five if c in e]
        others = [e for e in five if c not in e]
        if len(others) != 2 or (others[0] & others[1]): continue
        # each other edge meets each edge at c exactly once
        if all(len(o & e) == 1 for o in others for e in at_c):
            res.add(frozenset(five))
    return res
rng = random.Random(7)
mism = 0; tot = 0; withf7 = 0
for _ in range(400):
    n = rng.randint(7, 11); m = rng.randint(4, 12)
    E = random_linear(n, m, rng)
    a = f7_copies(E); b = f7_brute(E)
    tot += 1; withf7 += (len(b) > 0)
    if a != b: mism += 1
print('F7 detector vs brute force on', tot, 'random linear graphs:', mism, 'mismatches;', withf7, 'graphs with an F7')
# P3 brute vs Hall
mism = 0; tot = 0; fails = 0
for _ in range(400):
    n = rng.randint(5, 12); m = rng.randint(2, n)
    E = random_linear(n, m, rng)
    a = p3_brute(range(n), E)[0]; b = p3_hall(range(n), E)
    tot += 1; fails += (not a)
    if a != b: mism += 1
print('P3 brute vs Hall on', tot, 'random linear graphs:', mism, 'mismatches;', fails, 'P3 failures')
# tau: branch&bound vs brute force vs CP-SAT; all min transversals vs brute force
mism = 0; mism2 = 0; tot = 0
for _ in range(150):
    n = rng.randint(5, 11); m = rng.randint(2, n + 2)
    E = random_linear(n, m, rng)
    t = tau(E)
    tb = min(k for k in range(0, n + 1) if any(all(e & set(T) for e in E) for T in itertools.combinations(range(n), k)))
    tc = tau_cpsat(E, range(n))
    if not (t == tb == tc): mism += 1
    _, Ts = all_min_transversals(E, t)
    if Ts != all_min_transversals_brute(range(n), E, t): mism2 += 1
    tot += 1
print('tau B&B vs brute vs CP-SAT on', tot, 'graphs:', mism, 'mismatches; all-min-transversal enumeration mismatches:', mism2)
# stored lists: check stored (n,m,tau) and membership in C and I11 for all classes of the small cells
D = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
for c in ['3_1_1', '6_3_2', '8_5_3', '9_4_3', '10_7_4', '10_8_4', '14_12_6', '17_13_7', '15_11_6', '13_9_5', '16_10_6', '12_10_5']:
    bad = 0; badC = 0; neg = 0
    cells = read_cell(D + 'cell_%s.txt' % c)
    for (n, m, t, E) in cells:
        if len(E) != m or tau(E) != t: bad += 1
        if not in_C(range(n), E): badC += 1
        if 3 * n + 2 * m - 11 * t < 0: neg += 1
    print('cell', c, len(cells), 'classes: tau mismatches', bad, 'not in C', badC, 'negative slack', neg)
