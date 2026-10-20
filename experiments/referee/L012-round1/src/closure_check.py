"""Referee: closure (re-derivation) test of the prover's cell lists, independent of nauty.
For every class X of a checked list and EVERY vertex w of maximum degree d = Delta(X) (for the 699 route-4 classes: every
vertex of degree 4), every component K of X - w must be isomorphic (networkx VF2 inside Weisfeiler-Lehman buckets) to a member
of the prover's list cell(n_K, m_K, tau_K, d) (route-4 classes: of the list of the route-4 inputs' type with D = 4).
The engine generated X from ONE such w; the other choices of w are an independent consistency test of the lower lists."""
import sys, re, os, collections, itertools
import networkx as nx
from networkx.algorithms import isomorphism as iso
CD = '/home/user/Erdos-757/experiments/prover/L012/out/cells'
nm = iso.categorical_node_match('kind', None)
def edges_of(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def inc(E, V):
    G = nx.Graph()
    for v in V: G.add_node(('v', v), kind='v')
    for i, e in enumerate(E):
        G.add_node(('e', i), kind='e')
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
def wl(G): return nx.weisfeiler_lehman_graph_hash(G, node_attr='kind', iterations=4)
def tau(E):
    E = list(E)
    def rec(k, S, i):
        while i < len(E) and (E[i][0] in S or E[i][1] in S or E[i][2] in S): i += 1
        if i == len(E): return True
        if k == 0: return False
        return any(rec(k - 1, S | {v}, i + 1) for v in E[i])
    k = 0
    while not rec(k, frozenset(), 0): k += 1
    return k
CACHE = {}
def lst(n, m, t, D):
    key = (n, m, t, D)
    if key not in CACHE:
        fn = os.path.join(CD, 'cell_%d_%d_%d_D%d.txt' % key)
        if not os.path.exists(fn): CACHE[key] = None
        else:
            reps = [edges_of(l) for l in open(fn) if l.startswith('FOUND')]
            b = collections.defaultdict(list)
            for E in reps:
                G = inc(E, range(n)); b[wl(G)].append(G)
            CACHE[key] = b
    return CACHE[key]
def components(E, V):
    par = {v: v for v in V}
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b, c in E: par[f(a)] = f(b); par[f(b)] = f(c)
    comp = collections.defaultdict(list)
    for v in V: comp[f(v)].append(v)
    out = []
    for vs in comp.values():
        S = set(vs); Ek = [e for e in E if e[0] in S]
        out.append((vs, Ek))
    return out
def check_list(reps, n, Dfix=None, only_deg=None):
    stats = collections.Counter()
    for E in reps:
        deg = collections.Counter(v for e in E for v in e)
        d = max(deg.values()) if Dfix is None else Dfix
        ws = [v for v in range(n) if deg[v] == (only_deg if only_deg else max(deg.values()))]
        for w in ws:
            Ew = [e for e in E if w not in e]; V = [v for v in range(n) if v != w]
            for vs, Ek in components(Ew, V):
                if len(vs) == 1: stats['isolated'] += 1; continue
                relabel = {v: i for i, v in enumerate(sorted(vs))}; Er = [tuple(relabel[x] for x in e) for e in Ek]
                typ = (len(vs), len(Er), tau(Er))
                L = lst(*typ, d)
                if L is None: stats['MISSING_CELL %s D%d' % (typ, d)] += 1; continue
                G = inc(Er, range(len(vs))); k = wl(G)
                if any(iso.GraphMatcher(G, H, node_match=nm).is_isomorphic() for H in L.get(k, [])): stats['found'] += 1
                else: stats['NOT_FOUND %s D%d' % (typ, d)] += 1
            stats['deletions'] += 1
    return stats
if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'route4':
        reps = [edges_of(l) for l in open(sys.argv[2]) if l.startswith('FOUND')]
        print('route4 classes', len(reps), dict(check_list(reps, 23, Dfix=4, only_deg=4)))
    else:
        n, m, t, D = map(int, what.split(','))
        reps = [edges_of(l) for l in open(os.path.join(CD, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))) if l.startswith('FOUND')]
        print('cell', (n, m, t, D), 'classes', len(reps), dict(check_list(reps, n)))
    sys.stdout.flush()
