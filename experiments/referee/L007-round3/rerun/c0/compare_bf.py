"""Completeness test of enum_conn (and of conn_dfs2_all) against the brute force bf_cells on n <= 9:
for every (n, m, t, D) the number of LABELLED connected linear 3-graphs on [n] with m edges, tau >= t and max degree <= D
(brute force, no isomorphism reduction) must equal  sum over the isomorphism classes found by the enumerator of n!/|Aut|."""
import subprocess, re, sys, math, itertools, json
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
def parse(out):
    return [[tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)] for l in out.splitlines() if l.startswith('FOUND:')]
def inc_graph(es):
    G = nx.Graph()
    for i, e in enumerate(es):
        G.add_node(('e', i), t=1)
        for v in e: G.add_node(('v', v), t=0); G.add_edge(('e', i), ('v', v))
    return G
nm = lambda a, b: a['t'] == b['t']
def classes(lst):
    buckets = {}; reps = []
    for es in lst:
        G = inc_graph(es); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t')
        b = buckets.setdefault(h, [])
        if not any(nx.is_isomorphic(G, H, node_match=nm) for H in b): b.append(G); reps.append(es)
    return reps
def aut(es):
    G = inc_graph(es); return sum(1 for _ in GraphMatcher(G, G, node_match=nm).isomorphisms_iter())
def tau(es, n):
    masks = [sum(1 << v for v in e) for e in es]
    for k in range(n + 1):
        for T in itertools.combinations(range(n), k):
            s = sum(1 << v for v in T)
            if all(mk & s for mk in masks): return k
def maxdeg(es):
    d = {}
    for e in es:
        for v in e: d[v] = d.get(v, 0) + 1
    return max(d.values())
prog = sys.argv[1]  # 'mine' or 'theirs'
res = []; bad = 0
for n in range(3, 10):
    bf = {}
    for l in open('bf_n%d.txt' % n):
        m, t, d, c = map(int, l.split()); bf[(m, t, d)] = c
    ms = sorted({k[0] for k in bf})
    for m in ms:
        tmax = max(k[1] for k in bf if k[0] == m)
        dmax = max(k[2] for k in bf if k[0] == m)
        for t in range(0, tmax + 2):
            for D in sorted({2, 3, dmax, 100}):
                if prog == 'mine':
                    out = subprocess.run(['./enum_conn', str(n), str(m), str(t), str(D), '1'], capture_output=True, text=True).stdout
                else:
                    out = subprocess.run(['../bin/conn_dfs2_all', str(n), str(m), str(t), str(D)], capture_output=True, text=True).stdout
                lst = parse(out)
                reps = classes(lst)
                ok_sound = all(tau(es, n) >= t and maxdeg(es) <= D and len(es) == m and set().union(*es) == set(range(n)) for es in lst)
                lab = sum(math.factorial(n) // aut(es) for es in reps)
                want = sum(c for (mm, tt, dd), c in bf.items() if mm == m and tt >= t and dd <= D)
                ok = ok_sound and lab == want
                bad += not ok
                res.append(dict(n=n, m=m, t=t, D=D, found=len(lst), classes=len(reps), labelled_from_classes=lab, brute_force=want, ok=ok))
                if not ok: print('MISMATCH', res[-1], flush=True)
print(prog, 'cells compared:', len(res), 'mismatches:', bad, 'nonempty cells:', sum(1 for r in res if r['brute_force'] > 0),
      'total classes:', sum(r['classes'] for r in res))
json.dump(res, open('compare_bf_%s.json' % prog, 'w'), indent=0)
