"""L021 core: exact transversal numbers, induced-copy search and the deficiency
DEF_L(F) = max(0, max_X sum_{P in X} W(P) - 35 |E*(X)|) for epsilon = 1/6, t = 11/12
(all quantities multiplied by 12: A(F) = 27n + 35m - 132 tau, W = -A, edge cost C = 35).
Hypergraphs: n (vertices 0..n-1) and a list of 3-tuples. Exact integer arithmetic only."""
import re, sys, itertools
sys.setrecursionlimit(10000)
CN, CM, CT, CE = 27, 35, 132, 35      # A = CN*n + CM*m - CT*tau ; edge cost in DEF = CE

def parse_edges(line):
    return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]

def read_cell(path):
    return [parse_edges(l) for l in open(path) if l.startswith('FOUND')]

def nverts(edges):
    return 1 + max(max(e) for e in edges) if edges else 0

def tau_masks(em):
    em = list(em); best = [len(em)]
    def lb(rem):
        used = 0; k = 0
        for e in rem:
            if not e & used: used |= e; k += 1
        return k
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        if k + lb(rem) >= best[0]: return
        e = rem[0]; m = e
        while m:
            b = m & -m; m ^= b
            rec([f for f in rem if not f & b], k + 1)
    rec(em, 0)
    return best[0]

def masks(edges):
    return [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]

def A_value(n, m, t):
    return CN * n + CM * m - CT * t

def min_transversals(em, t):
    res = []
    def lb(rem):
        used = 0; k = 0
        for e in rem:
            if not e & used: used |= e; k += 1
        return k
    def rec(rem, chosen, k, forb):
        if not rem:
            res.append(chosen); return
        if k == t or k + lb(rem) > t: return
        e = rem[0]; cand = e & ~forb; f2 = forb
        while cand:
            b = cand & -cand; cand ^= b
            rec([f for f in rem if not f & b], chosen | b, k + 1, f2)
            f2 |= b
    rec(list(em), 0, 0, 0)
    return res

class Piece:
    def __init__(self, edges, name):
        self.edges = [tuple(e) for e in edges]
        self.n = nverts(self.edges); self.m = len(self.edges)
        self.tau = tau_masks(masks(self.edges))
        self.W = -A_value(self.n, self.m, self.tau)
        self.name = name
        adj = [set() for _ in range(self.n)]
        self.inc = [[] for _ in range(self.n)]
        for i, e in enumerate(self.edges):
            for x in e:
                self.inc[x].append(i)
                for y in e:
                    if y != x: adj[x].add(y)
        self.deg = [len(self.inc[x]) for x in range(self.n)]
        # BFS order for matching (connected pieces)
        order = [max(range(self.n), key=lambda x: self.deg[x])]; seen = set(order)
        i = 0
        while i < len(order):
            for y in sorted(adj[order[i]], key=lambda y: -self.deg[y]):
                if y not in seen: seen.add(y); order.append(y)
            i += 1
        assert len(order) == self.n, 'piece must be connected'
        self.order = order
        self.adj = adj

def induced_copies(piece, n, edges):
    """all vertex sets W (bitmasks) with F[W] isomorphic to piece (F = (n, edges))."""
    if piece.n > n: return set()
    eset = set(tuple(sorted(e)) for e in edges)
    deg = [0] * n
    adj = [set() for _ in range(n)]
    for e in edges:
        for x in e:
            deg[x] += 1
            for y in e:
                if y != x: adj[x].add(y)
    fm = masks(edges)
    found = set()
    P = piece; order = P.order
    pos = {x: i for i, x in enumerate(order)}
    phi = {}; used = set()
    # for each piece vertex, the piece edges whose vertices are all mapped once it is mapped
    check_at = [[] for _ in range(P.n)]
    for e in P.edges:
        last = max(e, key=lambda x: pos[x]); check_at[pos[last]].append(e)
    def rec(i):
        if i == P.n:
            W = 0
            for x in phi.values(): W |= 1 << x
            if W in found: return
            k = sum(1 for e in fm if e & W == e)
            if k == P.m: found.add(W)
            return
        x = order[i]
        # candidates: neighbours of an already mapped neighbour (connectivity), else all
        mapped_nb = [phi[y] for y in P.adj[x] if y in phi]
        if mapped_nb:
            cand = set(adj[mapped_nb[0]])
            for z in mapped_nb[1:]: cand &= adj[z]
        else:
            cand = set(range(n))
        for u in cand:
            if u in used or deg[u] < P.deg[x]: continue
            phi[x] = u; used.add(u)
            ok = True
            for e in check_at[i]:
                if tuple(sorted(phi[y] for y in e)) not in eset: ok = False; break
            if ok: rec(i + 1)
            del phi[x]; used.discard(u)
    rec(0)
    return found

def deficiency(n, edges, pieces, proper=True, want_family=False):
    """exact DEF (times 12) over families of disjoint induced copies of the given pieces
    (only pieces with fewer vertices than F if proper).  objective of a family X with union U:
    sum_P (W_P + 35 m_P) - 35 |{edges meeting U}|."""
    fm = masks(edges)
    copies = []
    for P in pieces:
        if proper and P.n >= n: continue
        if P.W <= 0: continue
        for W in induced_copies(P, n, edges):
            copies.append((W, P.W, P.m, P.name))
    copies.sort(key=lambda c: -c[1])
    best = [0, []]
    def bd(U):
        return sum(1 for e in fm if e & U)
    def rec(i, U, gainsum, fam):
        # objective
        obj = gainsum - CE * bd(U)
        if obj > best[0]:
            best[0] = obj; best[1] = list(fam)
        # bound: obj + sum of W of remaining compatible copies
        ub = obj + sum(c[1] for c in copies[i:] if not c[0] & U)
        if ub <= best[0]: return
        for j in range(i, len(copies)):
            W, w, mP, name = copies[j]
            if W & U: continue
            fam.append((W, name))
            rec(j + 1, U | W, gainsum + w + CE * mP, fam)
            fam.pop()
    rec(0, 0, 0, [])
    if want_family:
        return best[0], best[1], len(copies)
    return best[0]
