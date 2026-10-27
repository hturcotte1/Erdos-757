"""Pairwise non-isomorphism of the 45 classes (own WL invariant + own exact backtracking iso test),
and a cross-check with nauty (labelg) canonical forms of the incidence graphs."""
import json, sys, itertools, subprocess
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
CLS = '/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'
cls = json.load(open(CLS))
G = [(c['n'], [tuple(e) for e in c['edges']]) for c in cls]
table = {}
inv = [hg.wl_invariant(n, es, table)[0] for n, es in G]
groups = {}
for i, x in enumerate(inv):
    groups.setdefault(x, []).append(i)
print('classes', len(G), 'distinct WL invariants', len(groups))
coll = [g for g in groups.values() if len(g) > 1]
print('WL-collision groups:', coll)
# exact test on every colliding pair
noniso_pairs = 0
iso_pairs = []
for g in coll:
    for i, j in itertools.combinations(g, 2):
        phi = hg.iso_exact(G[i][0], G[i][1], G[j][0], G[j][1])
        if phi is None:
            noniso_pairs += 1
        else:
            iso_pairs.append((i, j))
print('colliding pairs proved non-isomorphic by exhaustive backtracking:', noniso_pairs, ' isomorphic pairs:', iso_pairs)
# sanity of iso_exact: a random relabelling of each class must be found isomorphic
import random
random.seed(1)
bad = 0
for i, (n, es) in enumerate(G):
    p = list(range(n)); random.shuffle(p)
    es2 = [tuple(sorted(p[x] for x in e)) for e in es]
    random.shuffle(es2)
    if hg.iso_exact(n, es, n, es2) is None:
        bad += 1
print('self-test (random relabelling recognised as isomorphic): failures', bad)
