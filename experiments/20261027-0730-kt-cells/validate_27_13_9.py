"""validate_def.py-style brute force for the 18 graphs of cell(27,13,9,3) (A=-4): induced copies of the 32 pieces found by
enumerating ALL connected edge subsets F (2^13 subsets), W=V(F), sub-hypergraph H[W] (all edges inside W), networkx isomorphism with each piece
of the same (n,m); DEF = plain max over all families of pairwise disjoint copies (no bounding).  Compares with kt.deficiency (L021) and
prints P = A + DEF.  Expected: DEF=4, P=0 for all 18."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
import networkx as nx
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
pieces = [Piece(p['edges'], p['name']) for p in R['pieces']]
nm = lambda a, b: a['t'] == b['t']
def inc(edges):
    G = nx.Graph()
    for i, e in enumerate(edges):
        G.add_node(('e', i), t=1)
        for x in e: G.add_node(('v', x), t=0); G.add_edge(('e', i), ('v', x))
    return G
PG = [(P, inc(P.edges)) for P in pieces]
def brute(n, edges):
    m = len(edges); fm = masks(edges); copies = {}
    for mask in range(1, 1 << m):
        F = [edges[i] for i in range(m) if mask >> i & 1]
        W = 0
        for e in F: 
            for x in e: W |= 1 << x
        # connected (edge-wise)?
        comp = [F[0]]; rest = F[1:]; vs = set(F[0]); ch = True
        while ch:
            ch = False
            for e in rest[:]:
                if vs & set(e): vs |= set(e); rest.remove(e); ch = True
        if rest: continue
        k = bin(W).count('1')
        if W in copies: continue
        sub = [e for e, f in zip(edges, fm) if f & W == f]
        for P, G in PG:
            if P.n == k and P.m == len(sub) and nx.is_isomorphic(G, inc(sub), node_match=nm):
                copies[W] = (P.W, P.m); break
    cps = [(W, w, mP) for W, (w, mP) in copies.items()]
    best = 0
    def rec(i, U, g):
        nonlocal best
        best = max(best, g - CE * sum(1 for f in fm if f & U))
        for j in range(i, len(cps)):
            W, w, mP = cps[j]
            if not W & U: rec(j + 1, U | W, g + w + CE * mP)
    rec(0, 0, 0)
    return best, len(cps)
gs = read_cell('lists/cell_27_13_9_D3.txt')
bad = 0
for i, g in enumerate(gs):
    n = nverts(g); A = A_value(n, len(g), tau_masks(masks(g)))
    d1 = deficiency(n, g, pieces, proper=True); d2, nc = brute(n, g)
    print(f'graph {i}: A={A} DEF(kt)={d1} DEF(brute)={d2} copies={nc} P={A + d2}', flush=True)
    if d1 != d2: bad += 1
print('mismatches', bad, 'of', len(gs))
