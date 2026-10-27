"""L017, illustrative check of Lemma M (Step 9).
(a) Every simple graph G with maximum degree <= 3 satisfies 11 nu(G) >= 3 |E(G)|, with equality only if E(G) is empty:
    exhaustive over all graphs with max degree <= 3 on n <= NMAX vertices (nauty geng -D3, not necessarily connected).
(b) For linear 3-uniform H with max degree <= 2: tau(H) = m - nu(G) where G is the dual graph (vertices = edges of H,
    one G-edge per degree-2 vertex of H), and slack(H) = 3 n0 + 11 nu(G) - 3 |E(G)|: random instances, tau(H) computed
    directly on H by the exact branch and bound of hyp.py (independently of G).
Usage: python3 check_lemma_m.py NMAX NRANDOM SEED"""
import sys, subprocess, random, os
import networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyp import tau, slack, is_linear
GENG = '/home/user/Erdos-757/experiments/referee/L013-round2/out/nauty_build/geng'

def nu(G):
    return len(nx.max_weight_matching(G, maxcardinality=True))

def part_a(NMAX):
    tot = 0; worst = None; eq_nonempty = 0; minpos = None; minpos_ex = None
    for n in range(1, NMAX + 1):
        out = subprocess.run([GENG, '-q', '-D3', str(n)], capture_output=True, text=True, timeout=3000).stdout.split()
        cnt = 0
        for g6 in out:
            G = nx.from_graph6_bytes(g6.encode()); M = G.number_of_edges(); v = nu(G)
            d = 11 * v - 3 * M
            assert d >= 0, ('VIOLATION', g6, v, M)
            if M > 0:
                if d == 0: eq_nonempty += 1
                if minpos is None or d < minpos: minpos, minpos_ex = d, (n, g6, v, M)
            cnt += 1
        tot += cnt
        print('n=%d graphs(maxdeg<=3)=%d  all satisfy 11nu-3M >= 0' % (n, cnt), flush=True)
    print('PART A: %d graphs, 0 violations; graphs with M>0 and 11nu=3M: %d; min of 11nu-3M over M>0: %s at %s' % (tot, eq_nonempty, minpos, minpos_ex))

def random_dual(rng, NG, n0):
    """random simple graph with max degree <= 3 on NG vertices, turned into the linear max-degree-2 3-graph H."""
    G = nx.Graph(); G.add_nodes_from(range(NG))
    pairs = [(i, j) for i in range(NG) for j in range(i + 1, NG)]; rng.shuffle(pairs)
    target = rng.randint(0, 3 * NG // 2)
    for (i, j) in pairs:
        if G.number_of_edges() >= target: break
        if G.degree(i) < 3 and G.degree(j) < 3: G.add_edge(i, j)
    # H: vertices = G-edges (degree 2) + half-edges (degree 1) + n0 isolated vertices; edges = G-vertices
    vid = {}; nxt = 0; hedges = {i: [] for i in range(NG)}
    for (i, j) in G.edges():
        vid[(i, j)] = nxt; hedges[i].append(nxt); hedges[j].append(nxt); nxt += 1
    for i in range(NG):
        while len(hedges[i]) < 3:
            hedges[i].append(nxt); nxt += 1
    n = nxt + n0
    # random relabelling of H's vertices so that nothing about the construction is visible to the tau solver
    perm = list(range(n)); rng.shuffle(perm)
    edges = [tuple(sorted(perm[x] for x in hedges[i])) for i in range(NG)]
    return G, n, edges

def part_b(NR, seed):
    rng = random.Random(seed); bad = 0; mins = None
    for it in range(NR):
        NG = rng.randint(1, 14); n0 = rng.randint(0, 2)
        G, n, edges = random_dual(rng, NG, n0)
        assert is_linear(edges)
        m = len(edges); t = tau(n, edges); v = nu(G)
        ok1 = (t == m - v); s = slack(n, m, t); ok2 = (s == 3 * n0 + 11 * v - 3 * G.number_of_edges())
        if not (ok1 and ok2 and s >= 0): bad += 1; print('MISMATCH', n, edges, t, v, s)
        if G.number_of_edges() > 0 and n0 == 0 and nx.is_connected(G):
            mins = s if mins is None else min(mins, s)
    print('PART B: %d random linear max-degree-2 3-graphs (1..14 edges, 0..2 isolated vertices): tau = m - nu(G) and slack = 3n0 + 11nu - 3|E(G)| >= 0 in all; mismatches: %d; min slack over connected ones with >= 2 edges: %s' % (NR, bad, mins))

if __name__ == '__main__':
    NMAX = int(sys.argv[1]); NR = int(sys.argv[2]); seed = int(sys.argv[3])
    part_a(NMAX); part_b(NR, seed)
