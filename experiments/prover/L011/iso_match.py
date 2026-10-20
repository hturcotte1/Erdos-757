"""Check that two lists of hypergraphs (FOUND-lines file, or a JSON list of edge lists) have the same isomorphism classes;
for every hypergraph of list B report whether it is isomorphic to one of list A (networkx VF2 on incidence graphs)."""
import re, sys, json
import networkx as nx
def load(f):
    if f.endswith('.json'): return [[tuple(e) for e in es] for es in json.load(open(f))]
    return [[tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)] for l in open(f) if l.startswith('FOUND:')]
def inc(es):
    G = nx.Graph()
    for i, e in enumerate(es):
        G.add_node(('e', i), t=1)
        for v in e: G.add_node(('v', v), t=0); G.add_edge(('e', i), ('v', v))
    return G
nm = lambda a, b: a['t'] == b['t']
A, B = load(sys.argv[1]), load(sys.argv[2])
bk = {}
for i, es in enumerate(A): G = inc(es); bk.setdefault(nx.weisfeiler_lehman_graph_hash(G, node_attr='t'), []).append((i, G))
hitA = set(); miss = 0
for es in B:
    G = inc(es); m = [i for i, H in bk.get(nx.weisfeiler_lehman_graph_hash(G, node_attr='t'), []) if nx.is_isomorphic(G, H, node_match=nm)]
    if m: hitA.add(m[0])
    else: miss += 1
print('A =', sys.argv[1], len(A), '| B =', sys.argv[2], len(B), '| B members not isomorphic to any A member:', miss, '| A classes hit by B:', sorted(hitA))
