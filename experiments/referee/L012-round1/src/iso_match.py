"""Referee: isomorphism test independent of nauty (networkx VF2 on the vertex/edge incidence graph, kinds as node colours).
(1) the 699 prover representatives are pairwise non-isomorphic (VF2 inside every Weisfeiler-Lehman hash bucket);
(2) every survivor of the referee's own extension run is isomorphic to one of the 699 (VF2), and every representative is hit."""
import sys, re, collections
import networkx as nx
from networkx.algorithms import isomorphism as iso
def edges_of(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def inc(E, n):
    G = nx.Graph()
    for v in range(n): G.add_node(('v', v), kind='v')
    for i, e in enumerate(E):
        G.add_node(('e', i), kind='e')
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
def key(G): return nx.weisfeiler_lehman_graph_hash(G, node_attr='kind', iterations=4)
nm = iso.categorical_node_match('kind', None)
reps = [edges_of(l) for l in open(sys.argv[1]) if l.startswith('FOUND')]
n = int(sys.argv[3])
RG = [inc(E, n) for E in reps]; RK = [key(G) for G in RG]
buckets = collections.defaultdict(list)
for i, k in enumerate(RK): buckets[k].append(i)
pairs = 0; isopairs = 0
for k, L in buckets.items():
    for a in range(len(L)):
        for b in range(a + 1, len(L)):
            pairs += 1
            if iso.GraphMatcher(RG[L[a]], RG[L[b]], node_match=nm).is_isomorphic(): isopairs += 1
print('(1) representatives %d, WL buckets %d, VF2 pairs tested %d, isomorphic pairs %d' % (len(reps), len(buckets), pairs, isopairs))
surv = [edges_of(l) for l in open(sys.argv[2]) if l.startswith('S:') and '#conn=1' in l]
hit = collections.Counter(); unmatched = 0
for E in surv:
    G = inc(E, n); k = key(G); found = None
    for i in buckets.get(k, []):
        if iso.GraphMatcher(G, RG[i], node_match=nm).is_isomorphic(): found = i; break
    if found is None: unmatched += 1
    else: hit[found] += 1
print('(2) connected survivors %d, matched to a representative %d, UNMATCHED %d, representatives hit %d of %d' % (len(surv), len(surv) - unmatched, unmatched, len(hit), len(reps)))
