"""defcheck.py [TAG] < lines : definitional membership test for the class C, written for referee L009 round 2.
For each hypergraph line (tuples "(a,b,c)"): linear (every pair of edges shares <= 1 vertex); F7 (a colour-preserving
subgraph MONOMORPHISM of the incidence graph of F7 = {012,034,056,135,246} into the incidence graph of H, found by networkx's
generic matcher, i.e. an injective map of the 7 points and 5 edges preserving incidence); (P3) e(S) <= |S|-2 for every vertex
subset S with |S| >= 2 (all 2^n subsets); tau by brute force over vertex subsets in increasing size.  Prints one line per graph."""
import sys, re, itertools
import networkx as nx
from networkx.algorithms import isomorphism as iso
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def inc_graph(es):
    G = nx.Graph()
    for v in {v for e in es for v in e}: G.add_node(('p', v), c='p')
    for j, e in enumerate(es):
        G.add_node(('e', j), c='e')
        for v in e: G.add_edge(('p', v), ('e', j))
    return G
GF = inc_graph(F7)
def has_f7(es):
    GH = inc_graph(es)
    GM = iso.GraphMatcher(GH, GF, node_match=lambda a, b: a['c'] == b['c'])
    for _ in GM.subgraph_monomorphisms_iter():
        return True
    return False
def linear(es):
    return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(es, 2))
def p3(es, n):
    masks = [sum(1 << v for v in e) for e in es]
    for S in range(1 << n):
        k = bin(S).count('1')
        if k < 2: continue
        if sum(1 for e in masks if e & S == e) > k - 2: return False
    return True
def tau(es, n):
    for k in range(n + 1):
        for T in itertools.combinations(range(n), k):
            T = set(T)
            if all(T & set(e) for e in es): return k
tag = sys.argv[1] if len(sys.argv) > 1 else None
for line in sys.stdin:
    if tag and not line.startswith(tag): continue
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]
    if not es: continue
    n = max(v for e in es for v in e) + 1
    lin = linear(es); f7 = has_f7(es); ok3 = p3(es, n)
    print("DEF n=%d m=%d linear=%d f7=%d p3=%d C=%d tau=%d" % (n, len(es), lin, f7, ok3, int(lin and not f7 and ok3), tau(es, n)))
