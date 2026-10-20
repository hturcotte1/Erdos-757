"""Referee L014 round 2: spot-check of the labelg class matching with networkx VF2 (independent of nauty): for a random sample of
my member graphs, find the prover's representative with the same labelg canonical form and confirm a colour-preserving
isomorphism of the incidence graphs with VF2; also confirm that the sampled member is NOT isomorphic (VF2) to a few other random
representatives (negative control).  usage: python3 vf2_spot.py n m MYFILE PROVERFILE SAMPLE"""
import sys, random, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher, categorical_node_match
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L014-round2')
from canon_cmp import read_hg, canon
n, m = int(sys.argv[1]), int(sys.argv[2]); k = int(sys.argv[5]); rng = random.Random(2026)
mine_all = read_hg(sys.argv[3], n, m); prov = read_hg(sys.argv[4], n, m)
mine = rng.sample(mine_all, min(k, len(mine_all)))
cm = canon(n, m, mine); cp = canon(n, m, prov); idx = {c: i for i, c in enumerate(cp)}
def G(es):
    g = nx.Graph()
    for v in range(n): g.add_node(('v', v), c=0)
    for j, e in enumerate(es):
        g.add_node(('e', j), c=1)
        for v in e: g.add_edge(('v', v), ('e', j))
    return g
ok = neg = negok = 0
for c, es in zip(cm, mine):
    j = idx[c]
    if GraphMatcher(G(es), G(prov[j]), node_match=categorical_node_match('c', None)).is_isomorphic(): ok += 1
    for _ in range(2):
        r = rng.randrange(len(prov))
        if r == j: continue
        neg += 1
        if not GraphMatcher(G(es), G(prov[r]), node_match=categorical_node_match('c', None)).is_isomorphic(): negok += 1
print('VF2 spot check n=%d m=%d: sample %d, matched representative isomorphic (VF2) %d; negative controls %d, non-isomorphic %d' % (n, m, len(mine), ok, neg, negok))
