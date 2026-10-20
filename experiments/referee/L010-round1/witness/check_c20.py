"""Referee L010 r1: the witness C20 from the definitions only (integers; no e757, no judge).
(4,5): every 4-subset has >= 5 distinct absolute differences.  h: largest Sidon subset (all sums x+y, x<=y, distinct),
by exhaustive search over all 12- and 13-subsets (C(20,13) = 77,520), plus CP-SAT on the 'equal sum' conflicts as a
second method; also the 3-AP count m and the I11 slack of its AP pattern."""
import itertools, sys
A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
C20 = sorted(A_base + [5000, 5101, 5202] + [20000, 20103, 20206])
assert len(set(C20)) == 20
bad = [q for q in itertools.combinations(C20, 4) if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5]
print('n =', len(C20), '4-subsets:', sum(1 for _ in itertools.combinations(C20, 4)), 'with < 5 distinct differences:', len(bad))
def sidon(S):
    sums = [a + b for i, a in enumerate(S) for b in S[i:]]
    return len(sums) == len(set(sums))
for k in (12, 13):
    cnt = sum(1 for S in itertools.combinations(C20, k) if sidon(S))
    print('Sidon %d-subsets: %d' % (k, cnt))
aps = [(a, b, c) for a, b, c in itertools.combinations(C20, 3) if a + c == 2 * b]
print('3-term APs m =', len(aps))
from ortools.sat.python import cp_model
md = cp_model.CpModel(); x = {a: md.NewBoolVar(str(a)) for a in C20}
pairs = [(a, b) for i, a in enumerate(C20) for b in C20[i:]]
bysum = {}
for a, b in pairs: bysum.setdefault(a + b, []).append((a, b))
ncon = 0
for s, L in bysum.items():
    for (a, b), (c, d) in itertools.combinations(L, 2):
        S = {a, b, c, d}; md.Add(sum(x[v] for v in S) <= len(S) - 1); ncon += 1
md.Maximize(sum(x.values())); sv = cp_model.CpSolver(); sv.parameters.num_workers = 1; st = sv.Solve(md)
print('CP-SAT: status', sv.StatusName(st), 'h =', int(sv.ObjectiveValue()), 'conflicts', ncon)
tau = 20 - int(sv.ObjectiveValue()); print('tau =', tau, 'I11 slack 3n+2m-11tau =', 60 + 2 * len(aps) - 11 * tau)
