"""Referee L019, Part C: the class L' = linear + F7-free (hereditary; Theorems 1-4, Lemma 7, Proposition 10 use only
heredity, linearity, F7-freeness (Prop 10) and Step 0.8, so they apply verbatim to L').
1. Enumerate all labelled linear 3-graphs on 8 vertices; check that every F7-free one satisfies I11 (with the n <= 7
   enumeration of test_linear_analogue.py this gives the hypothesis 'I11 on L' up to N = 8').
2. For every connected F7-free F on 8 vertices with s(F) <= 1 (up to isomorphism) and every triple of disjoint pairs with
   H = F + v in L': Theorem 3, Theorem 4(a) equivalences, 4(c) degree conditions, 4(d), Lemma 7; for failures of C1:
   Theorem 1 conclusions for H (9 vertices), Theorem 2(iv) (edges critical), Theorem 6 if s(F) = 0, Proposition 10."""
import sys, os, itertools, collections
import networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import degrees, linear, f7_copies, components, fold, adjacent

FAILS = []
CNT = collections.Counter()


def fail(msg):
    FAILS.append(msg)
    if len(FAILS) <= 30:
        print('FAIL', msg)


def tau_small(n, E):
    ms = [sum(1 << x for x in g) for g in E]
    for k in range(0, n + 1):
        for T in itertools.combinations(range(n), k):
            tm = sum(1 << x for x in T)
            if all(e & tm for e in ms):
                return k


def min_transversals(n, E, t):
    ms = [sum(1 << x for x in g) for g in E]
    out = []
    for T in itertools.combinations(range(n), t):
        tm = sum(1 << x for x in T)
        if all(e & tm for e in ms):
            out.append(tm)
    return out


def s_of(n, E, t=None):
    if t is None:
        t = tau_small(n, E)
    return 3 * n + 2 * len(E) - 11 * t


n = 8
triples = list(itertools.combinations(range(n), 3))
pairs_of = [frozenset(itertools.combinations(g, 2)) for g in triples]
cands = []
total = 0


def rec(start, used, cur):
    global total
    total += 1
    E = list(cur)
    if not f7_copies(E):
        t = tau_small(n, E)
        s = 3 * n + 2 * len(E) - 11 * t
        if s < 0:
            fail('I11 fails in L\' on 8 vertices: %s' % E)
        if s <= 1 and len(E) >= 4 and len(components(n, E)) == 1:
            cands.append((E, t, s))
    for i in range(start, len(triples)):
        if used & pairs_of[i]:
            continue
        cur.append(triples[i])
        rec(i + 1, used | pairs_of[i], cur)
        cur.pop()


rec(0, frozenset(), [])
print('labelled linear 3-graphs on 8 vertices:', total, '; connected F7-free with s <= 1 (labelled):', len(cands))


def inc_graph(E):
    G = nx.Graph()
    for x in range(n):
        G.add_node(('v', x), b=0)
    for i, g in enumerate(E):
        G.add_node(('e', i), b=1)
        for x in g:
            G.add_edge(('v', x), ('e', i))
    return G


reps = []
buckets = collections.defaultdict(list)
for (E, t, s) in cands:
    G = inc_graph(E)
    h = nx.weisfeiler_lehman_graph_hash(G, node_attr='b')
    found = False
    for (E2, G2) in buckets[h]:
        if nx.is_isomorphic(G, G2, node_match=lambda a, b: a['b'] == b['b']):
            found = True
            break
    if not found:
        buckets[h].append((E, G))
        reps.append((E, t, s))
print('isomorphism classes of connected F7-free F on 8 vertices with s <= 1:', len(reps),
      [(len(E), t, s) for (E, t, s) in reps])

