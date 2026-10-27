"""Referee L019: test Theorems 1-4, 6, Lemma 7 and Proposition 8 numerically in hereditary classes where minimal
counterexamples to I11 exist (the proofs of these statements use only heredity, linearity and Step 0.8, so they apply
verbatim to the class L of all linear 3-graphs (with F7 the first violator) and, except for parts using (P3), to
L' = linear + F7-free).
Part A (class L): enumerate all labelled linear 3-graphs on [n], n <= 7; check s >= 0 for n <= 6 (hypothesis N = 6);
  Theorem 1 at n = 7; Theorem 2(i)-(iii) for all K on <= 6 vertices and all k, all gadget pair choices with K+ in L;
  Theorem 2(iv) for all K on <= 6 vertices and all D, and on 7 vertices for all K with s < 0 and a sample;
  Theorems 3, 4, 6, Lemma 7 for all connected F on 6 vertices with s(F) <= 1 and all perfect matchings P with F+v in L.
Part B (class L'): the two (9,8,4) linear violators of L017 C3: check vertex-criticality, F7-freeness, Theorem 1,
  Theorem 2(iv), Theorem 3/4 at each degree-3 vertex with H-v connected, Lemma 7, Proposition 10 (exact min cover of
  the edges meeting Z), Theorem 5(c),(e)."""
import sys, os, itertools, collections, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import tau_bb, degrees, linear, f7_copies, components, fold, common_neighbours, adjacent

FAILS = []
STATS = collections.Counter()


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


def all_min_transversals(n, E, t):
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


def enum_linear(n):
    triples = list(itertools.combinations(range(n), 3))
    pairs_of = [frozenset(itertools.combinations(g, 2)) for g in triples]
    out = []

    def rec(start, used, cur):
        out.append(list(cur))
        for i in range(start, len(triples)):
            if used & pairs_of[i]:
                continue
            cur.append(triples[i])
            rec(i + 1, used | pairs_of[i], cur)
            cur.pop()
    rec(0, frozenset(), [])
    return out


def gadget(n, E, Qs):
    w = n
    return n + 1, E + [tuple(sorted((w,) + tuple(Q))) for Q in Qs]


def disjoint_pair_choices(n, k):
    pairs = list(itertools.combinations(range(n), 2))
    for Qs in itertools.combinations(pairs, k):
        if len(set(x for Q in Qs for x in Q)) == 2 * k:
            yield Qs


# ---------------- Part A ----------------
graphs = {}
for n in range(0, 8):
    graphs[n] = enum_linear(n)
    print('n =', n, 'labelled linear 3-graphs:', len(graphs[n]))
    sys.stdout.flush()

# hypothesis: I11 for all linear 3-graphs with <= 6 vertices
for n in range(0, 7):
    for E in graphs[n]:
        if s_of(n, E) < 0:
            fail('I11 fails in L on %d vertices: %s' % (n, E))
print('I11 on L for n <= 6 checked')

# Theorem 1 at n = 7 (N = 6)
viol7 = []
smin = 99
for E in graphs[7]:
    n = 7
    t = tau_small(n, E)
    s = s_of(n, E, t)
    smin = min(smin, s)
    if s < 0:
        viol7.append(E)
        d = degrees(n, E)
        if max(d) != 3:
            fail('Thm1 Delta != 3: %s' % E)
        if s not in (-1, -2):
            fail('Thm1 slack %d' % s)
        for x in range(n):
            Ex = [g for g in E if x not in g]
            # K - x relabelled
            lab = {u: i for i, u in enumerate([u for u in range(n) if u != x])}
            Ex2 = [tuple(lab[u] for u in g) for g in Ex]
            tx = tau_small(n - 1, Ex2)
            if tx != t - 1:
                fail('Thm1 vertex not co-transversal')
            if s_of(n - 1, Ex2, tx) != s + 8 - 2 * d[x]:
                fail('Thm1 slack bookkeeping')
