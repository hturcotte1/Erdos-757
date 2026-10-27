# independent validation of the C implementation at n=28..40: tau by CP-SAT (min hitting set), class C by networkx matching (Hall pairs) + python F7 search + linearity
import json, random, itertools, sys, collections
from ortools.sat.python import cp_model
import networkx as nx
from common import *
random.seed(7)
gd = json.load(open('out/glue_main.json'))['best']
graphs = []
for n, L in gd.items():
    if 28 <= int(n) <= 40:
        for x in L[:20]: graphs.append((int(n), [tuple(e) for e in x['edges']]))
# random growth graphs via the C tool are not exported; use beam pool graphs too
import gzip
for f in ['out/beam_d5a_pools.jsonl.gz', 'out/beam_d5b_pools.jsonl.gz']:
    for l in gzip.open(f, 'rt'):
        d = json.loads(l)
        if 28 <= d['n'] <= 40:
            t = d['line'].split(' '); n = int(t[0]); graphs.append((n, [tuple(int(x) for x in w.split(',')) for w in t[2:]]))
random.shuffle(graphs); graphs = graphs[:400]
res = run_eval([line(n, e) for n, e in graphs])
def tau_cp(n, es):
    m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
    for e in es: m.AddBoolOr([x[v] for v in e])
    m.Minimize(sum(x)); s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 60
    st = s.Solve(m); return int(s.ObjectiveValue()), st == cp_model.OPTIMAL
def in_class_py(n, es):
    S = [frozenset(e) for e in es]
    for a, b in itertools.combinations(S, 2):
        if len(a & b) >= 2: return False
    Es = set(S)
    for v in range(n):
        inc = [e for e in S if v in e]
        for a, b, c in itertools.combinations(inc, 3):
            P = [sorted(a - {v}), sorted(b - {v}), sorted(c - {v})]
            for ch in itertools.product((0, 1), repeat=3):
                X = frozenset(P[i][ch[i]] for i in range(3)); Y = frozenset(P[i][1 - ch[i]] for i in range(3))
                if X in Es and Y in Es: return False
    used = sorted(set(v for e in es for v in e))
    for x, y in itertools.combinations(used, 2):
        G = nx.Graph()
        for i, e in enumerate(es):
            for v in e:
                if v not in (x, y): G.add_edge(('e', i), ('v', v))
        top = [('e', i) for i in range(len(es))]
        M = nx.bipartite.maximum_matching(G, top_nodes=[t for t in top if t in G]) if G.number_of_nodes() else {}
        if sum(1 for t in top if t in M) < len(es): return False
    return True
bad = 0; chk = 0; nopt = 0
for (n, es), r in zip(graphs, res):
    t, opt = tau_cp(n, es); nopt += (not opt)
    ic = in_class_py(n, es) if len(graphs) and chk < 150 else None
    if ic is not None: chk += 1
    if t != r[2] or (ic is not None and ic != (r[4] == 0)): bad += 1; print('MISMATCH', n, r, t, ic)
print(json.dumps(dict(graphs=len(graphs), tau_checked=len(graphs), class_checked=chk, mismatches=bad, cpsat_not_optimal=nopt, n_range=[min(g[0] for g in graphs), max(g[0] for g in graphs)])))
json.dump(dict(graphs=len(graphs), class_checked=chk, mismatches=bad, cpsat_not_optimal=nopt), open('out/validate_tau.json', 'w'))
