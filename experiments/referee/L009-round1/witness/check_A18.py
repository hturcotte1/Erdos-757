"""Referee L009: independent check of the witness A_18 (no e757, no judge).
(1) distinct integers; (2) every 4-subset has >= 5 distinct absolute differences; (3) number of 3-term APs;
(4) largest Sidon subset: (a) brute force over all 2^18 subsets (Sidon = all pairwise sums x+y, x<=y, distinct),
    (b) CP-SAT maximisation with one 'not all chosen' constraint per additive quadruple a+b=c+d."""
from itertools import combinations
from fractions import Fraction
A = [0,352,492,600,632,704,916,1200,1264,1388,1613,1696,1767,1838,2176,2476,4352,7440]
n = len(A); assert len(set(A)) == n == 18
bad = [Q for Q in combinations(A, 4) if len({abs(x - y) for x, y in combinations(Q, 2)}) < 5]
print('4-subsets:', len(list(combinations(A, 4))), 'with <5 distinct differences:', len(bad))
S = set(A)
aps = [(a, b, c) for a, b, c in combinations(sorted(A), 3) if a + c == 2 * b]
print('3-term APs:', len(aps))
def sidon(T):
    sums = set()
    for i in range(len(T)):
        for j in range(i, len(T)):
            s = T[i] + T[j]
            if s in sums: return False
            sums.add(s)
    return True
best = 0; cnt = {}
for mask in range(1 << n):
    k = bin(mask).count('1')
    if k <= best: continue
    T = [A[i] for i in range(n) if mask >> i & 1]
    if sidon(T): best = k
print('brute force max Sidon size:', best)
n11 = sum(1 for T in combinations(A, 11) if sidon(list(T))); n12 = sum(1 for T in combinations(A, 12) if sidon(list(T)))
print('Sidon 11-subsets:', n11, ' Sidon 12-subsets:', n12)
from ortools.sat.python import cp_model
md = cp_model.CpModel(); x = {a: md.NewBoolVar(str(a)) for a in A}
quads = set()
pairs = [(a, b) for i, a in enumerate(A) for b in A[i:]]
bys = {}
for a, b in pairs: bys.setdefault(a + b, []).append((a, b))
for s, L in bys.items():
    for (a, b), (c, d) in combinations(L, 2):
        md.AddBoolOr([x[v].Not() for v in {a, b, c, d}])
md.Maximize(sum(x.values())); sv = cp_model.CpSolver(); sv.parameters.num_workers = 1
st = sv.Solve(md); print('CP-SAT status', sv.StatusName(st), 'max Sidon', int(sv.ObjectiveValue()))
print('ratio h/n =', Fraction(best, n), ' 4/7 =', Fraction(4, 7), ' h/n < 4/7 ?', Fraction(best, n) < Fraction(4, 7))
