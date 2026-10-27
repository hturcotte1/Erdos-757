"""Consistency check: every near-tight graph built by build_bf.py / pattern_e_build.py with <= 26 vertices must be
isomorphic to a class of the stored complete refereed list of its cell (Delta<=3 classes)."""
import sys, json, collections, networkx as nx
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
def inc(n, E):
    G = nx.Graph()
    for x in range(n): G.add_node(('v', x), t=0)
    for i, e in enumerate(E):
        G.add_node(('e', i), t=1)
        for x in e: G.add_edge(('e', i), ('v', x))
    return G
nm = lambda a, b: a['t'] == b['t']
built = []
for f in sys.argv[1:]: built += json.load(open(f))
bycell = collections.defaultdict(list)
for d in built:
    if d['n'] <= 26: bycell[(d['n'], d['m'], d['tau'])].append(d)
for (n, m, t), ds in sorted(bycell.items()):
    stored = [(nn, es) for (nn, es) in read_any(I + 'cell_%d_%d_%d.txt' % (n, m, t)) if max(hyp.degrees(nn, es)) <= 3]
    reps = collections.defaultdict(list)
    for (nn, es) in stored:
        G = inc(nn, es); reps[nx.weisfeiler_lehman_graph_hash(G, node_attr='t', iterations=4)].append(G)
    miss = 0; hitc = set()
    for d in ds:
        G = inc(d['n'], d['edges']); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t', iterations=4)
        ok = False
        for j, G2 in enumerate(reps.get(h, [])):
            if nx.is_isomorphic(G, G2, node_match=nm): ok = True; hitc.add((h, j)); break
        miss += not ok
    print((n, m, t), 'built', len(ds), 'not in stored list:', miss, '; stored classes hit:', len(hitc), 'of', len(stored), flush=True)
