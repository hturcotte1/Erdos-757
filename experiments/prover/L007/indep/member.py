"""Is the falsifier's F7-containing (14,11,6) example isomorphic to one of the outputs in the given FOUND-file?"""
import json, sys
import networkx as nx
from iso_compare import parse, inc, nm
ex = [tuple(e) for e in json.load(open('/home/user/Erdos-757/experiments/falsify/i11-inequality/f7_containing_violation.json'))['edges']]
G = inc(ex); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t')
for f in sys.argv[1:]:
    L = parse(f)
    hit = [i for i, es in enumerate(L) if nx.weisfeiler_lehman_graph_hash(inc(es), node_attr='t') == h and nx.is_isomorphic(G, inc(es), node_match=nm)]
    print(f, 'outputs', len(L), 'isomorphic copies of the example:', len(hit))
