"""Adversarial numerical check of L021 Theorem 6 (Delta <= 2), Steps 6.1-6.5, with own
code: for connected simple subcubic graphs G (networkx atlas up to 7 nodes, plus random
ones), build the dual H, check tau(H) = N - nu(G) and A = 132 nu - 16N - 27M, and for
EVERY Tutte-Berge set U (all subsets when N <= 10; the Gallai-Edmonds set otherwise)
check M <= 3|U| + sum e_i, A >= 35|U| + sum theta_i, the theta classification, and
that the explicit family X of 6.4 is a valid L*-family (induced copies of E_1 and of
(8,5,3)#0, pairwise disjoint, E*_H(X) contained in U) with A + DEF_H(X) >= 0.
Usage: thm6_check.py n_random max_N seed"""
import sys, random, time
from itertools import combinations
import networkx as nx
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rlib import tau, iso, A_of, masks

E853 = [(0, 1, 2), (1, 5, 6), (2, 4, 7), (3, 4, 6), (3, 5, 7)]
E1 = [(0, 1, 2)]


def dual(G):
    nodes = sorted(G.nodes())
    vid = {}
    k = 0
    for (a, b) in G.edges():
        vid[frozenset((a, b))] = k
        k += 1
    edges = {}
    for x in nodes:
        vs = [vid[frozenset((x, y))] for y in G.neighbors(x)]
        while len(vs) < 3:
            vs.append(k)
            k += 1
        edges[x] = tuple(vs)
    return k, edges, vid


def nu(G):
    return len(nx.max_weight_matching(G, maxcardinality=True))


def odd_comps(G, U):
    R = G.subgraph([x for x in G.nodes() if x not in U])
    return [sorted(c) for c in nx.connected_components(R)]


def check_U(G, U, nH, Hedges, vid, A, nuG, report):
    N, M = G.number_of_nodes(), G.number_of_edges()
    comps = odd_comps(G, U)
    o = sum(1 for c in comps if len(c) % 2 == 1)
    assert 2 * nuG == N + len(U) - o
    se = 0
    th_sum = 0
    o1 = o5 = 0
    members = []
    for c in comps:
        sub = G.subgraph(c)
        ci, ei = sub.number_of_nodes(), sub.number_of_edges()
        se += ei
        th = 50 * ci - 27 * ei - 66 * (ci % 2)
        th_sum += th
        if th < 0:
            if ci == 1:
                o1 += 1
                assert th == -16
                members.append((set(Hedges[c[0]]), 16, E1))
            else:
                assert (ci, ei) == (5, 7) and th == -5, (ci, ei, th)
                o5 += 1
                degs = dict(sub.degree())
                u0 = [x for x in c if degs[x] == 2]
                assert len(u0) == 1
                u0 = u0[0]
                Vs = set(vid[frozenset(e)] for e in sub.edges())
                third = [w for w in Hedges[u0] if w not in Vs]
                assert len(third) == 1
                Vs.add(third[0])
                members.append((Vs, 5, E853))
    assert M <= 3 * len(U) + se
    assert A >= 35 * len(U) + th_sum
    # validate the family
    allE = list(Hedges.values())
    for i, (Vs, W, P) in enumerate(members):
        inside = [e for e in allE if set(e) <= Vs]
        assert len(Vs) == (3 if W == 16 else 8)
        relabel = {v: j for j, v in enumerate(sorted(Vs))}
        assert iso([tuple(relabel[v] for v in e) for e in inside], P)
    for (V1, _, _), (V2, _, _) in combinations(members, 2):
        assert not (V1 & V2)
    VX = set().union(*[m[0] for m in members]) if members else set()
    estar = [x for x, e in Hedges.items() if (set(e) & VX) and not any(set(e) <= m[0] for m in members)]
    assert set(estar) <= set(U), (estar, U)
    DEFX = sum(m[1] for m in members) - 35 * len(estar)
    assert DEFX >= 16 * o1 + 5 * o5 - 35 * len(U)
    assert A + DEFX >= 0
    report["negA"] += (A < 0)
    report["o5"] += o5
    report["minP"] = min(report["minP"], A + DEFX)


def run_graph(G, report, allU):
    N, M = G.number_of_nodes(), G.number_of_edges()
    nH, Hedges, vid = dual(G)
    E = list(Hedges.values())
    t = tau(nH, E)
    nuG = nu(G)
    assert t == N - nuG, (t, N, nuG)
    A = A_of(nH, len(E), t)
    assert A == 132 * nuG - 16 * N - 27 * M
    assert nH == 3 * N - M
    nodes = list(G.nodes())
    if allU:
        cnt = 0
        for r in range(0, N + 1):
            for U in combinations(nodes, r):
                comps = odd_comps(G, set(U))
                o = sum(1 for c in comps if len(c) % 2 == 1)
                if N + r - o == 2 * nuG:
                    check_U(G, set(U), nH, Hedges, vid, A, nuG, report)
                    cnt += 1
        assert cnt >= 1
        report["U_sets"] += cnt
    else:
        D = set(x for x in nodes if nu(G.subgraph([y for y in nodes if y != x])) == nuG)
        Aset = set(y for x in D for y in G.neighbors(x)) - D
        check_U(G, Aset, nH, Hedges, vid, A, nuG, report)
        report["U_sets"] += 1
    report["graphs"] += 1


def random_subcubic(N, rng):
    while True:
        G = nx.Graph()
        G.add_nodes_from(range(N))
        order = list(range(N))
        rng.shuffle(order)
        for i in range(1, N):  # random tree with degree cap 3
            cands = [order[j] for j in range(i) if G.degree(order[j]) < 3]
            G.add_edge(order[i], rng.choice(cands))
        extra = rng.randint(0, N // 2 + 1)
        for _ in range(extra * 3):
            a, b = rng.sample(range(N), 2)
            if not G.has_edge(a, b) and G.degree(a) < 3 and G.degree(b) < 3:
                G.add_edge(a, b)
                extra -= 1
                if extra <= 0:
                    break
        if nx.is_connected(G) and max(d for _, d in G.degree()) <= 3:
            return G


if __name__ == "__main__":
    nrand = int(sys.argv[1]); maxN = int(sys.argv[2]); seed = int(sys.argv[3])
    rng = random.Random(seed)
    t0 = time.time()
    rep = dict(graphs=0, U_sets=0, negA=0, o5=0, minP=10 ** 9)
    from networkx.generators.atlas import graph_atlas_g
    for G in graph_atlas_g()[1:]:
        if G.number_of_nodes() >= 1 and nx.is_connected(G) and max((d for _, d in G.degree()), default=0) <= 3 and G.number_of_edges() >= 0:
            if G.number_of_nodes() == 1:
                continue  # m = 1 edge H: the E_1 itself; included via random N=1 below
            run_graph(nx.convert_node_labels_to_integers(G), rep, allU=True)
    atlas = dict(rep)
    print("atlas (connected subcubic, 2..7 nodes):", atlas, f"[{time.time()-t0:.0f}s]", flush=True)
    G1 = nx.Graph(); G1.add_node(0)
    run_graph(G1, rep, allU=True)
    for i in range(nrand):
        N = rng.randint(2, maxN)
        G = random_subcubic(N, rng)
        run_graph(G, rep, allU=(N <= 10))
    print("total:", rep, f"[{time.time()-t0:.0f}s]")
    print("ALL OK (no assertion failed)")
