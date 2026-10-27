"""Independent brute force for the small D=3 component cells not found in the refereed tarballs: (5,3,1,3)=0, (8,4,2,3)=3, (11,5,3,3)=4.
Grow connected linear 3-graphs edge by edge (each new edge meets the current vertex set; at most 1 vertex in common with every old edge;
new vertices appended), dedupe by networkx isomorphism of the incidence graph, then filter by (n,m,tau), Delta<=3 and (P3)
e(S)<=|S|-2 for all vertex sets S with |S|>=2 (F7 has 5 edges and 7 vertices, so it cannot occur for n=8,m=4 or n=11,m=5 hypertrees)."""
import itertools, networkx as nx
nm = lambda a, b: a['t'] == b['t']
def inc(edges):
    G = nx.Graph()
    for i, e in enumerate(edges):
        G.add_node(('e', i), t=1)
        for v in e: G.add_node(('v', v), t=0); G.add_edge(('e', i), ('v', v))
    return G
def tau(edges):
    es = [frozenset(e) for e in edges]; best = [len(es)]
    def rec(rem, k):
        if not rem: best[0] = min(best[0], k); return
        if k + 1 > best[0]: return
        for v in rem[0]: rec([e for e in rem if v not in e], k + 1)
    rec(es, 0); return best[0]
def p3(edges, n):
    es = [frozenset(e) for e in edges]
    for mask in range(1, 1 << n):
        S = frozenset(i for i in range(n) if mask >> i & 1)
        if len(S) >= 2 and sum(1 for e in es if e <= S) > len(S) - 2: return False
    return True
def classes(m):
    level = [[(0, 1, 2)]]
    for k in range(2, m + 1):
        nxt = []; buckets = {}
        for edges in level:
            nv = 1 + max(max(e) for e in edges)
            for new_in in range(1, 4):        # number of vertices of the new edge among old vertices
                for old in itertools.combinations(range(nv), new_in):
                    e = tuple(old) + tuple(range(nv, nv + 3 - new_in))
                    if any(len(set(e) & set(f)) > 1 for f in edges): continue
                    ne = edges + [e]
                    G = inc(ne)
                    h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t')
                    if any(nx.is_isomorphic(G, inc(R), node_match=nm) for R in buckets.get(h, [])): continue
                    buckets.setdefault(h, []).append(ne); nxt.append(ne)
        level = nxt
    return level
for (n, m, t) in [(5, 3, 1), (8, 4, 2), (11, 5, 3)]:
    cl = classes(m); cnt = 0
    for edges in cl:
        nv = 1 + max(max(e) for e in edges)
        if nv != n or tau(edges) != t: continue
        deg = [sum(1 for e in edges if v in e) for v in range(nv)]
        if max(deg) > 3 or not p3(edges, nv): continue
        cnt += 1
    print(f'cell({n},{m},{t},3): {cnt} classes (all connected linear 3-graphs with {m} edges: {len(cl)} classes)')
