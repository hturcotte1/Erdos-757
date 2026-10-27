"""my_localconf.py -- referee's independent enumeration of pendant-root local configurations (L018 Theorem 3).

Independent implementation. Same branching semantics as described in L018 Step 3.3 (so node counts can be compared),
but a different (Red) test: a quick brute force over |Z| <= 3 followed by an exact CP-SAT (integer programming) model
    max 3 sum z_v + 2 sum y_e - 11 sum t_v,  y_e = OR(z_v : v in e processed),  sum_{v in e} t_v >= y_e,  z_q = 1
over Z subsets of processed vertices containing the just-processed vertex q (Z != V when the configuration is closed).
Also classifies every radius-R leaf structurally (P-tree-R / P-tri-R / OTHER) and groups leaves by isomorphism (networkx).
Usage: python3 my_localconf.py ROOTDEG R
"""
import sys, itertools, time
from ortools.sat.python import cp_model
import networkx as nx

class Conf:
    __slots__ = ('edges', 'dist', 'nproc', 'deg')
    def __init__(self):
        self.edges = []; self.dist = []; self.nproc = 0; self.deg = []
    def copy(self):
        c = Conf(); c.edges = list(self.edges); c.dist = list(self.dist); c.nproc = self.nproc; c.deg = list(self.deg); return c
    def nv(self):
        return len(self.dist)
    def new_vertex(self, d):
        self.dist.append(d); self.deg.append(None); return len(self.dist) - 1
    def add_edge(self, e):
        self.edges.append(tuple(sorted(e)))
    def degree(self, v):
        return sum(1 for e in self.edges if v in e)
    def share(self, u, v):
        return any((u in e) and (v in e) for e in self.edges)

# ---------- exact tau (own implementation: branch on the vertices of a max-degree edge, no cache) ----------
def tau_edges(E):
    E = [frozenset(e) for e in E]
    best = [len(E)]
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        if k + 1 >= best[0]:
            return
        # pick edge; branch on its vertices
        e = rem[0]
        for v in e:
            rec([f for f in rem if v not in f], k + 1)
    rec(E, 0)
    return best[0]

def quick_small_Z(c, q, closed, kmax=3):
    P = [v for v in range(c.nproc) if v != q]
    nV = c.nv()
    for k in range(0, kmax):
        for S in itertools.combinations(P, k):
            Z = set(S) | {q}
            if closed and len(Z) == nV:
                continue
            EZ = [e for e in c.edges if Z & set(e)]
            val = 3 * len(Z) + 2 * len(EZ) - 11 * tau_edges(EZ)
            if val >= 0:
                return True, val, Z
    return False, None, None

def cpsat_best(c, q, closed):
    """exact maximum of value(Z) over Z subset of processed vertices with q in Z (Z != V if closed)."""
    m = cp_model.CpModel()
    nV = c.nv(); P = list(range(c.nproc))
    z = {v: m.NewBoolVar('z%d' % v) for v in P}
    t = [m.NewBoolVar('t%d' % v) for v in range(nV)]
    y = [m.NewBoolVar('y%d' % i) for i in range(len(c.edges))]
    m.Add(z[q] == 1)
    for i, e in enumerate(c.edges):
        pe = [v for v in e if v < c.nproc]
        assert pe, 'edge without processed vertex'
        for v in pe:
            m.Add(y[i] >= z[v])
        m.Add(y[i] <= sum(z[v] for v in pe))
        m.Add(sum(t[v] for v in e) >= y[i])
    if closed:
        m.Add(sum(z.values()) <= len(P) - 1)
    m.Maximize(3 * sum(z.values()) + 2 * sum(y) - 11 * sum(t))
    s = cp_model.CpSolver(); s.parameters.num_search_workers = 1; s.parameters.max_time_in_seconds = 600
    st = s.Solve(m)
    assert st == cp_model.OPTIMAL, 'CP-SAT not optimal'
    val = int(round(s.ObjectiveValue()))
    Z = frozenset(v for v in P if s.Value(z[v]))
    return val, Z

STATS = {'nodes': 0, 'reducible': 0, 'leaves': 0, 'cpsat_calls': 0, 'redZ': {}}

