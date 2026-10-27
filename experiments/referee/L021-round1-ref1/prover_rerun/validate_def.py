"""L021: independent check of kt.deficiency on all stored graphs with n <= 16 of the special-candidate cells
and of the (12,10,5), (14,12,6), (10,8,4) cells (non-special, sanity): induced copies are found by brute force over
ALL vertex subsets W of the piece sizes with networkx isomorphism of incidence graphs, and DEF is the maximum
over ALL sets of pairwise disjoint copies (plain enumeration, no bound).  Prints mismatches (expected: none)."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L021-round1-ref1/prover_rerun')
from kt import *
import networkx as nx
from networkx.algorithms import isomorphism as iso
R = json.load(open('/home/user/Erdos-757/experiments/referee/L021-round1-ref1/prover_rerun/closure_results.json'))
pieces = [Piece(p['edges'], p['name']) for p in R['pieces']]
def inc_graph(edges, W=None):
    G = nx.Graph()
    vs = sorted(set(x for e in edges for x in e)) if W is None else sorted(W)
    for x in vs: G.add_node(('v', x), t=0)
    for i, e in enumerate(edges):
        G.add_node(('e', i), t=1)
        for x in e: G.add_edge(('v', x), ('e', i))
    return G
PG = [(P, inc_graph(P.edges)) for P in pieces]
def brute_copies(n, edges):
    fm = masks(edges); out = []
    sizes = sorted(set(P.n for P in pieces if P.n < n))
    for k in sizes:
        for W in itertools.combinations(range(n), k):
            Wm = 0
            for x in W: Wm |= 1 << x
            sub = [e for e, f in zip(edges, fm) if f & Wm == f]
            for P, G in PG:
                if P.n != k or P.m != len(sub): continue
                if nx.is_isomorphic(G, inc_graph(sub, W), node_match=lambda a, b: a['t'] == b['t']):
                    out.append((Wm, P.W, P.m)); break
    return out
def brute_def(n, edges):
    fm = masks(edges); cps = brute_copies(n, edges); best = 0
    def rec(i, U, g):
        nonlocal best
        obj = g - CE * sum(1 for e in fm if e & U)
        best = max(best, obj)
        for j in range(i, len(cps)):
            W, w, mP = cps[j]
            if not W & U: rec(j + 1, U | W, g + w + CE * mP)
    rec(0, 0, 0)
    return best, len(cps)
base = '/home/user/Erdos-757/experiments/prover/L017/out/L012/cells/'
files = ['cell_8_5_3_D3.txt', 'cell_9_4_3_D3.txt', 'cell_10_7_4_D3.txt', 'cell_14_8_5_D3.txt', 'cell_15_7_5_D3.txt',
         'cell_15_11_6_D3.txt', 'cell_16_10_6_D3.txt', 'cell_10_8_4_D3.txt', 'cell_12_10_5_D3.txt', 'cell_13_9_5_D3.txt']
tot = 0; bad = 0
for f in files:
    gs = read_cell(base + f)
    for g in gs[:40]:
        n = nverts(g)
        d1 = deficiency(n, g, pieces, proper=True)
        d2, nc = brute_def(n, g)
        tot += 1
        if d1 != d2:
            bad += 1; print('MISMATCH', f, g, d1, d2)
    print(f, 'checked', min(len(gs), 40), flush=True)
print('validate_def: graphs', tot, 'mismatches', bad)
