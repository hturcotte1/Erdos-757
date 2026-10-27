"""Isomorphism classes of the pattern-(e) graphs (networkx: incidence graph, WL hash + exact is_isomorphic)."""
import sys, json, networkx as nx
data = json.load(open(sys.argv[1]))
def inc(d):
    G = nx.Graph()
    for x in range(d['n']): G.add_node(('v', x), t=0)
    for i, e in enumerate(d['edges']):
        G.add_node(('e', i), t=1)
        for x in e: G.add_edge(('e', i), ('v', x))
    return G
reps = []
for i, d in enumerate(data):
    G = inc(d); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t', iterations=4)
    for (h2, G2, j) in reps:
        if h2 == h and nx.is_isomorphic(G, G2, node_match=lambda a, b: a['t'] == b['t']): break
    else:
        reps.append((h, G, i))
print('labelled', len(data), 'classes', len(reps), 'representative indices', [j for (_, _, j) in reps])
json.dump([data[j] for (_, _, j) in reps], open(sys.argv[2], 'w'))
