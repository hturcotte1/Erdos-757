"""Referee L011: check the witness C22 of Theorem 2 from the definitions (no e757, no judge).
(i) 22 distinct integers; C22 = B12 u (5000 + 15*B10) as stated;
(ii) every 4-subset determines >= 5 distinct absolute differences;
(iii) largest Sidon subset: (a) all solutions of x+y=z+w ({x,y} != {z,w} as multisets) give the forbidden sets; exact
      maximum independent set by my own branch and bound; (b) brute force: no 14-subset is Sidon, some 13-subset is Sidon
      (Sidon tested directly: all sums x+y, x<=y, distinct); (c) CP-SAT ILP if ortools is importable.
(iv) h/n vs 4/7 with Fractions."""
import itertools, sys
from fractions import Fraction
B12 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]
B10 = [0, 50, 73, 80, 87, 96, 100, 112, 127, 174]
C22 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575, 5000, 5750, 6095, 6200, 6305, 6440, 6500, 6680, 6905, 7610]
assert sorted(B12 + [5000 + 15 * b for b in B10]) == C22, 'C22 != B12 u (5000+15 B10)'
A = C22; n = len(A)
assert len(set(A)) == n == 22
bad4 = [Q for Q in itertools.combinations(A, 4) if len({abs(a - b) for a, b in itertools.combinations(Q, 2)}) < 5]
print('4-subsets:', len(list(itertools.combinations(A, 4))), 'with < 5 distinct differences:', len(bad4))
# forbidden sets from x+y = z+w
sums = {}
for i in range(n):
    for j in range(i, n):
        sums.setdefault(A[i] + A[j], []).append((i, j))
forb = set()
for s, L in sums.items():
    for (p, q) in itertools.combinations(L, 2):
        forb.add(frozenset(p) | frozenset(q))
print('forbidden sets:', len(forb), 'sizes:', sorted({len(f) for f in forb}),
      '3-term APs (size-3 sets):', sum(1 for f in forb if len(f) == 3))
def is_sidon(S):
    seen = set()
    for i, a in enumerate(S):
        for b in S[i:]:
            if a + b in seen: return False
            seen.add(a + b)
    return True
# exact max independent set (branch and bound)
forb_l = [tuple(sorted(f)) for f in forb]
best = [0, None]
def bb(i, chosen):
    if len(chosen) + (n - i) <= best[0]: return
    if i == n:
        best[0] = len(chosen); best[1] = list(chosen); return
    # include i if no forbidden set becomes fully chosen
    cs = set(chosen) | {i}
    if all(not (set(f) <= cs) for f in forb_l if i in f):
        chosen.append(i); bb(i + 1, chosen); chosen.pop()
    bb(i + 1, chosen)
bb(0, [])
S = [A[i] for i in best[1]]
print('branch and bound: h =', best[0], 'example', S, 'is_sidon', is_sidon(S))
# brute force
c14 = sum(1 for T in itertools.combinations(A, 14) if is_sidon(list(T)))
c13 = sum(1 for T in itertools.combinations(A, 13) if is_sidon(list(T)))
print('brute force: Sidon 14-subsets:', c14, '| Sidon 13-subsets:', c13)
claimed = [0, 269, 385, 467, 511, 521, 523, 5000, 5750, 6095, 6200, 6680, 6905]
print('certificate 13-subset of the proof is Sidon:', is_sidon(claimed), 'subset of C22:', set(claimed) <= set(A), len(claimed))
try:
    from ortools.sat.python import cp_model
    md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(n)]
    for f in forb_l: md.Add(sum(x[i] for i in f) <= len(f) - 1)
    md.Maximize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.num_workers = 1; st = sv.Solve(md)
    print('CP-SAT:', sv.StatusName(st), 'h =', int(sv.ObjectiveValue()))
except ImportError:
    print('ortools not available')
h = best[0]
print('h/n =', Fraction(h, n), '; 4/7 =', Fraction(4, 7), '; h/n < 4/7:', Fraction(h, n) < Fraction(4, 7))
# AP hypergraph parameters
aps = [f for f in forb if len(f) == 3]
mids = set()
for f in aps:
    a, b, c = sorted(A[i] for i in f); assert a + c == 2 * b; mids.add(b)
print('m (3-APs) =', len(aps), 'distinct midpoints =', len(mids), 'tau = n - h =', n - h, 'I11 slack 3n+2m-11tau =', 3 * n + 2 * len(aps) - 11 * (n - h))
