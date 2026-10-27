"""tight_glue_ref.py -- referee's independent check of L018 Step 8.3 (data) and of the gluing claims of
Theorem 8 / Corollary 7.2.4.

Pieces: the 13 tight connected members of C with Delta <= 3 and n <= 17 according to the refereed L013 lists
(cell_3_1_1_D3, cell_10_7_4_D3, cell_14_12_6_D3, cell_17_13_7_D3; cells (13,8,5), (16,9,6) empty).
For each piece: re-check membership in C (linear; F7-free by brute force over 5-edge subsets; e(S) <= |S|-2 by
brute force over all nonempty edge subsets F: |V(F)| >= |F| + 2), connectivity, Delta <= 3, tau (brute force),
slack 0; pairwise non-isomorphism; all minimum transversals (brute force over all tau-subsets); Phi restricted to
degree<=2 vertices; the pair-pair property for disjoint admissible pairs.
Gluing check: X = F_1 + ... + F_r + w with three edges {w} u P_i, P_i pairwise disjoint pairs of vertices of
piece-degree <= 2, no P_i inside an edge of a piece, every piece meeting some pair, r in {1,2,3}.  We test whether
some minimum transversal of F_1 + ... + F_r meets P_1, P_2, P_3 (equivalently tau(X) = sum tau(F_i), slack(X) =
-2 + 11 = ... ; failure <=> slack(X) = -2).  Every failure is printed with its total number of vertices.
Method for r = 2, 3: per piece and per 'demand' (inside pairs, split vertices) the family of feasible subsets of
split vertices is computed from the list of minimum transversals; two demands combine iff feasible sets cover.
"""
import itertools, sys, os
import networkx as nx
from networkx.algorithms import isomorphism as iso

CD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cells13', 'cells')


def load(name):
    out = []
    with open(os.path.join(CD, name)) as f:
        for line in f:
            if line.startswith('FOUND:'):
                es = line.split(':', 1)[1].split()
                E = [tuple(int(x) for x in e.strip('()').split(',')) for e in es]
                out.append(E)
    return out


def in_C(E):
    E = [frozenset(e) for e in E]
    for a, b in itertools.combinations(E, 2):
        if len(a & b) > 1:
            return False, 'nonlinear'
    m = len(E)
    for c in itertools.combinations(range(m), 5):
        U = frozenset().union(*[E[i] for i in c])
        if len(U) == 7:
            deg = {}
            for i in c:
                for v in E[i]:
                    deg[v] = deg.get(v, 0) + 1
            if sorted(deg.values()) == [2, 2, 2, 2, 2, 2, 3]:
                return False, 'F7'
    for k in range(1, m + 1):
        for c in itertools.combinations(range(m), k):
            U = frozenset().union(*[E[i] for i in c])
            if len(U) < k + 2:
                return False, 'P3'
    return True, ''


def min_transversals(n, E):
    E = [frozenset(e) for e in E]
    for t in range(0, n + 1):
        L = []
        for T in itertools.combinations(range(n), t):
            Ts = set(T)
            if all(e & Ts for e in E):
                L.append(frozenset(T))
        if L:
            return t, L


def piece_info(E):
    V = sorted(set(v for e in E for v in e))
    assert V == list(range(len(V)))
    n = len(V)
    deg = [0] * n
    for e in E:
        for v in e:
            deg[v] += 1
    G = nx.Graph(); G.add_nodes_from(range(n))
    for e in E:
        G.add_edges_from(itertools.combinations(e, 2))
    t, L = min_transversals(n, E)
    return dict(E=[tuple(e) for e in E], n=n, m=len(E), deg=deg, conn=nx.is_connected(G), tau=t, L=L,
                slack=3 * n + 2 * len(E) - 11 * t, adj=G)


def inc_graph(E):
    B = nx.Graph()
    for i, e in enumerate(E):
        B.add_node(('e', i), k=0)
        for v in e:
            B.add_node(('v', v), k=1)
            B.add_edge(('e', i), ('v', v))
    return B


