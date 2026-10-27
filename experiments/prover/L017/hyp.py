"""L017 helper library (illustrative checks only; exact integer arithmetic, no floats).

Hypergraphs are 3-uniform, given by a vertex count n (vertices 0..n-1) and a list of 3-tuples.
Internally edges are bitmasks.  tau = transversal number (minimum vertex set meeting every edge),
slack = 3n + 2m - 11 tau (the I11 slack)."""
import re, os

def parse_edges(line):
    return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]

def read_cell(path):
    """list of edge lists from an engine cell file (lines 'FOUND: (a,b,c) ...')."""
    out = []
    for l in open(path):
        if l.startswith('FOUND:'):
            out.append(parse_edges(l))
    return out

def masks(edges):
    return [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]

def _lb(rem):
    used = 0; lb = 0
    for e in rem:
        if not e & used:
            used |= e; lb += 1
    return lb

def tau_masks(em):
    """exact transversal number of the edge-mask list em (branch and bound)."""
    em = list(em)
    best = [len(em)]
    def rec(rem, k):
        if not rem:
            if k < best[0]: best[0] = k
            return
        if k + _lb(rem) >= best[0]: return
        # branch on the edge whose vertices cover the most remaining edges is not needed; take rem[0]
        e = rem[0]; m = e
        while m:
            b = m & -m; m ^= b
            rec([f for f in rem if not f & b], k + 1)
    rec(em, 0)
    return best[0]

def tau(n, edges):
    return tau_masks(masks(edges))

def all_min_transversals(em, t=None):
    """every transversal of size tau (as bitmasks), each exactly once."""
    em = list(em)
    if t is None: t = tau_masks(em)
    res = []
    def rec(rem, chosen, k, forb):
        if not rem:
            res.append(chosen); return
        if k == t or k + _lb(rem) > t: return
        e = rem[0]; cand = e & ~forb; f2 = forb
        while cand:
            b = cand & -cand; cand ^= b
            rec([f for f in rem if not f & b], chosen | b, k + 1, f2)
            f2 |= b
    rec(em, 0, 0, 0)
    return res, t

def slack(n, m, t):
    return 3 * n + 2 * m - 11 * t

def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for x in e: d[x] += 1
    return d

def induced(edges, keep):
    """edges inside the vertex set keep (a set)."""
    return [e for e in edges if all(x in keep for x in e)]

def components(vertices, edges):
    """components of the hypergraph on the vertex set `vertices` (iterable) with the given edges (inside it)."""
    vs = list(vertices); parent = {v: v for v in vs}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for e in edges:
        r = find(e[0])
        for x in e[1:]:
            q = find(x)
            if q != r: parent[q] = r
    comp = {}
    for v in vs: comp.setdefault(find(v), []).append(v)
    return list(comp.values())

def relabel(vs, edges):
    """relabel the sub-hypergraph on vertex list vs to 0..len(vs)-1."""
    idx = {v: i for i, v in enumerate(vs)}
    return len(vs), [tuple(idx[x] for x in e) for e in edges], idx

def tau_sub(vs, edges):
    """tau of the induced sub-hypergraph on vertex set vs (edges = all edges of the big graph)."""
    S = set(vs)
    return tau_masks(masks(induced(edges, S)))

def is_linear(edges):
    es = [set(e) for e in edges]
    for i in range(len(es)):
        for j in range(i + 1, len(es)):
            if len(es[i] & es[j]) > 1: return False
    return True

F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]

def contains_F7(n, edges):
    """brute force: is there a subhypergraph isomorphic to F7 = {012,034,056,135,246}?
    F7: vertex 0 of degree 3 with edges {0,a,b},{0,c,d},{0,e,f} and two disjoint edges each meeting every one of the three pairs."""
    E = [frozenset(e) for e in edges]; Es = set(E)
    inc = [[] for _ in range(n)]
    for e in E:
        for x in e: inc[x].append(e)
    for v in range(n):
        if len(inc[v]) < 3: continue
        L = inc[v]
        import itertools
        for t3 in itertools.combinations(L, 3):
            pairs = [tuple(sorted(e - {v})) for e in t3]
            # choose one vertex from each pair for edge X, the others for edge Y
            for bits in range(8):
                X = frozenset(pairs[i][(bits >> i) & 1] for i in range(3))
                Y = frozenset(pairs[i][1 - ((bits >> i) & 1)] for i in range(3))
                if X in Es and Y in Es: return True
    return False

def p3_ok(n, edges):
    """e(S) <= |S| - 2 for every S with |S| >= 2 (exhaustive over subsets; only for small n)."""
    em = masks(edges)
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 2: continue
        e = sum(1 for f in em if f & S == f)
        if e > k - 2: return False
    return True
