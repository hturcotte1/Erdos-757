"""Structural statistics of saturated ordered midpoint patterns. Exact, integer. [verified-here]"""
import itertools, numpy as np
from collections import Counter

_cache = {}
def _masks(n):
    if n not in _cache:
        _cache[n] = np.arange(1 << n, dtype=np.int64)
    return _cache[n]

def tree_stats(par, verts, root):
    """par: dict child->parent on verts (tree rooted at root)."""
    ch = {v: [] for v in verts}
    for c, p in par.items():
        ch[p].append(c)
    depth = {root: 0}
    stack = [root]
    while stack:
        v = stack.pop()
        for c in ch[v]:
            depth[c] = depth[v] + 1
            stack.append(c)
    assert len(depth) == len(verts)
    deg = {v: len(ch[v]) + (0 if v == root else 1) for v in verts}
    leaves = [v for v in verts if deg[v] == 1]
    internal = [v for v in verts if deg[v] > 1]
    iset = set(internal)
    nbr = {v: [] for v in verts}
    for c, p in par.items():
        nbr[c].append(p); nbr[p].append(c)
    cat = all(sum(1 for u in nbr[v] if u in iset) <= 2 for v in internal)
    cls = Counter(d % 2 for d in depth.values())
    return dict(depth=max(depth.values()), leaves=len(leaves), caterpillar=int(cat),
                cls=tuple(sorted((cls[0], cls[1]))), rootcls=cls[0], maxdeg=max(deg.values()),
                rootdeg=deg[root], internal=len(internal))

def matching_number(edges):
    best = 0
    es = [frozenset(e) for e in edges]
    def rec(idx, used, cnt):
        nonlocal best
        best = max(best, cnt)
        if cnt + (len(es) - idx) <= best:
            return
        for t in range(idx, len(es)):
            if not (es[t] & used):
                rec(t + 1, used | es[t], cnt + 1)
    rec(0, frozenset(), 0)
    return best

def stats(edges, n):
    edges = [tuple(e) for e in edges]
    deg = [0] * n; L = [0] * n; M = [0] * n; R = [0] * n
    for (i, j, k) in edges:
        for v in (i, j, k): deg[v] += 1
        L[i] += 1; M[j] += 1; R[k] += 1
    s = {}
    s['degseq'] = tuple(sorted(deg, reverse=True))
    s['maxdeg'] = max(deg)
    s['deg0'] = deg[0]; s['degN'] = deg[n - 1]
    s['deg0+degN'] = deg[0] + deg[n - 1]
    s['deg1'] = deg[1]; s['degN-2'] = deg[n - 2]
    for d in (1, 2, 3, 4, 5):
        s['n_deg%d' % d] = sum(1 for x in deg if x == d)
    s['roles'] = tuple(sorted(zip(L, M, R)))
    s['maxL'] = max(L); s['maxR'] = max(R)
    s['L0'] = L[0]; s['RN'] = R[n - 1]
    s['n_Lonly'] = sum(1 for v in range(n) if L[v] and not R[v] and not M[v])
    s['n_Ronly'] = sum(1 for v in range(n) if R[v] and not L[v] and not M[v])
    s['n_Monly'] = sum(1 for v in range(n) if M[v] and not L[v] and not R[v])
    s['n_LR_noM'] = sum(1 for v in range(n) if L[v] and R[v] and not M[v])   # none for ends
    s['n_roles3'] = sum(1 for v in range(n) if (L[v] > 0) + (M[v] > 0) + (R[v] > 0) == 3)
    spans = [k - i for (i, j, k) in edges]
    s['spans'] = tuple(sorted(spans))
    s['maxspan'] = max(spans); s['minspan'] = min(spans)
    s['full_edge'] = int(any(i == 0 and k == n - 1 for (i, j, k) in edges))
    s['n_edges_0_or_N'] = sum(1 for (i, j, k) in edges if i == 0 or k == n - 1 or j == 0)
    s['n_edges_0_and_N'] = sum(1 for (i, j, k) in edges if i == 0 and k == n - 1)
    parL = {j: i for (i, j, k) in edges}
    parR = {j: k for (i, j, k) in edges}
    tl = tree_stats(parL, list(range(n - 1)), 0)
    tr = tree_stats({j: parR[j] for j in parR}, list(range(1, n)), n - 1)
    for key, v in tl.items(): s['GL_' + key] = v
    for key, v in tr.items(): s['GR_' + key] = v
    s['GL_GR_shape_eq'] = int(tl == tr)
    s['r1'] = parR[1] if 1 in parR else -1           # right end of vertex 1's edge (0,1,r)
    s['l(N-2)'] = parL[n - 2] if n - 2 in parL else -1
    s['nu'] = matching_number(edges)
    # independent sets
    masks = _masks(n)
    bad = np.zeros(len(masks), dtype=bool)
    for e in edges:
        em = (1 << e[0]) | (1 << e[1]) | (1 << e[2])
        bad |= (masks & em) == em
    ind = ~bad
    pc = np.zeros(len(masks), dtype=np.int8)
    for b in range(n):
        pc += ((masks >> b) & 1).astype(np.int8)
    a = int(pc[ind].max())
    s['alpha'] = a
    s['n_maxind'] = int(np.count_nonzero(ind & (pc == a)))
    s['n_ind_alpha-1'] = int(np.count_nonzero(ind & (pc == a - 1)))
    # vertices lying in no maximum independent set / in all
    mis = masks[ind & (pc == a)]
    s['n_in_all_MIS'] = int(sum(1 for b in range(n) if np.all((mis >> b) & 1)))
    s['n_in_no_MIS'] = int(sum(1 for b in range(n) if not np.any((mis >> b) & 1)))
    # extra local features
    ls = [parL[j] for j in range(1, n - 1)]; rs = [parR[j] for j in range(1, n - 1)]
    s['n_l_adj'] = sum(1 for j in range(1, n - 1) if parL[j] == j - 1)
    s['n_r_adj'] = sum(1 for j in range(1, n - 1) if parR[j] == j + 1)
    s['n_span2'] = sum(1 for (i, j, k) in edges if k - i == 2)
    s['inv_l'] = sum(1 for a in range(len(ls)) for b in range(a + 1, len(ls)) if ls[a] > ls[b])
    s['inv_r'] = sum(1 for a in range(len(rs)) for b in range(a + 1, len(rs)) if rs[a] > rs[b])
    s['n_edges_through_1'] = deg[1]
    s['n_edges_12'] = sum(1 for (i, j, k) in edges if j <= (n - 1) // 2)       # midpoints in lower half
    s['n_deg_ge3_adj'] = sum(1 for v in range(n - 1) if deg[v] >= 3 and deg[v + 1] >= 3)
    s['n_deg_le2_adj'] = sum(1 for v in range(n - 1) if deg[v] <= 2 and deg[v + 1] <= 2)
    s['n_Lnodes'] = sum(1 for v in range(n) if L[v] > 0)
    s['n_Rnodes'] = sum(1 for v in range(n) if R[v] > 0)
    s['n_Mnodes_with_LR'] = sum(1 for v in range(n) if M[v] and (L[v] or R[v]))
    s['sum_deg_even_pos'] = sum(deg[v] for v in range(0, n, 2))
    s['maxdeg_pos'] = min(v for v in range(n) if deg[v] == max(deg))
    # reflection symmetric
    refl = sorted((n - 1 - k, n - 1 - j, n - 1 - i) for (i, j, k) in edges)
    s['refl_sym'] = int(refl == sorted(edges))
    return s
