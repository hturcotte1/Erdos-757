"""Tally minimal forbidden cores with <= 4 edges (data/forbidden_ordered_n7.json, _n8.json) by the unlabeled
configuration (hypergraph) they live on.  Usage: python3 tally_cores.py"""
import json, itertools
from collections import Counter
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

def inc(edges):
    G = nx.Graph()
    for t, e in enumerate(edges):
        G.add_node(("e", t), k=1)
        for v in e:
            G.add_node(("v", v), k=0); G.add_edge(("e", t), ("v", v))
    return G

REF = {
 "single edge": [(0,1,2)], "two edges sharing a vertex": [(0,1,2),(0,3,4)],
 "two disjoint edges": [(0,1,2),(3,4,5)],
 "triangle": [(0,1,2),(0,3,4),(1,3,5)], "path of 3": [(0,1,2),(0,3,4),(1,5,6)], "star of 3": [(0,1,2),(0,3,4),(0,5,6)],
 "Pasch": [(0,1,2),(0,3,4),(1,3,5),(2,4,5)],
 "triangle+pendant at corner": [(0,1,2),(0,3,4),(0,5,6),(1,3,7)],
 "star3+transversal": [(0,1,2),(0,3,4),(0,5,6),(1,3,5)],
 "triangle+pendant at private vertex": [(0,1,2),(0,3,4),(1,5,6),(2,3,7)],
 "4-cycle": [(0,1,2),(0,3,4),(1,5,6),(3,5,7)],
 "two triangles sharing two edges": [(0,1,2),(0,3,4),(1,5,6),(2,3,5)],
}
def name(edges):
    for k, r in REF.items():
        if len(r) == len(edges) and GraphMatcher(inc(r), inc(edges), node_match=lambda a, b: a["k"] == b["k"]).is_isomorphic():
            return k
    return "other (" + str(len(edges)) + " edges, e.g. path/star of 4, disconnected)"
t = Counter()
for f in ["data/forbidden_ordered_n7.json", "data/forbidden_ordered_n8.json"]:
    for c in json.load(open("../../" + f))["cores"]:
        if len(c["edges"]) <= 4:
            t[(c["n"], name(c["edges"]), c["kind"], len(c["edges"]))] += 1
for k, v in sorted(t.items()):
    print(f"n={k[0]} {k[1]} [{k[3]} edges] kind={k[2]}: {v}")
