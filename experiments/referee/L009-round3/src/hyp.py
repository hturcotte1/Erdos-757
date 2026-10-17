"""Referee L009 round 3: DEFINITIONAL checks for 3-graphs given as 'TAG: (a,b,c) ...' lines (any tag).
 - linear: every two edges share <= 1 vertex
 - F7: some 5 edges form a subhypergraph isomorphic to F7 = {012,034,056,135,246}; tested with networkx
   is_isomorphic on 2-coloured incidence graphs (vertices vs edges), over all 5-subsets of edges whose union has 7 vertices
 - P3: e(S) <= |S|-2 for every vertex subset S with |S| >= 2 (all subsets)
 - tau: least k such that some k-subset of vertices meets every edge (itertools.combinations)
 - connected, max degree, n (= number of vertices present, or N1 if given)
Usage: hyp.py [N1] < lines ;  prints one line per graph: 'CHK n=.. m=.. tau=.. f7=.. p3=.. C=.. lin=.. conn=.. dmax=..: <edges>'"""
import sys, re, itertools
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def incidence(edges):
    G = nx.Graph()
    vs = sorted({v for e in edges for v in e})
    for v in vs: G.add_node(('v', v), side=0)
    for j, e in enumerate(edges):
        G.add_node(('e', j), side=1)
        for v in e: G.add_edge(('v', v), ('e', j))
    return G
F7G = incidence(F7)
def is_f7(edges5):
    G = incidence(edges5)
    if G.number_of_nodes() != 12: return False
    return GraphMatcher(G, F7G, node_match=lambda a, b: a['side'] == b['side']).is_isomorphic()
def contains_f7(edges):
    for sub in itertools.combinations(edges, 5):
        if len(set().union(*map(set, sub))) != 7: continue
        if is_f7(list(sub)): return True
    return False
def linear(edges):
    return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(edges, 2))
def p3(edges, vs):
    es = [frozenset(e) for e in edges]
    for k in range(2, len(vs) + 1):
        for S in itertools.combinations(vs, k):
            Sset = set(S)
            if sum(1 for e in es if e <= Sset) > k - 2: return False
    return True
def tau(edges, vs):
    es = [set(e) for e in edges]
    for k in range(0, len(vs) + 1):
        for S in itertools.combinations(vs, k):
            Sset = set(S)
            if all(e & Sset for e in es): return k
def connected(edges, vs):
    G = nx.Graph(); G.add_nodes_from(vs)
    for e in edges: G.add_edge(e[0], e[1]); G.add_edge(e[0], e[2])
    return nx.is_connected(G)
def main():
    N1 = int(sys.argv[1]) if len(sys.argv) > 1 else None
    for line in sys.stdin:
        if ':' not in line: continue
        body = line.split(':', 1)[1]
        edges = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', body)]
        if not edges: continue
        vs = sorted({v for e in edges for v in e}) if N1 is None else list(range(N1))
        deg = {v: 0 for v in vs}
        for e in edges:
            for v in e: deg[v] += 1
        lin = linear(edges); f7 = contains_f7(edges); ok3 = p3(edges, vs); t = tau(edges, vs); cn = connected(edges, vs)
        print("CHK n=%d m=%d tau=%d f7=%d p3=%d C=%d lin=%d conn=%d dmax=%d:%s" % (len(vs), len(edges), t, f7, ok3, int(lin and not f7 and ok3), lin, cn, max(deg.values()), ' '.join('(%d,%d,%d)' % e for e in edges)))
if __name__ == '__main__': main()
