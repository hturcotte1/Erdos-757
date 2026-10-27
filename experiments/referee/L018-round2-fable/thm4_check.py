"""Theorem 4 (L018), independent check on cubic cages: Petersen (g=5), Heawood (g=6),
Tutte-Coxeter (g=8), each with one edge subdivided (4.1), H built as in 4.2.
Checks: 4.2 (3-uniform, linear, Delta=2, one pendant, connected); 4.3 (class C: F7-free, Hall);
tau(H) = m - nu(G) (2.2); 7 slack >= n_2 (Theorem 2); forest lemma 4.4 (exhaustive on Petersen:
G[W] forest => value(Z) < 0; every Z with value >= 0 has |W| >= g and |Z| >= g/2);
4.5: K_r^sp(p) is the complete binary hypertree for 2r+4 <= g (and also for 2r+2 <= g), and
max value over nonempty Z subset of B_r(p) is < 0."""
import sys, itertools
import networkx as nx
from common import *


def build_H(G0):
    G = nx.Graph(G0)
    u, v = next(iter(G.edges()))
    G.remove_edge(u, v)
    g0 = max(G.nodes()) + 1
    G.add_edge(u, g0); G.add_edge(g0, v)
    # H: vertices = edges of G (as frozensets) plus 'p'
    eid = {frozenset(e): i for i, e in enumerate(G.edges())}
    p = len(eid)
    H = []
    for w in G.nodes():
        e = frozenset(eid[frozenset((w, x))] for x in G.neighbors(w))
        if w == g0:
            e = e | {p}
        H.append(frozenset(e))
    return G, g0, eid, p, H


def girth(G):
    g = None
    for s in G.nodes():
        dist = {s: 0}; par = {s: None}; q = [s]
        for x in q:
            for y in G.neighbors(x):
                if y not in dist:
                    dist[y] = dist[x] + 1; par[y] = x; q.append(y)
                elif par[x] != y:
                    c = dist[x] + dist[y] + 1
                    if g is None or c < g:
                        g = c
    return g


def forest(G, W):
    sub = G.subgraph(W)
    return sub.number_of_edges() == sub.number_of_nodes() - nx.number_connected_components(sub)


def bfs_H(H, root):
    adj = defaultdict(set)
    for e in H:
        for a in e:
            adj[a] |= e - {a}
    dist = {root: 0}; q = [root]
    for x in q:
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1; q.append(y)
    return dist


def check_hypertree(H, p, dist, r):
    """K_r = edges meeting B_r(p). Verify: no boundary vertex lies in two edges of K_r (no
    splitting), and K_r is the complete binary hypertree of depth r."""
    Br = {x for x, d in dist.items() if d <= r}
    Kr = [e for e in H if e & Br]
    boundary = {x for e in Kr for x in e if dist[x] == r + 1}
    if any(sum(1 for e in Kr if b in e) != 1 for b in boundary):
        return False, 'boundary vertex in >=2 edges'
    if len(Br) != 2 ** (r + 1) - 1 or len(Kr) != 2 ** (r + 1) - 1:
        return False, f'counts |B_r|={len(Br)} |K_r|={len(Kr)}'
    d = degrees(Kr)
    if d[p] != 1 or any(d[x] != 2 for x in Br if x != p):
        return False, 'degrees'
    # each edge of K_r has one vertex at distance j and two at distance j+1
    for e in Kr:
        ds = sorted(dist[x] for x in e)
        if not (ds[1] == ds[2] == ds[0] + 1):
            return False, f'edge level pattern {ds}'
    for j in range(r + 2):
        if sum(1 for x in dist if x in Br or x in boundary) and sum(1 for x in (Br | boundary) if dist[x] == j) != 2 ** j:
            return False, f'level {j} size'
    return True, 'complete binary hypertree'


