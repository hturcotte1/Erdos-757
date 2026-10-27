"""pend_enum.py -- referee's independent enumeration of split configurations around a root vertex
(check of L018 Theorem 3).  Written from the statement of Theorem 3 / Steps 3.1-3.4 only; does not import
the prover's code.

A configuration is grown in BFS order from the root y.  Vertices at distance <= R are 'processed': when a
vertex q is processed its final degree D (1..3) is chosen and all its missing edges are added; the other two
vertices of a new edge are fresh (distance d_q+1; boundary if d_q = R) or existing unprocessed vertices of
distance d_q or d_q+1 (only distance R when d_q = R, since boundary vertices of a split configuration lie in
one edge).  Only linearity and maximum degree 3 are imposed.  After q is processed every set Z of processed
vertices containing q is tested; value(Z) = 3|Z| + 2e(Z) - 11 tau(E_Z) >= 0 (with Z != V if no unprocessed
vertex remains) prunes the branch.  tau is computed by an independent exact routine (minimum hitting set by
increasing size with a matching lower bound).

Output: number of nodes, pruned nodes, leaves, and the leaves themselves (edge lists, processed degrees),
plus an isomorphism classification (networkx, rooted, processed/boundary-coloured incidence graphs).
Usage: python3 pend_enum.py ROOTDEG R
"""
import sys, itertools
import networkx as nx
from networkx.algorithms import isomorphism as iso

sys.setrecursionlimit(10000)


def popcount(x):
    return bin(x).count('1')


class State:
    def __init__(self):
        self.E = []        # list of sorted 3-tuples
        self.vm = []       # vertex -> bitmask of incident edges
        self.dist = []
        self.np = 0        # vertices 0..np-1 processed

    def clone(self):
        s = State()
        s.E = self.E[:]
        s.vm = self.vm[:]
        s.dist = self.dist[:]
        s.np = self.np
        return s

    def new_vertex(self, d):
        self.vm.append(0)
        self.dist.append(d)
        return len(self.vm) - 1

    def add_edge(self, a, b, c):
        i = len(self.E)
        self.E.append(tuple(sorted((a, b, c))))
        for v in (a, b, c):
            self.vm[v] |= (1 << i)

    def adjacent(self, u, w):
        # u, w lie in a common edge
        for i in range(len(self.E)):
            if (self.vm[u] >> i) & 1 and (self.vm[w] >> i) & 1:
                return True
        return False


def tau_edges(edge_list):
    """exact minimum hitting set of a list of 3-sets; independent routine."""
    edges = [frozenset(e) for e in edge_list]
    if not edges:
        return 0
    verts = sorted(set().union(*edges))
    # lower bound: greedy matching; upper bound: greedy cover
    def lb(es):
        used = set(); c = 0
        for e in sorted(es, key=lambda f: sorted(f)):
            if not (e & used):
                used |= e; c += 1
        return c
    best = [len(edges)]
    def rec(es, k):
        if not es:
            if k < best[0]:
                best[0] = k
            return
        if k + lb(es) >= best[0]:
            return
        # branch on an edge of minimum 'degree sum' (any edge works); choose first in a fixed order
        e = min(es, key=lambda f: sorted(f))
        for v in sorted(e):
            rec([f for f in es if v not in f], k + 1)
    rec(edges, 0)
    return best[0]


TAUMEMO = {}


def tau_mask(st, F):
    key = tuple(st.E[i] for i in range(len(st.E)) if (F >> i) & 1)
    if key in TAUMEMO:
        return TAUMEMO[key]
    t = tau_edges(key)
    TAUMEMO[key] = t
    return t


def max_value_containing(st, q, closed):
    P = [v for v in range(st.np) if v != q]
    nV = len(st.vm)
    best = None
    for k in range(len(P) + 1):
        for S in itertools.combinations(P, k):
            Z = (q,) + S
            if closed and len(Z) == nV:
                continue
            F = st.vm[q]
            for z in S:
                F |= st.vm[z]
            val = 3 * len(Z) + 2 * popcount(F) - 11 * tau_mask(st, F)
            if best is None or val > best[0]:
                best = (val, Z)
    return best


