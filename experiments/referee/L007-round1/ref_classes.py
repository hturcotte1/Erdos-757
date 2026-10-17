"""Referee: isomorphism classes, |Aut|, tau, maxdeg of 3-graphs (networkx VF2 on the vertex-edge incidence graph,
sides kept apart).  Used to validate ref_enum against the brute force ref_bf (labelled count = sum n!/|Aut|)."""
import sys, re, itertools, math, subprocess, json
import networkx as nx
from networkx.algorithms import isomorphism as iso
def parse_lines(lines, tag='G:'):
    out = []
    for l in lines:
        if l.startswith(tag):
            out.append([tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)])
    return out
def inc_graph(es):
    G = nx.Graph()
    vs = sorted(set(v for e in es for v in e))
    for v in vs: G.add_node(('v', v), side=0)
    for i, e in enumerate(es):
        G.add_node(('e', i), side=1)
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
nm = iso.categorical_node_match('side', None)
def tau(es):
    vs = sorted(set(v for e in es for v in e))
    for k in range(0, len(vs) + 1):
        for T in itertools.combinations(vs, k):
            S = set(T)
            if all(S & set(e) for e in es): return k
def maxdeg(es):
    d = {}
    for e in es:
        for v in e: d[v] = d.get(v, 0) + 1
    return max(d.values())
def classes(graphs):
    """returns list of (rep, count_of_outputs, G)"""
    buckets = {}
    reps = []
    for es in graphs:
        G = inc_graph(es)
        h = nx.weisfeiler_lehman_graph_hash(G, node_attr='side', iterations=4)
        lst = buckets.setdefault(h, [])
        for r in lst:
            if nx.is_isomorphic(G, r[2], node_match=nm):
                r[1] += 1; break
        else:
            r = [es, 1, G]; lst.append(r); reps.append(r)
    return reps
def aut(G):
    return sum(1 for _ in iso.GraphMatcher(G, G, node_match=nm).isomorphisms_iter())