def main():
    cages = [('Petersen', nx.petersen_graph(), True), ('Heawood', nx.heawood_graph(), False),
             ('Tutte-Coxeter', nx.LCF_graph(30, [-13, -9, 7, -7, 9, 13], 5), False)]
    for name, G0, exhaustive in cages:
        G, g0, eid, p, H = build_H(G0)
        g = girth(G)
        V = set(range(p + 1)); n = len(V); m = len(H)
        d = degrees(H, V)
        print(f'== {name}: G has {G.number_of_nodes()} vertices, {G.number_of_edges()} edges, girth {g}; H: n={n} m={m}')
        assert all(len(e) == 3 for e in H)
        print('  linear', is_linear(H), '| Delta', max(d.values()), '| pendants', [x for x in V if d[x] == 1], '| connected', is_connected(H, V))
        print('  F7-free', not has_f7(H), '| Hall e(S)<=|S|-2', hall_condition(H, V))
        t = tau_ilp(H); nu = len(nx.max_weight_matching(G, maxcardinality=True))
        if m <= 16:
            assert tau(H) == t, 'branch-and-bound and CP-SAT disagree'
        s = 3 * n + 2 * m - 11 * t
        n2 = sum(1 for x in V if d[x] == 2)
        print(f'  tau={t} m-nu(G)={m - nu} slack={s} n2={n2} 7*slack-n2={7 * s - n2} (>=0?)')
        dist = bfs_H(H, p)
        for r in range(0, (g - 2) // 2 + 1):
            ok, msg = check_hypertree(H, p, dist, r)
            Br = [x for x in V if dist[x] <= r]
            best = None
            memo = {}
            for k in range(1, len(Br) + 1):
                for Z in itertools.combinations(Br, k):
                    W = frozenset(i for i, e in enumerate(H) if e & set(Z))
                    if W not in memo:
                        memo[W] = tau([H[i] for i in W])
                    val = 3 * k + 2 * len(W) - 11 * memo[W]
                    best = val if best is None else max(best, val)
            tag = '2r+4<=g' if 2 * r + 4 <= g else ('2r+2<=g' if 2 * r + 2 <= g else 'beyond')
            print(f'  r={r} [{tag}]: K_r^sp(p) {msg}: {ok}; |B_r(p)|={len(Br)}; max value over Z in B_r(p) = {best}')
        if exhaustive:
            # forest lemma, all nonempty proper Z
            Vl = sorted(V); memo = {}
            viol = 0; nonneg = 0; minZ = None; minW = None
            for mask in range(1, 2 ** n - 1):
                Z = [Vl[i] for i in range(n) if mask >> i & 1]
                W = frozenset(i for i, e in enumerate(H) if e & set(Z))
                if W not in memo:
                    memo[W] = tau([H[i] for i in W])
                val = 3 * len(Z) + 2 * len(W) - 11 * memo[W]
                Wn = [list(G.nodes())[i] for i in W]
                if forest(G, Wn) and val >= 0:
                    viol += 1
                if val >= 0:
                    nonneg += 1
                    minZ = len(Z) if minZ is None else min(minZ, len(Z))
                    minW = len(W) if minW is None else min(minW, len(W))
            print(f'  exhaustive: {2 ** n - 2} sets Z; value>=0 for {nonneg}; forest-lemma violations {viol}; min|Z| with value>=0: {minZ} (g/2={g / 2}); min|W| = {minW} (g={g})')
            # also the Lemma 2.2 bound value(Z) <= 11 nu(G[W]) - 3|E_G(W)| on all Z
            bad = 0
            for mask in range(1, 2 ** n - 1):
                Z = [Vl[i] for i in range(n) if mask >> i & 1]
                W = frozenset(i for i, e in enumerate(H) if e & set(Z))
                val = 3 * len(Z) + 2 * len(W) - 11 * memo[W]
                Wn = [list(G.nodes())[i] for i in W]
                nuW = len(nx.max_weight_matching(G.subgraph(Wn), maxcardinality=True))
                EGW = sum(1 for e in G.edges() if e[0] in Wn or e[1] in Wn)
                if val > 11 * nuW - 3 * EGW:
                    bad += 1
            print(f'  Lemma 2.2 bound violated on {bad} sets')


main()
