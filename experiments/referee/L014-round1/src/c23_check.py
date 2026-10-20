"""Referee L014 r1: own exact check of the explicit set C23 (no e757, no judge code).
(1) C23 == B12 u (10^9 + 7919*B11) with B12 the third 12-point record (START_HERE s.6) and B11 = data/small_records.json['11'];
(2) 23 distinct integers; every 4-subset has >= 5 distinct absolute differences;
(3) largest Sidon subset by (a) exhaustive search over all 15-subsets (none Sidon, definition: all pairwise sums x+y, x<=y,
    distinct) and an explicit Sidon 14-subset; (b) CP-SAT on the full sum-relation structure (all a+b=c+d, {a,b}!={c,d},
    a<=b, c<=d), maximize |S|.  Exact integers throughout."""
import itertools, json, sys
from fractions import Fraction
B12 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]
B11 = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']['11']['set']
C23 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575, 1000000000, 16909350190, 23979971882, 27868723536, 28399336131,
       30343711958, 30696250000, 31050593574, 31757475190, 32818700380, 60392500000]
glued = sorted(B12 + [10**9 + 7919 * b for b in B11])
print('B11 =', B11, 'len', len(B11)); print('C23 equals B12 u (10^9+7919*B11):', glued == sorted(C23))
A = sorted(C23); n = len(A); print('n =', n, 'distinct:', len(set(A)) == n, 'all int:', all(isinstance(x, int) for x in A))
bad = 0; cnt = 0
for q in itertools.combinations(A, 4):
    cnt += 1
    if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: bad += 1
print('4-subsets checked', cnt, 'with < 5 distinct differences:', bad)
def sidon(S):
    s = [x + y for i, x in enumerate(S) for y in S[i:]]
    return len(s) == len(set(s))
# also check the two pieces
for nm, X in (('B12', B12), ('B11', B11)):
    Xs = sorted(X); best = 0
    for k in range(len(Xs), 0, -1):
        if any(sidon(list(c)) for c in itertools.combinations(Xs, k)): best = k; break
    b45 = all(len({abs(x - y) for x, y in itertools.combinations(q, 2)}) >= 5 for q in itertools.combinations(Xs, 4))
    print(nm, 'n', len(Xs), '(4,5):', b45, 'h (brute force) =', best)
# exhaustive: is any 15-subset Sidon?
c15 = 0; s15 = 0
for c in itertools.combinations(A, 15):
    c15 += 1
    if sidon(c): s15 += 1
print('15-subsets', c15, 'Sidon among them', s15)
s14 = None; c14 = 0
for c in itertools.combinations(A, 14):
    c14 += 1
    if sidon(c): s14 = c; break
print('first Sidon 14-subset', s14, 'after', c14, 'candidates; Sidon re-check:', sidon(list(s14)))
# CP-SAT on sum relations
from ortools.sat.python import cp_model
rel = {}
for i in range(n):
    for j in range(i, n):
        rel.setdefault(A[i] + A[j], []).append((i, j))
md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(n)]; ncons = 0
for s, prs in rel.items():
    for p, q in itertools.combinations(prs, 2):
        vs = sorted(set(p) | set(q)); md.Add(sum(x[v] for v in vs) <= len(vs) - 1); ncons += 1
md.Maximize(sum(x)); sol = cp_model.CpSolver(); sol.parameters.num_workers = 1; st = sol.Solve(md)
S = [A[i] for i in range(n) if sol.Value(x[i])]
print('CP-SAT status', sol.StatusName(st), 'sum relations', ncons, 'max Sidon size', int(sol.ObjectiveValue()), 'bound', int(sol.BestObjectiveBound()), 'subset Sidon:', sidon(S))
# 3-term APs and ratio
aps = [(a, b, c) for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b]
print('3-term APs', len(aps), ' h/n = %s vs 4/7 = %s: h/n > 4/7: %s' % (Fraction(14, 23), Fraction(4, 7), Fraction(14, 23) > Fraction(4, 7)))
