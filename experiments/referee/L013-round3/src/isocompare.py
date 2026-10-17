"""isocompare.py n fileA fileB : compare two FOUND lists of 3-graphs on n vertices up to isomorphism (networkx VF2 on the
incidence graphs with side colours). Reports |A|, |B|, classes of A found in B and vice versa, and duplicates within each list."""
import sys, re, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
n = int(sys.argv[1])
def load(p):
    out = []
    for l in open(p):
        if l.startswith('FOUND:') or l.startswith('HIT'):
            out.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
    return out
def inc(es):
    g = nx.Graph()
    for v in range(n): g.add_node(('v', v), side=0)
    for i, e in enumerate(es):
        g.add_node(('e', i), side=1)
        for v in e: g.add_edge(('v', v), ('e', i))
    return g
def inv(es):
    deg = [0] * n
    for e in es:
        for v in e: deg[v] += 1
    # degree sequence + multiset of (sum of degrees of edge vertices)
    return (tuple(sorted(deg)), tuple(sorted(sum(deg[v] for v in e) for e in es)))
def iso(g1, g2): return GraphMatcher(g1, g2, node_match=lambda a, b: a['side'] == b['side']).is_isomorphic()
A, B = load(sys.argv[2]), load(sys.argv[3])
GA, GB = [inc(e) for e in A], [inc(e) for e in B]; IA, IB = [inv(e) for e in A], [inv(e) for e in B]
def match(GX, IX, GY, IY):
    found = 0; missing = []
    for i, g in enumerate(GX):
        ok = any(IX[i] == IY[j] and iso(g, GY[j]) for j in range(len(GY)))
        found += ok
        if not ok: missing.append(i)
    return found, missing
fa, ma = match(GA, IA, GB, IB); fb, mb = match(GB, IB, GA, IA)
dupA = sum(1 for i in range(len(GA)) for j in range(i) if IA[i] == IA[j] and iso(GA[i], GA[j]))
dupB = sum(1 for i in range(len(GB)) for j in range(i) if IB[i] == IB[j] and iso(GB[i], GB[j]))
print('ISOCOMPARE n=%d: |A|=%d |B|=%d; A-classes found in B: %d (missing %s); B-classes found in A: %d (missing %s); isomorphic duplicates within A: %d, within B: %d; %s' %
      (n, len(A), len(B), fa, ma[:5], fb, mb[:5], dupA, dupB, 'EQUAL' if (fa == len(A) and fb == len(B) and dupA == 0 and dupB == 0) else 'DIFFERENT'))