def reducible(c, q):
    closed = (c.nproc >= c.nv())
    ok, val, Z = quick_small_Z(c, q, closed)
    if ok:
        return True, val, Z
    STATS['cpsat_calls'] += 1
    val, Z = cpsat_best(c, q, closed)
    return (val >= 0), val, Z

def gen(c, R, leaves):
    q = c.nproc
    if q >= c.nv() or c.dist[q] > R:
        STATS['leaves'] += 1; leaves.append(c.copy()); return
    k = c.degree(q); dq = c.dist[q]
    cands = [w for w in range(q + 1, c.nv())
             if c.degree(w) < 3 and not c.share(q, w) and (c.dist[w] == dq or (c.dist[w] == dq + 1 and dq + 1 <= R))]
    NEW = -1
    types = [(NEW, NEW)] + [(w, NEW) for w in cands] + [(u, w) for u, w in itertools.combinations(cands, 2) if not c.share(u, w)]
    for D in range(max(k, 1), 4):
        r = D - k
        for combo in itertools.combinations_with_replacement(range(len(types)), r):
            used = [x for ti in combo for x in types[ti] if x != NEW]
            if len(used) != len(set(used)):
                continue
            c2 = c.copy()
            for ti in combo:
                a, b = types[ti]
                if a == NEW: a = c2.new_vertex(dq + 1)
                if b == NEW: b = c2.new_vertex(dq + 1)
                c2.add_edge((q, a, b))
            c2.deg[q] = D; c2.nproc = q + 1
            STATS['nodes'] += 1
            red, val, Z = reducible(c2, q)
            if red:
                STATS['reducible'] += 1
                key = (len(Z), val); STATS['redZ'][key] = STATS['redZ'].get(key, 0) + 1
                continue
            gen(c2, R, leaves)

def run(rootdeg, R):
    c = Conf(); r = c.new_vertex(0)
    for _ in range(rootdeg):
        a = c.new_vertex(1); b = c.new_vertex(1); c.add_edge((r, a, b))
    c.deg[r] = rootdeg; c.nproc = 1
    leaves = []
    gen(c, R, leaves)
    return leaves

# ---------- structural classification of a pendant-root leaf ----------
def ball(c, y, r):
    """vertices within 2-section distance r of y"""
    adj = {v: set() for v in range(c.nv())}
    for e in c.edges:
        for u in e:
            adj[u] |= set(e)
    B = {y}; frontier = {y}
    for _ in range(r):
        frontier = set().union(*(adj[v] for v in frontier)) - B
        B |= frontier
    return B

