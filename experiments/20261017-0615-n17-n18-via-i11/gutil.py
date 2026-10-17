import networkx as nx
def graph(es):
    G=nx.Graph()
    for i,e in enumerate(es):
        G.add_node(('e',i),t=1)
        for v in e: G.add_node(('v',v),t=0); G.add_edge(('e',i),('v',v))
    return G
