"""Own verifier for referee round 2 of L020 (fable). No imports from e757/, judge/ or prover code.
3-graphs are lists of 3-tuples of ints; vertex set = set of all vertices that occur plus explicit extras."""
import sys, itertools, random

def parse_cell_file(path):
    out = []
    for line in open(path):
        t = line.split()
        if not t: continue
        n, m, tau = int(t[0]), int(t[1]), int(t[2])
        nums = list(map(int, t[3:]))
        assert len(nums) == 3*m, (path, line[:50])
        edges = [tuple(sorted(nums[3*i:3*i+3])) for i in range(m)]
        out.append((n, m, tau, edges))
    return out

def degrees(edges, verts):
    d = {v: 0 for v in verts}
    for e in edges:
        for v in e: d[v] += 1
    return d

def is_linear(edges):
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            if len(set(edges[i]) & set(edges[j])) >= 2: return False
    return True

def has_F7(edges):
    """F7 present iff some vertex x has 3 edges whose union U (7 vertices) contains two disjoint
    further edges avoiding x (then, by linearity, each meets each hub edge in exactly one vertex)."""
    inc = {}
    for e in edges:
        for v in e: inc.setdefault(v, []).append(e)
    eset = set(edges)
    for x, es in inc.items():
        if len(es) < 3: continue
        for trip in itertools.combinations(es, 3):
            U = set().union(*trip) - {x}
            if len(U) != 6: continue
            inside = [e for e in edges if set(e) <= U]
            for a in range(len(inside)):
                for b in range(a+1, len(inside)):
                    if not (set(inside[a]) & set(inside[b])): return True
    return False

def kuhn_saturates(edges, forbidden):
    """Hall test for the pair 'forbidden' = {x,y}: is there an SDR of the sets e \\ {x,y}?"""
    cand = [[v for v in e if v not in forbidden] for e in edges]
    match = {}  # vertex -> edge index
    def try_edge(i, seen):
        for v in cand[i]:
            if v in seen: continue
            seen.add(v)
            if v not in match or try_edge(match[v], seen):
                match[v] = i
                return True
        return False
    for i in range(len(edges)):
        if not try_edge(i, set()): return False
    return True

def p3_hall(edges, verts):
    vl = sorted(verts)
    for x, y in itertools.combinations(vl, 2):
        if not kuhn_saturates(edges, {x, y}): return False
    return True

def p3_exhaustive(edges):
    """|union E'| >= |E'| + 2 for every nonempty E' (only for small m)."""
    m = len(edges)
    masks = []
    for e in edges:
        mk = 0
        for v in e: mk |= 1 << v
        masks.append(mk)
    for sub in range(1, 1 << m):
        u = 0; k = 0
        s = sub
        i = 0
        while s:
            if s & 1:
                u |= masks[i]; k += 1
            s >>= 1; i += 1
        if bin(u).count('1') < k + 2: return False
    return True

def in_C(edges, verts):
    return is_linear(edges) and (not has_F7(edges)) and p3_hall(edges, verts)

# ---------- transversal number (own branch and bound, bitmasks) ----------
def _lb(rem):
    """greedy packing of pairwise disjoint edges = lower bound on tau"""
    used = 0; k = 0
    for e in rem:
        if not (e & used):
            used |= e; k += 1
    return k

def tau_masks(masks):
    best = [len(masks)]
    # order edges by decreasing total degree of their vertices to branch on 'heavy' edges first
    def rec(rem, cnt):
        if not rem:
            if cnt < best[0]: best[0] = cnt
            return
        if cnt + _lb(rem) >= best[0]: return
        # pick the edge with the fewest 'free' options? choose edge maximizing max vertex degree
        deg = {}
        for e in rem:
            x = e
            while x:
                b = x & -x; deg[b] = deg.get(b, 0) + 1; x ^= b
        # pick edge whose vertices have the largest degree sum
        e0 = max(rem, key=lambda e: sum(deg[b] for b in _bits(e)))
        for b in sorted(_bits(e0), key=lambda b: -deg[b]):
            rec([f for f in rem if not (f & b)], cnt + 1)
    rec(list(masks), 0)
    return best[0]

def _bits(x):
    out = []
    while x:
        b = x & -x; out.append(b); x ^= b
    return out

def to_masks(edges):
    out = []
    for e in edges:
        mk = 0
        for v in e: mk |= 1 << v
        out.append(mk)
    return out

def tau(edges):
    if not edges: return 0
    return tau_masks(to_masks(edges))

def induced(edges, removed):
    removed = set(removed)
    return [e for e in edges if not (set(e) & removed)]

def components(edges, verts):
    """components of the 3-graph on 'verts' with the given edges; returns (list of (vertset, edgelist)), isolated"""
    parent = {v: v for v in verts}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for e in edges:
        for u in e[1:]:
            ra, rb = find(e[0]), find(u)
            if ra != rb: parent[ra] = rb
    groups = {}
    for v in verts: groups.setdefault(find(v), set()).add(v)
    comps = []; isolated = set()
    for g in groups.values():
        es = [e for e in edges if e[0] in g]
        if es: comps.append((g, es))
        else: isolated |= g
    return comps, isolated

def slack(n, m, t): return 3*n + 2*m - 11*t

def cotransversal(edges, verts, X, t=None):
    """X co-transversal in (verts, edges) iff tau(H - X) = tau(H) - |X|"""
    if t is None: t = tau(edges)
    return tau(induced(edges, X)) == t - len(X)
