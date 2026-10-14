"""Exact checker for Lemmas 1, 2 (and 3 helpers) of kb/notes/gl_tight_structure.md."""
import itertools, json, sys
sys.path.insert(0, '/home/user/Erdos-757')
from e757.saturated import alpha_of_edges

def parse(n, edges):
    """edges: sorted triples (l,j,r). returns l,r dicts; None if not saturated ordered midpoint map."""
    l, r = {}, {}
    for a, j, b in edges:
        if not (a < j < b) or j in l: return None
        l[j], r[j] = a, b
    if sorted(l) != list(range(1, n - 1)): return None
    return l, r

def components_color(nv, pairs):
    """pairs on vertices 0..nv-1; check spanning tree; return colour list or None."""
    if len(pairs) != nv - 1: return None
    adj = [[] for _ in range(nv)]
    for a, b in pairs: adj[a].append(b); adj[b].append(a)
    col = [None] * nv; col[0] = 0; st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if col[w] is None: col[w] = 1 - col[u]; st.append(w)
            elif col[w] == col[u]: return None
    if any(c is None for c in col): return None
    return col

def is_transversal(edges, S):
    return all(any(v in S for v in e) for e in edges)

def check_L(n, edges, l, r, stats, tag):
    """G_L statements. returns list of failures."""
    k = n // 2; fails = []
    pairs = [(l[j], j) for j in range(1, n - 1)]
    col = components_color(n - 1, pairs)
    if col is None: return [('G_L not spanning tree', tag)]
    c1 = [v for v in range(n - 1) if col[v] == 1]; c0 = [v for v in range(n - 1) if col[v] == 0]
    if len(c0) > len(c1): c0, c1 = c1, c0; col = [1 - c for c in col]   # now C_0 small
    if (len(c0), len(c1)) != (k - 1, k): fails.append(('L1', len(c0), len(c1)))
    if not (is_transversal(edges, set(c0)) and is_transversal(edges, set(c1))): fails.append(('transv', ))
    stats['L1'] += 1
    # subtrees T_j: descendants via l-chain
    children = {}
    for j in range(1, n - 1): children.setdefault(l[j], []).append(j)
    def sub(j):
        out = []; st = [j]
        while st:
            u = st.pop(); out.append(u); st += children.get(u, [])
        return out
    for j in range(1, n - 1):
        rj = r[j]
        if rj == n - 1: stats['L2_skip_rn'] += 1; continue
        Tj = sub(j); Ts = set(Tj)
        if rj in Ts: stats['L2_skip_inT'] += 1; continue
        newpairs = [(l[i], i) if i != j else (j, rj) for i in range(1, n - 1)]
        nc = components_color(n - 1, newpairs)
        if nc is None: fails.append(('L2 not tree', j)); continue
        flipped = col[rj] != col[l[j]]
        # expected colouring
        exp = list(col)
        if flipped:
            for v in Ts: exp[v] = 1 - exp[v]
        if nc != exp and [1 - x for x in nc] != exp: fails.append(('L2 colouring mismatch', j))
        # make nc agree with exp orientation
        if nc != exp: nc = [1 - x for x in nc]
        s0 = [v for v in range(n - 1) if nc[v] == 0]; s1 = [v for v in range(n - 1) if nc[v] == 1]
        if not (is_transversal(edges, set(s0)) and is_transversal(edges, set(s1))): fails.append(('L2 transv', j))
        if min(len(s0), len(s1)) < k - 1: fails.append(('L2 size', j, len(s0), len(s1)))
        t0 = sum(1 for v in Tj if col[v] == 0); t1 = len(Tj) - t0
        if flipped:
            stats['L2_flip'] += 1
            if t1 - t0 not in (0, 1): fails.append(('L2 t1-t0', j, t0, t1))
        else:
            stats['L2_noflip'] += 1
    return fails

def reflect(n, edges):
    return [tuple(sorted(n - 1 - v for v in e)) for e in edges]

def check_all(n, edges, stats, tag=None):
    """Return list of failures for lemma 1,2 on G_L and G_R (via reflection)."""
    edges = [tuple(sorted(e)) for e in edges]
    p = parse(n, edges)
    if p is None: stats['not_saturated'] += 1; return []
    if n % 2: stats['odd'] += 1; return []
    tau = n - alpha_of_edges(n, edges)
    if tau != n // 2 - 1: stats['not_GLtight'] += 1; return []
    stats['tested'] += 1
    f = [('GL', x) for x in check_L(n, edges, p[0], p[1], stats, tag)]
    re = reflect(n, edges); pr = parse(n, re)
    f += [('GR', x) for x in check_L(n, re, pr[0], pr[1], stats, tag)]
    return f
