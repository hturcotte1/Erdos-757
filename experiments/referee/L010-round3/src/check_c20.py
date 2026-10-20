"""Referee L010 round 3: the witness C20 from the definitions only (integers; no e757, no judge)."""
import itertools
C = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056, 5000, 5101, 5202, 20000, 20103, 20206]
assert len(set(C)) == 20 and C == sorted(C)
bad = [q for q in itertools.combinations(C, 4) if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5]
print('four-subsets checked:', sum(1 for _ in itertools.combinations(C, 4)), '| with < 5 distinct differences:', len(bad))
aps = [(a, b, c) for a, b, c in itertools.combinations(C, 3) if a + c == 2 * b]
print('3-term APs (m):', len(aps))
# weak Sidon check (all sums x+y, x<y distinct) -- a consequence of (4,5)
sums = [x + y for x, y in itertools.combinations(C, 2)]; print('weak Sidon:', len(sums) == len(set(sums)))
def sidon(S):
    s = [x + y for x, y in itertools.combinations_with_replacement(S, 2)]; return len(s) == len(set(s))
# h via independent sets of the AP hypergraph (Sidon <=> 3-AP-free for weak Sidon sets), brute force over all 12- and 13-subsets
idx = {x: i for i, x in enumerate(C)}; E = [frozenset(idx[v] for v in e) for e in aps]
def indep(S): return not any(e <= S for e in E)
n13 = sum(1 for S in itertools.combinations(range(20), 13) if indep(frozenset(S)))
n12 = sum(1 for S in itertools.combinations(range(20), 12) if indep(frozenset(S)))
print('3-AP-free 13-subsets:', n13, '| 3-AP-free 12-subsets:', n12)
# direct Sidon check of the 12-subsets found (definition), and of a sample of 13-subsets
S12 = [S for S in itertools.combinations(range(20), 12) if indep(frozenset(S))]
print('all 3-AP-free 12-subsets are Sidon by the definition:', all(sidon([C[i] for i in S]) for S in S12))
print('some 13-subset is Sidon by the definition (should be False):', any(sidon([C[i] for i in S]) for S in itertools.combinations(range(20), 13)))
# tau and I11 slack
tau = 20 - 12; print('n=20 m=%d h=12 tau=%d  I11 slack 3n+2m-11tau = %d; 17tau <= 5n+3m: %s' % (len(aps), tau, 60 + 2 * len(aps) - 11 * tau, 17 * tau <= 100 + 3 * len(aps)))
# ratio h/n < 4/7 ?
from fractions import Fraction
print('h/n =', Fraction(12, 20), '< 4/7:', Fraction(12, 20) < Fraction(4, 7), '; ceil(80/7)-1 =', -(-80 // 7) - 1)
