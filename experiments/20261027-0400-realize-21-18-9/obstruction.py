"""For each of the 12 classes: smallest k such that the first k edges (in the search order) form a non-realizable sub-hypergraph
(exact test, same decide(), restricted to the vertices they cover).  Gives an explicit small obstruction (necessary: a set realizing the
whole hypergraph contains a realization of every sub-hypergraph, as the AP hypergraph of the sub-point-set only gains/keeps the edges)."""
import json
from rexact import *
res = json.load(open('results_main_21_18_9.json')); out = []
for r in res:
    E = [tuple(e) for e in r['edges']]; order = order_edges(E)
    for k in range(3, len(E) + 1):
        sub = [E[i] for i in order[:k]]
        vs = sorted({v for e in sub for v in e}); mp = {v: i for i, v in enumerate(vs)}
        sub2 = [tuple(mp[v] for v in e) for e in sub]
        sols, st = decide(sub2, len(vs), find_all=False)
        if not sols:
            out.append(dict(cls=r['cls'], k=k, nverts=len(vs), subedges=sub)); print(r['cls'], 'min k', k, 'verts', len(vs), flush=True); break
json.dump(out, open('obstructions.json', 'w'))
