"""An explicit 18-point (4,5)-set with h = 11 (so f(18) <= 11), checked from the definitions; the set is the best 18-point state of the
annealing run experiments/20261013-2257-anneal16/best.json ('best_valid_by_ratio')."""
import itertools, json, sys
d = json.load(open('/home/user/Erdos-757/experiments/20261013-2257-anneal16/best.json'))['best_valid_by_ratio']
A = sorted(d['set']); assert len(A) == 18
def nd(q): return len({abs(a - b) for a, b in itertools.combinations(q, 2)})
def sidon(S):
    s = [x + y for i, x in enumerate(S) for y in S[i:]]; return len(s) == len(set(s))
is45 = all(nd(q) >= 5 for q in itertools.combinations(A, 4))
aps = [(a, b, c) for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b]
h11 = any(sidon(S) for S in itertools.combinations(A, 11)); h12 = any(sidon(S) for S in itertools.combinations(A, 12))
print('A =', A); print('(4,5):', is45, '(%d four-subsets) | APs:' % len(list(itertools.combinations(A, 4))), len(aps), '| Sidon 11-subset:', h11, '| Sidon 12-subset:', h12)
sys.path.insert(0, '/home/user/Erdos-757'); from e757.core import alpha, ap_edges
print('e757.core: m =', len(ap_edges(A)), 'h =', alpha(A), '| recorded in best.json: h =', d['h'])
json.dump(dict(set=A, n=18, m=len(aps), h=11 if (h11 and not h12) else None, is45=is45), open('witness_18.json', 'w'))
