"""Referee's own exact toolkit for 3-uniform hypergraphs (written for the L020 round-1 review).
No import of e757/, judge/ or of any prover script.  Exact integer arithmetic (bitmasks) throughout.

Functions
  parse_line(line)                -> (n, m, tau_claimed, edges)      stored-list format "n m tau a b c a b c ..."
  degrees(n, E), is_linear(E), connected(n, E)
  contains_F7_direct(n, E)        -> bool   (search for an embedding of F7 anchored at a degree-3 vertex)
  contains_F7_bruteforce(n, E)    -> bool   (all 5-edge subsets, all vertex bijections fixing the degree-3 vertex)
  p3_complete(n, E)               -> bool   (ALL nonempty edge subsets: |union| >= |E'| + 2; m <= 24 recommended)
  p3_hall(n, E)                   -> bool   (for every pair {x,y}: matching edges -> V\\{x,y} saturating the edges)
  tau(n, E), exists_transversal(masks, k), min_transversal(masks)
  all_min_transversals(masks, n)  -> (list of vertex bitmasks, tau)
  sub(n, E, Z)                    -> induced hypergraph on V \\ Z (relabelled), as (n', E')
  components(n, E)                -> list of (vertex set) components (isolated vertices as singletons)
  canon(n, E)                     -> canonical certificate (own individualisation/refinement; no library)
"""
import itertools, sys

F7_EDGES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]


def parse_line(line):
    t = [int(x) for x in line.split()]
    n, m, tau = t[0], t[1], t[2]
    rest = t[3:]
    assert len(rest) == 3 * m, (n, m, tau, len(rest))
    E = [tuple(sorted(rest[3 * i:3 * i + 3])) for i in range(m)]
    return n, m, tau, E


def degrees(n, E):
    d = [0] * n
    for e in E:
        for x in e:
            d[x] += 1
    return d


def is_3uniform_distinct(n, E):
    S = set()
    for e in E:
        if len(e) != 3 or len(set(e)) != 3:
            return False
        if any(x < 0 or x >= n for x in e):
            return False
        fe = frozenset(e)
        if fe in S:
            return False
        S.add(fe)
    return True


def is_linear(E):
    S = [set(e) for e in E]
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            if len(S[i] & S[j]) > 1:
                return False
    return True


def connected(n, E):
    if n == 0:
        return True
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in E:
        for x in e[1:]:
            a, b = find(e[0]), find(x)
            if a != b:
                parent[a] = b
    return len({find(x) for x in range(n)}) == 1


def components(n, E):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in E:
        for x in e[1:]:
            a, b = find(e[0]), find(x)
            if a != b:
                parent[a] = b
    comp = {}
    for x in range(n):
        comp.setdefault(find(x), []).append(x)
    return sorted(comp.values())


def contains_F7_direct(n, E):
    """F7 = {012,034,056,135,246}: vertex 0 has degree 3; its three edges partition the other 6 vertices into
    pairs; the two remaining edges are transversals of these pairs.  Search for such a configuration."""
    Eset = set(frozenset(e) for e in E)
    at = [[] for _ in range(n)]
    for e in E:
        for x in e:
            at[x].append(e)
    for x in range(n):
        if len(at[x]) < 3:
            continue
        for A, B, C in itertools.combinations(at[x], 3):
            pa = [y for y in A if y != x]
            pb = [y for y in B if y != x]
            pc = [y for y in C if y != x]
            if len(pa) != 2 or len(pb) != 2 or len(pc) != 2:
                continue  # non-linear at x: not an F7 anchored here in the required way
            if len(set(pa) | set(pb) | set(pc)) != 6:
                continue
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        e1 = frozenset((pa[i], pb[j], pc[k]))
                        e2 = frozenset((pa[1 - i], pb[1 - j], pc[1 - k]))
                        if e1 in Eset and e2 in Eset:
                            return True
    return False


def contains_F7_bruteforce(n, E):
    """All 5-edge subsets whose union has 7 vertices; test isomorphism to F7 by all bijections that send the unique
    degree-3 vertex of F7 to a degree-3 vertex of the subset (6! maps each)."""
    F7set = set(frozenset(e) for e in F7_EDGES)
    for sub in itertools.combinations(E, 5):
        V = sorted(set(x for e in sub for x in e))
        if len(V) != 7:
            continue
        deg = {x: 0 for x in V}
        for e in sub:
            for x in e:
                deg[x] += 1
        if sorted(deg.values()) != [2, 2, 2, 2, 2, 2, 3]:
            continue
        subset = set(frozenset(e) for e in sub)
        hub = [x for x in V if deg[x] == 3][0]
        others = [x for x in V if x != hub]
        for perm in itertools.permutations(others):
            mp = {0: hub}
            for i, y in enumerate(perm):
                mp[i + 1] = y
            if all(frozenset(mp[x] for x in e) in subset for e in F7_EDGES):
                return True
    return False


