"""Referee #3 (round 2) helper library for L021. Independent of e757/, judge/ and
experiments/prover/L021/kt.py. Exact integer arithmetic only.

Hypergraphs: (n, edges) with edges a list of 3-tuples of ints in range(n).
"""
from itertools import combinations
import networkx as nx


def masks(edges):
    return [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]


def tau(n, edges):
    """Exact transversal number by branching on an uncovered edge (with bound)."""
    em = masks(edges)
    best = [n + 1]

    def rec(chosen, size):
        if size >= best[0]:
            return
        for e in em:
            if not (e & chosen):
                break
        else:
            best[0] = size
            return
        for v in range(n):
            if (e >> v) & 1:
                rec(chosen | (1 << v), size + 1)

    rec(0, 0)
    return best[0] if edges else 0


def min_transversals(n, edges, t=None):
    """All minimum transversals (as bitmasks) by brute force over t-subsets."""
    em = masks(edges)
    if t is None:
        t = tau(n, edges)
    out = []
    for S in combinations(range(n), t):
        m = 0
        for v in S:
            m |= 1 << v
        if all(e & m for e in em):
            out.append(m)
    return out


def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for v in e:
            d[v] += 1
    return d


def is_linear(edges):
    for e, f in combinations(edges, 2):
        if len(set(e) & set(f)) >= 2:
            return False
    return True


def is_connected(n, edges):
    if n == 0:
        return True
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for (a, b, c) in edges:
        G.add_edge(a, b)
        G.add_edge(b, c)
    return nx.is_connected(G)


def p3_ok(edges, must_contain=None):
    """(P3) e(S) <= |S|-2 for all |S|>=2  <=>  |V(F')| >= |F'|+2 for every nonempty
    edge set F'. Exhaustive over edge subsets. If must_contain (set of edge indices) is
    given, only subsets containing at least one of them are tested (the rest is assumed)."""
    m = len(edges)
    em = masks(edges)
    for r in range(1, m + 1):
        for F in combinations(range(m), r):
            if must_contain is not None and not (set(F) & must_contain):
                continue
            u = 0
            for i in F:
                u |= em[i]
            if bin(u).count("1") < r + 2:
                return False
    return True


def p3_ok_hall(n, edges):
    """(P3) via the surplus-2 Hall reduction: for every edge e, the incidence bipartite
    graph with e tripled has a matching saturating all edge nodes."""
    m = len(edges)
    for i in range(m):
        B = nx.Graph()
        left = []
        for j, e in enumerate(edges):
            copies = 3 if j == i else 1
            for c in range(copies):
                node = ("E", j, c)
                left.append(node)
                for v in e:
                    B.add_edge(node, ("V", v))
        M = nx.bipartite.hopcroft_karp_matching(B, top_nodes=left)
        if sum(1 for x in left if x in M) < len(left):
            return False
    return True


F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]


def inc_graph(edges):
    G = nx.Graph()
    for j, e in enumerate(edges):
        G.add_node(("E", j), t=1)
        for v in e:
            G.add_node(("V", v), t=0)
            G.add_edge(("E", j), ("V", v))
    return G


def iso(edges1, edges2):
    return nx.is_isomorphic(inc_graph(edges1), inc_graph(edges2),
                            node_match=lambda a, b: a["t"] == b["t"])


def has_F7(edges):
    """Any 5 edges spanning exactly 7 vertices and isomorphic to F7."""
    for F in combinations(edges, 5):
        vs = set()
        for e in F:
            vs |= set(e)
        if len(vs) == 7 and iso(list(F), F7):
            return True
    return False


def in_C(n, edges):
    return is_linear(edges) and (not has_F7(edges)) and p3_ok_hall(n, edges)


def induced_copies(n, edges, piece_edges, piece_n):
    """All vertex sets U with H[U] isomorphic to the piece (connected piece with
    m_P >= 1 edges): enumerate m_P-subsets of host edges whose union has piece_n
    vertices and no further host edge inside, then test isomorphism."""
    mP = len(piece_edges)
    em = masks(edges)
    out = set()
    for F in combinations(range(len(edges)), mP):
        u = 0
        for i in F:
            u |= em[i]
        if bin(u).count("1") != piece_n:
            continue
        inside = [i for i in range(len(edges)) if em[i] & u == em[i]]
        if len(inside) != mP:
            continue
        if iso([edges[i] for i in F], piece_edges):
            out.add(u)
    return sorted(out)


def deficiency(edges, copies):
    """copies: list of (vertex_mask, W). Exhaustive maximisation of
    sum W - 35 |E*(X)| over families of pairwise vertex-disjoint copies (X empty -> 0).
    E*(X): host edges meeting V(X) and lying inside no member."""
    em = masks(edges)
    best = [0, ()]
    k = len(copies)

    def value(sel):
        U = 0
        W = 0
        for i in sel:
            U |= copies[i][0]
            W += copies[i][1]
        estar = 0
        for e in em:
            if e & U and not any((e & copies[i][0]) == e for i in sel):
                estar += 1
        return W - 35 * estar

    def rec(start, sel, used):
        if sel:
            v = value(sel)
            if v > best[0]:
                best[0] = v
                best[1] = tuple(sel)
        for i in range(start, k):
            if copies[i][0] & used:
                continue
            sel.append(i)
            rec(i + 1, sel, used | copies[i][0])
            sel.pop()

    rec(0, [], 0)
    return best[0], best[1]


def A_of(n, m, t):
    return 27 * n + 35 * m - 132 * t


def s_of(n, m, t):
    return 3 * n + 2 * m - 11 * t
