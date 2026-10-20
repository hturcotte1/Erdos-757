"""Isomorphism classes of the enumerator outputs (networkx VF2 on incidence graphs); compare two lists class by class."""
import re, sys, itertools
import networkx as nx
sys.path.insert(0, '.')
from f7check import has_f7
def parse(path):
    return [[tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)] for l in open(path) if l.startswith('FOUND:')]
def inc(es):
    G = nx.Graph()
    for i, e in enumerate(es):
        G.add_node(('e', i), t=1)
        for v in e: G.add_node(('v', v), t=0); G.add_edge(('e', i), ('v', v))
    return G
nm = lambda a, b: a['t'] == b['t']
def classes(lst):
    reps = []  # (hash, G, es)
    for es in lst:
        G = inc(es); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t')
        if not any(h == h2 and nx.is_isomorphic(G, G2, node_match=nm) for h2, G2, _ in reps): reps.append((h, G, es))
    return reps
def tau(es):
    V = sorted(set().union(*es)); masks = [sum(1 << v for v in e) for e in es]
    for k in range(len(V) + 1):
        for T in itertools.combinations(V, k):
            s = sum(1 << v for v in T)
            if all(mk & s for mk in masks): return k
def p3(es):  # e(S) <= |S|-2 for all S with |S| >= 2 (only S that are unions of edges matter; brute force over vertex subsets)
    V = sorted(set().union(*es)); n = len(V); masks = [sum(1 << v for v in e) for e in es]
    for S in range(1, 1 << (max(V) + 1)):
        c = sum(1 for mk in masks if mk & S == mk)
        if c and c > bin(S).count('1') - 2: return False
    return True
if __name__ == '__main__':
    a, b = sys.argv[1], sys.argv[2]
    A, B = parse(a), parse(b)
    ca, cb = classes(A), classes(B)
    match = all(any(h1 == h2 and nx.is_isomorphic(G1, G2, node_match=nm) for h2, G2, _ in cb) for h1, G1, _ in ca) and \
            all(any(h1 == h2 and nx.is_isomorphic(G1, G2, node_match=nm) for h2, G2, _ in ca) for h1, G1, _ in cb)
    print(a, 'labelled', len(A), 'classes', len(ca), '|', b, 'labelled', len(B), 'classes', len(cb), '| same classes:', match)
    if len(sys.argv) > 3:
        for _, _, es in ca:
            degs = {}
            for e in es:
                for v in e: degs[v] = degs.get(v, 0) + 1
            print('  class', es, 'tau', tau(es), 'F7', has_f7(es), 'P3', p3(es), 'degrees', sorted(degs.values(), reverse=True))