def edge_masks(E):
    return [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in E]


def p3_complete(n, E):
    """(P3) e(S) <= |S| - 2 for all S with |S| >= 2  <=>  for every nonempty edge set E': |union E'| >= |E'| + 2.
    Proof of <=>: (=>) S := union E' has e(S) >= |E'| so |union E'| = |S| >= e(S)+2 >= |E'|+2.
    (<=) for S with e(S) = k >= 1 let E' be the edges inside S: |S| >= |union E'| >= k + 2; for e(S) = 0 trivial.
    Enumerates ALL 2^m - 1 nonempty subsets by DFS (complete check)."""
    masks = edge_masks(E)
    m = len(masks)
    # iterative DFS over subsets in index order
    stack = [(0, 0, 0)]  # (next index, union mask, count)
    while stack:
        i, u, c = stack.pop()
        if c >= 1 and bin(u).count('1') < c + 2:
            return False
        for j in range(i, m):
            stack.append((j + 1, u | masks[j], c + 1))
    return True


def _max_matching_edges_to_vertices(E, allowed):
    """Maximum bipartite matching between edges (left) and vertices in `allowed` (right); simple augmenting paths."""
    m = len(E)
    match_v = {}  # vertex -> edge index

    def try_edge(i, seen):
        for v in E[i]:
            if v in allowed and v not in seen:
                seen.add(v)
                if v not in match_v or try_edge(match_v[v], seen):
                    match_v[v] = i
                    return True
        return False

    size = 0
    for i in range(m):
        if try_edge(i, set()):
            size += 1
    return size


def p3_hall(n, E):
    """For every pair {x,y}: the edges have a system of distinct representatives in V \\ {x,y}  (Hall)."""
    m = len(E)
    for x in range(n):
        for y in range(x + 1, n):
            allowed = set(range(n)) - {x, y}
            if _max_matching_edges_to_vertices(E, allowed) < m:
                return False
    return True


def _lower_bound(masks, covered):
    """Greedy packing of pairwise disjoint uncovered edges: a lower bound on the number of further vertices."""
    used = 0
    cnt = 0
    for mk in masks:
        if mk & covered:
            continue
        if mk & used:
            continue
        used |= mk
        cnt += 1
    return cnt


def exists_transversal(masks, k, chosen=0, forbidden=0):
    """Is there a set T of at most k vertices (containing `chosen`, avoiding `forbidden`) meeting every edge?"""
    unc = [mk for mk in masks if not (mk & chosen)]
    if not unc:
        return True
    if k <= 0:
        return False
    if _lower_bound(unc, 0) > k:
        return False
    # branch on the uncovered edge with the fewest available vertices
    best = None
    bestavail = None
    for mk in unc:
        avail = mk & ~forbidden
        c = bin(avail).count('1')
        if best is None or c < bestavail:
            best, bestavail = avail, c
            if c <= 1:
                break
    if bestavail == 0:
        return False
    av = best
    forb = forbidden
    while av:
        b = av & -av
        av ^= b
        if exists_transversal(masks, k - 1, chosen | b, forb):
            return True
        forb |= b  # later branches exclude this vertex (each set found once)
    return False


def tau(n, E):
    masks = edge_masks(E)
    if not masks:
        return 0
    k = 0
    while not exists_transversal(masks, k):
        k += 1
    return k


def min_transversal(masks, k, chosen=0, forbidden=0):
    """Return a transversal with at most k vertices (as bitmask) or None."""
    unc = [mk for mk in masks if not (mk & chosen)]
    if not unc:
        return chosen
    if k <= 0:
        return None
    if _lower_bound(unc, 0) > k:
        return None
    best = None
    bestavail = None
    for mk in unc:
        avail = mk & ~forbidden
        c = bin(avail).count('1')
        if best is None or c < bestavail:
            best, bestavail = avail, c
            if c <= 1:
                break
    if bestavail == 0:
        return None
    av = best
    forb = forbidden
    while av:
        b = av & -av
        av ^= b
        r = min_transversal(masks, k - 1, chosen | b, forb)
        if r is not None:
            return r
        forb |= b
    return None


