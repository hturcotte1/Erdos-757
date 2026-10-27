"""(L023) Q8 is isomorphic to the configuration of the six lines of AG(2,3) through two points a, b other than the line ab,
on the 8 points other than the third point of the line ab (VF2 check)."""
import itertools, networkx as nx
from networkx.algorithms import isomorphism as iso
P = [(x, y) for x in range(3) for y in range(3)]
lines = set()
for p, q in itertools.combinations(P, 2):
    r = ((-p[0] - q[0]) % 3, (-p[1] - q[1]) % 3)   # third point of the line through p, q in AG(2,3): p + q + r = 0
    lines.add(frozenset((p, q, r)))
assert len(lines) == 12
a, b = (0, 0), (1, 0); c = ((-a[0] - b[0]) % 3, (-a[1] - b[1]) % 3)
L = [l for l in lines if (a in l or b in l) and not (a in l and b in l)]
pts = [x for x in P if x != c]; idx = {x: i for i, x in enumerate(pts)}
E1 = [tuple(sorted(idx[v] for v in l)) for l in L]
Q8 = [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 7, 2)]
def inc(E, n):
    G = nx.Graph()
    for i in range(n): G.add_node(('v', i), side='v')
    for j, e in enumerate(E):
        G.add_node(('e', j), side='e')
        for v in e: G.add_edge(('v', v), ('e', j))
    return G
print('AG(2,3) piece: %d lines on %d points; isomorphic to Q8: %s' % (len(E1), len(pts), nx.is_isomorphic(inc(E1, 8), inc(Q8, 8), node_match=iso.categorical_node_match('side', None))))
