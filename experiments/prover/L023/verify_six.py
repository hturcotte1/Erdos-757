"""(L023) The 6 classes of cell(25,23,11,4) (stored list) re-verified from the definitions with verify_c.py (own code):
n = 25 labels, m = 23 distinct triples, linear, F7-free, (P3), connected, tau = 11 exactly (no 10-cover; an explicit 11-cover),
degree sequence, Delta = 4; pairwise non-isomorphic (networkx VF2 on the vertex-edge incidence graphs, independent of nauty);
for every vertex w of degree 4 the component types (n_K, m_K, tau_K) of X - w, and tau(X - v) for every v.
usage: python3 verify_six.py cell_25_23_11_D4.txt"""
import sys, re, json, itertools, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from verify_c import in_C, connected, tau_exact, degrees
import networkx as nx
from networkx.algorithms import isomorphism as iso
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def comps(E, verts):
    verts = set(verts); adj = {v: set() for v in verts}
    for e in E:
        for v in e: adj[v] |= set(e) - {v}
    out = []; seen = set()
    for s in sorted(verts):
        if s in seen: continue
        C = {s}; st = [s]
        while st:
            v = st.pop()
            for w in adj[v]:
                if w not in C: C.add(w); st.append(w)
        seen |= C; out.append(C)
    return out
def inc_graph(E, n):
    G = nx.Graph()
    G.add_nodes_from(('v', i) for i in range(n)); G.add_nodes_from(('e', j) for j in range(len(E)))
    for j, e in enumerate(E):
        for v in e: G.add_edge(('v', v), ('e', j))
    for x in G.nodes: G.nodes[x]['side'] = x[0]
    return G
graphs = [parse(l) for l in open(sys.argv[1]) if l.startswith('FOUND:')]
allok = True
for gi, E in enumerate(graphs):
    n = 25
    ok, why = in_C(E, n)
    con = connected(E, n)
    t, cov = tau_exact(E, n)
    d = degrees(E, n)
    deg4 = [v for v in range(n) if d[v] == 4]
    types = collections.Counter()
    for w in deg4:
        Ew = [e for e in E if w not in e]
        cs = comps(Ew, [v for v in range(n) if v != w])
        ty = []
        for C in cs:
            EC = [e for e in Ew if set(e) <= C]
            idx = {v: i for i, v in enumerate(sorted(C))}
            EC2 = [tuple(idx[v] for v in e) for e in EC]
            ty.append((len(C), len(EC), tau_exact(EC2, len(C))[0] if EC2 else 0))
        types[tuple(sorted(ty, reverse=True))] += 1
    tv = collections.Counter()
    for v in range(n):
        Ev = [e for e in E if v not in e]
        idx = {u: i for i, u in enumerate([u for u in range(n) if u != v])}
        tv[tau_exact([tuple(idx[u] for u in e) for e in Ev], n - 1)[0]] += 1
    good = ok and con and t == 11 and len(E) == 23 and len(set(map(frozenset, E))) == 23 and max(d) == 4
    allok &= good
    print('CLASS %d: m=%d in_C=%s (%s) connected=%s tau=%d (cover %s) degree_sequence=%s Delta=%d deg4_vertices=%s X-w_types=%s tau(X-v)_counts=%s %s' % (
        gi, len(E), ok, why, con, t, cov, dict(sorted(collections.Counter(d).items())), max(d), deg4, dict(types), dict(tv), 'OK' if good else 'FAIL'), flush=True)
# pairwise non-isomorphism (VF2 with the two sides kept)
G = [inc_graph(E, 25) for E in graphs]
nm = iso.categorical_node_match('side', None)
noniso = True
for i, j in itertools.combinations(range(len(G)), 2):
    if nx.is_isomorphic(G[i], G[j], node_match=nm):
        noniso = False; print('ISOMORPHIC PAIR', i, j)
print('pairwise non-isomorphic:', noniso)
print('RESULT all %d classes are connected members of C with (n,m,tau) = (25,23,11) and Delta = 4: %s' % (len(graphs), allok))
