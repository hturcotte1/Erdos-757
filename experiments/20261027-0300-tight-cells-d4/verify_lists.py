"""Independent pure-Python (numpy for subset sums) re-verification of the connected members listed in a cell file:
linear, F7-free, e(S)<=|S|-2 for all S (|S|>=2), connected, n/m/tau as claimed (tau by exhaustive search), max degree, slack, pairwise non-isomorphic
(canonical form by pynauty-free refinement: we use the Levi-graph canonical via networkx WL hash + exact isomorphism check)."""
import sys, itertools, re, numpy as np, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def levi(n, E):
    G = nx.Graph()
    for v in range(n): G.add_node(('v', v), t=0)
    for i, e in enumerate(E):
        G.add_node(('e', i), t=1)
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def has_F7(n, E):
    fs = [frozenset(e) for e in E]; GF = levi(7, F7)
    for sub in itertools.combinations(range(len(fs)), 5):
        U = set().union(*[fs[i] for i in sub])
        if len(U) != 7: continue
        idx = {v: j for j, v in enumerate(sorted(U))}
        G = levi(7, [tuple(idx[v] for v in fs[i]) for i in sub])
        if GraphMatcher(G, GF, node_match=lambda a, b: a['t'] == b['t']).is_isomorphic(): return True
    return False
def tau_of(n, E):
    masks = [sum(1 << v for v in e) for e in E]
    for k in range(0, n + 1):
        for T in itertools.combinations(range(n), k):
            tm = sum(1 << v for v in T)
            if all(tm & m for m in masks): return k
def check_sets(n, E):
    S = np.arange(1 << n, dtype=np.uint32)
    cnt = np.zeros(1 << n, dtype=np.int16)
    for e in E:
        m = sum(1 << v for v in e); cnt += ((S & m) == m)
    pc = np.zeros(1 << n, dtype=np.int16)
    for v in range(n): pc += ((S >> v) & 1).astype(np.int16)
    sel = pc >= 2
    return bool(np.all(cnt[sel] <= pc[sel] - 2))
def main(fn, n, m, t):
    lines = [l for l in open(fn) if l.startswith('FOUND:')]; Gs = []; ok = True
    for l in lines:
        E = parse(l); assert len(E) == m
        vs = set(v for e in E for v in e); assert vs == set(range(n)), 'vertex set'
        # linear
        pairs = set()
        for e in E:
            for p in itertools.combinations(sorted(e), 2):
                assert p not in pairs, 'not linear'; pairs.add(p)
        deg = [sum(v in e for e in E) for v in range(n)]
        G = levi(n, E); assert nx.is_connected(G)
        assert not has_F7(n, E), 'F7'
        assert check_sets(n, E), 'e(S)'
        tt = tau_of(n, E); assert tt == t, ('tau', tt)
        assert 3 * n + 2 * m - 11 * t == 0
        Gs.append((G, max(deg), sorted(deg, reverse=True)))
    for i, j in itertools.combinations(range(len(Gs)), 2):
        assert not GraphMatcher(Gs[i][0], Gs[j][0], node_match=lambda a, b: a['t'] == b['t']).is_isomorphic(), ('iso', i, j)
    print(fn, 'classes', len(lines), 'ALL OK; maxdeg', sorted(g[1] for g in Gs), 'deg seqs', [''.join(map(str, g[2])) for g in Gs])
if __name__ == '__main__':
    fn, n, m, t = sys.argv[1], *map(int, sys.argv[2:5]); main(fn, n, m, t)
