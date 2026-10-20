"""Referee: consistency of the prover's lists: the Delta<=3 members of cell(n,m,t,4) must be exactly cell(n,m,t,3) (VF2)."""
import sys, collections, re
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L012-round1/src')
from closure_check import edges_of, inc, wl, nm, iso
CD = '/home/user/Erdos-757/experiments/prover/L012/out/cells'
for key in ['8_5_3', '10_7_4', '12_10_5', '14_12_6', '15_11_6', '19_16_8', '22_17_9']:
    n = int(key.split('_')[0])
    A = [edges_of(l) for l in open('%s/cell_%s_D4.txt' % (CD, key)) if l.startswith('FOUND')]
    A3 = [E for E in A if max(collections.Counter(v for e in E for v in e).values()) <= 3]
    B = [edges_of(l) for l in open('%s/cell_%s_D3.txt' % (CD, key)) if l.startswith('FOUND')]
    GB = [inc(E, range(n)) for E in B]; BB = collections.defaultdict(list)
    for i, g in enumerate(GB): BB[wl(g)].append(i)
    hit = collections.Counter(); un = 0
    for E in A3:
        g = inc(E, range(n)); f = next((i for i in BB.get(wl(g), []) if iso.GraphMatcher(g, GB[i], node_match=nm).is_isomorphic()), None)
        if f is None: un += 1
        else: hit[f] += 1
    print('(%s): D4 list %d, of which Delta<=3: %d; D3 list %d; unmatched %d; D3 classes hit %d' % (key, len(A), len(A3), len(B), un, len(hit)))
