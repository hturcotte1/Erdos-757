"""(L023) The AP hypergraph of the judged 21-point set C006 is isomorphic (VF2) to class 43 of the stored list cell(21,19,9,4)
(experiments/20261027-0340-induction-n28-n29-f25/lists/cell_21_19_9_D4.txt), the class rexact reports as REAL."""
import sys, json, re
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import ap_edges
import networkx as nx
from networkx.algorithms import isomorphism as iso
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def inc(E, n):
    G = nx.Graph()
    for i in range(n): G.add_node(('v', i), side='v')
    for j, e in enumerate(E):
        G.add_node(('e', j), side='e')
        for v in e: G.add_edge(('v', v), ('e', j))
    return G
A = json.load(open('/home/user/Erdos-757/results/claims/C006-tight-21pt-h12.json'))['set']
idx = {x: i for i, x in enumerate(sorted(A))}
E = [tuple(sorted(idx[v] for v in e)) for e in ap_edges(A)]
L = [parse(l) for l in open('/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/lists/cell_21_19_9_D4.txt') if l.startswith('FOUND:')]
nm = iso.categorical_node_match('side', None)
G = inc(E, 21)
print('C006: 21 points,', len(E), 'APs; isomorphic to class 43 of cell(21,19,9,4):', nx.is_isomorphic(G, inc(L[43], 21), node_match=nm))
