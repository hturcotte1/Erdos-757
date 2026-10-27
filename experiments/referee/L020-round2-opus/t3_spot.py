"""Spot-check of L020 Theorem 3 on stored near-tight graphs (n <= 26, so (H_n) holds by L016):
stratified random sample of degree-3 instances, every conclusion checked directly by own code."""
import random, sys
from collections import Counter, defaultdict
from hgr2 import HG, parse_list
from patt import analyse, slack

I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
cells = ['cell_8_5_3', 'cell_10_7_4', 'cell_12_10_5', 'cell_14_12_6', 'cell_15_11_6', 'cell_17_13_7',
         'cell_19_16_8', 'cell_22_17_9', 'cell_26_22_11']

def quick_pattern(K, v):
    eidx = [i for i in range(len(K.E)) if K.inc[v] >> i & 1]
    P = [tuple(u for u in K.E[i] if u != v) for i in eidx]
    Gmask = K.full & ~K.inc[v]
    comps, iso = K.components([u for u in K.V if u != v], Gmask)
    cid = {}
    for k, (Vc, em) in enumerate(comps):
        for u in Vc: cid[u] = k
    for y in iso: cid[y] = 'Y'
    r = len(comps)
    if iso: return 'Y%d-r%d' % (len(iso), r)
    if r == 1: return 'a'
    ty = [cid[p[0]] if cid[p[0]] == cid[p[1]] else 's' for p in P]
    ins = [t for t in ty if t != 's']
    if r == 2 and not ins: return 'b'
    if r == 2 and len(ins) == 2 and ins[0] != ins[1]: return 'e'
    if r == 2 and len(ins) == 1: return 'f'
    return 'other-r%d' % r

pool = defaultdict(list)
ngraphs = Counter()
for c in cells:
    for gi, (n, m, t, E) in enumerate(parse_list(I + c + '.txt')):
        V = list(range(n))
        K = HG(V, E)
        if max(K.deg(u) for u in V) > 3: continue
        comps, iso = K.components(V, K.full)
        if len(comps) != 1 or iso: continue
        ngraphs[c] += 1
        for v in V:
            if K.deg(v) == 3:
                pool[quick_pattern(K, v)].append((c, gi, v))
print('Delta<=3 connected graphs per list:', dict(ngraphs), 'total', sum(ngraphs.values()))
print('degree-3 instances by quick pattern:', {k: len(x) for k, x in pool.items()}, 'total', sum(len(x) for x in pool.values()))
rng = random.Random(20261027)
sample = []
for k in sorted(pool):
    sample += rng.sample(pool[k], min(4, len(pool[k])))
rest = [x for k in pool for x in pool[k] if x not in sample]
sample += rng.sample(rest, max(0, 30 - len(sample)))
lists = {c: parse_list(I + c + '.txt') for c in cells}
tot_f = 0
pc = Counter()
for (c, gi, v) in sample:
    n, m, t, E = lists[c][gi]
    K = HG(list(range(n)), E)
    assert K.tau() == t, (c, gi)
    res = analyse(K, v)
    pc[res['pattern']] += 1
    tot_f += len(res['fails'])
    print(c, 'class', gi, 'v', v, 's(K)=%d' % res['sK'], 'pattern', res['pattern'], 'cells', res['cells'], 'Y', res['iso'], 'FAILS', res['fails'])
print('sample size', len(sample), 'patterns', dict(pc), 'total fails', tot_f)
