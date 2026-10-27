"""Own minimal 3-graph toolkit for the L027 tests (exact integer / bitmask arithmetic only).

Independent of e757/, judge/ and of the L0xx code.  A 3-graph is (n, edges): vertices 0..n-1,
edges a list of sorted 3-tuples.  Everything here is brute force and meant for small graphs.
"""
from itertools import combinations


def emask(e):
    return (1 << e[0]) | (1 << e[1]) | (1 << e[2])


def tau_and_mts(n, edges, extra_bound=0):
    """Return (tau, list of all transversals T (bitmasks) with |T| <= tau + extra_bound that are
    inclusion-minimal-free, i.e. ALL vertex sets of size <= tau+extra_bound meeting every edge).
    Brute force over subsets by size; fine for n <= 16."""
    ems = [emask(e) for e in edges]
    if not ems:
        return 0, [0]
    t = None
    out = []
    for k in range(0, n + 1):
        found_k = []
        for comb in combinations(range(n), k):
            T = 0
            for u in comb:
                T |= 1 << u
            if all(em & T for em in ems):
                found_k.append(T)
        if found_k and t is None:
            t = k
        if t is not None:
            out.extend(found_k)
            if k >= t + extra_bound:
                break
    return t, out


def tau(n, edges):
    ems = [emask(e) for e in edges]
    best = [len(ems)]

    def rec(chosen, k):
        if k >= best[0]:
            return
        for em in ems:
            if not (em & chosen):
                x = em
                while x:
                    low = x & -x
                    rec(chosen | low, k + 1)
                    x ^= low
                return
        best[0] = k
    rec(0, 0)
    return best[0]


def min_transversals(n, edges):
    t, Ts = tau_and_mts(n, edges, 0)
    return t, [T for T in Ts if bin(T).count('1') == t]


def popc(x):
    return bin(x).count('1')


def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for u in e:
            d[u] += 1
    return d


def is_linear(edges):
    seen = set()
    for e in edges:
        for p in combinations(e, 2):
            if p in seen:
                return False
            seen.add(p)
    return len(set(edges)) == len(edges)


def has_F7(n, edges, through=None):
    """Copy of F7 = {012,034,056,135,246} as a sub-hypergraph (any 3-graph).
    If `through` is a vertex, only copies containing it are reported."""
    es = set(edges)
    inc = [[] for _ in range(n)]
    for e in edges:
        for u in e:
            inc[u].append(e)
    for o in range(n):
        for f1, f2, f3 in combinations(inc[o], 3):
            P = [tuple(u for u in f if u != o) for f in (f1, f2, f3)]
            if len({u for p in P for u in p}) != 6:
                continue
            for i in (0, 1):
                for j in (0, 1):
                    for k in (0, 1):
                        g = tuple(sorted((P[0][i], P[1][j], P[2][k])))
                        h = tuple(sorted((P[0][1 - i], P[1][1 - j], P[2][1 - k])))
                        if g in es and h in es:
                            V = {o} | set(P[0]) | set(P[1]) | set(P[2])
                            if through is None or through in V:
                                return True
    return False


def p3_violations(n, edges):
    """Return the list of vertex sets S (bitmasks) with |S| >= 2 and e(S) >= |S|-1 among the
    unions of nonempty edge subsets (enough: a (P3) violation can be shrunk to such a union)."""
    ems = [emask(e) for e in edges]
    m = len(ems)
    bad = []
    for F in range(1, 1 << m):
        V = 0
        k = 0
        x = F
        i = 0
        while x:
            if x & 1:
                V |= ems[i]
                k += 1
            x >>= 1
            i += 1
        if popc(V) <= k + 1:
            bad.append(V)
    return bad


def in_C(n, edges):
    return is_linear(edges) and not has_F7(n, edges) and not p3_violations(n, edges)


def e_inside(edges, S):
    return sum(1 for e in edges if (emask(e) & S) == emask(e))


def tight_sets_containing(n, edges, X, minsize=3):
    """All tight sets S (e(S) = |S|-2, |S| >= minsize) with X subset S (bitmasks); brute force."""
    out = []
    rest = [u for u in range(n) if not (X >> u & 1)]
    for k in range(0, len(rest) + 1):
        for comb in combinations(rest, k):
            S = X
            for u in comb:
                S |= 1 << u
            if popc(S) >= minsize and e_inside(edges, S) == popc(S) - 2:
                out.append(S)
    return out


def components(n, edges):
    par = list(range(n))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for e in edges:
        a, b, c = f(e[0]), f(e[1]), f(e[2])
        par[b] = a
        par[c] = a
        par[f(c)] = a
    comp = {}
    for u in range(n):
        comp.setdefault(f(u), []).append(u)
    return list(comp.values())


def slack(n, m, t):
    return 3 * n + 2 * m - 11 * t


def adjacent(edges, u, w):
    return any(u in e and w in e for e in edges)


def induced_minus(n, edges, Z):
    """G - Z, relabelled to 0..n-|Z|-1; returns (n', edges', relabel map old->new)."""
    keep = [u for u in range(n) if u not in Z]
    mp = {u: i for i, u in enumerate(keep)}
    es = [tuple(sorted(mp[u] for u in e)) for e in edges if not (set(e) & set(Z))]
    return len(keep), es, mp
