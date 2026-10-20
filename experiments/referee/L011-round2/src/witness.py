"""Referee L011 r2: the witness C22 = B12 u (5000 + 15*B10) from the definitions (own code, exact integers).
(4,5): every 4-subset has >= 5 distinct absolute differences.  Sidon number h: (a) brute force (no Sidon 14-subset among all
C(22,14); a Sidon 13-subset exists; Sidon checked as 'all positive differences distinct'); (b) CP-SAT on the conflict structure
(every relation a+b=c+d with {a,b} != {c,d}, a=b or c=d allowed, forbids selecting all elements involved)."""
import json, itertools, sys
from fractions import Fraction
recs = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
B12, B10 = recs['12']['set'], recs['10']['set']
C = sorted(B12 + [5000 + 15 * b for b in B10])
stated = [0,269,385,467,501,511,521,523,535,538,549,575,5000,5750,6095,6200,6305,6440,6500,6680,6905,7610]
print('C22 equals the stated set:', C == stated, '| n =', len(C), '| distinct:', len(set(C)) == len(C))
bad4 = sum(1 for Q in itertools.combinations(C, 4) if len({abs(a - b) for a, b in itertools.combinations(Q, 2)}) < 5)
print('4-subsets:', sum(1 for _ in itertools.combinations(C, 4)), 'with < 5 distinct differences:', bad4)
def sidon(S):
    d = [b - a for a, b in itertools.combinations(sorted(S), 2)]
    return len(d) == len(set(d))
n14 = sum(1 for S in itertools.combinations(C, 14) if sidon(S))
n13 = [S for S in itertools.combinations(C, 13) if sidon(S)]
print('Sidon 14-subsets:', n14, '| Sidon 13-subsets:', len(n13))
claimed = [0,269,385,467,511,521,523,5000,5750,6095,6200,6680,6905]
print('proof\'s 13-subset is Sidon and inside C:', sidon(claimed) and set(claimed) <= set(C))
# 3-term APs
aps = [(a, b, c) for a, b, c in itertools.combinations(C, 3) if a + c == 2 * b]
print('3-term APs:', len(aps), '| distinct midpoints:', len({b for _, b, _ in aps}))
# CP-SAT
from ortools.sat.python import cp_model
idx = {v: i for i, v in enumerate(C)}; M = cp_model.CpModel(); x = [M.NewBoolVar('x%d' % i) for i in range(len(C))]
conf = set()
sums = {}
for i in range(len(C)):
    for j in range(i, len(C)): sums.setdefault(C[i] + C[j], []).append((i, j))
for s, prs in sums.items():
    for (a, b), (c, d) in itertools.combinations(prs, 2): conf.add(frozenset((a, b, c, d)))
for K in conf: M.AddBoolOr([x[i].Not() for i in K])
M.Maximize(sum(x)); sol = cp_model.CpSolver(); sol.parameters.num_workers = 1; st = sol.Solve(M)
best = [C[i] for i in range(len(C)) if sol.Value(x[i])]
print('CP-SAT:', sol.StatusName(st), 'h =', int(sol.ObjectiveValue()), '| conflicts:', len(conf), '| sizes', sorted({len(K) for K in conf}), '| optimum Sidon:', sidon(best))
h = int(sol.ObjectiveValue())
print('h/n =', Fraction(h, len(C)), '>= 4/7:', Fraction(h, len(C)) >= Fraction(4, 7))
