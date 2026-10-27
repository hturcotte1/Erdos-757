"""Lemma 11 on stored graphs with Delta <= 3 (n <= 17, brute-force saturated sets); Proposition 10's k = 2 configuration
is an F7; Step 0.8's inequality 11 nu(G) >= 3|E(G)| on random simple subcubic graphs (networkx matching, independent);
Theorem 5(d) size bound: no saturated set of size 4 or 5 in a linear 3-graph."""
import sys, itertools, random, collections
from ref import *
import networkx as nx

D = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
st = collections.Counter()
for c in ['10_7_4', '14_12_6', '17_13_7', '12_10_5', '15_11_6', '10_8_4', '13_9_5', '16_10_6', '8_5_3', '9_4_3', '6_3_2']:
    for (n, m, t, E) in read_cell(D + 'cell_%s.txt' % c, 40):
        V = set(range(n)); d = degrees(V, E)
        if max(d.values()) > 3:
            continue
        st['graphs'] += 1
        for S in saturated_sets(V, E):
            st['saturated_sets'] += 1
            ES = [e for e in E if e <= S]
            dS = degrees(S, ES)
            if sum(3 - dS[y] for y in S) != 6: st['L11a_fail'] += 1
            if any(dS[y] == 0 for y in S): st['L11b0_fail'] += 1
            if len(S) in (4, 5): st['size45_fail'] += 1
            for y in S:
                if dS[y] == 1 and len(S) >= 4:
                    S2 = S - {y}
                    if e_inside(E, S2) != len(S2) - 2: st['L11b1_fail'] += 1
            if all(dS[y] >= 2 for y in S):
                st['two_core'] += 1
                ports = [y for y in S if dS[y] == 2]
                if len(ports) != 6: st['L11c_ports_fail'] += 1
                for y in S:
                    if dS[y] == 3 and d[y] != 3: st['L11c_inside_fail'] += 1
                leaving = [e for e in E if (e & S) and not (e <= S)]
                if len(leaving) > 6: st['L11c_leaving_fail'] += 1
                if any(not (e & set(ports)) for e in leaving): st['L11c_port_fail'] += 1
print('Lemma 11 on stored graphs:', dict(st))

# Proposition 10, k = 2: the three edges at v plus two disjoint edges each taking one vertex of each pair form an F7
v, a, b, c, d_, e, f = range(7)
for choice in itertools.product([0, 1], repeat=3):
    P = [(a, b), (c, d_), (e, f)]
    g1 = frozenset(P[i][choice[i]] for i in range(3))
    g2 = frozenset(P[i][1 - choice[i]] for i in range(3))
    E = [frozenset((v,) + p) for p in P] + [g1, g2]
    assert len(f7_copies(E)) == 1, (choice, E)
print('Prop 10 (k=2 configuration is an F7): all 8 choices verified')

# Step 0.8: 11 nu >= 3 |E| for simple graphs with max degree <= 3
rng = random.Random(3); worst = None; bad = 0; cnt = 0
for _ in range(3000):
    n = rng.randint(2, 16)
    G = nx.Graph(); G.add_nodes_from(range(n))
    tries = 0
    target = rng.randint(1, 3 * n // 2)
    while G.number_of_edges() < target and tries < 500:
        tries += 1
        u, w = rng.sample(range(n), 2)
        if G.degree(u) < 3 and G.degree(w) < 3 and not G.has_edge(u, w):
            G.add_edge(u, w)
    nu = len(nx.max_weight_matching(G, maxcardinality=True))
    cnt += 1
    if 11 * nu < 3 * G.number_of_edges(): bad += 1
    r = 11 * nu - 3 * G.number_of_edges()
    if G.number_of_edges() > 0 and (worst is None or r < worst[0]): worst = (r, n, G.number_of_edges(), nu)
print('Step 0.8: 11nu >= 3|E| on', cnt, 'random subcubic graphs: failures', bad, '; smallest 11nu-3|E| (E>0):', worst)
# Step 0.8 tightness-ish: K4 has nu=2, |E|=6: 22 >= 18; the Petersen graph: nu=5, |E|=15: 55 >= 45
# Theorem 1 sanity: F7 and the (9,8,4) violators
F7 = [frozenset(x) for x in [(0,1,6),(0,4,5),(1,2,3),(2,4,6),(3,5,6)]]
t, Ts, co = cotransversal_vertices(F7)
print('F7: tau', t, 'slack', 3*7+2*5-11*t, 'co-transversal vertices', sorted(co), 'Delta', max(degrees(range(7), F7).values()))
for name, E in [('984a', [(0,1,2),(0,3,4),(1,6,7),(2,5,8),(3,5,7),(3,6,8),(4,5,6),(4,7,8)]),
                ('984b', [(0,1,4),(0,2,3),(1,7,8),(2,5,6),(3,5,8),(3,6,7),(4,5,7),(4,6,8)])]:
    E = [frozenset(x) for x in E]
    t, Ts, co = cotransversal_vertices(E)
    d = degrees(range(9), E)
    print(name, 'linear', is_linear(E), 'F7 copies', len(f7_copies(E)), 'P3', p3_brute(range(9), E)[0], 'tau', t, 'slack', 27+16-11*t,
          'co-transversal', len(co), 'Delta', max(d.values()), 'all s(K-x)=s+8-2d:',
          all(3*8+2*len([e for e in E if x not in e])-11*tau([e for e in E if x not in e]) == (27+16-11*t)+8-2*d[x] for x in range(9)))