def max_value_all(st, closed):
    """brute force over ALL nonempty Z of processed vertices (used to re-check leaves)."""
    P = list(range(st.np))
    nV = len(st.vm)
    best = None
    for k in range(1, len(P) + 1):
        for Z in itertools.combinations(P, k):
            if closed and len(Z) == nV:
                continue
            F = 0
            for z in Z:
                F |= st.vm[z]
            val = 3 * len(Z) + 2 * popcount(F) - 11 * tau_mask(st, F)
            if best is None or val > best[0]:
                best = (val, Z)
    return best


def expand(st, R, stats, leaves):
    q = st.np
    if q >= len(st.vm) or st.dist[q] > R:
        leaves.append(st)
        return
    dq = st.dist[q]
    k = popcount(st.vm[q])
    # existing unprocessed vertices that may join an edge at q
    W = []
    for w in range(q + 1, len(st.vm)):
        if popcount(st.vm[w]) >= 3:
            continue
        if st.adjacent(q, w):
            continue
        if st.dist[w] == dq or (dq < R and st.dist[w] == dq + 1):
            W.append(w)
    # edge 'shapes': 0 = fresh+fresh, ('1',w) = w+fresh, ('2',u,w) = u+w
    shapes = [('0',)] + [('1', w) for w in W] + [('2', u, w) for u, w in itertools.combinations(W, 2) if not st.adjacent(u, w)]
    for D in range(max(k, 1), 4):
        need = D - k
        for pick in itertools.combinations_with_replacement(range(len(shapes)), need):
            used = []
            for p in pick:
                used.extend(shapes[p][1:])
            if len(set(used)) != len(used):
                continue
            ns = st.clone()
            for p in pick:
                sh = shapes[p]
                if sh[0] == '0':
                    a = ns.new_vertex(dq + 1); b = ns.new_vertex(dq + 1)
                elif sh[0] == '1':
                    a = sh[1]; b = ns.new_vertex(dq + 1)
                else:
                    a, b = sh[1], sh[2]
                ns.add_edge(q, a, b)
            ns.np = q + 1
            stats['nodes'] += 1
            closed = ns.np >= len(ns.vm)
            val, Z = max_value_containing(ns, q, closed)
            if val >= 0:
                stats['pruned'] += 1
                continue
            expand(ns, R, stats, leaves)


def incidence_graph(st):
    G = nx.Graph()
    for v in range(len(st.vm)):
        role = 'root' if v == 0 else ('proc' if v < st.np else 'bdry')
        G.add_node(('v', v), kind=role)
    for i, e in enumerate(st.E):
        G.add_node(('e', i), kind='edge')
        for v in e:
            G.add_edge(('e', i), ('v', v))
    return G


def main():
    rootdeg = int(sys.argv[1]); R = int(sys.argv[2])
    st = State()
    r = st.new_vertex(0)
    for _ in range(rootdeg):
        a = st.new_vertex(1); b = st.new_vertex(1)
        st.add_edge(r, a, b)
    st.np = 1
    stats = {'nodes': 0, 'pruned': 0}
    leaves = []
    expand(st, R, stats, leaves)
    print('rootdeg', rootdeg, 'R', R, 'nodes', stats['nodes'], 'pruned', stats['pruned'], 'leaves', len(leaves))
    # re-check every leaf by brute force over all Z
    classes = []
    nm = iso.categorical_node_match('kind', None)
    for L in leaves:
        closed = L.np >= len(L.vm)
        bv = max_value_all(L, closed)
        degs = [popcount(L.vm[v]) for v in range(L.np)]
        G = incidence_graph(L)
        found = None
        for ci, (G0, cnt, rep) in enumerate(classes):
            if nx.is_isomorphic(G, G0, node_match=nm):
                found = ci
                break
        if found is None:
            classes.append([G, 1, (L, bv, degs, closed)])
        else:
            classes[found][1] += 1
        print('LEAF closed=%s nproc=%d nV=%d best=%s degs=%s edges=%s' % (closed, L.np, len(L.vm), bv[0], degs, ' '.join('%d.%d.%d' % e for e in L.E)))
    print('isomorphism classes of leaves (rooted, processed/boundary coloured):', len(classes))
    for G0, cnt, (L, bv, degs, closed) in classes:
        print('  CLASS mult=%d closed=%s nproc=%d best=%s degs=%s edges=%s' % (cnt, closed, L.np, bv[0], degs, ' '.join('%d.%d.%d' % e for e in L.E)))


if __name__ == '__main__':
    main()
