# referee: which subcubic simple graphs G have 7 nu(G) = 2|E(G)| ?  (equality in Theorem 2)
import random, networkx as nx
random.seed(20261027)
graphs = [g for g in nx.graph_atlas_g() if g.number_of_nodes() >= 1 and (g.number_of_edges() == 0 or max(d for _, d in g.degree()) <= 3)]
for _ in range(20000):
    N = random.randint(2, 18)
    G = nx.Graph(); G.add_nodes_from(range(N))
    target = random.randint(0, (3 * N) // 2); tries = 0
    while G.number_of_edges() < target and tries < 20 * N:
        tries += 1
        a, b = random.sample(range(N), 2)
        if G.has_edge(a, b) or G.degree(a) >= 3 or G.degree(b) >= 3:
            continue
        G.add_edge(a, b)
    graphs.append(G)
K4s = nx.complete_graph(4); K4s.remove_edge(0, 1); K4s.add_edges_from([(0, 4), (4, 1)])
eq = 0; bad = 0
for G in graphs:
    if G.number_of_edges() == 0:
        continue
    nu = len(nx.max_weight_matching(G, maxcardinality=True))
    assert 7 * nu >= 2 * G.number_of_edges()
    if 7 * nu == 2 * G.number_of_edges():
        eq += 1
        for comp in nx.connected_components(G):
            H = G.subgraph(comp)
            if H.number_of_edges() == 0:
                continue
            if not nx.is_isomorphic(H, K4s):
                bad += 1
print('graphs', len(graphs), 'equality cases with |E|>0:', eq, 'components not K4-with-subdivided-edge:', bad)
