"""Referee C005 round 1: exact checks of results/claims/C005-lemmaE-SK6-E1.json (own code)."""
import sys, time, random
from fractions import Fraction
sys.path.insert(0, '.')
from common import *

t0 = time.time()
raw, pts = load_claim('/home/user/Erdos-757/results/claims/C005-lemmaE-SK6-E1.json')
A = sorted(pts)
n = len(A)
print('id', raw['id'], 'type', raw['type'], 'n', n, 'claimed_h', raw['claimed_h'])
print('distinct', len(set(pts)) == n, 'already sorted', pts == A, 'min', A[0], 'max', A[-1])
# structural consistency with the README description (not load-bearing)
t1 = A[1]; span7 = 269 ** 7
print('t1 = 3*269^7+1000003 ?', t1 == 3 * span7 + 1000003, ' max == 2*t1 ?', A[-1] == 2 * t1)

# literal (4,5) test
ok, cnt, five, bad = four_subset_literal(A)
print('4-subset literal test: ok', ok, 'subsets', cnt, 'C(67,4)=', 67*66*65*64//24, 'with exactly 5 distinct', five, 'bad', bad, f'({time.time()-t0:.1f}s)')

# Sidon violations from the definition
Fs, by_sum = forbidden_sets_from_sums(A)
Fd = forbidden_sets_from_diffs(A)
print('forbidden sets by sums', len(Fs), 'by diffs', len(Fd), 'equal', Fs == Fd)
from collections import Counter
print('sizes of forbidden sets', Counter(len(f) for f in Fs))
ws = [A[i] + A[j] for i in range(n) for j in range(i + 1, n)]
print('weak Sidon (sums x<y distinct)', len(ws) == len(set(ws)))
# list of 3-APs directly
aps = []
S = set(A)
for i in range(n):
    for k in range(i + 1, n):
        if (A[i] + A[k]) % 2 == 0 and (A[i] + A[k]) // 2 in S:
            aps.append((i, A.index((A[i] + A[k]) // 2), k))
print('3-APs found directly', len(aps), 'equal to forbidden sets', set(frozenset(e) for e in aps) == Fs)
mids = Counter(e[1] for e in aps)
print('distinct midpoints', len(mids), 'max multiplicity', max(mids.values()), 'n-2 =', n - 2)
deg = Counter(v for e in aps for v in e)
print('degree distribution', sorted(Counter(deg[v] for v in range(n)).items()))
# linearity
lin = all(len(set(e) & set(f)) <= 1 for e in aps for f in aps if e != f)
print('linear', lin)

# witness
W = sorted(raw['witness_sidon_subset'])
print('witness size', len(W), 'distinct', len(set(W)) == len(W), 'subset', set(W) <= S,
      'Sidon(sums)', is_sidon_def(W), 'Sidon(diffs)', is_sidon_diff(W))

# exact alpha via frontier DP (own), two orders
t = time.time()
order = greedy_order(n, Fs)
a1, wit1, ms1 = alpha_frontier_dp(n, Fs, order)
print('DP greedy order: alpha', a1, 'max states', ms1, f'({time.time()-t:.1f}s)')
Wd = [A[i] for i in wit1]
print('  DP witness size', len(Wd), 'Sidon(sums)', is_sidon_def(Wd), 'Sidon(diffs)', is_sidon_diff(Wd))
t = time.time()
order2 = list(reversed(order))
a2, wit2, ms2 = alpha_frontier_dp(n, Fs, order2)
print('DP reversed greedy order: alpha', a2, 'max states', ms2, f'({time.time()-t:.1f}s)')
print('  witness 2 Sidon', is_sidon_def([A[i] for i in wit2]), len(wit2))
r = Fraction(a1, n)
print('h/n =', r, ' < 4/7 :', r < Fraction(4, 7), ' 7h =', 7 * a1, ' 4n =', 4 * n)
print('claimed_h matches', raw['claimed_h'] == a1 == a2 == len(W))
print('total time', f'{time.time()-t0:.1f}s')