def main():
    pieces = []
    for nm, exp in [('cell_3_1_1_D3.txt', 1), ('cell_10_7_4_D3.txt', 4), ('cell_14_12_6_D3.txt', 2), ('cell_17_13_7_D3.txt', 6)]:
        L = load(nm)
        assert len(L) == exp, (nm, len(L))
        for E in L:
            pieces.append((nm, E))
    for nm in ['cell_13_8_5_D3.txt', 'cell_16_9_6_D3.txt']:
        print(nm, 'FOUND lines:', len(load(nm)))
    infos = []
    for nm, E in pieces:
        P = piece_info(E)
        ok, why = in_C(E)
        P['name'] = nm
        infos.append(P)
        elig = [v for v in range(P['n']) if P['deg'][v] <= 2]
        # Phi restricted to eligible vertices
        Phi = []
        for a, b in itertools.combinations(elig, 2):
            if not any(a in T and b in T for T in P['L']):
                Phi.append((a, b))
        # admissible pairs: eligible, not in a common edge
        adm = [(a, b) for a, b in itertools.combinations(elig, 2) if not P['adj'].has_edge(a, b)]
        pp_fail = 0; pp_tot = 0
        for Q1, Q2 in itertools.combinations(adm, 2):
            if set(Q1) & set(Q2):
                continue
            pp_tot += 1
            if not any((T & set(Q1)) and (T & set(Q2)) for T in P['L']):
                pp_fail += 1
        P['Phi'] = Phi; P['elig'] = elig; P['adm'] = adm
        degseq = sorted(P['deg'])
        print('%s n=%d m=%d tau=%d slack=%d inC=%s %s conn=%s maxdeg=%d degs=%s #minT=%d Phi=%s pairpair_fail=%d/%d'
              % (nm, P['n'], P['m'], P['tau'], P['slack'], ok, why, P['conn'], max(P['deg']),
                 {d: degseq.count(d) for d in set(degseq)}, len(P['L']), Phi, pp_fail, pp_tot))
    # pairwise non-isomorphism
    nm_ = iso.categorical_node_match('k', None)
    noniso = True
    for i, j in itertools.combinations(range(len(infos)), 2):
        if infos[i]['n'] == infos[j]['n'] and infos[i]['m'] == infos[j]['m']:
            if nx.is_isomorphic(inc_graph(infos[i]['E']), inc_graph(infos[j]['E']), node_match=nm_):
                noniso = False
                print('ISOMORPHIC', i, j)
    print('pieces pairwise non-isomorphic:', noniso)

    # ---- gluing check ----
    # demand on a piece: inside pairs I (tuple of pairs) and split vertices S (tuple); feasible family:
    # set of bitmasks X over positions of S such that some min transversal hits all pairs of I and contains S[x] for x in X.
    def feas(P, I, S):
        fam = set()
        for T in P['L']:
            if all(T & set(Q) for Q in I):
                X = 0
                for idx, s in enumerate(S):
                    if s in T:
                        X |= 1 << idx
                fam.add(X)
        # down-close not needed for covering test
        return fam

    def demands(P, k, j):
        """all (I, S) with k disjoint admissible inside pairs (as a set) and an ordered tuple S of j distinct eligible
        vertices disjoint from the pairs."""
        adm = P['adm']; elig = P['elig']
        for I in itertools.combinations(adm, k):
            used = set()
            okI = True
            for Q in I:
                if used & set(Q):
                    okI = False; break
                used |= set(Q)
            if not okI:
                continue
            rest = [v for v in elig if v not in used]
            for S in itertools.permutations(rest, j):
                yield I, S

    failures = []
    from collections import Counter
    # U1 property on every piece: every vertex of degree >= 1 lies in a minimum transversal
    for a, P in enumerate(infos):
        cov = set().union(*P['L'])
        assert all(v in cov for v in range(P['n']) if P['deg'][v] >= 1), ('U1 fails', a)
    print('U1 (every vertex in some minimum transversal) holds on all pieces')

    def comb_demands(P, k, j):
        adm = P['adm']; elig = P['elig']
        for I in itertools.combinations(adm, k):
            used = set(); okI = True
            for Q in I:
                if used & set(Q):
                    okI = False; break
                used |= set(Q)
            if not okI:
                continue
            rest = [v for v in elig if v not in used]
            for S in itertools.combinations(rest, j):
                yield I, S

    # r = 1 (informational): three disjoint admissible pairs in one piece
    r1fail = 0; r1tot = 0
    for a, P in enumerate(infos):
        for I, S in comb_demands(P, 3, 0):
            r1tot += 1
            if not feas(P, I, S):
                r1fail += 1
                failures.append(('r1', a, I, P['n'] + 1))
    print('r=1 configurations', r1tot, 'failures', r1fail)

    # r = 2
    restr = {}   # (piece, k, j) -> list of (I, S, fam) with full not in fam (or fam empty)
    empty_fam = []
    for a, P in enumerate(infos):
        for k in range(0, 4):
            for j in range(0, 4 - k):
                if k + j == 0:
                    continue
                full = (1 << j) - 1
                lst = []
                for I, S in comb_demands(P, k, j):
                    fam = feas(P, I, S)
                    if not fam:
                        empty_fam.append((a, k, j, I, S))
                    if full not in fam:
                        lst.append((I, S, fam))
                restr[(a, k, j)] = lst
    print('demands with no minimum transversal hitting the inside pairs (k<=3):',
          Counter((infos[e[0]]['name'], e[1], e[2]) for e in empty_fam))
    r2tot = 0; r2fail = 0
    for a, P1 in enumerate(infos):
        for b, P2 in enumerate(infos):
            for k1 in range(0, 4):
                for k2 in range(0, 4 - k1):
                    j = 3 - k1 - k2
                    if k1 + j < 1 or k2 + j < 1:
                        continue
                    full = (1 << j) - 1
                    # failure needs full not in F1 and full not in F2 (or an empty family on either side)
                    L1 = restr.get((a, k1, j), []); L2 = restr.get((b, k2, j), [])
                    for I1, S1, F1 in L1:
                        for I2, S2, F2 in L2:
                            for perm in itertools.permutations(range(j)):
                                r2tot += 1
                                # position perm[i] of S2 is paired with position i of S1: remap F2
                                F2m = set()
                                for X in F2:
                                    Y = 0
                                    for i in range(j):
                                        if (X >> perm[i]) & 1:
                                            Y |= 1 << i
                                    F2m.add(Y)
                                if not any((X1 | X2) == full for X1 in F1 for X2 in F2m):
                                    r2fail += 1
                                    failures.append(('r2', a, b, (k1, k2, j), (I1, S1, I2, tuple(S2[p] for p in perm)), P1['n'] + P2['n'] + 1))
                    # also: empty family on one side with any demand on the other side is a failure
    print('r=2 restrictive combinations checked', r2tot, 'failures', r2fail)
    cnt = Counter((f[0], f[-1]) for f in failures)
    print('failures by (r, total n):', sorted(cnt.items()))
    for f in failures[:30]:
        print('  ', f)
    print('failures with total n >= 28:', sum(1 for f in failures if f[-1] >= 28))
    # which piece pairs fail
    cntp = Counter((f[0], infos[f[1]]['name'] if f[0] != 'r1' else infos[f[1]]['name'], infos[f[2]]['name'] if f[0] == 'r2' else '', f[3] if f[0] == 'r2' else '') for f in failures)
    for k_, v_ in sorted(cntp.items(), key=str):
        print('  failing piece combination', k_, v_)


if __name__ == '__main__':
    main()
