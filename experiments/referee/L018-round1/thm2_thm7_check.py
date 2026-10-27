"""thm2_thm7_check.py -- referee checks of L018 Theorem 2 (Lemma M), Lemma 2.2, Theorem 1 and Theorem 7.

(A) every simple graph G with Delta <= 3 on <= 7 vertices (networkx graph atlas) and random subcubic graphs up to 40
    vertices: build the linear Delta<=2 3-graph H with dual G (+ n0 isolated vertices), compute tau(H) by exact branch
    and bound (independent of matchings), check tau = m - nu(G), slack = 3 n0 + 11 nu - 3 n2, 7 slack >= 21 n0 + n2.
(B) Theorem 1 (closure form) against brute force on census graphs (n <= 9) and on random linear Delta<=3 3-graphs.
(C) Theorem 7 on census graphs n <= 11: 7 slack >= 14|E_S| - 56|S| + 21 n0(H-S) + n2(H-S) for S = degree-3 vertices and
    for random S with Delta(H-S) <= 2; and the special case when no edge has two degree-3 vertices.
(D) Lemma 2.2 on (A)-graphs: value(Z) <= 11 nu(G[W]) - 3 |E_G(W)| for all Z (small cases).
"""
import itertools, random, sys, os
import networkx as nx

random.seed(20261027)


def tau_bb(E):
    E = [frozenset(e) for e in E]
    if not E:
        return 0
    best = [len(E)]
    def rec(es, k):
        if k >= best[0]:
            return
        if not es:
            best[0] = k; return
        # lower bound: greedy packing
        used = set(); lb = 0
        for e in es:
            if not (e & used):
                used |= e; lb += 1
        if k + lb >= best[0]:
            return
        e = es[0]
        for v in e:
            rec([f for f in es if v not in f], k + 1)
    rec(E, 0)
    return best[0]


def H_from_dual(G, n0=0):
    nodes = list(G.nodes())
    vid = {}
    nxt = [0]
    def new():
        nxt[0] += 1
        return nxt[0] - 1
    for e in G.edges():
        vid[frozenset(e)] = new()
    E = []
    for w in nodes:
        inc = [vid[frozenset((w, x))] for x in G.neighbors(w)]
        while len(inc) < 3:
            inc.append(new())
        E.append(tuple(inc))
    n = nxt[0] + n0
    return n, E


def check_A():
    cnt = 0; minval = None; eqcases = 0
    graphs = [g for g in nx.graph_atlas_g() if g.number_of_nodes() >= 1 and (g.number_of_edges() == 0 or max(d for _, d in g.degree()) <= 3)]
    for _ in range(3000):
        N = random.randint(2, 40)
        G = nx.Graph(); G.add_nodes_from(range(N))
        tries = 0
        target = random.randint(0, (3 * N) // 2)
        while G.number_of_edges() < target and tries < 20 * N:
            tries += 1
            a, b = random.sample(range(N), 2)
            if G.has_edge(a, b) or G.degree(a) >= 3 or G.degree(b) >= 3:
                continue
            G.add_edge(a, b)
        graphs.append(G)
    for G in graphs:
        if G.number_of_nodes() == 0:
            continue
        n0 = random.randint(0, 2)
        n, E = H_from_dual(G, n0)
        m = len(E)
        deg = [0] * n
        for e in E:
            for v in e:
                deg[v] += 1
        assert max(deg) <= 2
        assert all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2))
        n2 = sum(1 for d in deg if d == 2)
        n0c = sum(1 for d in deg if d == 0)
        assert n0c == n0 and n2 == G.number_of_edges()
        t = tau_bb(E)
        nu = len(nx.max_weight_matching(G, maxcardinality=True))
        assert t == m - nu, ('tau identity fails', t, m, nu)
        s = 3 * n + 2 * m - 11 * t
        assert s == 3 * n0 + 11 * nu - 3 * n2
        v = 7 * s - 21 * n0 - n2
        assert v >= 0, ('Theorem 2 fails', list(G.edges()))
        if v == 0 and n2 > 0:
            eqcases += 1
        minval = v if minval is None else min(minval, v)
        cnt += 1
    print('(A) Theorem 2: %d linear Delta<=2 3-graphs (all subcubic graphs <= 7 vertices + 3000 random, up to 40 vertices): '
          'identities tau = m - nu and slack = 3n0+11nu-3n2 hold; min of 7 slack - 21 n0 - n2 = %d; equality cases with n2>0: %d'
          % (cnt, minval, eqcases))


