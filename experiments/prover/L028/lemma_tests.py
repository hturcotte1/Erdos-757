"""Random tests of the unconditional transversal identities used in L028.

T1  pendant replacement (L025 Lemma 3): c co-transversal, {a,c},{b,c} NC, a,b
    non-adjacent  =>  tau((G-c)+{w,a,b}) = tau(G); membership in C preserved.
T2  move (L025 Lemma 5): x co-transversal of degree 1 with edge {x,x1,x2},
    y,z not in {x,x1}, {x,y},{x,z} NC  =>  tau((G-x)+{x1,y,z}) = tau(G).
T3  the replacement Q of L028 Lemma 2: F a 3-graph, X,Y,Z pairwise disjoint
    2-sets, Z inside no edge, u in X avoided in F, w in Y co-transversal in F-u,
    every transversal of F meeting X,Y,Z has >= tau(F)+2 vertices
    =>  tau(Q) = tau(F) for Q = (F-u-w)+{t} u Z, and
        s(Q) = s(F) - 1 - 2|d(u,w)|  (|d| = number of edges meeting {u,w}).
T4  union/intersection of saturated sets meeting in >= 2 vertices (in C).
T5  the counting identity sum_{t in S}(3-d_{G[S]}(t)) = 6 for every saturated S.
All checks exact; graphs are random linear 3-graphs (seeded).
Usage: python3 lemma_tests.py <trials> <seed>
"""
import random
import sys
from itertools import combinations

from hyp28 import (tau, min_transversals, transversals_upto, popcount, slack,
                   in_C, is_linear, saturated_sets, degrees, adjacent, masks)


def random_linear(n, m, rng, maxdeg=3):
    edges = []
    deg = [0] * n
    tries = 0
    while len(edges) < m and tries < 4000:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        if any(deg[u] >= maxdeg for u in e):
            continue
        ok = True
        for f in edges:
            if len(set(e) & set(f)) >= 2:
                ok = False
                break
        if ok:
            edges.append(e)
            for u in e:
                deg[u] += 1
    return edges


def cotrans_vertices(n, mts):
    s = 0
    for T in mts:
        s |= T
    return s


def nc_pair(mts, p, q):
    bit = (1 << p) | (1 << q)
    return not any((T & bit) == bit for T in mts)


