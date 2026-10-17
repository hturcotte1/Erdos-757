"""Isomorphism classes (networkx VF2 on incidence graphs, WL-hash buckets) of the hypergraphs on lines starting with TAG:."""
import re, sys
import networkx as nx
def inc(es):
    G = nx.Graph()
    for i, e in enumerate(es):
        G.add_node(('e', i), t=1)
        for v in e: G.add_node(('v', v), t=0); G.add_edge(('e', i), ('v', v))
    return G
nm = lambda a, b: a['t'] == b['t']
tag = sys.argv[2] + ':'
buckets = {}; reps = []; tot = 0
for l in open(sys.argv[1]):
    if not l.startswith(tag): continue
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]; tot += 1
    G = inc(es); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t'); b = buckets.setdefault(h, [])
    if not any(nx.is_isomorphic(G, H, node_match=nm) for H in b): b.append(G); reps.append(es)
print(sys.argv[1], tag, 'hypergraphs', tot, 'isomorphism classes', len(reps))
if len(sys.argv) > 3:
    with open(sys.argv[3], 'w') as f:
        for es in reps: f.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
