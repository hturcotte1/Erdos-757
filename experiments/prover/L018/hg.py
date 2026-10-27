"""hg.py -- exact helpers for 3-graphs (certificate L018).
Vertices are ints, edges are tuples of 3 ints. All arithmetic is integer."""
from functools import lru_cache
from itertools import combinations

def tau_of(edges):
    """minimum transversal size of a list of edges (any vertices), exact branch and bound."""
    edges = [frozenset(e) for e in edges]
    best = [len(edges)]
    def rec(rem, k):
        if k >= best[0]:
            return
        if not rem:
            best[0] = k
            return
        # lower bound: greedy disjoint edges
        used = set(); lb = 0
        for e in rem:
            if not (e & used):
                lb += 1; used |= e
        if k + lb >= best[0]:
            return
        e = rem[0]
        for v in e:
            rec([f for f in rem if v not in f], k + 1)
    rec(edges, 0)
    return best[0]

def tau_mask(masks, inc_of_vertex, F):
    """tau of edge-subset F (bitmask over edge indices) with memo dict passed in masks['memo']"""
    raise NotImplementedError

class TauCache:
    """tau over subsets of a fixed edge list, edges given as tuples; subsets as int bitmasks."""
    def __init__(self, edges):
        self.edges = [tuple(e) for e in edges]
        self.inc = {}
        for i, e in enumerate(self.edges):
            for v in e:
                self.inc[v] = self.inc.get(v, 0) | (1 << i)
        self.memo = {0: 0}
    def tau(self, F):
        memo = self.memo
        if F in memo:
            return memo[F]
        low = (F & -F).bit_length() - 1
        best = 99
        for v in self.edges[low]:
            t = 1 + self.tau(F & ~self.inc[v])
            if t < best:
                best = t
        memo[F] = best
        return best

def in_class_C(edges, check_f7=True):
    """linear, F7-free, e(S) <= |S|-2 for all |S|>=2 (Hall form over all vertex pairs)."""
    E = [tuple(e) for e in edges]
    # linear
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            if len(set(E[i]) & set(E[j])) > 1:
                return False
    if check_f7 and has_f7(E):
        return False
    V = sorted(set(v for e in E for v in e))
    for x, y in combinations(V, 2):
        own = {}
        def augm(i, seen):
            for v in E[i]:
                if v == x or v == y or v in seen:
                    continue
                seen.add(v)
                if v not in own or augm(own[v], seen):
                    own[v] = i
                    return True
            return False
        for i in range(len(E)):
            if not augm(i, set()):
                return False
    return True

def has_f7(E):
    """F7 = {012,034,056,135,246}: 5 edges on 7 vertices, one vertex of degree 3, six of degree 2 (as a subhypergraph)."""
    E = [frozenset(e) for e in E]
    m = len(E)
    # a 5-edge subset on exactly 7 vertices with degree pattern 3,2^6 in a linear hypergraph is F7
    for c in combinations(range(m), 5):
        U = set()
        for i in c:
            U |= E[i]
        if len(U) != 7:
            continue
        deg = {}
        for i in c:
            for v in E[i]:
                deg[v] = deg.get(v, 0) + 1
        ds = sorted(deg.values())
        if ds == [2, 2, 2, 2, 2, 2, 3]:
            return True
    return False

def degrees(E):
    d = {}
    for e in E:
        for v in e:
            d[v] = d.get(v, 0) + 1
    return d

def tau_full(E):
    return tau_of(E)

def slack(E, n=None):
    V = set(v for e in E for v in e)
    if n is None:
        n = len(V)
    return 3 * n + 2 * len(E) - 11 * tau_of(E)
