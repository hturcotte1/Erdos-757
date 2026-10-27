"""my_thm4.py -- referee's independent check of L018 Theorem 4 (non-locality construction) on explicit cubic graphs
of girth 6 (Heawood), 7 (McGee, LCF [12,7,-7]^8) and 8 (Tutte-Coxeter, LCF [-13,-9,7,-7,9,13]^5).
For each: subdivide one edge, build H (vertices = edges of G plus p; H-edges = stars delta(w), plus p in the star of g0),
and verify: 3-uniform, linear, Delta = 2, exactly one pendant p, connected, F7-free (all 5-edge subsets), Hall e(S)<=|S|-2
(all edge subsets for m <= 16, SDR-per-pair otherwise), slack via own exact tau, slack >= n2/7, Theorem 1 Red pair
(Z = V - u, T = minimum transversal), NO (Red) pair with |Z| <= ZMAX (direct enumeration), local configuration K_r(p)
is the complete binary hypertree for 2r+4 <= girth, and the forest lemma value bound on all small Z.
Independent of experiments/prover/L018 (no import)."""
import itertools, sys, time
import networkx as nx

def tau_edges(E):
    E = [frozenset(e) for e in E]
    best = [len(E)]
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        if k + 1 >= best[0]:
            return
        # branch on the vertices of an edge of maximum "degree" within rem for speed
        e = max(rem, key=lambda f: sum(1 for g in rem if f & g))
        for v in e:
            rec([f for f in rem if v not in f], k + 1)
    rec(E, 0)
    return best[0]

def min_transversal(E):
    """a minimum transversal, by exact branch and bound (returns the set)."""
    E = [frozenset(e) for e in E]
    best = [set().union(*E)]
    def rec(rem, T):
        if not rem:
            if len(T) < len(best[0]): best[0] = set(T)
            return
        if len(T) + 1 >= len(best[0]): return
        e = max(rem, key=lambda f: sum(1 for g in rem if f & g))
        for v in e:
            rec([f for f in rem if v not in f], T | {v})
    rec(E, set())
    return best[0]

def is_linear(E):
    return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2))

def has_f7(E):
    Es = [frozenset(e) for e in E]
    for c in itertools.combinations(range(len(Es)), 5):
        U = set().union(*(Es[i] for i in c))
        if len(U) != 7: continue
        deg = {}
        for i in c:
            for v in Es[i]: deg[v] = deg.get(v, 0) + 1
        if sorted(deg.values()) == [2, 2, 2, 2, 2, 2, 3]:
            return True
    return False

def hall_ok(E):
    """e_ind(S) <= |S|-2 for all |S|>=2  <=>  |union F| >= |F|+2 for all nonempty edge sets F."""
    Es = [frozenset(e) for e in E]
    m = len(Es)
    if m <= 16:
        for mask in range(1, 1 << m):
            F = [Es[i] for i in range(m) if mask >> i & 1]
            if len(set().union(*F)) < len(F) + 2:
                return False
        return True
    # SDR form: for every vertex pair {x,y}, the edges have a system of distinct representatives avoiding x,y
    V = sorted(set().union(*Es))
    for x, y in itertools.combinations(V, 2):
        B = nx.Graph()
        B.add_nodes_from([('e', i) for i in range(m)], bipartite=0)
        for i, e in enumerate(Es):
            for v in e:
                if v != x and v != y:
                    B.add_edge(('e', i), ('v', v))
        M = nx.bipartite.hopcroft_karp_matching(B, top_nodes=[('e', i) for i in range(m)])
        if sum(1 for k in M if k[0] == 'e') < m:
            return False
    return True

def build_H(G):
    """G simple graph (networkx), one vertex g0 of degree 2 (others 3). Returns edges of H (tuples), vertex labels."""
    edges_G = [tuple(sorted(e)) for e in G.edges()]
    idx = {e: i for i, e in enumerate(edges_G)}
    p = len(edges_G)
    g0 = [v for v in G.nodes() if G.degree(v) == 2]
    assert len(g0) == 1; g0 = g0[0]
    H = []
    for w in G.nodes():
        star = [idx[tuple(sorted((w, u)))] for u in G.neighbors(w)]
        if w == g0: star.append(p)
        assert len(star) == 3
        H.append(tuple(sorted(star)))
    return H, p

def red_pairs_small(H, n, zmax):
    """all Z with |Z| <= zmax and value(Z) >= 0 (value = 3|Z| + 2e(Z) - 11 tau(E_Z))"""
    Es = [frozenset(e) for e in H]
    inc = {v: [e for e in Es if v in e] for v in range(n)}
    found = []
    maxval = {}
    for k in range(1, zmax + 1):
        mv = -999
        for Z in itertools.combinations(range(n), k):
            EZ = set()
            for z in Z: EZ |= set(inc[z])
            EZ = list(EZ)
            val = 3 * k + 2 * len(EZ) - 11 * tau_edges(EZ)
            mv = max(mv, val)
            if val >= 0 and k < n:
                found.append((Z, val))
        maxval[k] = mv
    return found, maxval

