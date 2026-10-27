# enumerate induced subgraphs of tight/record sets with slack<=1 (connected), dedupe by WL hash; save pieces.json
import sys, json, itertools, collections
from common import *
import networkx as nx
P, cls = load_pieces()
def inc_graph(n, edges):
    G = nx.Graph()
    for v in range(n): G.add_node(('v', v), t='v')
    for i, e in enumerate(edges):
        G.add_node(('e', i), t='e')
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
def wl(n, edges): return nx.weisfeiler_lehman_graph_hash(inc_graph(n, edges), node_attr='t', iterations=5)
found = {}  # hash -> (n,m,tau,slack,edges)
sources = {'Abase': P['Abase'], 'rec12': P['rec12'], 'rec12b': P['rec12b'], 'rec12c': P['rec12c'], 'rec11': P['rec11'], 'rec10': P['rec10'], 'rec8': P['rec8']}
import random; random.seed(5)
for k in random.sample(range(len(cls)), 40): sources['cls%d' % k] = cls[k]
stat = collections.Counter()
for name, (n, edges) in sources.items():
    batch = []; subs = []
    for mask in range(1 << n):
        S = [v for v in range(n) if mask >> v & 1]
        if len(S) < 3: continue
        nn, ee = induced(n, edges, S)
        if not ee: continue
        batch.append(line(nn, ee)); subs.append((nn, ee))
        if len(batch) == 20000 or mask == (1 << n) - 1:
            res = run_eval(batch)
            for (nn, ee), r in zip(subs, res):
                assert r[4] == 0
                if r[3] <= 1 and r[6] == 1 and r[7] == 0:  # connected, no isolated
                    h = wl(nn, ee)
                    if h not in found: found[h] = (nn, len(ee), r[2], r[3], ee, name)
            batch = []; subs = []
    print(name, len(found), flush=True)
out = [dict(n=v[0], m=v[1], tau=v[2], slack=v[3], edges=v[4], src=v[5]) for v in found.values()]
out.sort(key=lambda d: (d['slack'], d['n'], d['m']))
json.dump(out, open('pieces.json', 'w'))
c = collections.Counter((d['n'], d['m'], d['tau'], d['slack']) for d in out)
for k in sorted(c): print(k, c[k])