def all_min_transversals(masks, n):
    """All transversals of size exactly tau (each exactly once).  Branching: uncovered edge e={a,b,c}:
    a in T | a notin T, b in T | a,b notin T, c in T.  Returns (list of bitmasks, tau)."""
    if not masks:
        return [0], 0
    t = 0
    while not exists_transversal(masks, t):
        t += 1
    out = []

    def rec(chosen, forbidden, k):
        unc = [mk for mk in masks if not (mk & chosen)]
        if not unc:
            if k == 0:
                out.append(chosen)
            else:
                # pad with any k further vertices not forbidden: a minimum transversal has exactly t vertices, and
                # all its vertices are needed only if minimal; a transversal of size t that is not minimal cannot
                # exist (removing a vertex would give size t-1 < tau), so k == 0 here necessarily.
                raise AssertionError('non-minimal transversal of size tau')
            return
        if k <= 0:
            return
        if _lower_bound(unc, 0) > k:
            return
        best, bestavail = None, None
        for mk in unc:
            avail = mk & ~forbidden
            c = bin(avail).count('1')
            if best is None or c < bestavail:
                best, bestavail = avail, c
                if c <= 1:
                    break
        if bestavail == 0:
            return
        av = best
        forb = forbidden
        while av:
            b = av & -av
            av ^= b
            rec(chosen | b, forb, k - 1)
            forb |= b

    rec(0, 0, t)
    return out, t


def sub(n, E, Z):
    """Induced subhypergraph on V \\ Z, relabelled 0..n-|Z|-1; returns (n', E', old_of_new)."""
    Zs = set(Z)
    keep = [x for x in range(n) if x not in Zs]
    new = {x: i for i, x in enumerate(keep)}
    E2 = [tuple(sorted(new[x] for x in e)) for e in E if not (set(e) & Zs)]
    return len(keep), E2, keep


def tau_minus(n, E, Z):
    n2, E2, _ = sub(n, E, Z)
    return tau(n2, E2)


def cotransversal(n, E, Z, t=None):
    """Z is co-transversal iff tau(H - Z) == tau(H) - |Z|."""
    if t is None:
        t = tau(n, E)
    return tau_minus(n, E, Z) == t - len(Z)


# ---------------------------------------------------------------- canonical form (own implementation)
def canon(n, E):
    """Canonical certificate of the 2-coloured incidence graph (vertex nodes 0..n-1 colour 0, edge nodes colour 1)
    by individualisation-refinement with exhaustive search (minimum certificate over all leaves)."""
    m = len(E)
    N = n + m
    adj = [set() for _ in range(N)]
    for i, e in enumerate(E):
        for x in e:
            adj[x].add(n + i)
            adj[n + i].add(x)

    def refine(cells):
        # cells: list of lists (ordered partition); refine to equitable
        changed = True
        while changed:
            changed = False
            cell_of = {}
            for ci, cell in enumerate(cells):
                for v in cell:
                    cell_of[v] = ci
            newcells = []
            for cell in cells:
                if len(cell) == 1:
                    newcells.append(cell)
                    continue
                sig = {}
                for v in cell:
                    key = tuple(sorted(cell_of[u] for u in adj[v]))
                    sig.setdefault(key, []).append(v)
                if len(sig) > 1:
                    changed = True
                for key in sorted(sig):
                    newcells.append(sig[key])
            cells = newcells
        return cells

    best = [None]

    def leaf_cert(cells):
        order = [c[0] for c in cells]
        pos = {v: i for i, v in enumerate(order)}
        rows = []
        for v in order:
            rows.append(tuple(sorted(pos[u] for u in adj[v])))
        return tuple(rows)

    def search(cells):
        cells = refine(cells)
        if all(len(c) == 1 for c in cells):
            cert = leaf_cert(cells)
            if best[0] is None or cert < best[0]:
                best[0] = cert
            return
        # pick first smallest non-singleton cell
        idx = min((len(c), i) for i, c in enumerate(cells) if len(c) > 1)[1]
        cell = cells[idx]
        for v in cell:
            rest = [u for u in cell if u != v]
            newcells = cells[:idx] + [[v], rest] + cells[idx + 1:]
            search(newcells)

    init = [list(range(n)), list(range(n, N))]
    if m == 0:
        init = [list(range(n))]
    search(init)
    return (n, m, best[0])


def graph6_augmented(n, E):
    """graph6 string of the incidence graph plus a root adjacent to all edge nodes (for nauty labelg)."""
    m = len(E)
    N = n + m + 1
    root = n + m
    adjm = [[0] * N for _ in range(N)]
    for i, e in enumerate(E):
        for x in e:
            adjm[x][n + i] = adjm[n + i][x] = 1
        adjm[root][n + i] = adjm[n + i][root] = 1
    bits = []
    for j in range(N):
        for i in range(j):
            bits.append(adjm[i][j])
    while len(bits) % 6:
        bits.append(0)
    out = chr(N + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]:
            v = (v << 1) | b
        out += chr(v + 63)
    return out
