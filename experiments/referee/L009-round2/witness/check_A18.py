"""Referee L009 round 2: independent check of the witness A_18 (no e757, no judge).
(1) distinct integers; (2) every 4-subset has >= 5 distinct absolute differences; (3) 3-AP count;
(4) largest Sidon subset by two methods: (a) exhaustive over all 2^18 subsets with numpy, using the list of 'conflicts'
    (vertex sets {a,b,c,d} of size 3 or 4 with a+b=c+d, {a,b} != {c,d}; S is Sidon iff it contains no conflict);
    (b) CP-SAT ILP maximising |S| subject to 'not all of a conflict' constraints; plus the exact count of maximum Sidon subsets.
(5) the ratio test h/n vs 4/7 with Fractions; AP hypergraph tau = n - h and I11 slack."""
import itertools, sys
from fractions import Fraction
import numpy as np
A = [0,352,492,600,632,704,916,1200,1264,1388,1613,1696,1767,1838,2176,2476,4352,7440]
n = len(A); assert len(set(A)) == n == 18
nd = lambda q: len({abs(x - y) for x, y in itertools.combinations(q, 2)})
bad4 = [q for q in itertools.combinations(A, 4) if nd(q) < 5]
print("distinct:", len(set(A)) == n, "| 4-subsets:", len(list(itertools.combinations(A, 4))), "violating (<5 distinct differences):", len(bad4))
aps = [(a, b, c) for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b]
print("3-APs:", len(aps))
idx = {a: i for i, a in enumerate(A)}
sums = {}
for i in range(n):
    for j in range(i, n):
        sums.setdefault(A[i] + A[j], []).append((i, j))
conf = set()
for s, L in sums.items():
    for p, q in itertools.combinations(L, 2):
        conf.add(frozenset(p) | frozenset(q))
conf = sorted(conf, key=lambda c: sorted(c))
print("conflicts (sum collisions as vertex sets):", len(conf), "sizes:", sorted({len(c) for c in conf}))
# weak Sidon: no collision among sums of DISTINCT pairs
weak = all(not (len(set(p)) == 2 and len(set(q)) == 2) for s, L in sums.items() for p, q in itertools.combinations(L, 2))
print("weak Sidon (sums of distinct pairs distinct):", weak)
N = 1 << n
ok = np.ones(N, dtype=bool)
S = np.arange(N, dtype=np.int64)
for c in conf:
    cm = sum(1 << i for i in c)
    ok &= (S & cm) != cm
pc = np.array([bin(x).count('1') for x in range(N)], dtype=np.int64) if False else np.zeros(N, dtype=np.int64)
x = S.copy()
while True:
    pc += x & 1; x >>= 1
    if not x.any(): break
h = int(pc[ok].max()); cnt = int(((pc == h) & ok).sum())
print("exhaustive: largest Sidon subset size h =", h, "| number of maximum Sidon subsets:", cnt)
# definitional re-check of one maximum subset
best = int(S[(pc == h) & ok][0]); B = [A[i] for i in range(n) if best >> i & 1]
ss = [a + b for i, a in enumerate(B) for b in B[i:]]
print("one maximum Sidon subset:", B, "| Sidon by definition:", len(ss) == len(set(ss)))
from ortools.sat.python import cp_model
md = cp_model.CpModel(); xv = [md.NewBoolVar("x%d" % i) for i in range(n)]
for c in conf: md.Add(sum(xv[i] for i in c) <= len(c) - 1)
md.Maximize(sum(xv)); sol = cp_model.CpSolver(); sol.parameters.num_workers = 1; st = sol.Solve(md)
print("CP-SAT:", sol.StatusName(st), "objective", int(sol.ObjectiveValue()))
print("h/n =", Fraction(h, n), "< 4/7 ?", Fraction(h, n) < Fraction(4, 7), "| tau = n-h =", n - h, "| I11 slack 3n+2m-11tau =", 3*n + 2*len(aps) - 11*(n - h))
