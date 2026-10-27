"""Referee's own 3-graph library for the L024 review (independent of hyp24.py, kt.py, e757, judge).

Hypergraphs: (n, edges) with vertices 0..n-1 and edges as sorted 3-tuples.
Everything exact (ints, bitmasks).
"""
from itertools import combinations, permutations
import json


def degs(n, E):
    d = [0] * n
    for e in E:
        for x in e:
            d[x] += 1
    return d


def is_linear(E):
    seen = set()
    for e in E:
        for p in combinations(sorted(e), 2):
            if p in seen:
                return False
            seen.add(p)
    return len(set(tuple(sorted(e)) for e in E)) == len(E)


def has_F7(n, E):
    """F7 = {012,034,056,135,246}: centre 0 of degree 3, all others degree 2.
    Complete test: for every vertex c and every 3 edges at c with other vertices {a_i,b_i},
    look for x_i in {a_i,b_i} with {x1,x2,x3} and the complementary triple both edges."""
    Es = set(tuple(sorted(e)) for e in E)
    at = [[] for _ in range(n)]
    for e in E:
        for x in e:
            at[x].append(e)
    for c in range(n):
        if len(at[c]) < 3:
            continue
        for e1, e2, e3 in combinations(at[c], 3):
            o = [tuple(x for x in e if x != c) for e in (e1, e2, e3)]
            # need the three 'other pairs' pairwise disjoint (true in a linear graph)
            if len(set(o[0]) | set(o[1]) | set(o[2])) < 6:
                continue
            for s1 in range(2):
                for s2 in range(2):
                    for s3 in range(2):
                        x = tuple(sorted((o[0][s1], o[1][s2], o[2][s3])))
                        y = tuple(sorted((o[0][1 - s1], o[1][1 - s2], o[2][1 - s3])))
                        if x in Es and y in Es:
                            return True
    return False


def _bip_match(left_adj, nright):
    """left_adj: list of lists of right indices. Return size of max matching (Kuhn)."""
    match_r = [-1] * nright

    def try_k(u, seen):
        for w in left_adj[u]:
            if not seen[w]:
                seen[w] = True
                if match_r[w] == -1 or try_k(match_r[w], seen):
                    match_r[w] = u
                    return True
        return False

    cnt = 0
    for u in range(len(left_adj)):
        if try_k(u, [False] * nright):
            cnt += 1
    return cnt


def p3_ok(n, E):
    """(P3): e(S) <= |S|-2 for all S with |S|>=2  <=>  every nonempty edge set F spans >= |F|+2 vertices
    <=> for every edge e0, the incidence bipartite graph with e0 replicated 3 times has a matching
    saturating all edge copies (Hall).  Own derivation (edge tripling)."""
    E = [tuple(e) for e in E]
    if not E:
        return True
    for i0 in range(len(E)):
        left = []
        for i, e in enumerate(E):
            if i == i0:
                left.extend([list(e)] * 3)
            else:
                left.append(list(e))
        if _bip_match(left, n) < len(left):
            return False
    return True


def p3_brute(n, E):
    Es = [frozenset(e) for e in E]
    for k in range(1, len(Es) + 1):
        for F in combinations(Es, k):
            if len(frozenset().union(*F)) < k + 2:
                return False
    return True


def in_C3(n, E):
    d = degs(n, E)
    if d and max(d) > 3:
        return False
    return is_linear(E) and (not has_F7(n, E)) and p3_ok(n, E)


def min_transversals(n, E):
    """All minimum transversals as bitmasks; brute force by increasing size (small n only)."""
    emasks = [sum(1 << x for x in e) for e in E]
    if not emasks:
        return 0, [0]
    for t in range(0, n + 1):
        res = []
        for S in combinations(range(n), t):
            m = 0
            for x in S:
                m |= 1 << x
            if all(m & em for em in emasks):
                res.append(m)
        if res:
            return t, res
    raise RuntimeError


def tau_bb(n, E):
    """Exact transversal number by branch and bound (pick an uncovered edge, branch on its 3 vertices)."""
    emasks = [sum(1 << x for x in e) for e in E]
    best = [n + 1]

    def rec(cov, k):
        if k >= best[0]:
            return
        for em in emasks:
            if not (cov & em):
                break
        else:
            best[0] = k
            return
        # lower bound: greedy packing of pairwise disjoint uncovered edges
        lb = 0
        packed = 0
        for em2 in emasks:
            if not (cov & em2) and not (packed & em2):
                packed |= em2
                lb += 1
        if k + lb >= best[0]:
            return
        for x in range(n):
            if em >> x & 1:
                rec(cov | (1 << x), k + 1)

    rec(0, 0)
    return best[0]


