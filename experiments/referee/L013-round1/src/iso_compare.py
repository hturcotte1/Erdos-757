"""Compare two lists of hypergraphs (FOUND/HIT lines) as sets of isomorphism classes, using networkx VF2 on the
vertex/edge incidence graph with a node attribute (independent of nauty).  Usage: iso_compare.py nv fileA fileB
Prints: classes in A, classes in B (each list reduced to classes), A-not-in-B, B-not-in-A, duplicates within each list."""
import sys, re, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
def read(fn):
    out = []
    for l in open(fn):
        if l.startswith('FOUND') or l.startswith('HIT'):
            out.append([tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)])
    return out
def inc(nv, es):
    G = nx.Graph()
    for v in range(nv): G.add_node(('v', v), k=0)
    for i, e in enumerate(es):
        G.add_node(('e', i), k=1)
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
def key(G):
    return nx.weisfeiler_lehman_graph_hash(G, node_attr='k', iterations=4)
def iso(G, H):
    return GraphMatcher(G, H, node_match=lambda a, b: a['k'] == b['k']).is_isomorphic()
def classes(nv, L):
    buckets = {}; reps = []; dups = 0
    for es in L:
        G = inc(nv, es); k = key(G)
        found = False
        for H in buckets.get(k, []):
            if iso(G, H): found = True; break
        if found: dups += 1; continue
        buckets.setdefault(k, []).append(G); reps.append((k, G))
    return buckets, reps, dups
if __name__ == '__main__':
    nv = int(sys.argv[1]); A = read(sys.argv[2]); B = read(sys.argv[3])
    for es in A + B:
        assert all(0 <= v < nv for e in es for v in e), 'vertex out of range'
    bA, rA, dA = classes(nv, A); bB, rB, dB = classes(nv, B)
    def missing(r, b):
        c = 0
        for k, G in r:
            if not any(iso(G, H) for H in b.get(k, [])): c += 1
        return c
    print('A lines %d classes %d dups %d | B lines %d classes %d dups %d | A-not-in-B %d | B-not-in-A %d | %s' % (
        len(A), len(rA), dA, len(B), len(rB), dB, missing(rA, bB), missing(rB, bA),
        'EQUAL' if missing(rA, bB) == 0 and missing(rB, bA) == 0 else 'DIFFERENT'))