def local_tree_check(H, p, n, rmax):
    """K_r(p): is the configuration within distance r of p the complete binary hypertree (all processed non-root degree 2,
    2^(r+1)-1 vertices in B_r, every edge meeting B_r meets it in a 'parent' and two 'children' pattern)?"""
    Es = [frozenset(e) for e in H]
    adj = {v: set() for v in range(n)}
    for e in Es:
        for u in e: adj[u] |= e
    dist = {p: 0}; frontier = {p}
    while frontier:
        nf = set()
        for v in frontier:
            for u in adj[v]:
                if u not in dist: dist[u] = dist[v] + 1; nf.add(u)
        frontier = nf
    res = {}
    for r in range(0, rmax + 1):
        Br = {v for v, d in dist.items() if d <= r}
        ok = len(Br) == 2 ** (r + 1) - 1
        # every vertex at distance j>=1, j<=r has degree 2 and its two edges: one towards (contains a vertex at distance j-1), one away
        # every edge meeting B_r meets exactly: one vertex at distance j and two at distance j+1 (0<=j<=r)
        for e in Es:
            if e & Br:
                ds = sorted(dist[v] for v in e)
                if not (ds[1] == ds[0] + 1 and ds[2] == ds[0] + 1): ok = False
        # no vertex of B_r is in two edges with the same distance pattern "towards" (i.e. tree: distinct parents) -> implied by counts
        res[r] = (ok, len(Br))
    return res

def analyse(name, G):
    t0 = time.time()
    # subdivide one edge
    G = nx.Graph(G)
    u, v = next(iter(G.edges()))
    g0 = max(G.nodes()) + 1
    G.remove_edge(u, v); G.add_edge(u, g0); G.add_edge(g0, v)
    girth = min(len(c) for c in nx.minimum_cycle_basis(G))
    H, p = build_H(G)
    n = len(G.edges()) + 1
    deg = [0] * n
    for e in H:
        for x in e: deg[x] += 1
    print('==', name, ': G has', G.number_of_nodes(), 'vertices', G.number_of_edges(), 'edges, girth', girth)
    print('   H: n =', n, 'm =', len(H), 'degrees: Delta =', max(deg), 'pendants =', sum(1 for d in deg if d == 1), '(p =', p, ') isolated =', sum(1 for d in deg if d == 0))
    print('   3-uniform:', all(len(set(e)) == 3 for e in H), ' linear:', is_linear(H))
    Hn = nx.Graph()
    for e in H: Hn.add_edges_from(itertools.combinations(e, 2))
    print('   connected:', nx.is_connected(Hn) and Hn.number_of_nodes() == n)
    print('   F7-free:', not has_f7(H))
    print('   Hall e(S)<=|S|-2:', hall_ok(H))
    tau = tau_edges(H)
    n2 = sum(1 for d in deg if d == 2)
    slack = 3 * n + 2 * len(H) - 11 * tau
    print('   tau =', tau, ' slack =', slack, ' n2 =', n2, ' 7*slack >= n2:', 7 * slack >= n2, ' slack>=3:', slack >= 3)
    # Theorem 1 Red pair: Z = V - {u0}, T = minimum transversal
    T = min_transversal(H)
    Z = set(range(n)) - {0}
    EZ = [e for e in H if set(e) & Z]
    val = 3 * len(Z) + 2 * len(EZ) - 11 * len(T)
    print('   global Red pair (Z=V-{0}, T=min transversal): value =', val, '>= 0:', val >= 0, ' T meets all E_Z:', all(set(e) & T for e in EZ))
    zmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    found, maxval = red_pairs_small(H, n, zmax)
    print('   (Red) pairs with |Z| <=', zmax, ':', len(found), ' max value by |Z|:', maxval, ' forest-lemma prediction: none with |Z| < girth/2 =', girth / 2)
    if found: print('      examples:', found[:5])
    rmax = (girth - 4) // 2
    print('   local configuration K_r(p) is the complete binary hypertree for r <=', rmax, ':', local_tree_check(H, p, n, rmax))
    print('   (%.1f s)' % (time.time() - t0))

if __name__ == '__main__':
    analyse('Heawood (girth 6)', nx.heawood_graph())
    analyse('McGee (girth 7)', nx.LCF_graph(24, [12, 7, -7], 8))
    analyse('Tutte-Coxeter (girth 8)', nx.LCF_graph(30, [-13, -9, 7, -7, 9, 13], 5))
