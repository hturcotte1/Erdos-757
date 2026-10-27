"""L026 own library (independent of e757/, judge/ and of L021's kt.py).
Exact integer arithmetic only.  Hypergraphs: (n, edges) with vertices 0..n-1, edges 3-tuples.
A(H) = 27 n + 35 m - 132 tau ; DEF over L*-families (pieces read from L021's closure_results.json,
which is used as DATA only: the 32 edge lists of L*); P = A + DEF."""
import json, re, itertools, sys
sys.setrecursionlimit(100000)

PIECES_PATH = '/home/user/Erdos-757/experiments/prover/L021/closure_results.json'

def read_found(path):
    out = []
    for l in open(path):
        if l.startswith('FOUND'):
            E = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
            out.append(E)
    return out

def read_flat(path):
    out = []
    for l in open(path):
        t = l.split()
        if len(t) < 3: continue
        n, m, tau = int(t[0]), int(t[1]), int(t[2])
        f = list(map(int, t[3:3 + 3 * m]))
        out.append([tuple(f[3 * i:3 * i + 3]) for i in range(m)])
    return out

def nv(E):
    return 1 + max(max(e) for e in E) if E else 0

def degs(n, E):
    d = [0] * n
    for e in E:
        for x in e: d[x] += 1
    return d

def emasks(E):
    return [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in E]

def tau(E, forced=0, forbid=0):
    """minimum size of a transversal T with forced <= T and T & forbid == 0 (None if impossible)."""
    em = emasks(E)
    best = [None]
    def rec(rem, size):
        if best[0] is not None and size >= best[0]: return
        if not rem:
            best[0] = size; return
        # lower bound: greedy disjoint edges
        used = 0; lb = 0
        for e in rem:
            if not e & used: used |= e; lb += 1
        if best[0] is not None and size + lb >= best[0]: return
        e = min(rem, key=lambda f: bin(f & ~forbid).count('1'))
        cand = e & ~forbid
        while cand:
            b = cand & -cand; cand ^= b
            rec([f for f in rem if not f & b], size + 1)
    start = [e for e in em if not e & forced]
    size0 = bin(forced).count('1')
    rec(start, size0)
    return best[0]

def all_min_transversals(E, t=None):
    em = emasks(E)
    if t is None: t = tau(E)
    res = []
    def rec(rem, chosen, k, forb):
        if not rem:
            res.append(chosen); return
        if k == t: return
        used = 0; lb = 0
        for e in rem:
            if not e & used: used |= e; lb += 1
        if k + lb > t: return
        e = rem[0]; cand = e & ~forb; f2 = forb
        while cand:
            b = cand & -cand; cand ^= b
            rec([f for f in rem if not f & b], chosen | b, k + 1, f2)
            f2 |= b
    rec(list(em), 0, 0, 0)
    return res

def is_linear(E):
    seen = {}
    for i, e in enumerate(E):
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen[p] = i
    return len(set(tuple(sorted(e)) for e in E)) == len(E)

F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]

def has_F7(n, E):
    """F7 as a (not necessarily induced) subgraph; brute force over 5-edge subsets on 7 vertices
    with the F7 degree pattern; fine for small n."""
    Es = [tuple(sorted(e)) for e in E]
    d = degs(n, E)
    # F7 centre has degree 3 in F7; every F7 vertex has F7-degree >= 2
    inc = [[] for _ in range(n)]
    for i, e in enumerate(Es):
        for x in e: inc[x].append(i)
    for c in range(n):
        if d[c] < 3: continue
        for trio in itertools.combinations(inc[c], 3):
            pairs = [tuple(x for x in Es[i] if x != c) for i in trio]
            V = {c} | set(pairs[0]) | set(pairs[1]) | set(pairs[2])
            if len(V) != 7: continue
            # need two more edges inside V, disjoint from c, each meeting each pair in exactly one vertex
            inside = [Es[i] for i in range(len(Es)) if set(Es[i]) <= V and c not in Es[i]]
            for f, g in itertools.combinations(inside, 2):
                ok = True
                for pr in pairs:
                    if len(set(f) & set(pr)) != 1 or len(set(g) & set(pr)) != 1: ok = False; break
                if ok and len(set(f) & set(g)) == 0:
                    return True
    return False

def p3_ok(n, E):
    """(P3): e(S) <= |S| - 2 for every S with |S| >= 2.  A violation has an edge inside S, so it suffices
    to compute, for every edge e0, max over S containing e0 of e(S) - |S| (a maximum-weight closure:
    edge nodes +1, vertex nodes -1, an edge node requires its three vertex nodes; e0 forced by a large
    weight), via one minimum cut each: max_{S >= e0} (e(S) - |S|) = m - mincut.  Exact (integer capacities)."""
    import networkx as nx
    m = len(E)
    if m == 0: return True
    BIG = 10 * (m + n + 5)
    for i0 in range(m):
        G = nx.DiGraph()
        for i, e in enumerate(E):
            G.add_edge('s', ('e', i), capacity=(BIG if i == i0 else 1))
            for x in e:
                G.add_edge(('e', i), ('v', x), capacity=10 ** 9)
        for x in range(n):
            G.add_edge(('v', x), 't', capacity=1)
        cut, _ = nx.minimum_cut(G, 's', 't')
        best = (BIG + m - 1) - cut - (BIG - 1)
        if best >= -1: return False
    return True

