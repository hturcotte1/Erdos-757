"""(L012) Tests of bin/canon: (1) invariance: 5 random relabellings of each of the 699 route-4 classes and of every class of the cells
(14,12,6,4), (12,10,5,4), (19,16,8,4) have the canonical form of the original; (2) separation: within each of these lists, every pair
of classes with equal degree sequences is non-isomorphic by networkx's VF2 test on the incidence graphs (vertex/edge colours)."""
import random, re, subprocess, os, itertools, collections
import networkx as nx
from networkx.algorithms import isomorphism as iso
HERE = os.path.dirname(os.path.abspath(__file__)); random.seed(12)
def canon(lines, nv):
    return subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(nv)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
def edges(l): return [tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]
def line(es): return 'FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es)
def inc(es, nv):
    G = nx.Graph()
    for v in range(nv): G.add_node(('v', v), c=0)
    for i, e in enumerate(es):
        G.add_node(('e', i), c=1)
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
for path, nv in [('out/route4_classes_only.txt', 23), ('out/cells/cell_14_12_6_D4.txt', 14), ('out/cells/cell_12_10_5_D4.txt', 12), ('out/cells/cell_19_16_8_D4.txt', 19)]:
    L = [l.strip() for l in open(path) if l.startswith('FOUND:')]
    base = canon(L, nv); rel = []
    for l in L:
        es = edges(l)
        for _ in range(5):
            p = list(range(nv)); random.shuffle(p); es2 = [tuple(sorted(p[v] for v in e)) for e in es]; random.shuffle(es2); rel.append(line(es2))
    c2 = canon(rel, nv); inv = all(c2[5 * i + j] == base[i] for i in range(len(L)) for j in range(5))
    groups = collections.defaultdict(list)
    for i, l in enumerate(L):
        es = edges(l); d = collections.Counter(v for e in es for v in e); groups[tuple(sorted(d.values()))].append(es)
    pairs = 0; sep = True
    for g in groups.values():
        for a, b in itertools.combinations(g, 2):
            pairs += 1
            if iso.GraphMatcher(inc(a, nv), inc(b, nv), node_match=lambda x, y: x['c'] == y['c']).is_isomorphic(): sep = False
    print(path, 'classes', len(L), 'distinct canonical forms', len(set(base)), '| relabelling invariance:', inv, '| pairs with equal degree sequence', pairs, 'all non-isomorphic (VF2):', sep, flush=True)
