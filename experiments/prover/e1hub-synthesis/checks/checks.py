"""Judge's checks for the E1-hub synthesis (own code, see hyp.py).

S1  C10 re-check: no member of L* (32 pieces) has a hub triangle
    (x,y,z,v,b,c distinct; {x,y,z},{v,y,b},{v,z,c} edges; d(x)=1, d(y)=d(z)=d(v)=2).
    Positive control: the triangle (6,3,2) = {034,135,245} (three hub triangles expected).
S2  Degree-1 census and pendant b-configurations on stored near-tight lists (P2+ evidence).
S3  The L025 Theorem 12(a) residual on stored slack-8 lists: connected G'' with s = 8, three
    disjoint 2-sets A,B,C of avoided vertices of degree <= 2, none inside an edge, such that
    no (tau''+1)-transversal meets A, B and C (equivalently tau(G''-X) >= tau''-1 for all 8
    transversal triples X).  Any hit gives the I11 violator G''+pendants (+) hub with n''+7 vertices.
usage: python3 checks.py S1 <closure_results.json>
       python3 checks.py S2 <cell files...>
       python3 checks.py S3 <cell files...>
"""
import sys, json
from itertools import combinations
from hyp import read_cell, degrees, tau, all_min_transversals, is_linear


def hub_triangles(n, edges):
    d = degrees(n, edges)
    es = set(edges)
    inc = [[] for _ in range(n)]
    for e in edges:
        for u in e:
            inc[u].append(e)
    found = []
    for e0 in edges:
        for x in e0:
            if d[x] != 1:
                continue
            y, z = [u for u in e0 if u != x]
            if d[y] != 2 or d[z] != 2:
                continue
            fy = [f for f in inc[y] if f != e0][0]
            fz = [f for f in inc[z] if f != e0][0]
            common = set(fy) & set(fz)
            for v in common:
                if v in e0 or d[v] != 2:
                    continue
                b = [u for u in fy if u not in (v, y)][0]
                c = [u for u in fz if u not in (v, z)][0]
                if len({x, y, z, v, b, c}) == 6:
                    found.append((x, y, z, v, b, c))
    return found


def S1(path):
    data = json.load(open(path))
    pieces = data['pieces']
    tot = 0
    for p in pieces:
        edges = [tuple(sorted(e)) for e in p['edges']]
        ht = hub_triangles(p['n'], edges)
        tot += len(ht)
        print(p['name'], 'n', p['n'], 'm', len(edges), 'hub_triangles', len(ht))
    print('TOTAL hub triangles in', len(pieces), 'pieces:', tot)
    tri = [(0, 3, 4), (1, 3, 5), (2, 4, 5)]
    print('control triangle (6,3,2):', len(hub_triangles(6, tri)), 'hub triangles (expect 3)')


def nc_pairs(n, edges, mts):
    full = [False] * n
    co = set()
    for T in mts:
        vs = [u for u in range(n) if T >> u & 1]
        for p in combinations(vs, 2):
            co.add(p)
    return co


def S2(paths):
    for path in paths:
        cls = read_cell(path)
        hist = {}
        pend_b = 0
        for (n, edges, t) in cls:
            d = degrees(n, edges)
            ones = [u for u in range(n) if d[u] == 1]
            hist[len(ones)] = hist.get(len(ones), 0) + 1
            if len(ones) >= 3:
                tt, mts = all_min_transversals(n, edges)
                assert tt == t
                co = nc_pairs(n, edges, mts)
                edge_of = {}
                for e in edges:
                    for u in e:
                        edge_of.setdefault(u, []).append(e)
                for tr in combinations(ones, 3):
                    es = [edge_of[u][0] for u in tr]
                    if len(set(es)) < 3:
                        continue
                    if any(p in co for p in combinations(sorted(tr), 2)):
                        continue
                    pend_b += 1
        n0, m0, t0 = cls[0][0], len(cls[0][1]), cls[0][2] if cls else (0, 0, 0)
        print(path.split('/')[-1], 'classes', len(cls), 'slack', 3 * n0 + 2 * m0 - 11 * t0,
              'deg1-histogram', dict(sorted(hist.items())), 'pendant_b_configs', pend_b)


def connected(n, edges):
    par = list(range(n))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for e in edges:
        a, b, c = map(f, e)
        par[b] = a
        par[f(c)] = a
    return len({f(u) for u in range(n)}) == 1


def S3(paths):
    grand = 0
    for path in paths:
        cls = read_cell(path)
        hits = 0
        cand_total = 0
        for idx, (n, edges, t) in enumerate(cls):
            assert is_linear(edges)
            s = 3 * n + 2 * len(edges) - 11 * t
            assert s == 8, s
            if not connected(n, edges):
                continue
            tt, mts = all_min_transversals(n, edges)
            assert tt == t
            covered = 0
            for T in mts:
                covered |= T
            d = degrees(n, edges)
            U = [u for u in range(n) if not (covered >> u & 1) and d[u] <= 2]
            inedge = set()
            for e in edges:
                for p in combinations(e, 2):
                    inedge.add(p)
            # good 3-sets: contained in some (t+1)-transversal  <=> tau(G - X) <= t-2
            good = {}
            def is_good(X):
                X = tuple(sorted(X))
                if X not in good:
                    rm = sum(1 << u for u in X)
                    good[X] = tau(n, edges, removed=rm) <= t - 2
                return good[X]
            pairs = [p for p in combinations(U, 2) if p not in inedge]
            for P, Q, R in combinations(pairs, 3):
                if len(set(P) | set(Q) | set(R)) < 6:
                    continue
                cand_total += 1
                if not any(is_good((p, q, r)) for p in P for q in Q for r in R):
                    hits += 1
                    print('HIT', path.split('/')[-1], 'class', idx, 'A,B,C', P, Q, R)
        grand += hits
        print(path.split('/')[-1], 'classes', len(cls), 'candidate (A,B,C)', cand_total, 'hits', hits)
    print('TOTAL hits', grand)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'S1':
        S1(sys.argv[2])
    elif mode == 'S2':
        S2(sys.argv[2:])
    elif mode == 'S3':
        S3(sys.argv[2:])
