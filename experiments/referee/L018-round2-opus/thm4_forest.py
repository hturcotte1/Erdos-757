"""Referee round 2 (opus): Theorem 4 spot check. For a cubic graph G0, subdivide one edge (new vertex g0),
build H (vertices = E(G) + {p}; edges = delta(w), and delta(g0)+{p}); then for every Z (exhaustive, or a
random sample) check: (1) value(Z) <= 11 nu(G[W]) - 3|E_G(W)| (Lemma 2.2), W = E_Z;
(2) G[W] a forest => value(Z) < 0 (forest lemma 4.4); (3) the minimum |Z| of a (Red) pair is >= girth/2;
plus H linear, Delta(H)=2, exactly one pendant. Own code; networkx only for graphs/matchings."""
import sys, random, itertools
import networkx as nx

def build(G0):
    u, v = next(iter(G0.edges()))
    G = G0.copy(); G.remove_edge(u, v); g0 = ('sub',); G.add_edge(u, g0); G.add_edge(g0, v)
    Ged = [tuple(sorted(e, key=str)) for e in G.edges()]
    hid = {e: i for i, e in enumerate(Ged)}; p = len(Ged)
    Hed, owner = [], []
    for w in G.nodes():
        e = [hid[tuple(sorted(f, key=str))] for f in G.edges(w)]
        if w == g0: e.append(p)
        assert len(e) == 3; Hed.append(tuple(e)); owner.append(w)
    return G, g0, Ged, p, Hed, owner

def tau_factory(Hed, n):
    inc = [0] * n
    for i, e in enumerate(Hed):
        for x in e: inc[x] |= 1 << i
    memo = {}
    def tau(mask):
        if mask == 0: return 0
        r = memo.get(mask)
        if r is not None: return r
        i = (mask & -mask).bit_length() - 1
        r = min(1 + tau(mask & ~inc[x]) for x in Hed[i])
        memo[mask] = r; return r
    return inc, tau

def run(name, G0, sample=None, seed=1):
    G, g0, Ged, p, Hed, owner = build(G0)
    n = p + 1; m = len(Hed)
    girth = nx.girth(G)
    deg = [0] * n
    for e in Hed:
        for x in e: deg[x] += 1
    lin = all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(Hed, 2))
    inc, tau = tau_factory(Hed, n)
    T = tau((1 << m) - 1); slack = 3 * n + 2 * m - 11 * T
    stats = dict(checked=0, forest=0, red=0, l22viol=0, forestviol=0, minZred=None)
    rng = random.Random(seed)
    def Zs():
        if sample is None:
            for k in range(1, n):
                for Z in itertools.combinations(range(n), k): yield Z
        else:
            for _ in range(sample):
                k = rng.randint(1, min(n - 1, 2 * girth + 4)); yield tuple(rng.sample(range(n), k))
    for Z in Zs():
        F = 0
        for z in Z: F |= inc[z]
        W = [owner[i] for i in range(m) if (F >> i) & 1]
        val = 3 * len(Z) + 2 * bin(F).count('1') - 11 * tau(F)
        GW = G.subgraph(W)
        nu = len(nx.max_weight_matching(GW, maxcardinality=True))
        EGW = sum(1 for e in G.edges() if e[0] in set(W) or e[1] in set(W))
        stats['checked'] += 1
        if val > 11 * nu - 3 * EGW: stats['l22viol'] += 1
        if nx.is_forest(GW):
            stats['forest'] += 1
            if val >= 0: stats['forestviol'] += 1
        if val >= 0:
            stats['red'] += 1
            if stats['minZred'] is None or len(Z) < stats['minZred']: stats['minZred'] = len(Z)
    print('%-14s girth %d  H=(n %d, m %d, tau %d, slack %d) linear %s maxdeg %d pendants %d  %s  minZ>=g/2: %s' % (
        name, girth, n, m, T, slack, lin, max(deg), deg.count(1), stats,
        None if stats['minZred'] is None else stats['minZred'] >= girth / 2))

run('K4', nx.complete_graph(4))
run('K33', nx.complete_bipartite_graph(3, 3))
run('Q3', nx.hypercube_graph(3))
run('Petersen', nx.petersen_graph())
run('Heawood(s)', nx.heawood_graph(), sample=int(sys.argv[1]) if len(sys.argv) > 1 else 20000)