def read_census(n, maxgraphs=None):
    base = '/home/user/Erdos-757/experiments/20261027-0230-red-config/out'
    out = []
    for m in range(1, n - 1):
        f = os.path.join(base, 'cls_%d_%d.txt' % (n, m))
        if not os.path.exists(f):
            continue
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                es = [p for p in parts if '.' in p]
                E = [tuple(int(x) for x in p.split('.')) for p in es]
                if E:
                    out.append(E)
                if maxgraphs and len(out) >= maxgraphs:
                    return out
    return out


def red_bruteforce(n, E):
    """exists (Z,T): nonempty Z != V, T meets every edge at Z, 3|Z|+2e(Z)-11|T| >= 0 ?"""
    vm = [0] * n
    for j, e in enumerate(E):
        for v in e:
            vm[v] |= 1 << j
    memo = {}
    for mask in range(1, (1 << n) - 1):
        F = 0; z = 0
        for v in range(n):
            if (mask >> v) & 1:
                F |= vm[v]; z += 1
        if F not in memo:
            memo[F] = tau_bb([E[j] for j in range(len(E)) if (F >> j) & 1])
        if 3 * z + 2 * bin(F).count('1') - 11 * memo[F] >= 0:
            return True
    return False


def red_closure(n, E):
    """Theorem 1: exists nonempty T with cl(T) != V and w(T) >= 0, or cl(T) = V and w(T) >= 3."""
    vm = [0] * n
    for j, e in enumerate(E):
        for v in e:
            vm[v] |= 1 << j
    for k in range(1, n + 1):
        for T in itertools.combinations(range(n), k):
            Ts = set(T)
            ET = [j for j, e in enumerate(E) if Ts & set(e)]
            ETm = 0
            for j in ET:
                ETm |= 1 << j
            cl = [v for v in range(n) if (vm[v] & ~ETm) == 0]
            w = 3 * len(cl) + 2 * len(ET) - 11 * k
            if len(cl) != n and w >= 0:
                return True
            if len(cl) == n and w >= 3:
                return True
    return False


def check_B():
    tot = 0; agree = 0
    for n in range(5, 10):
        for E in read_census(n):
            nn = 1 + max(v for e in E for v in e)
            assert nn == n
            a = red_bruteforce(n, E); b = red_closure(n, E)
            tot += 1; agree += (a == b)
            assert a == b, ('Theorem 1 mismatch', E)
    # random linear 3-graphs (not nec. in C), Delta <= 3, n <= 10, no isolated vertices
    rtot = 0
    for _ in range(300):
        n = random.randint(4, 10)
        E = []
        for _t in range(60):
            e = tuple(sorted(random.sample(range(n), 3)))
            if e in E:
                continue
            if any(len(set(e) & set(f)) > 1 for f in E):
                continue
            deg = [sum(1 for f in E if v in f) for v in range(n)]
            if any(deg[v] >= 3 for v in e):
                continue
            E.append(e)
        used = sorted(set(v for e in E for v in e))
        if len(used) < 2:
            continue
        rel = {v: i for i, v in enumerate(used)}
        E2 = [tuple(rel[v] for v in e) for e in E]
        n2 = len(used)
        a = red_bruteforce(n2, E2); b = red_closure(n2, E2)
        assert a == b, ('Theorem 1 mismatch (random)', E2)
        rtot += 1
    print('(B) Theorem 1: closure form = brute force on %d census graphs (5 <= n <= 9) and %d random linear Delta<=3 3-graphs' % (tot, rtot))


