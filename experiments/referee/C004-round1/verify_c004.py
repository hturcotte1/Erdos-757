"""Referee verification of results/claims/C004-lemmaE-SK5-E1.json (own code; no e757/ or judge/ import)."""
import json
import sys
import time
from fractions import Fraction

sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402

CLAIM = '/home/user/Erdos-757/results/claims/C004-lemmaE-SK5-E1.json'
out = {}
t0 = time.time()
c = R.load_claim(CLAIM)  # raises on duplicate JSON keys
print('keys:', sorted(c.keys()))
print('id:', c['id'], ' type:', c['type'])
raw = R.as_int_list(c['set'])
W = R.as_int_list(c['witness_sidon_subset'])
print('claimed_h:', c['claimed_h'], type(c['claimed_h']).__name__)
A = sorted(raw)
n = len(A)
print('n =', n, ' distinct =', len(set(A)) == n, ' sorted-as-given =', raw == A)
print('min, max =', A[0], A[-1], ' max < 2^53:', A[-1] < 2 ** 53)
out['n'] = n
out['distinct'] = len(set(A)) == n

# literal (4,5) test
t = time.time()
ok, mind, n5, bad, tot = R.is45_literal(A)
print(f'(4,5) literal: ok={ok} checked={tot} min_distinct={mind} exactly5={n5} bad={bad} ({time.time()-t:.1f}s)')
out['is45'] = ok
out['four_subsets_checked'] = tot
out['min_distinct'] = mind
out['quads_with_exactly_5'] = n5

# collision structure from the definition
forb, census = R.forbidden_sets(A)
print('forbidden-set census (size: count):', census)
aps = R.ap_triples(A)
print('3-APs found directly:', len(aps))
print('forbidden sets == 3-AP index sets:', sorted(tuple(sorted(x)) for x in aps) == forb)
weak = census.get(4, 0) == 0
print('weak Sidon (no 4-distinct a+b=c+d):', weak)
out['weak_sidon'] = weak
out['m_aps'] = len(aps)
mids = sorted(set(j for (_, j, _) in aps))
print('distinct midpoints:', len(mids), ' midpoint injective:', len(mids) == len(aps),
      ' extremes are midpoints:', (0 in mids) or (n - 1 in mids))
# linearity: two APs share at most one point
lin = all(len(set(a) & set(b)) <= 1 for i, a in enumerate(aps) for b in aps[i + 1:])
print('linear:', lin)
deg = [0] * n
for e in aps:
    for v in e:
        deg[v] += 1
print('degree histogram:', {d: deg.count(d) for d in sorted(set(deg))})

# witness
Wset = set(W)
print('witness: size', len(W), ' distinct', len(Wset) == len(W), ' subset', Wset <= set(A),
      ' Sidon(sums)', R.is_sidon_sums(W), ' Sidon(diffs)', R.is_sidon_diffs(W))
out['witness_ok'] = (Wset <= set(A)) and R.is_sidon_sums(W) and R.is_sidon_diffs(W) and len(Wset) == len(W)
out['witness_size'] = len(W)

# exact maximum by variable elimination over the definition-derived forbidden sets
t = time.time()
order, width = R.greedy_order(n, forb)
print('elimination order width (primal graph, min-degree):', width)
opt, w2, I = R.ve_max_independent(n, forb, order)
pts = [A[i] for i in I]
print(f'VE optimum = {opt}  (tables of width {w2}; {time.time()-t:.1f}s)')
print('VE argmax: size', len(I), ' independent', R.check_independent(I, forb), ' Sidon(sums)',
      R.is_sidon_sums(pts), ' Sidon(diffs)', R.is_sidon_diffs(pts))
out['h_ve'] = opt
out['ve_width'] = w2
out['ve_argmax'] = pts

# a second elimination order (reverse value order) as an internal consistency check
order2 = list(range(n))[::-1]
opt2, w3, I2 = R.ve_max_independent(n, forb, order2)
print('VE with plain reverse order: optimum', opt2, 'width', w3)
out['h_ve_order2'] = opt2

r = Fraction(opt, n)
print('h/n =', r, ' < 4/7:', r < Fraction(4, 7), ' (7h =', 7 * opt, ', 4n =', 4 * n, ')')
out['ratio'] = str(r)
out['beats_4_7'] = r < Fraction(4, 7)
out['claimed_h_matches'] = (int(c['claimed_h']) == opt)
print('claimed_h matches exact optimum:', out['claimed_h_matches'])
print(f'total {time.time()-t0:.1f}s')
with open('/home/user/Erdos-757/experiments/referee/C004-round1/verify_c004.json', 'w') as fh:
    json.dump(out, fh, indent=1)