def classify(c, R):
    """returns a string describing the leaf type at radius R (root 0 pendant)."""
    E = [set(e) for e in c.edges]
    deg = lambda v: sum(1 for e in E if v in e)
    y = 0
    if c.nproc >= c.nv():
        return 'CLOSED(n=%d)' % c.nv()
    e0 = [e for e in E if y in e]
    if len(e0) != 1: return 'OTHER(rootdeg)'
    a, b = sorted(e0[0] - {y})
    if deg(a) != 2 or deg(b) != 2: return 'OTHER(a,b deg)'
    A = [e for e in E if a in e and y not in e][0]; B = [e for e in E if b in e and y not in e][0]
    B1 = ball(c, y, 1); B2 = ball(c, y, 2); B3 = ball(c, y, 3)
    def second_edges_ok(verts, prev_edge_of, Bprev):
        """each v in verts has degree 2; its second edge meets Bprev only in v; all second edges distinct"""
        secs = []
        for v in verts:
            if deg(v) != 2: return False, None
            s = [e for e in E if v in e and e != prev_edge_of[v]][0]
            if s & Bprev != {v}: return False, None
            secs.append(frozenset(s))
        if len(set(secs)) != len(secs): return False, None
        return True, secs
    if not (A & B):
        lvl2 = sorted((A | B) - {a, b})
        if len(lvl2) != 4: return 'OTHER(tree lvl2 count)'
        prev = {v: (A if v in A else B) for v in lvl2}
        ok, secs = second_edges_ok(lvl2, prev, B2)
        if not ok: return 'OTHER(tree lvl2)'
        if R == 2: return 'P-tree-2'
        lvl3 = [v for s in secs for v in s if v not in lvl2]
        if len(lvl3) != 8 or len(set(lvl3)) != 8: return 'OTHER(tree lvl3 distinct)'
        prev3 = {}
        for s in secs:
            for v in s:
                if v not in lvl2: prev3[v] = set(s)
        ok, secs3 = second_edges_ok(lvl3, prev3, B3)
        if not ok: return 'OTHER(tree lvl3)'
        if R == 3: return 'P-tree-3'
        return 'P-tree-%d(prefix ok)' % R
    else:
        cc = A & B
        if len(cc) != 1: return 'OTHER(|A&B|)'
        cv = next(iter(cc))
        if deg(cv) != 3: return 'OTHER(deg c)'
        ap = next(iter(A - {a, cv})); bp = next(iter(B - {b, cv}))
        if deg(ap) != 2 or deg(bp) != 2: return "OTHER(a',b' deg)"
        C = [e for e in E if cv in e and e != A and e != B][0]
        Ap = [e for e in E if ap in e and e != A][0]; Bp = [e for e in E if bp in e and e != B][0]
        if len({frozenset(C), frozenset(Ap), frozenset(Bp)}) != 3: return 'OTHER(C,A\',B\' distinct)'
        if C & B2 != {cv} or Ap & B2 != {ap} or Bp & B2 != {bp}: return 'OTHER(tri lvl2 meets B2)'
        if R == 2: return 'P-tri-2'
        six = [v for e in (C, Ap, Bp) for v in e if v not in (cv, ap, bp)]
        if len(six) != 6 or len(set(six)) != 6: return 'OTHER(tri six distinct)'
        inC = [v for v in C if v != cv]; inAB = [v for v in Ap | Bp if v not in (ap, bp)]
        if any(deg(v) != 2 for v in inAB): return "OTHER(tri A'B' degs)"
        dC = tuple(sorted(deg(v) for v in inC))
        if any(d not in (2, 3) for d in dC): return 'OTHER(tri C degs)'
        further = []
        for v in six:
            prev = C if v in C else (Ap if v in Ap else Bp)
            for e in E:
                if v in e and e != prev:
                    if e & B3 != {v}: return 'OTHER(tri further meets B3)'
                    further.append(frozenset(e))
        if len(set(further)) != len(further): return 'OTHER(tri further distinct)'
        if R == 3: return 'P-tri-3(Cdegs=%s)' % (dC,)
        return 'P-tri-%d(prefix ok)' % R

def leaf_graph(c):
    G = nx.Graph()
    for v in range(c.nv()):
        G.add_node(('v', v), kind='v', root=(v == 0), proc=(v < c.nproc), dist=c.dist[v])
    for i, e in enumerate(c.edges):
        G.add_node(('e', i), kind='e', root=False, proc=False, dist=-1)
        for v in e: G.add_edge(('e', i), ('v', v))
    return G

def nm(a, b):
    return a['kind'] == b['kind'] and a['root'] == b['root'] and a['proc'] == b['proc'] and a['dist'] == b['dist']

if __name__ == '__main__':
    rootdeg = int(sys.argv[1]); R = int(sys.argv[2])
    t0 = time.time()
    leaves = run(rootdeg, R)
    print('rootdeg', rootdeg, 'R', R, 'nodes', STATS['nodes'], 'reducible', STATS['reducible'], 'leaves', STATS['leaves'],
          'cpsat_calls', STATS['cpsat_calls'], 'secs %.1f' % (time.time() - t0))
    print('reducing (|Z|,value) counts:', sorted(STATS['redZ'].items()))
    # isomorphism classes of leaves
    classes = []
    for c in leaves:
        G = leaf_graph(c)
        for cl in classes:
            if nx.is_isomorphic(cl[0], G, node_match=nm):
                cl[1].append(c); break
        else:
            classes.append((G, [c]))
    print('isomorphism classes of leaves:', len(classes))
    for G, cs in classes:
        c = cs[0]
        print('  x%d  nV=%d nproc=%d closed=%s procdegs=%s type=%s' % (len(cs), c.nv(), c.nproc, c.nproc >= c.nv(),
              [c.deg[v] for v in range(c.nproc)], classify(c, R) if rootdeg == 1 else '-'))
        print('     edges', c.edges)
