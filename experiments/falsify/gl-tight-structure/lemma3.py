import sys, itertools, json, collections
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import KNOWN, ap_edges, alpha
from e757.saturated import alpha_of_edges
def sub_alpha(A, dele):
    B = [x for i, x in enumerate(A) if i not in dele]
    return alpha(B)   # recomputes AP edges of subset, exact
out = {}
for name, A in (('A_base', KNOWN['A_base (Ma-Tang 14-point, h=8)']),):
    A = sorted(A); n = len(A); k = n // 2
    h = alpha(A); tau = n - h
    # single deletions
    single = {v: alpha([x for i, x in enumerate(A) if i != v]) for v in range(n)}
    # every vertex in a min transversal  <=> h(A-v) = h(A)  (A-v independent set max of size h avoids v)
    print('n', n, 'h', h, 'tau', tau, 'h(A-v):', single)
    print('every vertex avoided by some max Sidon subset:', all(s == h for s in single.values()))
    # tau(H-v) = k-2 ?  (13 points: tau = 13 - h(A-v))
    print('tau(H-v)==k-2 for all v:', all((n - 1) - s == k - 2 for s in single.values()))
    pair = {}
    for u, v in itertools.combinations(range(n), 2):
        pair[(u, v)] = sub_alpha(A, {u, v})
    dist = collections.Counter(pair.values())
    print('h(A-u-v) distribution over 91 pairs (12-point subsets):', dict(dist))
    print('12-subsets with h=7 (= f(12)):', [p for p, s in pair.items() if s == 7])
    print('pairs with h(A-u-v)==h(A)=8 (in a common min transversal):', sum(1 for s in pair.values() if s == h))
    print('tau(H-u-v) values:', dict(collections.Counter((n - 2) - s for s in pair.values())))
    out = {'h': h, 'single': single, 'pair_dist': dict(dist), 'pairs_h7': [p for p, s in pair.items() if s == 7]}
json.dump(out, open('lemma3_results.json', 'w'), indent=1)
