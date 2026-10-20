"""Referee L009 round 3: independent check of A_18 (no e757, no judge). Exact integers.
(4,5)-set: every 4-subset has >= 5 distinct absolute differences. Sidon: all sums x+y (x<=y) distinct.
h(A): brute force over subsets by DFS (definitional Sidon test), and CP-SAT maximum 3-AP-free subset as a cross-check."""
import itertools
A = [0,352,492,600,632,704,916,1200,1264,1388,1613,1696,1767,1838,2176,2476,4352,7440]
n = len(A); assert len(set(A)) == n
bad = 0
for Q in itertools.combinations(A, 4):
    if len({abs(x - y) for x, y in itertools.combinations(Q, 2)}) < 5: bad += 1
print("n =", n, "; 4-subsets with < 5 distinct differences:", bad, "of", len(list(itertools.combinations(range(n), 4))))
aps = [(i, j, k) for i, j, k in itertools.combinations(range(n), 3) if A[i] + A[k] == 2 * A[j]]
print("3-term APs (i<j<k with A[i]+A[k]=2A[j]):", len(aps))
# weak Sidon?
sums = [A[i] + A[j] for i, j in itertools.combinations(range(n), 2)]
print("weak Sidon (sums of distinct pairs distinct):", len(sums) == len(set(sums)))
# brute-force maximum Sidon subset by DFS with definitional test (x+y distinct for x<=y, i.e. including doubles)
best = [0]; count_best = [0]
def sidon_ok(S, x):
    ss = {2 * s for s in S} | {s + t for s, t in itertools.combinations(S, 2)}
    new = {x + s for s in S} | {2 * x}
    return len(new) == len(S) + 1 and not (ss & new)
def dfs(i, S):
    if len(S) + (n - i) < best[0]: return
    if i == n:
        if len(S) > best[0]: best[0] = len(S); count_best[0] = 1
        elif len(S) == best[0]: count_best[0] += 1
        return
    if sidon_ok(S, A[i]): dfs(i + 1, S + [A[i]])
    dfs(i + 1, S)
dfs(0, [])
print("largest Sidon subset (DFS, definitional):", best[0], "; number of maximum Sidon subsets:", count_best[0])
try:
    from ortools.sat.python import cp_model
    md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(n)]
    for i, j, k in aps: md.Add(x[i] + x[j] + x[k] <= 2)
    md.Maximize(sum(x)); sol = cp_model.CpSolver(); st = sol.Solve(md)
    print("CP-SAT max 3-AP-free subset:", sol.StatusName(st), int(sol.ObjectiveValue()))
except Exception as e: print("CP-SAT skipped:", e)
from fractions import Fraction
print("h/n =", Fraction(best[0], n), "; 4/7 =", Fraction(4, 7), "; h/n < 4/7 ?", Fraction(best[0], n) < Fraction(4, 7))
