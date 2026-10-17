"""Check the descriptive (non-load-bearing) claims of C4 and the Sanity section about the 3,186 hits."""
import sys, re
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L007-round1')
from ref_f7 import f7_copies, has_f7
from ref_classes import inc_graph, nm, maxdeg
import networkx as nx
def parse(path, tag):
    out = []
    for l in open(path):
        if l.startswith(tag):
            out.append([tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)])
    return out
hits = parse('/home/user/Erdos-757/experiments/referee/L007-round1/rerun/c4_hits.txt', 'HIT:')
g13 = set(tuple(sorted(g)) for g in parse('/home/user/Erdos-757/experiments/referee/L007-round1/rerun/c2_13_8_5.txt', 'FOUND:'))
from13 = from10f7 = from10free = free_all13 = 0
for h in hits:
    G = h[:8]
    if tuple(sorted(G)) in g13: from13 += 1; continue
    assert (10, 11, 12) in G
    C = [e for e in G if e != (10, 11, 12)]
    if has_f7(C): from10f7 += 1
    else:
        from10free += 1
        if all(any(13 in h[i] for i in cp) for cp in f7_copies(h)): free_all13 += 1
print('hits', len(hits), 'from (13,8,5):', from13, 'from F7-containing (10,7,4):', from10f7, 'from F7-free (10,7,4):', from10free, 'of which every F7 copy uses 13:', free_all13)
D14 = [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
GD = inc_graph(D14)
d3 = [h for h in hits if maxdeg(h) == 3]; d4 = [h for h in hits if maxdeg(h) == 4]
print('maxdeg 3:', len(d3), 'maxdeg 4:', len(d4), 'other:', len(hits) - len(d3) - len(d4))
print('all maxdeg-3 hits isomorphic to D14:', all(nx.is_isomorphic(inc_graph(h), GD, node_match=nm) for h in d3))
mine = parse('/home/user/Erdos-757/experiments/referee/L007-round1/out/ref_ext_hits.txt', 'HIT:')
m3 = [h for h in mine if maxdeg(h) == 3]
print('referee Route-I hits with maxdeg 3:', len(m3), 'all isomorphic to D14:', all(nx.is_isomorphic(inc_graph(h), GD, node_match=nm) for h in m3))
