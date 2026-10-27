"""Own 3-graph routines for the L020 round-2 review (referee #3, opus).
Imports nothing from e757/, judge/ or experiments/prover/*. Exact integer arithmetic only.
"""
import itertools, sys

def parse_list(path):
    out = []
    with open(path) as f:
        for line in f:
            a = line.split()
            if not a:
                continue
            n, m, t = int(a[0]), int(a[1]), int(a[2])
            vs = list(map(int, a[3:]))
            assert len(vs) == 3 * m, path
            E = [tuple(sorted(vs[3 * i:3 * i + 3])) for i in range(m)]
            out.append((n, m, t, E))
    return out

class HG:
    """3-graph on vertex set V (list of ints) with edge list E; tau memoised on edge-index masks."""
    def __init__(self, V, E):
        self.V = sorted(set(V))
        self.E = [tuple(sorted(e)) for e in E]
        assert len(set(self.E)) == len(self.E)
        for e in self.E:
            assert len(set(e)) == 3 and all(u in set(self.V) for u in e)
        self.inc = {u: 0 for u in self.V}
        for i, e in enumerate(self.E):
            for u in e:
                self.inc[u] |= 1 << i
        self.full = (1 << len(self.E)) - 1
        self.memo = {0: 0}

    def deg(self, u, emask=None):
        if emask is None:
            emask = self.full
        return bin(self.inc[u] & emask).count("1")

    def tau_mask(self, emask):
        """exact transversal number of the sub-3-graph formed by the edges in emask"""
        memo = self.memo
        if emask in memo:
            return memo[emask]
        # branch on the edge whose vertices have smallest total degree (ties: lowest index)
        best_i, best_d = -1, 10 ** 9
        m = emask
        while m:
            low = m & -m
            i = low.bit_length() - 1
            m ^= low
            d = sum(bin(self.inc[u] & emask).count("1") for u in self.E[i])
            if d < best_d:
                best_d, best_i = d, i
        res = 10 ** 9
        for u in self.E[best_i]:
            r = 1 + self.tau_mask(emask & ~self.inc[u])
            if r < res:
                res = r
        memo[emask] = res
        return res

    def mask_without(self, X, emask=None):
        if emask is None:
            emask = self.full
        for x in X:
            emask &= ~self.inc[x]
        return emask

    def tau(self, X=(), emask=None):
        return self.tau_mask(self.mask_without(X, emask))

    def components(self, Vset, emask):
        """components (vertex sets, edge masks) of the 3-graph (Vset, edges of emask); isolated vertices separately"""
        parent = {u: u for u in Vset}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        m = emask
        while m:
            low = m & -m
            i = low.bit_length() - 1
            m ^= low
            a, b, c = self.E[i]
            ra, rb, rc = find(a), find(b), find(c)
            parent[rb] = ra
            parent[find(rc)] = find(ra)
        groups = {}
        for u in Vset:
            groups.setdefault(find(u), set()).add(u)
        comps, iso = [], []
        for g in groups.values():
            em = 0
            for u in g:
                em |= self.inc[u] & emask
            if em == 0:
                assert len(g) == 1
                iso.extend(g)
            else:
                comps.append((frozenset(g), em))
        return comps, iso

def popc(x):
    return bin(x).count("1")

def is_linear(E):
    for e, f in itertools.combinations(E, 2):
        if len(set(e) & set(f)) > 1:
            return False
    return True

def has_F7(E):
    """F7 = {012,034,056,135,246}: hub of degree 3 whose three edges split the other 6 vertices
    into 3 pairs, plus two complementary transversal edges of the pairs."""
    Es = set(tuple(sorted(e)) for e in E)
    at = {}
    for e in Es:
        for u in e:
            at.setdefault(u, []).append(e)
    for x, L in at.items():
        if len(L) < 3:
            continue
        for e1, e2, e3 in itertools.combinations(L, 3):
            P = [tuple(u for u in e if u != x) for e in (e1, e2, e3)]
            if len(set(P[0]) | set(P[1]) | set(P[2])) != 6:
                continue
            for ch in itertools.product((0, 1), repeat=3):
                t1 = tuple(sorted(P[j][ch[j]] for j in range(3)))
                t2 = tuple(sorted(P[j][1 - ch[j]] for j in range(3)))
                if t1 in Es and t2 in Es:
                    return True
    return False

def p3_hall(V, E):
    """(P3) e(S) <= |S|-2 for all |S|>=2, tested as: for every pair {x,y}, the edges have an SDR in V-{x,y}
    (equivalence proved in L020 Step 1.1 and re-proved by hand in this review). Own Kuhn matching."""
    V = list(V)
    if len(E) > len(V) - 2:
        return False
    for x, y in itertools.combinations(V, 2):
        match = {}  # vertex -> edge index
        def try_edge(i, seen):
            for u in E[i]:
                if u == x or u == y or u in seen:
                    continue
                seen.add(u)
                if u not in match or try_edge(match[u], seen):
                    match[u] = i
                    return True
            return False
        for i in range(len(E)):
            if not try_edge(i, set()):
                return False
    return True

def in_C(V, E):
    return is_linear(E) and (not has_F7(E)) and p3_hall(V, E)
