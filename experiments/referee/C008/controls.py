"""Positive/negative controls for the referee's own code (refcheck.py)."""
import json, random, itertools, sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C008')
from refcheck import *

REPO = '/home/user/Erdos-757'
d = json.load(open(REPO + '/data/small_records.json'))['sets']
print('-- record sets from data/small_records.json')
for k, v in d.items():
    A = parse(v['set'])
    E = aps(A)
    h1, h2 = h_numpy(A), h_cpsat(A)
    t = tau_bf(len(A), E)
    print(k, 'n', len(A), 'is45', is45_bf(A), 'weakS', weak_sidon(A), 'lin', linear(E), 'm', len(E),
          '(expect', v['m'], ') h_np', h1, 'h_cp', h2, '(expect', v['h'], ') tau', t, 'n-tau', len(A) - t,
          'F7homs', f7_homs(len(A), E), 'F7sub', f7_subsets(E))
print('-- (4,5) negative / boundary controls')
for S in ([1, 2, 3, 5], [0, 1, 2, 4], [0, 1, 3, 4], [1, 2, 3, 6], [0, 1, 2, 3]):
    print(S, 'is45', is45_bf(S), 'weakSidon', weak_sidon(S), 'linear', linear(aps(S)), 'h_np', h_numpy(S), 'h_cp', h_cpsat(S))
print('-- Fibonacci {2,3,5,8,...}: (4,5)?, h by numpy vs CP-SAT')
fib = [2, 3]
while len(fib) < 18:
    fib.append(fib[-1] + fib[-2])
for L in (5, 8, 10, 12, 15, 18):
    A = fib[:L]
    print(L, 'is45', is45_bf(A), 'h_np', h_numpy(A), 'h_cp', h_cpsat(A))
print('-- F7 detector controls (abstract hypergraphs)')
print('F7 itself: homs (=|Aut F7|)', f7_homs(7, F7), 'subsets', f7_subsets(F7))
# AG(2,3): points (x,y) in Z3^2, 12 lines
pts = [(x, y) for x in range(3) for y in range(3)]
pid = {p: i for i, p in enumerate(pts)}
lines = set()
for p, q in itertools.combinations(pts, 2):
    r = ((-p[0] - q[0]) % 3, (-p[1] - q[1]) % 3)
    lines.add(tuple(sorted((pid[p], pid[q], pid[r]))))
lines = sorted(lines)
print('AG(2,3): lines', len(lines), 'homs', f7_homs(9, lines), 'F7 subsets', f7_subsets(lines))
# relabelled F7 plus noise edges inside a larger vertex set
random.seed(7)
perm = random.sample(range(15), 15)
E = [tuple(perm[v] for v in e) for e in F7] + [(7, 8, 9), (10, 11, 12)]
E = [tuple(sorted((perm[a], perm[b], perm[c]))) if False else e for e in E for a, b, c in [e]]
print('relabelled F7 + 2 extra edges on 15 vertices: homs', f7_homs(15, E), 'subsets', f7_subsets(E))
# F7 minus an edge: must be 0
print('F7 minus one edge: homs', f7_homs(7, F7[:-1]), 'subsets', f7_subsets(F7[:-1]))