meets = lambda T, Q: bool(T >> Q[0] & 1 or T >> Q[1] & 1)
for (E, t, s) in reps:
    Ts = min_transversals(n, E, t)
    dF = degrees(n, E)
    for P in itertools.combinations(list(itertools.combinations(range(n), 2)), 3):
        if len(set(x for Q in P for x in Q)) != 6:
            continue
        v = n
        EH = E + [tuple(sorted((v,) + Q)) for Q in P]
        if not linear(EH) or f7_copies(EH):
            continue
        CNT['admissible triples'] += 1
        for i, j in itertools.combinations(range(3), 2):
            if not any(meets(T, P[i]) and meets(T, P[j]) for T in Ts):
                fail('Thm3 F=%s P=%s' % (E, P))
        c1 = any(all(meets(T, Q) for Q in P) for T in Ts)
        nH = n + 1
        tH = tau_small(nH, EH)
        sH = s_of(nH, EH, tH)
        tHv = tau_small(nH - 1, [g for g in EH if v not in g])
        vals = [not c1, tH == t + 1, tHv == tH - 1, sH < 0, sH == s - 2]
        if len(set(vals)) != 1:
            fail('Thm4(a) %s %s %s' % (E, P, vals))
        if c1:
            CNT['C1 holds'] += 1
            if sH != s + 9:
                fail('Thm4(a) otherwise')
            continue
        CNT['C1 fails (s(F)=%d)' % s] += 1
        if max(dF) >= 4 or any(dF[x] >= 3 for Q in P for x in Q):
            fail('Thm4(c)')
        dH = degrees(nH, EH)
        if max(dH) != 3 or sH not in (-1, -2):
            fail('Thm1 on H')
        for x in range(nH):
            keep = [u for u in range(nH) if u != x]; lab = {u: i for i, u in enumerate(keep)}
            Ex = [tuple(lab[u] for u in g) for g in EH if x not in g]
            tx = tau_small(nH - 1, Ex)
            if tx != tH - 1 or s_of(nH - 1, Ex, tx) != sH + 8 - 2 * dH[x]:
                fail('Thm1 co-transversal/bookkeeping on H')
        for i in range(len(EH)):
            if tau_small(nH, EH[:i] + EH[i + 1:]) != tH - 1:
                fail('Thm2(iv) edge not critical in H')
        for i, j in itertools.combinations(range(3), 2):
            k = 3 - i - j
            Tij = [T for T in Ts if meets(T, P[i]) and meets(T, P[j])]
            if not Tij or any(meets(T, P[k]) for T in Tij):
                fail('Thm4(d)')
            for T in Tij:
                for tv in P[k]:
                    for g in E:
                        if tv not in g:
                            continue
                        inter = [u for u in g if T >> u & 1]
                        if len(inter) != 1:
                            continue
                        y = inter[0]
                        priv = [h for h in E if [u for u in h if T >> u & 1] == [y]]
                        if priv == [g]:
                            CNT['lemma7 instances'] += 1
                            if not ([u for u in P[i] if T >> u & 1] == [y] or [u for u in P[j] if T >> u & 1] == [y]):
                                fail('Lemma 7')
        # Proposition 10 at v
        W = set(x for Q in P for x in Q)
        near = [g for g in EH if set(g) & (W | {v})]
        kk = len([g for g in E if set(g) & W])
        tn = tau_small(nH, near)
        CNT['prop10 (k,tau)=(%d,%d)' % (kk, tn)] += 1
        if kk < 3 or 11 * tn < 27 + 2 * kk - sH:
            fail('Prop 10')
        # Theorem 6 when s(F) = 0
        if s == 0:
            CNT['tight failures'] += 1
            if min(dH) < 2:
                fail('Thm6(a) degree')
            for x in range(nH):
                if dH[x] != 2:
                    continue
                ex = [g for g in EH if x in g]
                A = [u for u in ex[0] if u != x]; B = [u for u in ex[1] if u != x]
                for y in A:
                    for z in B:
                        if dH[y] == 3 and dH[z] == 3 and not adjacent(EH, y, z, avoid=x):
                            fail('Thm6(b)')
                        if adjacent(EH, y, z):
                            continue
                        n2, imgs, zeta = fold(nH, EH, x, y, z)
                        E2 = [tuple(sorted(g)) for g in imgs]
                        if linear(E2) and not f7_copies(E2):
                            fail('Thm6(c): fold in L\' for s = -2')
print(dict(CNT))
print('FAILURES:', len(FAILS))
