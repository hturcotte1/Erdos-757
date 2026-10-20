"""Referee L014 round 2: consistency of Theorem 2 (every 23-point (4,5)-set has h >= 14) with data: 23-point (4,5)-sets built from
data/small_records.json by generic gluing and by taking random 23-subsets of larger glued (4,5)-sets, plus the Fibonacci set
{F_3..F_25}.  Exact integers; h by CP-SAT on all additive-quadruple conflicts (own code)."""
import json, itertools, random
from collections import defaultdict
from ortools.sat.python import cp_model
R = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
S = {k: v['set'] for k, v in R.items()}
def is45(A):
    for q in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: return False
    return True
def h(A):
    A = sorted(A); n = len(A); sums = defaultdict(list)
    for i in range(n):
        for j in range(i, n): sums[A[i] + A[j]].append((i, j))
    conf = set()
    for L in sums.values():
        for p, q in itertools.combinations(L, 2): conf.add(frozenset(p) | frozenset(q))
    md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(n)]
    for c in conf: md.Add(sum(x[i] for i in c) <= len(c) - 1)
    md.Maximize(sum(x)); s = cp_model.CpSolver(); s.parameters.num_workers = 1; st = s.Solve(md)
    assert s.StatusName(st) == 'OPTIMAL'
    return int(s.ObjectiveValue()), sum(1 for c in conf if len(c) == 3)
def glue(A, B, q, t): return sorted(set(A) | {t + q * b for b in B})
rng = random.Random(23)
tests = []
F = [1, 2]
while len(F) < 26: F.append(F[-1] + F[-2])
fib = F[1:24]   # F_3 .. F_25 = 2, 3, 5, ...
tests.append(('Fibonacci F3..F25', fib))
tests.append(('C23 = B12 u B11', glue(S['12'], S['11'], 7919, 10**9)))
tests.append(('B12b u B11', glue(S['12b'], S['11'], 7919, 10**9)))
tests.append(('B12c u B11', glue(S['12c'], S['11'], 7919, 10**9)))
big = [('A_base u A_base', glue(S['14'], S['14'], 7919, 10**9)), ('A_base u B12', glue(S['14'], S['12'], 7919, 10**9)),
       ('B12 u B12b', glue(S['12'], S['12b'], 7919, 10**9)), ('A_base u B10', glue(S['14'], S['10'], 7919, 10**9))]
for name, A in big:
    for r in range(25):
        if len(A) >= 23: tests.append(('random 23-subset of ' + name, sorted(rng.sample(A, 23))))
viol = 0; minh = 99; done = 0
for name, A in tests:
    assert len(A) == 23 and len(set(A)) == 23
    if not is45(A): print('not a (4,5)-set:', name); continue
    hv, m = h(A); done += 1; minh = min(minh, hv)
    if hv < 14: viol += 1; print('VIOLATION', name, A, hv)
print('23-point (4,5)-sets tested %d; min h = %d; violations of h >= 14: %d' % (done, minh, viol))