def check_C():
    tot = 0; tot_rand = 0; special = 0; minslackgap = None
    for n in range(5, 12):
        for E in read_census(n):
            m = len(E)
            deg = [0] * n
            for e in E:
                for v in e:
                    deg[v] += 1
            t = tau_bb(E)
            s = 3 * n + 2 * m - 11 * t
            Ss = [set(v for v in range(n) if deg[v] == 3)]
            for _ in range(2):
                # random S containing enough vertices so that H-S has max degree <= 2
                S = set(v for v in range(n) if deg[v] == 3 and random.random() < 0.5)
                for v in range(n):
                    if deg[v] == 3 and v not in S:
                        # must drop an edge at v: add a random co-vertex of v
                        pass
                S2 = set(S)
                for v in range(n):
                    if v in S2 or deg[v] < 3:
                        continue
                    d_rem = sum(1 for e in E if v in e and not (set(e) & S2))
                    if d_rem > 2:
                        nb = [u for e in E if v in e and not (set(e) & S2) for u in e if u != v]
                        S2.add(random.choice(nb))
                Ss.append(S2)
            for S in Ss:
                ES = [e for e in E if set(e) & S]
                rest = [v for v in range(n) if v not in S]
                Erest = [e for e in E if not (set(e) & S)]
                dr = {v: 0 for v in rest}
                for e in Erest:
                    for v in e:
                        dr[v] += 1
                if any(d > 2 for d in dr.values()):
                    continue
                n0 = sum(1 for v in rest if dr[v] == 0)
                n2 = sum(1 for v in rest if dr[v] == 2)
                rhs = 14 * len(ES) - 56 * len(S) + 21 * n0 + n2
                assert 7 * s >= rhs, ('Theorem 7 fails', E, S)
                tot += 1
            # special case
            S3 = [v for v in range(n) if deg[v] == 3]
            if not any(sum(1 for v in e if deg[v] == 3) >= 2 for e in E):
                n2H = sum(1 for v in range(n) if deg[v] == 2)
                assert 7 * s >= n2H - 20 * len(S3)
                special += 1
    print('(C) Theorem 7: %d (H,S) instances from census graphs n <= 11 (S = degree-3 set and random S); special case on %d graphs: all hold' % (tot, special))


def check_D():
    cnt = 0
    for G in nx.graph_atlas_g():
        if G.number_of_nodes() == 0 or G.number_of_nodes() > 6:
            continue
        if G.number_of_edges() and max(d for _, d in G.degree()) > 3:
            continue
        n, E = H_from_dual(G, 0)
        if n > 12:
            continue
        # map H-edge index -> G-node
        nodes = list(G.nodes())
        vm = [0] * n
        for j, e in enumerate(E):
            for v in e:
                vm[v] |= 1 << j
        for mask in range(1, 1 << n):
            Z = [v for v in range(n) if (mask >> v) & 1]
            F = 0
            for z in Z:
                F |= vm[z]
            W = [nodes[j] for j in range(len(E)) if (F >> j) & 1]
            t = tau_bb([E[j] for j in range(len(E)) if (F >> j) & 1])
            val = 3 * len(Z) + 2 * len(W) - 11 * t
            GW = G.subgraph(W)
            nuW = len(nx.max_weight_matching(GW, maxcardinality=True))
            EGW = set()
            for w in W:
                for x in G.neighbors(w):
                    EGW.add(frozenset((w, x)))
            assert val <= 11 * nuW - 3 * len(EGW), ('Lemma 2.2 fails', list(G.edges()), Z)
            cnt += 1
    print('(D) Lemma 2.2: %d (H, Z) instances (duals of all subcubic graphs on <= 6 vertices): all hold' % cnt)


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C', 'D']
    if 'A' in which: check_A()
    if 'D' in which: check_D()
    if 'B' in which: check_B()
    if 'C' in which: check_C()
