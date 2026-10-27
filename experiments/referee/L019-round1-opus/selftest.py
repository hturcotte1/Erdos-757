"""Self-tests of refhg.py: tau_bb vs brute force, P3 table vs Hall/flow, F7 search on known graphs, stored-list headers."""
import random, sys, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import *

rng = random.Random(20261027)


def random_linear(n, m):
    E = []; used = set()
    for _ in range(4000):
        if len(E) >= m:
            break
        g = tuple(sorted(rng.sample(range(n), 3)))
        ps = list(itertools.combinations(g, 2))
        if any(p in used for p in ps):
            continue
        used.update(ps); E.append(g)
    return E


def random_3graph(n, m):
    E = set()
    while len(E) < m:
        E.add(tuple(sorted(rng.sample(range(n), 3))))
    return sorted(E)


bad = 0
for trial in range(400):
    n = rng.randint(4, 11)
    m = rng.randint(1, 2 * n)
    E = random_linear(n, m) if trial % 2 else random_3graph(n, min(m, n * (n - 1) * (n - 2) // 6))
    if tau_bb(E) != tau_brute(n, E):
        bad += 1; print('TAU MISMATCH', n, E)
    V = sorted(set(x for g in E for x in g))
    lab = {u: i for i, u in enumerate(V)}
    E2 = [tuple(lab[u] for u in g) for g in E]
    if p3_ok_table(len(V), E2) != p3_ok_flow(E2):
        bad += 1; print('P3 MISMATCH', E2)
print('tau / P3 random cross-checks done, mismatches:', bad)

F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
fano = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
grid = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8)]
print('F7 copies in F7:', len(f7_copies(F7)), 'tau', tau_bb(F7), 'slack', slack(7, F7), 'P3', p3_ok_table(7, F7), p3_ok_flow(F7))
print('F7 copies in Fano:', len(f7_copies(fano)), 'P3 Fano', p3_ok_table(7, fano), p3_ok_flow(fano))
print('grid in C:', in_C(9, grid), 'tau', tau_bb(grid))
# relabelled F7 plus pendant edge
F7r = [(6, 5, 4), (6, 3, 2), (6, 1, 0), (5, 3, 1), (4, 2, 0), (0, 7, 8)]
print('relabelled F7 + pendant: copies', len(f7_copies(F7r)))

# stored lists: headers and membership in C
D = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs'
tot = 0; badh = 0; notC = 0
for path in sorted(glob.glob(D + '/cell_*.txt')):
    cells = read_cell(path, 25)
    for (n, m, t, E) in cells:
        tot += 1
        if len(E) != m or tau_bb(E) != t or max(x for g in E for x in g) >= n:
            badh += 1; print('HEADER MISMATCH', path, n, m, t)
        if not in_C(n, E, use_table=(n <= 20)):
            notC += 1; print('NOT IN C', path, E)
print('stored lists (first 25 per cell):', tot, 'graphs; header mismatches', badh, '; not in C', notC)
