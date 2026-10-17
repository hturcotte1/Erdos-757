"""Referee L010 r2: witness C20 from the definitions (integers only; no e757, no judge code).
(4,5): every 4 distinct points give >= 5 distinct absolute differences.  Sidon: all sums x+y (x<=y) distinct, and
(cross-check) all positive differences distinct.  h by exhaustive search over 12- and 13-subsets, and by CP-SAT on the
equal-sum conflicts.  Also: number of 3-APs (m), tau = n - h, I11 slack."""
import itertools, sys
A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
C = A_base + [5000, 5101, 5202] + [20000, 20103, 20206]
assert len(C) == 20 and len(set(C)) == 20
C = sorted(C); n = len(C)
bad4 = [Q for Q in itertools.combinations(C, 4) if len({abs(a - b) for a, b in itertools.combinations(Q, 2)}) < 5]
print('n', n, 'distinct', len(set(C)) == n, '4-subsets', sum(1 for _ in itertools.combinations(C, 4)), 'with <5 distances', len(bad4))
def sidon_sums(S):
    s = [a + b for i, a in enumerate(S) for b in S[i:]]; return len(s) == len(set(s))
def sidon_diffs(S):
    d = [b - a for a, b in itertools.combinations(sorted(S), 2)]; return len(d) == len(set(d))
cnt = {}
for k in (11, 12, 13):
    c = 0; disagree = 0
    for S in itertools.combinations(C, k):
        x = sidon_sums(S); y = sidon_diffs(S); disagree += (x != y); c += x
    cnt[k] = c; print('Sidon %d-subsets: %d (sum/diff definitions disagree on %d)' % (k, c, disagree))
aps = [(a, b, c) for a, b, c in itertools.combinations(C, 3) if b - a == c - b]
print('3-APs m =', len(aps), '; weak Sidon (sums x+y, x<y, distinct):', len({a + b for a, b in itertools.combinations(C, 2)}) == n*(n-1)//2)
h = max(k for k in cnt if cnt[k] > 0) if cnt[13] == 0 else None
print('h =', h, 'tau = n-h =', n - h, 'I11 slack 3n+2m-11tau =', 3*n + 2*len(aps) - 11*(n - h))
try:
    from ortools.sat.python import cp_model
    M = cp_model.CpModel(); x = {a: M.NewBoolVar(str(a)) for a in C}
    sums = {}
    for i, a in enumerate(C):
        for b in C[i:]: sums.setdefault(a + b, []).append((a, b))
    ncons = 0
    for s, L in sums.items():
        for (a, b), (c, d) in itertools.combinations(L, 2):
            M.AddBoolOr([x[v].Not() for v in {a, b, c, d}]); ncons += 1
    M.Maximize(sum(x.values())); sol = cp_model.CpSolver(); sol.parameters.num_workers = 1; st = sol.Solve(M)
    print('CP-SAT conflicts', ncons, 'status', sol.StatusName(st), 'h =', int(sol.ObjectiveValue()))
except ImportError: print('ortools not available')
