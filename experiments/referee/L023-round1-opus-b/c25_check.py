"""Referee L023 (opus-b): Theorem 4, own code.  C25 from the certificate text; (a) distinct; (b) all 4-subsets have >= 5 distinct
differences; (c) h(C25) = 15 by two methods: CP-SAT on the Sidon conflict structure (every pair of distinct pairs {a,b},{c,d}, a<=b,
c<=d, with a+b = c+d is a forbidden configuration), and brute force over all C(25,16) 16-subsets (direct Sidon test); (d) the
claim file's witness subset is Sidon of size 15; (e) C25 equals A_base u (10^9 + 7919*B11) with B11 = data/small_records.json '11'."""
import itertools, json, re, time, sys
from fractions import Fraction
ROOT = '/home/user/Erdos-757'
txt = open(ROOT + '/results/proofs/L023-f25-equals-15.md').read()
m = re.search(r'\$C_\{25\}=\\\{([0-9,]+)\\\}\$', txt)
C = [int(x) for x in m.group(1).split(',')]
claim = json.load(open(ROOT + '/results/claims/C007-c25-witness-f25.json'))
print('n', len(C), 'distinct', len(set(C)) == len(C), 'equals claim file set', sorted(C) == sorted(claim['set']))
A_base = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
B11 = json.load(open(ROOT + '/data/small_records.json'))['sets']['11']['set']
print('C25 == A_base u (10^9+7919*B11):', sorted(C) == sorted(A_base + [10**9 + 7919 * x for x in B11]), 'B11', B11)
bad = 0
for B in itertools.combinations(C, 4):
    if len({abs(p - q) for p, q in itertools.combinations(B, 2)}) < 5: bad += 1
print('4-subsets', len(list(itertools.combinations(C, 4))), 'with < 5 distinct differences', bad)
def is_sidon(S):
    seen = set()
    for i in range(len(S)):
        for j in range(i, len(S)):
            s = S[i] + S[j]
            if s in seen: return False
            seen.add(s)
    return True
W = claim['witness_sidon_subset']
print('witness subset size', len(W), 'subset of C25', set(W) <= set(C), 'Sidon', is_sidon(sorted(W)))
# CP-SAT
from ortools.sat.python import cp_model
sums = {}
for i in range(len(C)):
    for j in range(i, len(C)):
        sums.setdefault(C[i] + C[j], []).append((i, j))
confl = set()
for s, ps in sums.items():
    for p, q in itertools.combinations(ps, 2):
        confl.add(frozenset(p) | frozenset(q))
mdl = cp_model.CpModel(); x = [mdl.NewBoolVar('x%d' % i) for i in range(len(C))]
for F in confl: mdl.Add(sum(x[i] for i in F) <= len(F) - 1)
mdl.Maximize(sum(x))
sol = cp_model.CpSolver(); sol.parameters.num_workers = 1; st = sol.Solve(mdl)
S = sorted(C[i] for i in range(len(C)) if sol.Value(x[i]))
print('CP-SAT conflicts', len(confl), 'status', sol.StatusName(st), 'max Sidon', int(sol.ObjectiveValue()), 'bound', int(sol.BestObjectiveBound()), 'solution Sidon', is_sidon(S))
t0 = time.time(); cnt = 0; sid = 0
Cs = sorted(C)
for T in itertools.combinations(Cs, 16):
    cnt += 1
    if is_sidon(T): sid += 1
print('brute force: 16-subsets', cnt, 'Sidon among them', sid, 'secs %.0f' % (time.time() - t0))
