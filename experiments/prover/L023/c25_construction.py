"""(L023) The explicit 25-point witness C25 = A_base u (10^9 + 7919 * B11), B11 = the 11-point record of data/small_records.json.
Exact integer checks: (4,5) on all 12,650 four-point subsets; weak Sidon; the 3-term APs (no AP uses points of both parts);
the AP hypergraph is in C (linear, F7-free, (P3)); tau by exhaustive branching; an explicit Sidon subset of size 15;
e757.core.alpha (exact branch and bound) = 15."""
import json, sys, itertools
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import alpha, ap_edges, is_45_set, is_sidon
from itertools import combinations
ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B11 = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']['11']['set']
C25 = sorted(ABASE + [10**9 + 7919 * x for x in B11])
print('A_base', len(ABASE), 'APs', len(ap_edges(ABASE)), 'is_45', is_45_set(ABASE), 'alpha', alpha(ABASE))
print('B11', B11, 'APs', len(ap_edges(B11)), 'is_45', is_45_set(B11), 'alpha', alpha(B11))
print('C25 =', C25)
n = len(C25); assert n == 25 and len(set(C25)) == 25
bad = 0; cnt = 0
for B in combinations(C25, 4):
    cnt += 1
    if len({abs(x - y) for x, y in combinations(B, 2)}) < 5: bad += 1
print('four-point subsets', cnt, 'with < 5 distinct differences', bad)
sums = [x + y for x, y in combinations(C25, 2)]
print('weak Sidon', len(sums) == len(set(sums)))
aps = ap_edges(C25)
lowpart = set(ABASE)
cross = [e for e in aps if len({v in lowpart for v in e}) > 1]
print('3-term APs', len(aps), '(A_base %d + B11 %d)' % (len(ap_edges(ABASE)), len(ap_edges(B11))), 'APs using both parts', len(cross))
idx = {x: i for i, x in enumerate(C25)}
E = [tuple(sorted(idx[v] for v in e)) for e in aps]
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from verify_c import in_C, tau_exact
okC, why = in_C(E, n)
t, cover = tau_exact(E, n)
print('AP hypergraph in C:', okC, why, '; tau =', t, 'minimum cover', [C25[i] for i in cover])
S = [C25[i] for i in range(n) if i not in cover]
print('Sidon subset (complement of the minimum cover): size', len(S), 'is_sidon', is_sidon(S))
a = alpha(C25)
print('e757.core.alpha(C25) =', a, '; h = n - tau =', n - t)
assert bad == 0 and len(sums) == len(set(sums)) and is_45_set(C25) and okC and a == 15 and n - t == 15 and is_sidon(S) and len(S) == 15 and not cross
print('RESULT C25 is a 25-point (4,5)-set with h = 15')
json.dump(C25, open('c25_set.json', 'w'))
