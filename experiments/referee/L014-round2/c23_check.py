"""Referee L014 round 2: own exact check of the witness C23 (no e757 import, no prover code).
(1) C23 = B12 U (10^9 + 7919*B11) equals the 23 integers listed in the certificate;
(2) 23 distinct integers; every 4-subset has >= 5 distinct absolute differences;
(3) h(C23) = largest Sidon subset, by two methods different from e757.core.alpha:
    (a) the conflict family = all multisets {a,b},{c,d} with a+b=c+d, {a,b}!={c,d} (point sets of size 3 or 4);
        brute force: no 15-subset avoids all conflict sets, and some 14-subset does (exhaustive over all C(23,14), C(23,15));
    (b) OR-tools CP-SAT maximum with the same conflict sets (independently built by direct sum enumeration)."""
import itertools, json, sys
from collections import defaultdict
B12 = [0,269,385,467,501,511,521,523,535,538,549,575]
B11 = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']['11']['set']
C = sorted(B12 + [10**9 + 7919*b for b in B11])
listed = [0,269,385,467,501,511,521,523,535,538,549,575,1000000000,16909350190,23979971882,27868723536,28399336131,30343711958,30696250000,31050593574,31757475190,32818700380,60392500000]
print('B11', B11)
print('C23 equals the listed set:', C == sorted(listed), 'n =', len(C), 'distinct:', len(set(C)) == len(C))
bad = 0; cnt = 0
for q in itertools.combinations(C, 4):
    cnt += 1
    if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: bad += 1
print('4-subsets', cnt, 'with < 5 distinct differences', bad)
# conflict sets: all pairs of distinct multisets {a<=b},{c<=d} with equal sums
sums = defaultdict(list)
for i in range(len(C)):
    for j in range(i, len(C)):
        sums[C[i] + C[j]].append((i, j))
conf = set()
for s, L in sums.items():
    for (p, q) in itertools.combinations(L, 2):
        conf.add(frozenset(p) | frozenset(q))
conf = sorted(conf, key=lambda x: sorted(x))
print('conflict sets', len(conf), 'sizes', sorted(set(len(x) for x in conf)))
aps = [sorted(x) for x in conf if len(x) == 3]
print('3-point conflicts (3-APs)', len(aps), '4-point conflicts', sum(1 for x in conf if len(x) == 4))
masks = [sum(1 << v for v in x) for x in conf]
def sidon(mask): return all((mask & cm) != cm for cm in masks)
n = len(C)
best = None
for k in (14, 15):
    found = None; tot = 0
    for comb in itertools.combinations(range(n), k):
        tot += 1
        mk = 0
        for v in comb: mk |= 1 << v
        if sidon(mk): found = comb; break
    print('size', k, 'Sidon subset exists:', found is not None, '(searched %d subsets%s)' % (tot, '' if found is None else ', stopped at first'))
    if found is not None: best = found
S = [C[i] for i in best]
diffs = [b - a for a, b in itertools.combinations(sorted(S), 2)]
print('explicit Sidon 14-subset', S, 'all differences distinct:', len(diffs) == len(set(diffs)))
from ortools.sat.python import cp_model
md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(n)]
for c in conf: md.Add(sum(x[i] for i in c) <= len(c) - 1)
md.Maximize(sum(x)); sol = cp_model.CpSolver(); sol.parameters.num_workers = 1
st = sol.Solve(md)
print('CP-SAT status', sol.StatusName(st), 'max Sidon size', int(sol.ObjectiveValue()), 'bound', int(sol.BestObjectiveBound()))
