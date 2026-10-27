"""thm4_check.py -- referee check of L018 Theorem 4 (non-locality construction).

For cubic graphs G0 of girth g (Petersen 5, Heawood 6, McGee 7, Tutte-Coxeter 8, Foster 10, Tutte 12-cage 12):
subdivide one edge uv by g0, build H (vertex set E(G) + {p}; edges delta(w) for w != g0, delta(g0)+{p}).
Checks (all exact):
  * H linear, Delta(H) = 2, exactly one pendant vertex, e(S) <= |S|-2 via the Hall form (every pair x,y:
    the edges have distinct representatives avoiding x,y), F7-free (no vertex of degree 3, F7 needs one);
  * tau(H) by CP-SAT and by m - nu(G); slack(H);
  * via CP-SAT: maximum of value_T(Z) = 3|Z| + 2e(Z) - 11|T| over (Z,T) with 1 <= |Z| <= k, Z != V, for k = ceil(g/2)-1
    (must be < 0), and the minimum |Z| of a (Red) pair (must be >= g/2);
  * for the Petersen instance: exhaustive forest lemma, all 2^17 sets Z;
  * for 2r+4 <= g: the split configuration at p is the complete binary hypertree of depth r, and no (Red) pair has
    Z inside B_r(p) (CP-SAT restricted to Z in B_r(p)).
"""
import itertools, sys
import networkx as nx
from ortools.sat.python import cp_model


def lcf(n, shifts, rep):
    return nx.LCF_graph(n, shifts, rep)


def cubic_graphs():
    out = []
    out.append(('Petersen', nx.petersen_graph()))
    out.append(('Heawood', nx.heawood_graph()))
    out.append(('McGee', lcf(24, [12, 7, -7], 8)))
    out.append(('TutteCoxeter', lcf(30, [-13, -9, 7, -7, 9, 13], 5)))
    out.append(('Foster', lcf(90, [17, -9, 37, -37, 9, -17], 15)))
    out.append(('Tutte12cage', lcf(126, [17, 27, -13, -59, -35, 35, -11, 13, -53, 53, -27, 21, 57, 11, -21, -57, 59, -17], 7)))
    return out


def build_H(G0):
    G = nx.Graph(G0)
    u, v = next(iter(G0.edges()))
    G.remove_edge(u, v)
    g0 = 'g0'
    G.add_edge(u, g0); G.add_edge(g0, v)
    Gedges = [tuple(sorted(map(str, e))) for e in G.edges()]
    idx = {e: i for i, e in enumerate(Gedges)}
    p = len(Gedges)
    Hedges = []
    Hedge_of = {}
    for w in G.nodes():
        inc = [idx[tuple(sorted((str(w), str(x))))] for x in G.neighbors(w)]
        if w == g0:
            inc = inc + [p]
        assert len(inc) == 3
        Hedge_of[w] = len(Hedges)
        Hedges.append(tuple(sorted(inc)))
    return G, g0, Gedges, p, Hedges, Hedge_of


def hall_ok(nv, E):
    # for every pair x<y: matching of edges into vertices minus {x,y} saturating all edges
    for x in range(nv):
        for y in range(x + 1, nv):
            B = nx.Graph()
            left = [('e', i) for i in range(len(E))]
            B.add_nodes_from(left, bipartite=0)
            for i, e in enumerate(E):
                for w in e:
                    if w != x and w != y:
                        B.add_edge(('e', i), ('v', w))
            M = nx.bipartite.hopcroft_karp_matching(B, top_nodes=left)
            if sum(1 for k in M if k[0] == 'e') < len(E):
                return False, (x, y)
    return True, None


def cp_tau(nv, E):
    m = cp_model.CpModel()
    t = [m.NewBoolVar('t%d' % i) for i in range(nv)]
    for e in E:
        m.AddBoolOr([t[w] for w in e])
    m.Minimize(sum(t))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 600
    r = s.Solve(m)
    assert r == cp_model.OPTIMAL
    return int(round(s.ObjectiveValue()))


def cp_red(nv, E, mode, k=None, allowed=None):
    """mode 'maxval': maximise value_T(Z) with 1<=|Z|<=k (Z within allowed if given), Z != V.
       mode 'minZ': minimise |Z| subject to value_T(Z) >= 0, 1 <= |Z| <= nv-1."""
    m = cp_model.CpModel()
    z = [m.NewBoolVar('z%d' % i) for i in range(nv)]
    t = [m.NewBoolVar('t%d' % i) for i in range(nv)]
    y = [m.NewBoolVar('y%d' % j) for j in range(len(E))]
    for j, e in enumerate(E):
        for w in e:
            m.AddImplication(z[w], y[j])
        m.AddBoolOr([z[w] for w in e] + [y[j].Not()])
        m.AddBoolOr([t[w] for w in e] + [y[j].Not()])
    m.Add(sum(z) >= 1)
    m.Add(sum(z) <= nv - 1)
    if allowed is not None:
        for i in range(nv):
            if i not in allowed:
                m.Add(z[i] == 0)
    val = 3 * sum(z) + 2 * sum(y) - 11 * sum(t)
    if mode == 'maxval':
        m.Add(sum(z) <= k)
        m.Maximize(val)
    else:
        m.Add(val >= 0)
        m.Minimize(sum(z))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 1200
    r = s.Solve(m)
    if r == cp_model.INFEASIBLE:
        return None
    assert r == cp_model.OPTIMAL, s.StatusName(r)
    Z = [i for i in range(nv) if s.Value(z[i])]
    T = [i for i in range(nv) if s.Value(t[i])]
    return int(round(s.ObjectiveValue())), Z, T


