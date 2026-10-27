"""Theorem 2, Step 2.4: nu(G) >= 2|E|/7 for simple graphs with Delta<=3 (random test), and the
equality case. Also the identity tau(H) = m - nu(G) for the dual 3-graph of random subcubic graphs
with pendant vertices added (own tau)."""
import random
import networkx as nx
from common import tau

random.seed(2)
worst = None; eq = 0; tested = 0
for trial in range(3000):
    n = random.randint(2, 14)
    G = nx.Graph(); G.add_nodes_from(range(n))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    random.shuffle(pairs)
    for (i, j) in pairs:
        if G.degree(i) < 3 and G.degree(j) < 3 and random.random() < 0.7:
            G.add_edge(i, j)
    E = G.number_of_edges()
    if E == 0:
        continue
    nu = len(nx.max_weight_matching(G, maxcardinality=True))
    tested += 1
    if 7 * nu < 2 * E:
        print('VIOLATION', list(G.edges()))
    if 7 * nu == 2 * E:
        eq += 1
    r = 7 * nu - 2 * E
    worst = r if worst is None else min(worst, r)
    # dual 3-graph: vertex per G-vertex is an H-edge; each G-edge is a degree-2 H-vertex; pad
    # each H-edge to 3 vertices with pendant vertices
    if trial % 10 == 0:
        H = []; nxt = E
        for w in G.nodes():
            e = set(G.edges()).__class__()
            e = set(i for i, (a, b) in enumerate(G.edges()) if w in (a, b))
            while len(e) < 3:
                e.add(nxt); nxt += 1
            H.append(frozenset(e))
        if len(H) <= 14:
            assert tau(H) == len(H) - nu, ('tau identity failed', list(G.edges()))
print(f'tested {tested} subcubic graphs: min(7nu-2|E|) = {worst}; equality cases {eq}; tau=m-nu identity asserted on the sampled duals')
