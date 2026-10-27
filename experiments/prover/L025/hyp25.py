"""L025: own hypergraph utilities (written from scratch for this certificate; no import of e757, judge or other L0xx code).
Exact integer / bitmask arithmetic only.  Edges are tuples of vertex labels 0..n-1 (or arbitrary ints)."""
from itertools import combinations
import json, os

INPUTS = os.path.join(os.path.dirname(__file__), '..', '..', '20261027-0300-transversal-richness', 'inputs')
K29 = os.path.join(os.path.dirname(__file__), '..', 'L020', 'K29_classes.json')

def parse_line(line):
    t = list(map(int, line.split()))
    n, m, tau = t[0], t[1], t[2]
    E = [tuple(sorted(t[3 + 3 * i: 6 + 3 * i])) for i in range(m)]
    assert len(E) == m
    return n, m, tau, E

def load_cell(n, m, tau):
    fn = os.path.join(INPUTS, 'cell_%d_%d_%d.txt' % (n, m, tau))
    out = []
    with open(fn) as f:
        for line in f:
            if line.strip():
                out.append(parse_line(line))
    return out

def load_k29():
    d = json.load(open(K29))
    return [(c['n'], c['m'], c['tau'], [tuple(sorted(e)) for e in c['edges']]) for c in d]

def verts(E, n=None):
    V = set(v for e in E for v in e)
    if n is not None:
        V |= set(range(n))
    return sorted(V)

def degrees(E, V):
    d = {v: 0 for v in V}
    for e in E:
        for v in e:
            d[v] += 1
    return d

def sigma(E):
    """set of frozenset pairs lying in a common edge"""
    s = set()
    for e in E:
        for p in combinations(e, 2):
            s.add(frozenset(p))
    return s

def neighbours(E, V):
    nb = {v: set() for v in V}
    for e in E:
        for v in e:
            nb[v] |= set(e) - {v}
    return nb

def linear(E):
    S = [frozenset(e) for e in E]
    if len(set(S)) != len(S) or any(len(e) != 3 for e in S):
        return False
    seen = set()
    for e in S:
        for p in combinations(sorted(e), 2):
            if p in seen:
                return False
            seen.add(p)
    return True

def has_f7(E):
    """structural F7 test: centre c with three edges {c,p_i,q_i}, and two more edges {x1,x2,x3}, {y1,y2,y3} with {x_i,y_i}={p_i,q_i}"""
    S = set(frozenset(e) for e in E)
    at = {}
    for e in E:
        for v in e:
            at.setdefault(v, []).append(e)
    for c, es in at.items():
        if len(es) < 3:
            continue
        for e1, e2, e3 in combinations(es, 3):
            P = [tuple(v for v in e if v != c) for e in (e1, e2, e3)]
            p1, q1 = P[0]
            for (x2, y2) in (P[1], P[1][::-1]):
                for (x3, y3) in (P[2], P[2][::-1]):
                    if frozenset((p1, x2, x3)) in S and frozenset((q1, y2, y3)) in S:
                        return True
    return False

def _sdr_avoid(E, banned):
    """True iff the edges of E have a system of distinct representatives avoiding the set banned (Hall / augmenting paths)."""
    owner = {}  # vertex -> edge index
    for i in range(len(E)):
        # DFS augmenting path
        visited = set()
        def aug(f):
            for v in E[f]:
                if v in banned or v in visited:
                    continue
                visited.add(v)
                if v not in owner or aug(owner[v]):
                    owner[v] = f
                    return True
            return False
        if not aug(i):
            return False
    return True

def p3(E, V):
    """e(S) <= |S|-2 for every S subset of V with |S| >= 2  <=>  for every pair {x,y} of V the edges have an SDR avoiding x,y."""
    E = [tuple(e) for e in E]
    V = sorted(set(V) | set(v for e in E for v in e))
    if len(V) < 2:
        return True
    for x, y in combinations(V, 2):
        if not _sdr_avoid(E, {x, y}):
            return False
    return True