print('Theorem 1 at n=7: min slack', smin, 'violators (labelled):', len(viol7))

# Theorem 2 (i)-(iii) with N = 6: K on <= 6 vertices
N = 6
for n in range(1, 7):
    for E in graphs[n]:
        t = tau_small(n, E)
        s = s_of(n, E, t)
        for k in (1, 2, 3):
            if 2 * k > n:
                continue
            for Qs in disjoint_pair_choices(n, k):
                n2, E2 = gadget(n, E, Qs)
                if not linear(E2):
                    continue
                d2 = degrees(n2, E2)
                cond_i = (n <= N - 1 and s <= 7 - 2 * k)
                cond_ii = (n == N and s <= 5 - 2 * k)
                cond_iii = (n == N and s <= 7 - 2 * k and max(d2) >= 4)
                if cond_i or cond_ii or cond_iii:
                    STATS['thm2_instances_k%d' % k] += 1
                    t2 = tau_small(n2, E2)
                    if t2 != t:
                        fail('Thm2 (i)-(iii) n=%d k=%d s=%d E=%s Q=%s' % (n, k, s, E, Qs))
                # sharpness bookkeeping: just outside the hypothesis
                elif n == N and s == 6 - 2 * k and max(d2) <= 3:
                    t2 = tau_small(n2, E2)
                    if t2 != t:
                        STATS['thm2_ii_boundary_failures_k%d' % k] += 1
print('Theorem 2 (i)-(iii) checked', dict(STATS))