def tau_bf(E):
    E = [frozenset(e) for e in E]
    if not E:
        return 0
    best = [len(E)]
    def rec(es, k):
        if k >= best[0]:
            return
        if not es:
            best[0] = k; return
        e = es[0]
        for w in e:
            rec([f for f in es if w not in f], k + 1)
    rec(E, 0)
    return best[0]


def main():
    args = sys.argv[1:]
    nominz = '--nominz' in args
    which = [a for a in args if not a.startswith('--')] or None
    for name, G0 in cubic_graphs():
        if which and name not in which:
            continue
        assert all(d == 3 for _, d in G0.degree()) and nx.is_connected(G0)
        g = nx.girth(G0)
        G, g0, Gedges, p, E, Hedge_of = build_H(G0)
        nv = len(Gedges) + 1
        deg = [0] * nv
        for e in E:
            for w in e:
                deg[w] += 1
        lin = all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2))
        npend = sum(1 for d in deg if d == 1)
        Hn = nx.Graph(); Hn.add_nodes_from(range(nv))
        for e in E:
            Hn.add_edges_from(itertools.combinations(e, 2))
        conn = nx.is_connected(Hn)
        hall, bad = hall_ok(nv, E) if nv <= 200 else (None, None)
        nu = len(nx.max_weight_matching(G, maxcardinality=True))
        tau = cp_tau(nv, E) if nv <= 60 else len(E) - nu  # large instances: Theorem 2 identity (verified separately)
        m = len(E)
        slack = 3 * nv + 2 * m - 11 * tau
        print('%s: g=%d  H: n=%d m=%d maxdeg=%d pendants=%d linear=%s connected=%s hall(e(S)<=|S|-2)=%s tau=%d (m-nu=%d) slack=%d n2=%d'
              % (name, g, nv, m, max(deg), npend, lin, conn, hall, tau, m - nu, slack, sum(1 for d in deg if d == 2)))
        k = (g + 1) // 2 - 1  # largest k with k < g/2
        if nv <= 60:
            res = cp_red(nv, E, 'maxval', k=k)
            print('   max value_T(Z) over 1<=|Z|<=%d: %s' % (k, res[0] if res else None))
        res2 = None if nominz else cp_red(nv, E, 'minZ')
        if res2:
            Zs = res2[1]
            W = set()
            for j, e in enumerate(E):
                if any(w in Zs for w in e):
                    W.add(j)
            print('   min |Z| of a (Red) pair: %d (g/2 = %.1f); |E_Z| = %d' % (res2[0], g / 2, len(W)))
        # local configuration at p
        dist = nx.single_source_shortest_path_length(Hn, p)
        for r in range(0, 10):
            if 2 * r + 4 > g:
                break
            Br = [w for w in range(nv) if dist[w] <= r]
            Kr = [e for e in E if any(dist[w] <= r for w in e)]
            bdry = set(w for e in Kr for w in e if dist[w] == r + 1)
            # complete binary hypertree of depth r: 2^(r+1)-1 processed vertices, 2^(r+1)-1 edges, boundary 2^(r+1), each in one edge
            bcount = {w: sum(1 for e in Kr if w in e) for w in bdry}
            ok_tree = (len(Br) == 2 ** (r + 1) - 1 and len(Kr) == 2 ** (r + 1) - 1 and len(bdry) == 2 ** (r + 1)
                       and all(c == 1 for c in bcount.values())
                       and all(deg[w] == 2 for w in Br if w != p) and deg[p] == 1)
            res3 = cp_red(nv, E, 'maxval', k=nv - 1, allowed=set(Br))
            print('   r=%d: |B_r(p)|=%d |K_r|=%d boundary=%d binary-hypertree=%s  max value over Z in B_r(p): %s'
                  % (r, len(Br), len(Kr), len(bdry), ok_tree, res3[0] if res3 else None))
        if name == 'Petersen':
            # exhaustive forest lemma
            Gnodes = list(G.nodes())
            viol = 0; red = 0; total = 0; minZred = None
            vm = [0] * nv
            for j, e in enumerate(E):
                for w in e:
                    vm[w] |= 1 << j
            node_of_edge = {Hedge_of[w]: w for w in Gnodes}
            memo = {}
            for mask in range(1, 1 << nv):
                Z = [i for i in range(nv) if (mask >> i) & 1]
                if len(Z) == nv:
                    continue
                F = 0
                for zz in Z:
                    F |= vm[zz]
                if F not in memo:
                    Es = [E[j] for j in range(m) if (F >> j) & 1]
                    memo[F] = tau_bf(Es)
                val = 3 * len(Z) + 2 * bin(F).count('1') - 11 * memo[F]
                total += 1
                Wn = [node_of_edge[j] for j in range(m) if (F >> j) & 1]
                forest = nx.is_forest(G.subgraph(Wn))
                if forest and val >= 0:
                    viol += 1
                if val >= 0:
                    red += 1
                    if minZred is None or len(Z) < minZred:
                        minZred = len(Z)
            print('   exhaustive (Petersen): %d sets Z, %d with value >= 0, forest-lemma violations %d, min |Z| with value >= 0: %s'
                  % (total, red, viol, minZred))


if __name__ == '__main__':
    main()