def in_C(E, V):
    return linear(E) and (not has_f7(E)) and p3(E, V)

# ---------- transversals with bitmasks ----------
def masks(E, idx):
    return [sum(1 << idx[v] for v in e) for e in E]

def _lb(rem):
    # greedy packing of pairwise disjoint edges: a lower bound for tau of rem
    used = 0; c = 0
    for e in rem:
        if e & used == 0:
            used |= e; c += 1
    return c

def tau_mask(EM):
    best = [len(EM)]
    def rec(rem, k):
        if not rem:
            if k < best[0]:
                best[0] = k
            return
        if k + _lb(rem) >= best[0]:
            return
        e = rem[0]
        b = e
        while b:
            low = b & -b
            b ^= low
            rec([f for f in rem if not (f & low)], k + 1)
    rec(sorted(EM), 0)
    return best[0]

def all_min_transversals_mask(EM, t):
    """all vertex sets (bitmasks) of size exactly t meeting every edge, given tau = t (they are then all minimal)."""
    out = set()
    def rec(rem, chosen, k):
        if not rem:
            if k == t:
                out.add(chosen)
            return
        if k + _lb(rem) > t:
            return
        e = rem[0]
        b = e & ~chosen
        while b:
            low = b & -b
            b ^= low
            rec([f for f in rem if not (f & low)], chosen | low, k + 1)
    rec(list(EM), 0, 0)
    return out

class Hyp:
    def __init__(self, E, V=None):
        self.E = [tuple(sorted(e)) for e in E]
        VV = set(v for e in self.E for v in e)
        if V is not None:
            VV |= set(V)
        self.V = sorted(VV)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.EM = masks(self.E, self.idx)
        self.deg = degrees(self.E, self.V)
        self.sig = sigma(self.E)
        self._tau = None; self._mt = None
    @property
    def n(self): return len(self.V)
    @property
    def m(self): return len(self.E)
    def tau(self):
        if self._tau is None:
            self._tau = tau_mask(self.EM) if self.EM else 0
        return self._tau
    def slack(self):
        return 3 * self.n + 2 * self.m - 11 * self.tau()
    def min_transversals(self):
        if self._mt is None:
            t = self.tau()
            self._mt = all_min_transversals_mask(self.EM, t) if self.EM else {0}
        return self._mt
    def bit(self, v):
        return 1 << self.idx[v]
    def cotransversal(self, X):
        b = 0
        for v in X:
            b |= self.bit(v)
        return any((T & b) == b for T in self.min_transversals())
    def co_pairs(self):
        """set of frozenset pairs contained in some minimum transversal"""
        cp = set()
        for T in self.min_transversals():
            vs = [v for v in self.V if T >> self.idx[v] & 1]
            for p in combinations(vs, 2):
                cp.add(frozenset(p))
        return cp
    def in_C(self):
        return in_C(self.E, self.V)
    def connected(self):
        if not self.V:
            return True
        adj = neighbours(self.E, self.V)
        seen = {self.V[0]}; st = [self.V[0]]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); st.append(w)
        return len(seen) == len(self.V)
    def maxdeg(self):
        return max(self.deg.values()) if self.deg else 0

def delete(E, V, Z):
    Z = set(Z)
    return [e for e in E if not (set(e) & Z)], [v for v in V if v not in Z]

def oplus(E, V, a, b, c):
    """G (+) (a,b,c): new vertices v,x,y,z and edges {x,y,z},{v,x,a},{v,y,b},{v,z,c}"""
    N = max(V) + 1
    v, x, y, z = N, N + 1, N + 2, N + 3
    E2 = list(E) + [(x, y, z), (v, x, a), (v, y, b), (v, z, c)]
    return [tuple(sorted(e)) for e in E2], list(V) + [v, x, y, z]

def identify(E, V, a, b):
    """identify a and b into a (b disappears)"""
    E2 = [tuple(sorted(a if u == b else u for u in e)) for e in E]
    return E2, [u for u in V if u != b]
