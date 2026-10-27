"""L017, end-to-end brute-force check of Theorem 4(iii)-(iv) + C5 (Corollary 13.3) on small disjoint unions G of known
low-slack graphs: enumerate EVERY way of adding a vertex v with three edges {v} u P_j (P_j pairwise disjoint pairs of
vertices of G-degree <= 2, no P_j inside an edge of G, every component of G meeting some P_j, i.e. H connected) and test
(star) tau(H) = tau(G) + 1 directly by the exact branch and bound of hyp.py on H (no use of the pattern conditions).
Corollary 13.3's argument predicts: for r >= 2 components from the known lists, the only (star) configurations are those
with G = E1 + E1 (H = F7, pattern (b)); for r = 1 (pattern (a)) configurations may exist (they are then violators outside C).
Usage: python3 brute_patterns.py"""
import os, sys, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyp import read_cell, tau, degrees, components, contains_F7, p3_ok
HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda f: read_cell(os.path.join(HERE, 'out/L012/cells', f))
E1 = L('cell_3_1_1_D3.txt'); T10 = L('cell_10_7_4_D3.txt'); S8 = L('cell_8_5_3_D3.txt')

def union(parts):
    es = []; off = 0
    for (n, edges) in parts:
        es += [tuple(x + off for x in e) for e in edges]; off += n
    return off, es

def run(name, parts):
    n, es = union(parts); d = degrees(n, es); t = tau(n, es)
    comp = components(range(n), es); cid = {x: i for i, c in enumerate(comp) for x in c}
    inedge = set(p for e in es for p in itertools.combinations(sorted(e), 2))
    V2 = [x for x in range(n) if d[x] <= 2]
    pairs = [p for p in itertools.combinations(V2, 2) if p not in inedge]
    tot = star = 0; examples = []
    for P in itertools.combinations(pairs, 3):
        vs = set(P[0]) | set(P[1]) | set(P[2])
        if len(vs) < 6: continue
        if len(set(cid[x] for x in vs)) < len(comp): continue   # H connected
        tot += 1
        H = es + [(n,) + p for p in P]
        if tau(n + 1, H) == t + 1:
            star += 1
            if len(examples) < 2: examples.append(P)
    print('%s: G has %d vertices, %d components, tau %d; configurations %d, with (star) %d %s'
          % (name, n, len(comp), t, tot, star, ('e.g. ' + str(examples)) if examples else ''), flush=True)
    return star

if __name__ == '__main__':
    run('E1+E1 (expect F7, pattern b)', [(3, E1[0]), (3, E1[0])])
    for i, g in enumerate(T10): run('E1+(10,7,4)#%d' % i, [(3, E1[0]), (10, g)])
    for i, g in enumerate(S8): run('E1+(8,5,3)#%d' % i, [(3, E1[0]), (8, g)])
    for i, g in enumerate(S8): run('E1+E1+(8,5,3)#%d' % i, [(3, E1[0]), (3, E1[0]), (8, g)])
    run('E1+E1+(10,7,4)#0', [(3, E1[0]), (3, E1[0]), (10, T10[0])])
    run('E1+E1+(10,7,4)#1', [(3, E1[0]), (3, E1[0]), (10, T10[1])])
    for i, g in enumerate(S8): run('(8,5,3)#%d alone (pattern a; (9,8,4) graphs expected)' % i, [(8, g)])
    for i, g in enumerate(T10): run('(10,7,4)#%d alone (pattern a)' % i, [(10, g)])
