"""Independent check of cell(27,13,9,3): connected members of C with n=27, m=13, tau=9, Delta<=3.
n=2m+1 forces a linear hypertree (all such are in C: F7 has cycles; e(S)<=(|S|-1)/2 <= |S|-2).  tau=9 and acyclic => tau=nu=9
(Konig for hypertrees), so 9 disjoint edges ('blocks') cover all 27 vertices, the other 4 edges are connectors meeting 3 different
blocks in one vertex each, and contracting blocks gives a 3-uniform linear hypertree T on 9 nodes with 4 edges.
Enumerate T (grown by leaf edges), then per block the set partitions of its connectors into parts of size <=2 (Delta<=3), dedupe
by networkx isomorphism, brute-force tau = 9 and compare with the engine list (as isomorphism classes)."""
import itertools, sys, re
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
def inc_graph(edges):
    G = nx.Graph()
    for i, e in enumerate(edges):
        G.add_node(('e', i), t=1)
        for v in e: G.add_node(('v', v), t=0); G.add_edge(('e', i), ('v', v))
    return G
nm = lambda a, b: a['t'] == b['t']
def set_partitions_max2(items):
    items = list(items)
    if not items: yield []; return
    a = items[0]; rest = items[1:]
    for p in set_partitions_max2(rest):          # a alone
        yield [[a]] + p
    for i, b in enumerate(rest):                  # a with b
        r2 = rest[:i] + rest[i+1:]
        for p in set_partitions_max2(r2): yield [[a, b]] + p
def partitions_le3(items):
    return [p for p in set_partitions_max2(items) if len(p) <= 3]
# hypertrees T
Ts = []
def grow(edges, nn):
    if len(edges) == 4: Ts.append((list(edges), nn)); return
    for a in range(nn):
        grow(edges + [(a, nn, nn + 1)], nn + 2)
grow([(0, 1, 2)], 3)
assert all(nn == 9 for _, nn in Ts)
# dedupe T up to isomorphism
reps = []
for T, _ in Ts:
    G = inc_graph(T)
    if not any(nx.is_isomorphic(G, inc_graph(R), node_match=nm) for R in reps): reps.append(T)
print('hypertree shapes T (4 edges, 9 nodes):', len(reps))
classes = []
def tau(edges):
    es = [frozenset(e) for e in edges]; best = len(es)
    for k in range(1, len(es) + 1):
        pass
    # exact via recursion
    best = [len(es)]
    def rec(rem, k):
        if not rem: best[0] = min(best[0], k); return
        if k + 1 > best[0]: return
        for v in rem[0]: rec([e for e in rem if v not in e], k + 1)
    rec(es, 0); return best[0]
for T in reps:
    # connectors at each block
    at = {b: [ci for ci, e in enumerate(T) if b in e] for b in range(9)}
    opts = [partitions_le3(at[b]) for b in range(9)]
    for choice in itertools.product(*opts):
        # vertex id of block b position j: 3b+j ; connector ci vertex in block b
        conn = [[None]*3 for _ in T]
        for b in range(9):
            for j, part in enumerate(choice[b]):
                for ci in part: conn[ci][T[ci].index(b)] = 3*b + j
        edges = [(3*b, 3*b+1, 3*b+2) for b in range(9)] + [tuple(c) for c in conn]
        G = inc_graph(edges)
        if not any(nx.is_isomorphic(G, inc_graph(R), node_match=nm) for R in classes): classes.append(edges)
print('classes (blocks+connectors, Delta<=3):', len(classes))
assert all(tau(e) == 9 for e in classes)
# engine list
eng = []
for l in open('out/cells/cell_27_13_9_D3.txt'):
    if l.startswith('FOUND'): eng.append([tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)])
print('engine classes:', len(eng))
match = 0
for g in eng:
    G = inc_graph(g)
    if any(nx.is_isomorphic(G, inc_graph(R), node_match=nm) for R in classes): match += 1
print('engine classes matched to independent list:', match, 'of', len(eng), '; independent list size', len(classes))
