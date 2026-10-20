"""Descriptive claims about the 3,186 extension hits (C4 and Sanity checks), recomputed with my own code (det_A copies)."""
import re, itertools, collections, json
import networkx as nx
from f7_ref import COPIES, inc, det_A
def parse(p, tag):
    return [frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([0-9,]+)\)', l)) for l in open(p) if l.startswith(tag)]
a = parse('rerun/ext_vertex_hits_mine_input.txt', 'HIT:'); b = parse('rerun/ext_indep_hits_mine_input.txt', 'HIT:')
c = parse('rerun/ext_vertex_hits.txt', 'HIT:')
print('hits: ext_vertex_all(my input)', len(a), 'ext_indep(my input)', len(b), 'ext_vertex_all(stored input)', len(c), '; equal as sets:', set(a) == set(b) == set(c))
def copies(es):
    out = []
    for five in itertools.combinations(sorted(es), 5):
        U = sorted(set().union(*five))
        if len(U) != 7: continue
        r = {v: i for i, v in enumerate(U)}
        if frozenset(tuple(sorted(r[v] for v in e)) for e in five) in COPIES: out.append(five)
    return out
D14 = [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
GD = inc(D14); nm = lambda x, y: x['t'] == y['t']
cnt = collections.Counter(); md = collections.Counter(); iso = 0
for h in b:
    G = [e for e in h if 13 not in e]
    if (10, 11, 12) in G and all(max(e) <= 9 for e in G if e != (10, 11, 12)):
        C = [e for e in G if e != (10, 11, 12)]
        typ = '10-7-4 with F7' if det_A(C) else '10-7-4 F7-free'
    else:
        typ = '13-8-5'
    cps = copies(h); via = all(any(13 in e for e in cp) for cp in cps)
    cnt[(typ, via)] += 1
    deg = collections.Counter(v for e in h for v in e); d = max(deg.values()); md[d] += 1
    if d <= 3 and nx.is_isomorphic(inc(sorted(h)), GD, node_match=nm): iso += 1
print({'%s | every F7 copy uses 13: %s' % k: v for k, v in sorted(cnt.items())})
print('max degree histogram', dict(sorted(md.items())), 'max-degree-3 hits isomorphic to D14:', iso)
