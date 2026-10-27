"""L027 tests of the exact transversal / slack statements of Part A and of J1 (own code).

Each test builds the modified graph explicitly and recomputes tau and membership in C by brute
force (hyp27.py).  Tested on random members of C (and on arbitrary random linear 3-graphs where the
statement does not need C).  Usage: python3 lemmas27.py <seed> <number of base graphs>
Counters: applicable configurations tested / failures.  Exit status 1 on any failure.
"""
import sys, random
from itertools import combinations
from hyp27 import (tau, min_transversals, tau_and_mts, popc, degrees, is_linear, has_F7,
                   p3_violations, in_C, e_inside, tight_sets_containing, components, slack,
                   adjacent, induced_minus, emask)

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
rng2 = random.Random(1000 + (int(sys.argv[1]) if len(sys.argv) > 1 else 1))
NBASE = int(sys.argv[2]) if len(sys.argv) > 2 else 200
cnt = {}
fail = {}


def ok(name, cond, info=None):
    cnt[name] = cnt.get(name, 0) + 1
    if not cond:
        fail[name] = fail.get(name, 0) + 1
        if fail[name] <= 3:
            print('FAIL', name, info)


def random_C(n, m, tries=200):
    for _ in range(tries):
        edges = []
        pairs = set()
        att = 0
        while len(edges) < m and att < 400:
            att += 1
            e = tuple(sorted(random.sample(range(n), 3)))
            ps = list(combinations(e, 2))
            if any(p in pairs for p in ps):
                continue
            cand = edges + [e]
            if has_F7(n, cand) or p3_violations(n, cand):
                continue
            edges = cand
            pairs.update(ps)
        if len(edges) == m:
            return edges
    return None


def random_C_rng(rng, n, m, tries=200):
    if m == 0:
        return []
    if n < 3:
        return None
    for _ in range(tries):
        edges = []
        pairs = set()
        att = 0
        while len(edges) < m and att < 400:
            att += 1
            e = tuple(sorted(rng.sample(range(n), 3)))
            ps = list(combinations(e, 2))
            if any(p in pairs for p in ps):
                continue
            cand = edges + [e]
            if has_F7(n, cand) or p3_violations(n, cand):
                continue
            edges = cand
            pairs.update(ps)
        if len(edges) == m:
            return edges
    return None


def nc(Ts, u, w):
    return not any((T >> u & 1) and (T >> w & 1) for T in Ts)


def cotrans(Ts, u):
    return any(T >> u & 1 for T in Ts)


def neighbours(edges, u):
    return {w for e in edges if u in e for w in e if w != u}


