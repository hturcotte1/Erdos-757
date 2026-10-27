"""(L023) For every X_i and every vertex w of degree 4 such that X_i - w has a component K of type (14,12,6): the isomorphism class of K
among the 11 classes of the refereed list cell(14,12,6,4) (VF2), and the verdict of realize_sdr on K itself."""
import sys, re, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def comps(E, verts):
    verts = set(verts); adj = {v: set() for v in verts}
    for e in E:
        for v in e: adj[v] |= set(e) - {v}
    out = []; seen = set()
    for s0 in sorted(verts):
        if s0 in seen: continue
        C = {s0}; st = [s0]
        while st:
            v = st.pop()
            for x in adj[v]:
                if x not in C: C.add(x); st.append(x)
        seen |= C; out.append(C)
    return out
def inc_graph(E, n):
    import networkx as nx
    G = nx.Graph()
    for i in range(n): G.add_node(('v', i), side='v')
    for j, e in enumerate(E):
        G.add_node(('e', j), side='e')
        for v in e: G.add_edge(('v', v), ('e', j))
    return G
import networkx as nx
from networkx.algorithms import isomorphism as iso
from realize_sdr import decide
from verify_c import degrees
L14 = [parse(l) for l in open('topcell/cells/cell_14_12_6_D4.txt') if l.startswith('FOUND:')]
G14 = [inc_graph(E, 14) for E in L14]
nm = iso.categorical_node_match('side', None)
graphs = [parse(l) for l in open('cell_25_23_11_D4.txt') if l.startswith('FOUND:')]
for gi, E in enumerate(graphs):
    d = degrees(E, 25)
    for w in [v for v in range(25) if d[v] == 4]:
        Ew = [e for e in E if w not in e]
        for C in comps(Ew, [v for v in range(25) if v != w]):
            EC = [e for e in Ew if set(e) <= C]
            if len(C) == 14 and len(EC) == 12:
                idx = {v: i for i, v in enumerate(sorted(C))}
                K = [tuple(idx[v] for v in e) for e in EC]
                Gk = inc_graph(K, 14)
                cls = [j for j, H in enumerate(G14) if nx.is_isomorphic(Gk, H, node_match=nm)]
                st, ex = decide(K, 14)
                print('X_%d w=%d: (14,12,6) component = class %s of cell(14,12,6,4); realize_sdr: %s %s' % (gi, w, cls, 'REALIZABLE' if st['REAL'] else 'NOT-REALIZABLE', json.dumps(st)), flush=True)