def automorphisms(n, E):
    """All automorphisms (vertex permutations mapping E onto E) by backtracking with degree refinement."""
    Es = set(tuple(sorted(e)) for e in E)
    d = degs(n, E)
    at = [[] for _ in range(n)]
    for e in E:
        for x in e:
            at[x].append(tuple(sorted(e)))
    # invariant: degree and sorted neighbour-degree multiset
    inv = []
    for x in range(n):
        nb = sorted(d[y] for e in at[x] for y in e if y != x)
        inv.append((d[x], tuple(nb)))
    order = sorted(range(n), key=lambda x: -d[x])
    res = []
    img = [-1] * n
    used = [False] * n

    def consistent(x):
        # all edges among assigned vertices must map to edges
        for e in at[x]:
            if all(img[y] >= 0 for y in e):
                if tuple(sorted(img[y] for y in e)) not in Es:
                    return False
        return True

    def rec(i):
        if i == n:
            res.append(tuple(img))
            return
        x = order[i]
        for y in range(n):
            if not used[y] and inv[y] == inv[x]:
                img[x] = y
                used[y] = True
                if consistent(x):
                    rec(i + 1)
                used[y] = False
                img[x] = -1

    rec(0)
    return res


def isomorphic(n1, E1, n2, E2):
    if n1 != n2 or len(E1) != len(E2):
        return False
    if sorted(degs(n1, E1)) != sorted(degs(n2, E2)):
        return False
    Es2 = set(tuple(sorted(e)) for e in E2)
    d1, d2 = degs(n1, E1), degs(n2, E2)
    at1 = [[] for _ in range(n1)]
    for e in E1:
        for x in e:
            at1[x].append(tuple(sorted(e)))
    at2 = [[] for _ in range(n2)]
    for e in E2:
        for x in e:
            at2[x].append(tuple(sorted(e)))
    inv1 = [(d1[x], tuple(sorted(d1[y] for e in at1[x] for y in e if y != x))) for x in range(n1)]
    inv2 = [(d2[x], tuple(sorted(d2[y] for e in at2[x] for y in e if y != x))) for x in range(n2)]
    if sorted(inv1) != sorted(inv2):
        return False
    # order vertices of graph 1 by BFS from a max-degree vertex to keep consistency checks early
    start = max(range(n1), key=lambda x: d1[x])
    order, seen = [], set()
    for s in [start] + list(range(n1)):
        if s in seen:
            continue
        q = [s]
        seen.add(s)
        while q:
            x = q.pop(0)
            order.append(x)
            for e in at1[x]:
                for y in e:
                    if y not in seen:
                        seen.add(y)
                        q.append(y)
    img = [-1] * n1
    used = [False] * n2

    def consistent(x):
        for e in at1[x]:
            if all(img[y] >= 0 for y in e):
                if tuple(sorted(img[y] for y in e)) not in Es2:
                    return False
        return True

    def rec(i):
        if i == n1:
            return True
        x = order[i]
        for y in range(n2):
            if not used[y] and inv2[y] == inv1[x]:
                img[x] = y
                used[y] = True
                if consistent(x) and rec(i + 1):
                    return True
                used[y] = False
                img[x] = -1
        return False

    return rec(0)


def connected(n, E):
    if n == 0:
        return True
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for e in E:
        a = f(e[0])
        for y in e[1:]:
            b = f(y)
            if a != b:
                par[b] = a
    return len(set(f(x) for x in range(n))) == 1


def load_pieces(path='/home/user/Erdos-757/experiments/prover/L021/closure_results.json'):
    d = json.load(open(path))
    out = []
    for p in d['pieces']:
        out.append((p['name'], p['n'], [tuple(sorted(e)) for e in p['edges']], p))
    return out


def load_cell(path):
    out = []
    for line in open(path):
        a = list(map(int, line.split()))
        if not a:
            continue
        n, m, t = a[0], a[1], a[2]
        rest = a[3:]
        E = [tuple(sorted(rest[3 * i:3 * i + 3])) for i in range(m)]
        out.append((n, m, t, E))
    return out