def run(trials, seed):
    rng = random.Random(seed)
    c = dict(T1=0, T1C=0, T2=0, T3=0, T3neg=0, T4=0, T5=0, graphs=0, inC=0)
    fails = []
    for it in range(trials):
        n = rng.randint(7, 12)
        m = rng.randint(n // 2, n - 2)
        edges = random_linear(n, m, rng)
        if not edges:
            continue
        c['graphs'] += 1
        t = tau(n, edges)
        mts = min_transversals(n, edges, t)
        cot = cotrans_vertices(n, mts)
        G_in_C = in_C(n, edges)
        c['inC'] += G_in_C
        deg = degrees(n, edges)
        # ---------------- T1 pendant replacement
        for cc in range(n):
            if not (cot >> cc) & 1:
                continue
            for a, b in combinations([x for x in range(n) if x != cc], 2):
                if adjacent(edges, a, b):
                    continue
                if not (nc_pair(mts, a, cc) and nc_pair(mts, b, cc)):
                    continue
                # G^p = (G - c) + {w,a,b}, w = new vertex n (keep labels, c isolated removed)
                keep = [u for u in range(n) if u != cc]
                mp = {u: i for i, u in enumerate(keep)}
                ne = [tuple(sorted(mp[x] for x in e)) for e in edges if cc not in e]
                w = len(keep)
                ne.append(tuple(sorted((mp[a], mp[b], w))))
                tp = tau(w + 1, ne)
                c['T1'] += 1
                if tp != t:
                    fails.append(('T1', n, edges, cc, a, b, t, tp))
                if G_in_C:
                    c['T1C'] += 1
                    if not in_C(w + 1, ne):
                        fails.append(('T1C', n, edges, cc, a, b))
        # ---------------- T2 move
        for x in range(n):
            if deg[x] != 1 or not (cot >> x) & 1:
                continue
            ex = [e for e in edges if x in e][0]
            others = [u for u in ex if u != x]
            for x1 in others:
                cand = [u for u in range(n) if u not in (x, x1) and nc_pair(mts, x, u)]
                for y, z in combinations(cand, 2):
                    keep = [u for u in range(n) if u != x]
                    mp = {u: i for i, u in enumerate(keep)}
                    ne = [tuple(sorted(mp[v] for v in e)) for e in edges if x not in e]
                    newe = tuple(sorted((mp[x1], mp[y], mp[z])))
                    if newe in ne:
                        continue
                    ne.append(newe)
                    tm = tau(len(keep), ne)
                    c['T2'] += 1
                    if tm != t:
                        fails.append(('T2', n, edges, x, x1, y, z, t, tm))
        # ---------------- T3 the replacement Q
        avoided = [u for u in range(n) if not (cot >> u) & 1]
        if avoided:
            trs = transversals_upto(n, edges, t + 1)
            verts = list(range(n))
            # choose three disjoint 2-sets X,Y,Z with u in X avoided
            for u in avoided:
                for xm in verts:
                    if xm == u:
                        continue
                    X = (u, xm)
                    rest = [v for v in verts if v not in X]
                    for Y in combinations(rest, 2):
                        rest2 = [v for v in rest if v not in Y]
                        for Z in combinations(rest2, 2):
                            if adjacent(edges, Z[0], Z[1]):
                                continue
                            bX = (1 << X[0]) | (1 << X[1])
                            bY = (1 << Y[0]) | (1 << Y[1])
                            bZ = (1 << Z[0]) | (1 << Z[1])
                            if any((T & bX) and (T & bY) and (T & bZ) for T in trs):
                                continue  # needs: every transversal meeting X,Y,Z has >= t+2
                            # F - u
                            keep = [v for v in range(n) if v != u]
                            mp = {v: i for i, v in enumerate(keep)}
                            Fu = [tuple(sorted(mp[v] for v in e)) for e in edges if u not in e]
                            tu = tau(len(keep), Fu)
                            mtu = min_transversals(len(keep), Fu, tu)
                            cotu = cotrans_vertices(len(keep), mtu)
                            for w in Y:
                                if not (cotu >> mp[w]) & 1:
                                    continue
                                keep2 = [v for v in range(n) if v not in (u, w)]
                                mp2 = {v: i for i, v in enumerate(keep2)}
                                Q = [tuple(sorted(mp2[v] for v in e)) for e in edges
                                     if u not in e and w not in e]
                                tt = len(keep2)
                                Q.append(tuple(sorted((mp2[Z[0]], mp2[Z[1]], tt))))
                                nQ = tt + 1
                                tq = tau(nQ, Q)
                                dd = sum(1 for e in edges if u in e or w in e)
                                c['T3'] += 1
                                if tq != t:
                                    fails.append(('T3tau', n, edges, X, Y, Z, u, w, t, tq))
                                sQ = 3 * nQ + 2 * len(Q) - 11 * tq
                                if sQ != slack(n, edges, t) - 1 - 2 * dd:
                                    fails.append(('T3slack', n, edges, X, Y, Z, u, w))
                                if sQ < 0:
                                    c['T3neg'] += 1
        # ---------------- T4, T5 saturated sets
        if G_in_C and n <= 12:
            sats = saturated_sets(n, edges)
            em = masks(edges)
            for S in sats:
                if max(deg) <= 3:
                    dS = [0] * n
                    for e in em:
                        if e & S == e:
                            for v in range(n):
                                if (e >> v) & 1:
                                    dS[v] += 1
                    tot = sum(3 - dS[v] for v in range(n) if (S >> v) & 1)
                    c['T5'] += 1
                    if tot != 6:
                        fails.append(('T5', n, edges, S, tot))
            for S1, S2 in combinations(sats, 2):
                I = S1 & S2
                if popcount(I) < 2:
                    continue
                U = S1 | S2
                eU = sum(1 for e in em if e & U == e)
                eI = sum(1 for e in em if e & I == e)
                c['T4'] += 1
                if eU != popcount(U) - 2 or eI != popcount(I) - 2:
                    fails.append(('T4', n, edges, S1, S2))
    return c, fails


if __name__ == '__main__':
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    c, fails = run(trials, seed)
    print('counts:', c)
    print('failures:', len(fails))
    for f in fails[:10]:
        print('  ', f)
