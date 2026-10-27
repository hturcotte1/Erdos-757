"""Referee #2 (L021) independent library.  No import of e757, judge, or experiments/prover/L021/kt.py.
tau via SAT (pysat) with cardinality constraints; induced copies via edge subsets + VF2 on incidence graphs;
DEF via exhaustive / branch-and-bound over disjoint families (own code)."""
import re, itertools, sys
import networkx as nx
from networkx.algorithms import isomorphism as iso
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

CN, CM, CT, CE = 27, 35, 132, 35

def parse_cell(path):
    out = []
    for line in open(path):
        if line.startswith('FOUND'):
            out.append([tuple(int(a) for a in t) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', line)])
    return out

def nverts(edges):
    return 1 + max(max(e) for e in edges) if edges else 0

def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for x in e: d[x] += 1
    return d

def is_linear(edges):
    es = [set(e) for e in edges]
    for i in range(len(es)):
        if len(es[i]) != 3: return False
        for j in range(i):
            if len(es[i] & es[j]) >= 2: return False
    return True

def is_connected(n, edges):
    if n == 0: return True
    adj = [set() for _ in range(n)]
    for e in edges:
        for x in e:
            for y in e:
                if x != y: adj[x].add(y)
    seen = {0}; stack = [0]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); stack.append(y)
    return len(seen) == n

def has_F7(edges):
    """F7 = unique linear 3-graph with 5 edges, 7 vertices, degree sequence (3,2,2,2,2,2,2)."""
    for sub in itertools.combinations(edges, 5):
        vs = set().union(*map(set, sub))
        if len(vs) != 7: continue
        d = {}
        for e in sub:
            for x in e: d[x] = d.get(x, 0) + 1
        if sorted(d.values()) == [2, 2, 2, 2, 2, 2, 3] and is_linear(sub):
            return True
    return False

def P3_ok(n, edges, maxsize=None):
    """e(S) <= |S|-2 for all |S|>=2  <=>  every nonempty edge set U spans >= |U|+2 vertices."""
    m = len(edges)
    rng = range(1, m + 1) if maxsize is None else range(1, min(m, maxsize) + 1)
    for k in rng:
        for sub in itertools.combinations(edges, k):
            if len(set().union(*map(set, sub))) < k + 2: return False
    return True

def tau_sat(n, edges, with_vertices=(), ub=None):
    """minimum transversal size via SAT: variables 1..n; each edge a clause; cardinality atmost k."""
    if not edges: return 0
    lo = 0
    k = len(edges) if ub is None else ub
    best = None
    # decreasing search
    for t in range(k, -1, -1):
        if sat_transversal(n, edges, t, with_vertices): best = t
        else: break
    return best

def sat_transversal(n, edges, t, with_vertices=()):
    """is there a transversal of size <= t containing all vertices of with_vertices?"""
    if t < 0: return False
    cnf = [[x + 1 for x in e] for e in edges]
    for v in with_vertices: cnf.append([v + 1])
    top = n
    card = CardEnc.atmost(lits=list(range(1, n + 1)), bound=t, top_id=top, encoding=EncType.seqcounter)
    with Solver(name='cadical153', bootstrap_with=cnf + card.clauses) as s:
        return s.solve()

def min_transversals_brute(n, edges, t):
    """all transversals of size exactly t (as frozensets), brute force over combinations (small graphs only)."""
    es = [set(e) for e in edges]
    res = []
    for T in itertools.combinations(range(n), t):
        Ts = set(T)
        if all(e & Ts for e in es): res.append(frozenset(T))
    return res

def incidence_graph(vs, edges):
    G = nx.Graph()
    for v in vs: G.add_node(('v', v), kind=0)
    for i, e in enumerate(edges):
        G.add_node(('e', i), kind=1)
        for x in e: G.add_edge(('v', x), ('e', i))
    return G

_nm = iso.categorical_node_match('kind', None)

def hyper_iso(vs1, e1, vs2, e2):
    if len(vs1) != len(vs2) or len(e1) != len(e2): return False
    d1 = sorted(degrees_dict(vs1, e1).values()); d2 = sorted(degrees_dict(vs2, e2).values())
    if d1 != d2: return False
    return nx.is_isomorphic(incidence_graph(vs1, e1), incidence_graph(vs2, e2), node_match=_nm)

def degrees_dict(vs, edges):
    d = {v: 0 for v in vs}
    for e in edges:
        for x in e: d[x] += 1
    return d

class Piece:
    def __init__(self, edges, name):
        self.edges = [tuple(e) for e in edges]
        self.n = nverts(self.edges); self.m = len(self.edges)
        self.tau = tau_sat(self.n, self.edges)
        self.A = CN * self.n + CM * self.m - CT * self.tau
        self.W = -self.A
        self.name = name
        self.degseq = sorted(degrees(self.n, self.edges))
        self.inc = incidence_graph(range(self.n), self.edges)

def induced_copies(piece, n, edges):
    """vertex sets S (bitmask) with H[S] isomorphic to piece: enumerate m_F-subsets of edges whose union has n_F
    vertices and contains no further edge, then VF2 on incidence graphs."""
    res = set()
    if piece.n > n or piece.m > len(edges): return res
    esets = [frozenset(e) for e in edges]
    for sub in itertools.combinations(range(len(edges)), piece.m):
        vs = frozenset().union(*(esets[i] for i in sub))
        if len(vs) != piece.n: continue
        mask = 0
        for x in vs: mask |= 1 << x
        if mask in res: continue
        # induced: no other edge inside vs
        inside = [i for i in range(len(edges)) if esets[i] <= vs]
        if len(inside) != piece.m: continue
        subedges = [edges[i] for i in sub]
        d = sorted(degrees_dict(vs, subedges).values())
        if d != piece.degseq: continue
        if nx.is_isomorphic(incidence_graph(vs, subedges), piece.inc, node_match=_nm):
            res.add(mask)
    return res

def deficiency(n, edges, pieces, proper=True, exhaustive_limit=18):
    """DEF = max over families X of disjoint induced copies of pieces of sum W - 35 |E*(X)|, X = empty allowed (-> >= 0).
    Returns (DEF, best family list of (mask, name))."""
    emasks = []
    for e in edges:
        mk = 0
        for x in e: mk |= 1 << x
        emasks.append(mk)
    full = (1 << n) - 1
    copies = []
    for P in pieces:
        if P.W <= 0: continue
        for mk in induced_copies(P, n, edges):
            if proper and mk == full: continue
            copies.append((mk, P.W, P.m, P.name))
    copies.sort(key=lambda c: (-c[1], c[0]))
    def objective(sel):
        U = 0; gain = 0; inside = 0
        for (mk, w, mP, nm) in sel:
            U |= mk; gain += w; inside += mP
        meets = sum(1 for em in emasks if em & U)
        return gain - CE * (meets - inside)
    best = [0, []]
    if len(copies) <= exhaustive_limit:
        # exhaustive over all subsets of pairwise disjoint copies
        def rec(i, sel, U):
            if i == len(copies):
                val = objective(sel)
                if val > best[0]: best[0] = val; best[1] = list(sel)
                return
            rec(i + 1, sel, U)
            if not (copies[i][0] & U):
                sel.append(copies[i]); rec(i + 1, sel, U | copies[i][0]); sel.pop()
        rec(0, [], 0)
        return best[0], [(c[0], c[3]) for c in best[1]], len(copies)
    # branch and bound (bound: adding a copy raises the objective by at most its W, since E* only grows)
    def rec2(i, sel, U):
        val = objective(sel)
        if val > best[0]: best[0] = val; best[1] = list(sel)
        ub = val + sum(c[1] for c in copies[i:] if not (c[0] & U))
        if ub <= best[0]: return
        for j in range(i, len(copies)):
            if copies[j][0] & U: continue
            sel.append(copies[j]); rec2(j + 1, sel, U | copies[j][0]); sel.pop()
    rec2(0, [], 0)
    return best[0], [(c[0], c[3]) for c in best[1]], len(copies)