# Theorem 2 (iv)
for n in range(1, 8):
    pool = graphs[n]
    if n == 7:
        rng = random.Random(1)
        pool = [E for E in graphs[7] if s_of(7, E) < 0] + rng.sample(graphs[7], min(3000, len(graphs[7])))
    for E in pool:
        t = tau_small(n, E)
        s = s_of(n, E, t)
        m = len(E)
        for r in range(1, m + 1):
            for D in itertools.combinations(range(m), r):
                ED = [E[i] for i in range(m) if i not in D]
                tD = tau_small(n, ED)
                bound = -((-(2 * r - s - (2 if n == N + 1 else 0))) // 11)  # ceil
                if tD > t - bound:
                    fail('Thm2(iv) n=%d E=%s D=%s' % (n, E, D))
                STATS['thm2iv_checks'] += 1
        if (n <= N and s <= 1) or (n == N + 1 and s < 0):
            for i in range(m):
                ED = [E[j] for j in range(m) if j != i]
                if tau_small(n, ED) != t - 1:
                    fail('Thm2(iv) edge not critical n=%d E=%s' % (n, E))
print('Theorem 2(iv) checks:', STATS['thm2iv_checks'])

# Theorems 3, 4, 6, Lemma 7 with F on 6 vertices (N = n_F = 6), class L
cnt = collections.Counter()
for E in graphs[6]:
    n = 6
    if len(components(n, E)) != 1:
        continue
    t = tau_small(n, E)
    s = s_of(n, E, t)
    if s > 1:
        continue
    cnt['F'] += 1
    Ts = all_min_transversals(n, E, t)
    dF = degrees(n, E)
    for P in disjoint_pair_choices(n, 3):
        nH, EH = gadget(n, E, P)
        if not linear(EH):
            continue
        cnt['admissible'] += 1
        v = n
        meets = lambda T, Q: bool(T >> Q[0] & 1 or T >> Q[1] & 1)
        c1 = any(all(meets(T, Q) for Q in P) for T in Ts)
        # Theorem 3
        for i, j in itertools.combinations(range(3), 2):
            if not any(meets(T, P[i]) and meets(T, P[j]) for T in Ts):
                fail('Thm3 pair-pair coverage fails F=%s P=%s' % (E, P))
        tH = tau_small(nH, EH)
        sH = s_of(nH, EH, tH)
        EHv = [g for g in EH if v not in g]
        cot_v = (tau_small(nH - 1, EHv) == tH - 1)
        # Theorem 4(a): (1) not c1, (2) tH = t+1, (3) v co-transversal, (4) sH < 0, (5) sH = s-2
        vals = [not c1, tH == t + 1, cot_v, sH < 0, sH == s - 2]
        if len(set(vals)) != 1:
            fail('Thm4(a) equivalence F=%s P=%s %s' % (E, P, vals))
        if c1 and sH != s + 9:
            fail('Thm4(a) otherwise-clause')
        if not c1:
            cnt['C1 fails'] += 1
            # Theorem 4(c)
            if max(dF) >= 4 or any(dF[x] >= 3 for Q in P for x in Q):
                fail('Thm4(c) degree condition violated by a failure')
            # Theorem 4(d)
            for i, j in itertools.combinations(range(3), 2):
                k = 3 - i - j
                Tij = [T for T in Ts if meets(T, P[i]) and meets(T, P[j])]
                if not Tij or any(meets(T, P[k]) for T in Tij):
                    fail('Thm4(d)')
                # Lemma 7
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
                                cnt['lemma7_instances'] += 1
                                Pi = [u for u in P[i] if T >> u & 1]
                                Pj = [u for u in P[j] if T >> u & 1]
                                if not (Pi == [y] or Pj == [y]):
                                    fail('Lemma 7')
            # Theorem 1 conclusions for H (n = 7 = N+1)
            dH = degrees(nH, EH)
            if max(dH) != 3:
                fail('H Delta')
            # Theorem 6 when s(F) = 0
            if s == 0:
                cnt['tight failures'] += 1
                if sH != -2:
                    fail('Thm6 sH')
                if min(dH) < 2 or max(dH) > 3:
                    fail('Thm6(a) degrees')
                n2 = sum(1 for x in range(nH) if dH[x] == 2)
                if n2 != 3 * (nH - len(EH)):
                    fail('Thm6(a) count')
                for x in range(nH):
                    if dH[x] != 2:
                        continue
                    ex = [g for g in EH if x in g]
                    A = [u for u in ex[0] if u != x]; B = [u for u in ex[1] if u != x]
                    for y in A:
                        for z in B:
                            adjx = adjacent(EH, y, z, avoid=x)
                            if dH[y] == 3 and dH[z] == 3 and not adjx:
                                fail('Thm6(b)')
                            if adjacent(EH, y, z):
                                continue
                            n2f, imgs, zeta = fold(nH, EH, x, y, z)
                            E2 = [tuple(sorted(g)) for g in imgs]
                            if linear(E2):
                                fail('Thm6(c)/5(e): fold in L for s=-2: %s x=%d y=%d z=%d' % (EH, x, y, z))
                            cnt['folds_checked'] += 1
                # Theorem 6(d)
                for i in range(3):
                    for x in P[i]:
                        if dH[x] != 2:
                            continue
                        ex = [g for g in E if x in g]
                        assert len(ex) == 1
                        pq = [u for u in ex[0] if u != x]
                        others = set(P[(i + 1) % 3]) | set(P[(i + 2) % 3])
                        for tv in pq:
                            if tv in others:
                                continue
                            if dH[tv] != 2:
                                fail('Thm6(d) degree')
                                continue
                            gt = [g for g in E if tv in g and x not in g]
                            assert len(gt) == 1
                            n2f, imgs, zeta = fold(nH, EH, x, v, tv)
                            E2 = [tuple(sorted(g)) for g in imgs]
                            blocked = not linear(E2)
                            pred = bool(set(gt[0]) & others)
                            if blocked != pred:
                                fail('Thm6(d) blocked criterion')
                            cnt['thm6d_instances'] += 1
print('Part A Theorems 3/4/6/Lemma 7:', dict(cnt))

# ---------------- Part B ----------------
G = {'984a': (9, [(0, 1, 2), (0, 3, 4), (1, 6, 7), (2, 5, 8), (3, 5, 7), (3, 6, 8), (4, 5, 6), (4, 7, 8)]),
     '984b': (9, [(0, 1, 4), (0, 2, 3), (1, 7, 8), (2, 5, 6), (3, 5, 8), (3, 6, 7), (4, 5, 7), (4, 6, 8)])}
for name, (n, E) in G.items():
    t = tau_small(n, E); s = s_of(n, E, t); d = degrees(n, E)
    print(name, 'n m tau s', n, len(E), t, s, 'degrees', d, 'linear', linear(E), 'F7 copies', len(f7_copies(E)))
    # vertex-critical: every proper induced subgraph has s >= 0
    vc = True
    for r in range(1, n + 1):
        for Z in itertools.combinations(range(n), r):
            keep = [u for u in range(n) if u not in Z]
            lab = {u: i for i, u in enumerate(keep)}
            EZ = [tuple(lab[u] for u in g) for g in E if not set(g) & set(Z)]
            if s_of(len(keep), EZ) < 0:
                vc = False
    print('  vertex-critical:', vc)
    # Theorem 1 conclusions
    for x in range(n):
        keep = [u for u in range(n) if u != x]; lab = {u: i for i, u in enumerate(keep)}
        Ex = [tuple(lab[u] for u in g) for g in E if x not in g]
        tx = tau_small(n - 1, Ex)
        if tx != t - 1 or s_of(n - 1, Ex, tx) != s + 8 - 2 * d[x]:
            fail('PartB Thm1 %s x=%d' % (name, x))
    # Theorem 2(iv): every edge critical
    for i in range(len(E)):
        if tau_small(n, [E[j] for j in range(len(E)) if j != i]) != t - 1:
            fail('PartB edge not critical')
    # degree-3 vertices
    for v in range(n):
        if d[v] != 3:
            continue
        keep = [u for u in range(n) if u != v]; lab = {u: i for i, u in enumerate(keep)}
        F = [tuple(lab[u] for u in g) for g in E if v not in g]
        P = [tuple(lab[u] for u in g if u != v) for g in E if v in g]
        conn = len(components(n - 1, F)) == 1
        tF = tau_small(n - 1, F); sF = s_of(n - 1, F, tF)
        Ts = all_min_transversals(n - 1, F, tF)
        meets = lambda T, Q: bool(T >> Q[0] & 1 or T >> Q[1] & 1)
        c1 = any(all(meets(T, Q) for Q in P) for T in Ts)
        pp = all(any(meets(T, P[i]) and meets(T, P[j]) for T in Ts) for i, j in itertools.combinations(range(3), 2))
        # Proposition 10
        W = set(x for Q in P for x in Q)
        Zset = W | {v}
        near = [g for g in E if set(g) & Zset]
        k = len([g for g in E if v not in g and set(g) & W])
        tnear = tau_small(n, near)
        ok10 = (k >= 3) and (11 * tnear >= 27 + 2 * k - s)
        print('  v=%d H-v connected %s s(F)=%d C1 holds %s pair-pair %s | Prop10: k=%d tau(near)=%d ok=%s'
              % (v, conn, sF, c1, pp, k, tnear, ok10))
        if c1 or not pp or not ok10 or sF != s + 2:
            fail('PartB degree-3 vertex %s v=%d' % (name, v))
    # Theorem 5(c),(e) for s = -1: every fold that is linear and F7-free has slack 0
    for x in range(n):
        if d[x] != 2:
            continue
        ex = [g for g in E if x in g]
        A = [u for u in ex[0] if u != x]; B = [u for u in ex[1] if u != x]
        for y in A:
            for z in B:
                if adjacent(E, y, z):
                    continue
                n2, imgs, zeta = fold(n, E, x, y, z)
                E2 = [tuple(sorted(g)) for g in imgs]
                s2 = s_of(n2, E2)
                if s2 != s + 1:
                    fail('PartB fold slack')
print('FAILURES:', len(FAILS))
