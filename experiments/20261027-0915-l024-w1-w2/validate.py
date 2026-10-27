"""Independent validation of tau (CP-SAT) and DEF (networkx subgraph-isomorphism copies + plain enumeration of disjoint families)
for every configuration stored in the given result json files (configs with edges/n/tau/A[/DEF]).
usage: python3 validate.py file1.json file2.json ..."""
import sys, json, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
from hyp24 import load_pieces, CN, CM, CT, CE
from ortools.sat.python import cp_model
import networkx as nx
from networkx.algorithms import isomorphism as iso

def tau_cpsat(n, edges):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(n)]
    for e in edges: m.AddBoolOr([x[i] for i in e])
    m.Minimize(sum(x))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1
    st = s.Solve(m)
    assert st == cp_model.OPTIMAL
    return int(round(s.ObjectiveValue()))

def inc(edges, verts):
    G = nx.Graph()
    for x in verts: G.add_node(('v', x), t=0)
    for i, e in enumerate(edges):
        G.add_node(('e', i), t=1)
        for x in e: G.add_edge(('v', x), ('e', i))
    return G

pieces = load_pieces()
PG = [(P, inc(P['edges'], range(P['n']))) for P in pieces]

def copies(n, edges):
    G = inc(edges, range(n)); out = set()
    for P, PGraph in PG:
        if P['n'] > n: continue
        GM = iso.GraphMatcher(G, PGraph, node_match=lambda a, b: a['t'] == b['t'])
        for mp in GM.subgraph_monomorphisms_iter():   # mp: G-node -> piece-node
            vs = frozenset(nd[1] for nd in mp if nd[0] == 'v')
            if len(vs) != P['n']: continue
            inner = [e for e in edges if all(y in vs for y in e)]
            if len(inner) == P['m']: out.add((vs, P['name'], P['W'], P['m']))
    return list(out)

def def_brute(n, edges):
    cps = copies(n, edges); best = 0
    es = [frozenset(e) for e in edges]
    def rec(i, U, g):
        nonlocal best
        obj = g - CE * sum(1 for e in es if e & U)
        best = max(best, obj)
        for j in range(i, len(cps)):
            vs, nm, w, mP = cps[j]
            if not (vs & U): rec(j + 1, U | vs, g + w + CE * mP)
    rec(0, frozenset(), 0)
    return best, len(cps)

tot = dict(configs=0, tau_checked=0, tau_mismatch=0, A_neg=0, def_checked=0, def_mismatch=0, Pneg=0)
t0 = time.time()
for f in sys.argv[1:]:
    D = json.load(open(f))
    for c in D['configs']:
        if 'tau' not in c: continue
        tot['configs'] += 1
        n = c['n'] if 'n' in c else None
        edges = [tuple(e) for e in c['edges']]
        if n is None: n = max(max(e) for e in edges) + 1
        t = tau_cpsat(n, edges); tot['tau_checked'] += 1
        if t != c['tau']: tot['tau_mismatch'] += 1; print('TAU MISMATCH', f, c['tau'], t)
        A = CN * n + CM * len(edges) - CT * t
        if A != c['A']: tot['tau_mismatch'] += 1; print('A MISMATCH')
        if A < 0:
            tot['A_neg'] += 1
            d, nc = def_brute(n, edges); tot['def_checked'] += 1
            if 'DEF' in c and d != c['DEF']: tot['def_mismatch'] += 1; print('DEF MISMATCH', f, c['DEF'], d)
            if A + d < 0: tot['Pneg'] += 1; print('NEGATIVE P (validated)', f, c)
    print(f, tot, f'{time.time()-t0:.0f}s', flush=True)
print('VALIDATE TOTAL', tot)
