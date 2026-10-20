"""Breakdown of the 3,186 extension hits (ext_indep_hits.txt): type of G, whether every F7 copy uses the new vertex 13,
maximum degree, and (for maximum degree <= 3) isomorphism with D14 = f7_containing_violation.json (two F7's joined by an edge)."""
import re, json, itertools, collections
import networkx as nx
from f7check import has_f7
from iso_compare import inc, nm
def f7copies(es):
    out = []
    for five in itertools.combinations(es, 5):
        deg = {}
        for e in five:
            for v in e: deg[v] = deg.get(v, 0) + 1
        if len(deg) == 7 and sorted(deg.values()) == [2, 2, 2, 2, 2, 2, 3]: out.append(five)
    return out
hits = [[tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)] for l in open('ext_indep_hits.txt') if l.startswith('HIT:')]
ex = [tuple(e) for e in json.load(open('/home/user/Erdos-757/experiments/falsify/i11-inequality/f7_containing_violation.json'))['edges']]
Gx = inc(ex); hx = nx.weisfeiler_lehman_graph_hash(Gx, node_attr='t')
c = collections.Counter(); md_hist = collections.Counter(); iso = 0
for h in hits:
    G = [e for e in h if 13 not in e]
    typ = '13-8-5' if not ((10, 11, 12) in G and all(max(e) <= 9 for e in G if e != (10, 11, 12))) else ('10-7-4 with F7' if has_f7(G) else '10-7-4 F7-free')
    via_v = all(any(13 in e for e in cp) for cp in f7copies(h))
    c[(typ, 'every F7 copy uses v' if via_v else 'some F7 copy avoids v')] += 1
    d = collections.Counter(v for e in h for v in e); md = max(d.values()); md_hist[md] += 1
    if md <= 3:
        Gh = inc(h)
        if nx.weisfeiler_lehman_graph_hash(Gh, node_attr='t') == hx and nx.is_isomorphic(Gh, Gx, node_match=nm): iso += 1
for k, v in sorted(c.items()): print(k, v)
print('max-degree histogram:', dict(sorted(md_hist.items())), '; hits with max degree <= 3 isomorphic to D14:', iso)
