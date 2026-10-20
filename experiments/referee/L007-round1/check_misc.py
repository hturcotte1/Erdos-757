import sys, re, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L007-round1')
from ref_f7 import has_f7, is_linear, f7_copies
from ref_classes import inc_graph, nm, tau, classes
import networkx as nx
R = '/home/user/Erdos-757/experiments/referee/L007-round1/'
F = '/home/user/Erdos-757/experiments/falsify/i11-inequality/'
def keyset(path, tag):
    S = []
    for l in open(path):
        if l.startswith(tag):
            S.append(tuple(sorted(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l))))
    return S
for a, b in [('rerun/e2_13_8_5.txt', 'rerun/c2_13_8_5.txt'), ('rerun/e2_10_7_4.txt', 'rerun/c2_10_7_4.txt')]:
    A = keyset(R + a, 'FOUND:'); B = keyset(R + b, 'FOUND:')
    print(a, len(A), 'distinct', len(set(A)), '|', b, len(B), 'distinct', len(set(B)), '| equal sets:', set(A) == set(B))
# rebuild the 796-line extension input (in the referee folder) and compare with the stored falsifier input
g13 = keyset(R + 'rerun/c2_13_8_5.txt', 'FOUND:'); g10 = keyset(R + 'rerun/c2_10_7_4.txt', 'FOUND:')
mine = [tuple(sorted(g)) for g in g13] + [tuple(sorted(list(g) + [(10, 11, 12)])) for g in g10]
stored = []
for l in open(F + 'ext_vertex_input.txt'):
    t = list(map(int, l.split())); stored.append(tuple(sorted(tuple(sorted(t[1 + 3*i: 4 + 3*i])) for i in range(t[0]))))
print('ext input: stored', len(stored), 'distinct', len(set(stored)), '| rebuilt', len(mine), '| equal multisets:', sorted(stored) == sorted(mine))
# the two hit lists equal as sets?
H1 = keyset(R + 'rerun/c4_hits.txt', 'HIT:'); H2 = keyset(R + 'rerun/c4_indep_hits.txt', 'HIT:')
print('hit lists: ext_vertex_all', len(H1), 'ext_indep', len(H2), 'distinct', len(set(H1)), len(set(H2)), 'equal sets:', set(H1) == set(H2))
# explicit (13,8,5) graphs of C2
X1 = [(0,1,2),(2,3,4),(3,5,6),(4,7,8),(4,9,10),(7,11,12),(8,9,11),(8,10,12)]
X2 = [(0,1,2),(2,3,4),(3,5,6),(4,7,8),(4,9,10),(4,11,12),(7,9,11),(8,10,12)]
cl = classes([list(g) for g in g13])
for X in (X1, X2):
    print('explicit (13,8,5) graph: tau', tau(X), 'linear', is_linear(X), 'F7', has_f7(X), 'copies', f7_copies(X),
          'isomorphic to one of the 2 classes:', [nx.is_isomorphic(inc_graph(X), r[2], node_match=nm) for r in cl])
print('X1 vs X2 isomorphic:', nx.is_isomorphic(inc_graph(X1), inc_graph(X2), node_match=nm))
d = json.load(open(F + 'f7free_nonO_violation_9_8_4.json'))
es = [tuple(e) for e in d['edges']]
n = len(set(v for e in es for v in e))
print('f7free_nonO_violation: n', n, 'm', len(es), 'tau', tau(es), 'linear', is_linear(es), 'F7', has_f7(es), 's', 3*n + 2*len(es) - 11*tau(es))