def test_graph(n, edges):
    t, Ts = min_transversals(n, edges)
    s = slack(n, len(edges), t)
    d = degrees(n, edges)
    V = list(range(n))
    es = set(edges)
    # ---------- Lemma 1 (hub) ----------
    tri = [X for X in combinations(V, 3) if X not in es]
    for (a, b, c) in random.sample(tri, min(4, len(tri))):
        v, x, y, z = n, n + 1, n + 2, n + 3
        H = edges + [tuple(sorted(f)) for f in ((x, y, z), (v, x, a), (v, y, b), (v, z, c))]
        th = tau(n + 4, H)
        two = any(popc(T & ((1 << a) | (1 << b) | (1 << c))) >= 2 for T in Ts)
        ok('L1 hub in C', in_C(n + 4, H), (edges, a, b, c))
        ok('L1 hub tau', th == t + (1 if two else 2), (edges, a, b, c))
    # ---------- Lemma 2 (fold) ----------
    for (a, b) in combinations(V, 2):
        if adjacent(edges, a, b):
            continue
        for c in V:
            if c in (a, b) or random.random() > 0.3:
                continue
            v, z = n, n + 1
            G2 = edges + [tuple(sorted((v, a, b))), tuple(sorted((v, z, c)))]
            ok('L2 fold in C', in_C(n + 2, G2), (edges, a, b, c))
            good = any((T >> c & 1) and (T & ((1 << a) | (1 << b))) for T in Ts)
            ok('L2 fold tau', tau(n + 2, G2) == t + (0 if good else 1), (edges, a, b, c))
    # ---------- Lemma 3 (pendant replacement) ----------
    for c in V:
        if not cotrans(Ts, c):
            continue
        for (a, b) in combinations([u for u in V if u != c], 2):
            if adjacent(edges, a, b) or not nc(Ts, a, c) or not nc(Ts, b, c):
                continue
            n1, e1, mp = induced_minus(n, edges, {c})
            w = n1
            Gp = e1 + [tuple(sorted((w, mp[a], mp[b])))]
            ok('L3 pendant-replacement in C', in_C(n1 + 1, Gp), (edges, a, b, c))
            tp = tau(n1 + 1, Gp)
            ok('L3 pendant-replacement tau', tp == t, (edges, a, b, c))
            ok('L3 slack', slack(n1 + 1, len(Gp), tp) == s + 2 - 2 * d[c])
    # ---------- Lemma 4 (identification) ----------
    for (x, y) in combinations(V, 2):
        for (p, q) in ((x, y), (y, x)):
            if not cotrans(Ts, p) or not nc(Ts, p, q) or adjacent(edges, p, q):
                continue
            if neighbours(edges, p) & neighbours(edges, q):
                continue
            # G_{p=q}: replace q by p, delete q
            img = [tuple(sorted(p if u == q else u for u in e)) for e in edges]
            n1, _, mp = induced_minus(n, [], {q})
            img2 = [tuple(sorted(mp[u] for u in e)) for e in img]
            ok('L4 identification linear', is_linear(img2), (edges, p, q))
            ti = tau(n1, img2)
            ok('L4 identification tau', ti == t, (edges, p, q))
            inC = in_C(n1, img2)
            f7 = has_F7(n1, img2, through=mp[p])
            ts = tight_sets_containing(n, edges, (1 << p) | (1 << q), minsize=3)
            ok('L4 membership iff (no F7 through x, no tight S>={x,y}, |S|>=3)',
               inC == (not f7 and not ts), (edges, p, q, inC, f7, ts))
    # ---------- Lemma 5 (move) ----------
    for x0 in V:
        if d[x0] != 1 or not cotrans(Ts, x0):
            continue
        ex = [e for e in edges if x0 in e][0]
        for x1 in ex:
            if x1 == x0:
                continue
            for (y, z) in combinations([u for u in V if u not in (x0, x1)], 2):
                if not nc(Ts, x0, y) or not nc(Ts, x0, z):
                    continue
                n1, e1, mp = induced_minus(n, edges, {x0})
                newe = tuple(sorted((mp[x1], mp[y], mp[z])))
                ok('L5 new edge is not an old edge', newe not in set(e1), (edges, x0, x1, y, z))
                M = e1 + [newe]
                ok('L5 move tau', tau(n1, M) == t, (edges, x0, x1, y, z))
    # ---------- Lemma 6 (edge on three avoided vertices) ----------
    av = [u for u in V if not cotrans(Ts, u)]
    for Y in combinations(av, 3):
        ok('L6 avoided triple not an edge', Y not in es)
        ok('L6 tau+1', tau(n, edges + [Y]) == t + 1, (edges, Y))
    # ---------- Lemma 7 (pendant edges on pairs) ----------
    pairs = list(combinations(V, 2))
    for k in (1, 2, 3):
        for _ in range(3):
            P = random.sample(pairs, k)
            if len({u for p in P for u in p}) != 2 * k:
                continue
            Fp = list(edges)
            for i, (p1, p2) in enumerate(P):
                Fp.append(tuple(sorted((p1, p2, n + i))))
            tf = tau(n + k, Fp)
            t2, Ts2 = tau_and_mts(n, edges, k)
            pred = min(popc(T) + sum(1 for (p1, p2) in P if not (T >> p1 & 1 or T >> p2 & 1)) for T in Ts2)
            ok('L7 tau formula', tf == pred, (edges, P))
            if all(not any(p1 in e and p2 in e for e in edges) for (p1, p2) in P):
                ok('L7 in C', in_C(n + k, Fp), (edges, P))
    # ---------- Lemma 8 ----------
    for u in av:
        n1, e1, _ = induced_minus(n, edges, {u})
        ok('L8a', slack(n1, len(e1), tau(n1, e1)) == s - 3 - 2 * d[u])
    for (x, y) in combinations(V, 2):
        for (p, q) in ((x, y), (y, x)):
            if cotrans(Ts, p) and nc(Ts, p, q):
                n1, e1, _ = induced_minus(n, edges, {p, q})
                t1 = tau(n1, e1)
                dd = sum(1 for e in edges if p in e or q in e)
                ok('L8b tau', t1 == t - 1)
                ok('L8b slack', slack(n1, len(e1), t1) == s + 5 - 2 * dd)
    # ---------- Lemma 9 ----------
    for (a, b, c) in combinations(V, 3):
        if (a, b, c) in es or min(d[a], d[b], d[c]) < 1:
            continue
        if not (nc(Ts, a, b) and nc(Ts, a, c) and nc(Ts, b, c)):
            continue
        for p in (a, b, c):
            if not cotrans(Ts, p):
                continue
            q, r = [u for u in (a, b, c) if u != p]
            n1, e1, _ = induced_minus(n, edges, {p, q})
            ok('L9 tau(G-a-b)', tau(n1, e1) == t - 1)
            n2, e2, _ = induced_minus(n, edges, {a, b, c})
            t2 = tau(n2, e2)
            ok('L9 tau(G-abc) in {t-2,t-1}', t2 in (t - 2, t - 1))
            dd = sum(1 for e in edges if set(e) & {a, b, c})
            if t2 == t - 1:
                ok('L9 drop-1 slack', slack(n2, len(e2), t2) == s + 2 - 2 * dd and dd >= 2)
    # ---------- gadget formula (Part D) ----------
    t3, Ts3 = tau_and_mts(n, edges, 1)
    for _ in range(4):
        P = random.sample(pairs, 3)
        if len({u for p in P for u in p}) != 6:
            continue
        (a1, a2), (b1, b2), (c1, c2) = P
        mA, mB, mC = (1 << a1) | (1 << a2), (1 << b1) | (1 << b2), (1 << c1) | (1 << c2)
        v, x, y, z, a, b, c = range(n, n + 7)
        gad = [(x, y, z), (v, x, a), (v, y, b), (v, z, c), (a, a1, a2), (b, b1, b2), (c, c1, c2)]
        Hg = edges + [tuple(sorted(f)) for f in gad]
        th = tau(n + 7, Hg)
        cond_i = all(not (T & (mA | mB | mC)) for T in Ts3 if popc(T) == t)
        cond_ii = not any(popc(T) == t + 1 and (T & mA) and (T & mB) and (T & mC) for T in Ts3)
        ok('gadget tau in {t+2,t+3,t+4}', th in (t + 2, t + 3, t + 4), (edges, P))
        ok('gadget tau = t+4 iff (i) and (ii)', (th == t + 4) == (cond_i and cond_ii), (edges, P))
    # ---------- J1 graph K + w(B,C) ----------
    for _ in range(4):
        P = random.sample(pairs, 2)
        if len({u for p in P for u in p}) != 4:
            continue
        (b1, b2), (c1, c2) = P
        w = n
        K2 = edges + [tuple(sorted((w, b1, b2))), tuple(sorted((w, c1, c2)))]
        tk = tau(n + 1, K2)
        both = any((T & ((1 << b1) | (1 << b2))) and (T & ((1 << c1) | (1 << c2))) for T in Ts)
        ok('J1 tau', tk == t + (0 if both else 1), (edges, P))
        if not any((b1 in e and b2 in e) or (c1 in e and c2 in e) for e in edges):
            ok('J1 linear', is_linear(K2))
            inC = in_C(n + 1, K2)
            ts = tight_sets_containing(n, edges, (1 << b1) | (1 << b2) | (1 << c1) | (1 << c2), 4)
            f7 = has_F7(n + 1, K2, through=w)
            ok('J1 membership iff (no tight S >= B u C, no F7 through w)', inC == (not ts and not f7))
            # the F7 shape
            def shape(B, C):
                for i in (0, 1):
                    bi, bo = B[i], B[1 - i]
                    for (cc1, cc2) in ((C[0], C[1]), (C[1], C[0])):
                        for e1 in edges:
                            if bi in e1 and cc1 in e1:
                                q = [u for u in e1 if u not in (bi, cc1)][0]
                                for e2 in edges:
                                    if bi in e2 and cc2 in e2:
                                        s2 = [u for u in e2 if u not in (bi, cc2)][0]
                                        if tuple(sorted((bo, q, s2))) in es:
                                            return True
                return False
            ok('J1 F7-through-w shape', f7 == (shape((b1, b2), (c1, c2)) or shape((c1, c2), (b1, b2))))
    # ---------- tight-set union ----------
    tsets = tight_sets_containing(n, edges, 0, minsize=3)
    for S1, S2 in combinations(tsets[:40], 2):
        if popc(S1 & S2) >= 2:
            U = S1 | S2
            ok('tight union', e_inside(edges, U) == popc(U) - 2)
    # ---- extra tests (separate random stream rng2, so the counts above are unchanged) ----
    # A12(b)-(d): largest tight set S_X containing a pair X; leaving edges; edges at vertices
    for S in tsets[:20]:
        vs = [u for u in range(n) if S >> u & 1]
        ok('A12(d) every vertex of a tight set lies in an edge inside it',
           all(any((emask(e) & S) == emask(e) and t in e for e in edges) for t in vs))
        X = (1 << vs[0]) | (1 << vs[1])
        SX = 0
        for S2 in tsets:
            if (S2 & X) == X:
                SX |= S2
        ok('A12(b) S_X tight', e_inside(edges, SX) == popc(SX) - 2)
        ok('A12(c) edges with >=2 vertices in S_X lie inside S_X',
           all(popc(emask(e) & SX) != 2 for e in edges))
    # Lemma Q identity: H = H1 + H2 + {p,q,c}
    H2 = None
    for _ in range(20):
        n2 = rng2.randint(1, 7)
        m2 = rng2.randint(0, max(0, n2 - 2))
        e2 = random_C_rng(rng2, n2, m2)
        if e2 is not None:
            H2 = (n2, e2)
            break
    if H2 is not None:
        n2, e2 = H2
        nonadj = [(p, q) for (p, q) in combinations(V, 2) if not adjacent(edges, p, q)]
        if nonadj:
            p, q = rng2.choice(nonadj)
            c = rng2.randrange(n2)
            sh = [tuple(sorted((u + n, w + n, z + n))) for (u, w, z) in e2]
            Hq = edges + sh + [tuple(sorted((p, q, c + n)))]
            tH = tau(n + n2, Hq)
            t2, Ts2 = min_transversals(n2, e2)
            ok('LemmaQ tau(H) in {t1+t2, t1+t2+1}', tH in (t + t2, t + t2 + 1))
            sH = slack(n + n2, len(Hq), tH)
            s1 = s
            s2 = slack(n2, len(e2), t2)
            if tH == t + t2:
                ok('LemmaQ first value: s(H) = s1+s2+2', sH == s1 + s2 + 2)
            else:
                miss1 = all(not (T >> p & 1 or T >> q & 1) for T in Ts)
                avoid2 = all(not (T >> c & 1) for T in Ts2)
                ok('LemmaQ second value: {p,q} missed by all min T of H1 and c avoided in H2', miss1 and avoid2)
                Hs = edges + [tuple(sorted((p, q, n)))]
                ts = tau(n + 1, Hs)
                ok('LemmaQ tau(H#) = t1+1', ts == t + 1)
                n3, e3, _ = induced_minus(n2, e2, {c})
                s3 = slack(n3, len(e3), tau(n3, e3))
                dc = sum(1 for e in e2 if c in e)
                ok('LemmaQ identity s(H) = s(H#) + s(H2-c) + 2 d(c)',
                   sH == slack(n + 1, len(Hs), ts) + s3 + 2 * dc)


nb = 0
while nb < NBASE:
    n = random.randint(5, 11)
    m = random.randint(1, max(1, n - 2))
    edges = random_C(n, m)
    if edges is None:
        continue
    nb += 1
    test_graph(n, edges)

for k in sorted(cnt):
    print(f'{k}: tested {cnt[k]}, failures {fail.get(k, 0)}')
print('BASE GRAPHS', NBASE, 'TOTAL FAILURES', sum(fail.values()))
sys.exit(1 if fail else 0)
