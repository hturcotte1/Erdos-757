"""Referee (L013 round 2): every Delta<=2 cell by the DUAL-GRAPH method (independent of genbg/enum_conn/the recursion).
A connected linear 3-graph H with Delta(H) <= 2, n vertices, m edges  <->  a connected simple graph G on m vertices with Delta(G) <= 3 and
3m - n edges (hyperedges = vertices of G, degree-2 points = edges of G, degree-1 points = 3 - deg_G pendant slots).  Isomorphism classes
correspond.  tau(H) = m - nu(G) (nu = matching number); (P3) and F7-freeness are automatic for Delta <= 2 (checked anyway by refx).
For each cell (n,m,t,2) of the prover's directory: geng -c -D3 m (3m-n):(3m-n), keep nu(G) = m - t, build H, check H with refx
(linear, connected, F7, (P3), tau exactly, maxdeg), and match the survivors with the prover's representatives by isomorphism
of the dual graphs (networkx VF2 after WL-hash bucketing).  Reports counts and set equality."""
import sys, os, re, subprocess, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
HERE = os.path.dirname(os.path.abspath(__file__)); CD = sys.argv[1]
def g6_graphs(m, e):
    if m == 1: return [nx.empty_graph(1)] if e == 0 else []
    out = subprocess.run([os.path.join(HERE, 'bin', 'geng'), '-q', '-c', '-D3', str(m), '%d:%d' % (e, e)], capture_output=True, text=True).stdout
    return [nx.from_graph6_bytes(l.encode()) for l in out.split()]
def H_of_G(G):
    edges = {v: [] for v in G.nodes()}; nxt = 0
    for (a, b) in G.edges():
        edges[a].append(nxt); edges[b].append(nxt); nxt += 1
    for v in G.nodes():
        while len(edges[v]) < 3: edges[v].append(nxt); nxt += 1
    return nxt, [tuple(sorted(edges[v])) for v in G.nodes()]
def G_of_H(n, es):
    G = nx.Graph(); G.add_nodes_from(range(len(es)))
    inc = {}
    for i, e in enumerate(es):
        for v in e: inc.setdefault(v, []).append(i)
    for v, L in inc.items():
        assert len(L) <= 2
        if len(L) == 2: G.add_edge(L[0], L[1])
    return G
def refx_check(n, Hs):
    if not Hs: return []
    inp = ''.join('X: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n' for es in Hs)
    out = subprocess.run([os.path.join(HERE, 'bin', 'refx'), 'check', str(n)], input=inp, capture_output=True, text=True).stdout.splitlines()
    res = []
    for l in out:
        d = dict(kv.split('=') for kv in l.split()[1:]); res.append({k: int(v) for k, v in d.items()})
    assert len(res) == len(Hs)
    return res
tot_cells = 0; bad = 0; rows = []
for fn in sorted(os.listdir(CD)):
    mt = re.match(r'cell_(\d+)_(\d+)_(\d+)_D2\.txt$', fn)
    if not mt: continue
    n, m, t = map(int, mt.groups()); tot_cells += 1
    reps = [[tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in open(os.path.join(CD, fn)) if l.startswith('FOUND:')]
    e = 3 * m - n
    Gs = [G for G in g6_graphs(m, e)] if e >= 0 else []
    sel = []
    for G in Gs:
        nu = len(nx.max_weight_matching(G, maxcardinality=True))
        if m - nu == t: sel.append(G)
    Hs = [H_of_G(G) for G in sel]
    chk = refx_check(n, [es for (nn, es) in Hs])
    for (nn, es), c in zip(Hs, chk):
        assert nn == n and c['tau'] == t and c['linear'] == 1 and c['connected'] == 1 and c['F7'] == 0 and c['P3'] == 1 and c['maxdeg'] <= 2, (fn, c)
    # cross-check tau = m - nu on ALL generated graphs for small sets
    if len(Gs) <= 3000:
        allH = [H_of_G(G) for G in Gs]; allc = refx_check(n, [es for (nn, es) in allH])
        for G, c in zip(Gs, allc):
            assert c['tau'] == m - len(nx.max_weight_matching(G, maxcardinality=True)), fn
    # match with prover reps
    pG = [G_of_H(n, r) for r in reps]
    for r in reps: assert len(r) == m
    def h(G): return nx.weisfeiler_lehman_graph_hash(G, iterations=4)
    buck = {}
    for i, G in enumerate(sel): buck.setdefault(h(G), []).append(i)
    used = set(); ok = (len(pG) == len(sel))
    for G in pG:
        cand = [i for i in buck.get(h(G), []) if i not in used and nx.is_isomorphic(G, sel[i])]
        if not cand: ok = False; break
        used.add(cand[0])
    if not ok: bad += 1
    rows.append((n, m, t, len(Gs), len(sel), len(reps), 'EQUAL' if ok else 'DIFFERENT'))
for r in sorted(rows): print('(%d,%d,%d,2): dual graphs %d, selected %d, prover %d, %s' % r)
print('cells', tot_cells, 'different', bad)