def in_C3(n, E):
    d = degs(n, E)
    if d and max(d) > 3: return False
    if not is_linear(E): return False
    if has_F7(n, E): return False
    return p3_ok(n, E)

def A_val(n, m, t):
    return 27 * n + 35 * m - 132 * t

# ---------------- pieces and DEF ----------------
class Piece:
    def __init__(self, name, edges):
        self.name = name
        self.E = [tuple(e) for e in edges]
        self.n = nv(self.E); self.m = len(self.E)
        self.t = tau(self.E)
        self.W = -A_val(self.n, self.m, self.t)
        self.adj = [set() for _ in range(self.n)]
        for e in self.E:
            for x in e:
                for y in e:
                    if x != y: self.adj[x].add(y)
        self.deg = degs(self.n, self.E)
        order = [max(range(self.n), key=lambda x: self.deg[x])]
        seen = set(order); i = 0
        while i < len(order):
            for y in sorted(self.adj[order[i]]):
                if y not in seen: seen.add(y); order.append(y)
            i += 1
        assert len(order) == self.n
        self.order = order
        self.Eset = set(tuple(sorted(e)) for e in self.E)

def load_pieces():
    d = json.load(open(PIECES_PATH))
    return [Piece(p['name'], p['edges']) for p in d['pieces']]

def induced_copies(P, n, E):
    """vertex sets (bitmasks) W with H[W] isomorphic to P (H = (n, E))."""
    if P.n > n: return []
    Es = set(tuple(sorted(e)) for e in E)
    adj = [set() for _ in range(n)]
    for e in E:
        for x in e:
            for y in e:
                if x != y: adj[x].add(y)
    d = degs(n, E)
    em = emasks(E)
    found = set()
    phi = {}; used = set()
    pos = {x: i for i, x in enumerate(P.order)}
    def rec(i):
        if i == P.n:
            Wm = 0
            for u in phi.values(): Wm |= 1 << u
            if Wm in found: return
            if sum(1 for f in em if f & Wm == f) == P.m:
                found.add(Wm)
            return
        x = P.order[i]
        nb = [phi[y] for y in P.adj[x] if y in phi]
        cand = set(adj[nb[0]]) if nb else set(range(n))
        for z in nb[1:]: cand &= adj[z]
        for u in cand:
            if u in used or d[u] < P.deg[x]: continue
            ok = True
            # adjacency must be preserved exactly among mapped vertices? (induced: checked at the end by
            # edge count; here only check piece edges whose vertices are all mapped)
            phi[x] = u; used.add(u)
            for e in P.E:
                if x in e and all(y in phi for y in e):
                    if tuple(sorted(phi[y] for y in e)) not in Es: ok = False; break
            if ok: rec(i + 1)
            del phi[x]; used.discard(u)
    rec(0)
    return list(found)

def DEF(n, E, pieces, want=False):
    em = emasks(E)
    copies = []
    for P in pieces:
        for Wm in induced_copies(P, n, E):
            copies.append((Wm, P.W, P.m, P.name))
    copies.sort(key=lambda c: -c[1])
    best = [0, []]
    def bd(U):
        return sum(1 for f in em if f & U)
    def rec(i, U, gain, fam):
        obj = gain - 35 * bd(U)
        if obj > best[0]: best[0] = obj; best[1] = list(fam)
        ub = obj + sum(c[1] for c in copies[i:] if not c[0] & U)
        if ub <= best[0]: return
        for j in range(i, len(copies)):
            Wm, w, mP, name = copies[j]
            if Wm & U: continue
            fam.append((Wm, name))
            rec(j + 1, U | Wm, gain + w + 35 * mP, fam)
            fam.pop()
    rec(0, 0, 0, [])
    return (best[0], best[1]) if want else best[0]

def P_val(n, E, pieces):
    t = tau(E) if E else 0
    return A_val(n, len(E), t) + (DEF(n, E, pieces) if E else 0)

def components(n, E):
    par = list(range(n))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in E:
        a = f(e[0])
        for x in e[1:]:
            b = f(x)
            if a != b: par[b] = a
    comp = {}
    for x in range(n): comp.setdefault(f(x), []).append(x)
    return list(comp.values())

def induced(E, S):
    """induced subgraph on vertex list S, relabelled 0..|S|-1 in the order of S."""
    idx = {x: i for i, x in enumerate(S)}
    return [tuple(idx[x] for x in e) for e in E if all(x in idx for x in e)]

def P_of_vertexset(E, S, pieces):
    Ei = induced(E, S)
    return P_val(len(S), Ei, pieces)

def hub(n, E, a, b, c):
    v, x, y, z = n, n + 1, n + 2, n + 3
    return n + 4, list(E) + [(x, y, z), (v, x, a), (v, y, b), (v, z, c)]
