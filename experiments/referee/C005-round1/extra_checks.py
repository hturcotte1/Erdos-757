import sys, json, itertools, time
from fractions import Fraction
sys.path.insert(0, '.')
from common import *
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

raw, pts = load_claim('/home/user/Erdos-757/results/claims/C005-lemmaE-SK6-E1.json')
A = sorted(pts); n = len(A)
W = raw['witness_sidon_subset']
print('witness entries all int:', all(type(x) is int for x in W), ' claimed_h type', type(raw['claimed_h']).__name__)
print('judge-style parsing identical:', [Fraction(str(x)) for x in A] == [Fraction(x) for x in A])

# second (4,5) test, structurally different: list every coincidence of differences (pair,pair) with
# multiplicity; a 4-set has < 5 distinct differences iff it contains >= 2 coincidences.
by_d = {}
for i in range(n):
    for j in range(i + 1, n):
        by_d.setdefault(A[j] - A[i], []).append((i, j))
coinc = []
for d, prs in by_d.items():
    for p, q in itertools.combinations(prs, 2):
        coinc.append(frozenset(p) | frozenset(q))
bad4 = [c for c in coinc if len(c) == 4]      # a 4-point relation = 2 coincidences in one 4-set
bad_pairs = sum(1 for c1, c2 in itertools.combinations(coinc, 2) if len(c1 | c2) <= 4)
print('coincidences', len(coinc), 'four-point ones', len(bad4), 'pairs of coincidences inside one 4-set', bad_pairs,
      '=> (4,5):', not bad4 and bad_pairs == 0)

# link to the community set C003 (I_6) : C005 = {0, 2 t1} U (t1 + I_6)
c3 = json.load(open('/home/user/Erdos-757/results/claims/C003-reader-5-9-K6.json'))['set']
I6 = sorted(int(x) for x in c3)
t1 = 3 * (I6[-1] - I6[0]) + 1000003
rebuilt = sorted([0, 2 * t1] + [t1 + x for x in I6])
print('C003 min/max', I6[0], I6[-1], '= 0, 269^7:', I6[0] == 0 and I6[-1] == 269 ** 7,
      '| C005 == {0,2t1} U (t1 + C003):', rebuilt == A, '| t1 =', t1)

# third exact-type method: MILP (HiGHS) max sum x, each 3-AP (all relations are 3-APs here) sum <= 2
F, _ = forbidden_sets_from_sums(A)
rows = []
for f in F:
    r = np.zeros(n); r[list(f)] = 1; rows.append(r)
res = milp(c=-np.ones(n), constraints=LinearConstraint(np.array(rows), -np.inf, [len(f) - 1 for f in F]),
           integrality=np.ones(n), bounds=Bounds(0, 1), options={'mip_rel_gap': 0})
print('HiGHS MILP status', res.status, res.message, 'obj', -res.fun, 'dual bound', -getattr(res, 'mip_dual_bound', float('nan')),
      'gap', getattr(res, 'mip_gap', None))
xs = [A[i] for i in range(n) if res.x[i] > 0.5]
print('  MILP solution size', len(xs), 'Sidon', is_sidon_def(xs))
# LP relaxation value (for information)
from scipy.optimize import linprog
lp = linprog(-np.ones(n), A_ub=np.array(rows), b_ub=[len(f) - 1 for f in F], bounds=(0, 1), method='highs')
print('  LP relaxation value', -lp.fun)

# consistency of the Lemma-E premise (NOT load-bearing): min of I_6 universal in I_6
F6, _ = forbidden_sets_from_sums(I6); n6 = len(I6)
h6 = alpha_frontier_dp(n6, F6, greedy_order(n6, F6))[0]
def alpha_without(v):
    keep = [u for u in range(n6) if u != v]
    idx = {u: i for i, u in enumerate(keep)}
    Fv = [frozenset(idx[u] for u in f) for f in F6 if v not in f]
    return alpha_frontier_dp(len(keep), Fv, greedy_order(len(keep), Fv))[0]
print('h(I_6) =', h6, '| alpha(H - min) =', alpha_without(0), '| alpha(H - max) =', alpha_without(n6 - 1))
# universality in the extension: which vertices of C005 are in every maximum Sidon subset
h = alpha_frontier_dp(n, F, greedy_order(n, F))[0]
univ = []
for v in range(n):
    keep = [u for u in range(n) if u != v]; idx = {u: i for i, u in enumerate(keep)}
    Fv = [frozenset(idx[u] for u in f) for f in F if v not in f]
    if alpha_frontier_dp(n - 1, Fv, greedy_order(n - 1, Fv))[0] == h - 1:
        univ.append(v)
print('h(C005) =', h, '| universal vertices of C005 (indices):', univ)
