"""Referee: compare two class lists (FOUND lines) by networkx VF2 isomorphism: bijection check."""
import sys, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L012-round1/src')
from closure_check import edges_of, inc, wl, nm, iso
def classes(fn, n):
    G = [inc(edges_of(l), range(n)) for l in open(fn) if l.startswith('FOUND')]
    B = collections.defaultdict(list)
    for i, g in enumerate(G): B[wl(g)].append(i)
    return G, B
out = []
for spec in sys.argv[1:]:
    a, b, n = spec.split(':'); n = int(n)
    GA, BA = classes(a, n); GB, BB = classes(b, n)
    hit = collections.Counter(); un = 0
    for g in GA:
        k = wl(g); f = next((i for i in BB.get(k, []) if iso.GraphMatcher(g, GB[i], node_match=nm).is_isomorphic()), None)
        if f is None: un += 1
        else: hit[f] += 1
    print('%s vs %s: |A|=%d |B|=%d unmatched_in_A=%d B_hit=%d multiply_hit=%d' % (a.split('/')[-1], b.split('/')[-1], len(GA), len(GB), un, len(hit), sum(1 for v in hit.values() if v > 1)))
