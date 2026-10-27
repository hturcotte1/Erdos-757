"""Referee (L022, referee #2): independent test of Theorem 2 (sub-extension lemma) and of the L017 Theorem 4
facts it uses, with my own transversal code (bitmask branch and bound; all minimum transversals by
canonical DFS).  No import of e757, judge, hyp.py or lib22.

Part 1: F7 and the two (9,8,4) linear vertex-critical violators of L017 C3.
Part 2: random connected linear 3-graphs with Delta<=3 (own generator, own seeds); keep the vertex-critical
        violators (every proper induced subgraph has s>=0); check Theorem 2 at every degree-3 vertex.
Part 3: targeted constructions: random pieces F1, F2 glued by a degree-3 vertex in pattern (e), (f) or (b)
        (and random (c1)/(c2)/(d)); keep those that are vertex-critical violators; check Theorem 2.
usage: python3 -u t2.py seed trials_random trials_targeted
"""
import sys, random, itertools

def masks(E):
    return [sum(1 << x for x in e) for e in E]

def lb(rem):
    """greedy packing of pairwise disjoint edges: lower bound on tau."""
    used = 0; k = 0
    for e in rem:
        if not (e & used):
            used |= e; k += 1
    return k

def tau(em):
    if not em:
        return 0
    best = [len(em)]
    def rec(rem, k):
        if not rem:
            if k < best[0]: best[0] = k
            return
        if k + lb(rem) >= best[0]:
            return
        e = min(rem, key=lambda x: bin(x).count('1'))  # any uncovered edge
        for x in range(e.bit_length()):
            if (e >> x) & 1:
                rec([f for f in rem if not (f >> x) & 1], k + 1)
    rec(list(em), 0)
    return best[0]

def all_min_transversals(em, t=None):
    """all transversals of size t = tau as bitmasks; canonical DFS (first vertex of the branching edge in T)."""
    if t is None:
        t = tau(em)
    res = []
    def rec(rem, chosen, k, forb):
        if not rem:
            if k == t: res.append(chosen)
            return
        if k >= t or k + lb(rem) > t:
            return
        e = rem[0]
        tried = 0
        for x in range(e.bit_length()):
            if (e >> x) & 1:
                if not (forb >> x) & 1:
                    rec([f for f in rem if not (f >> x) & 1], chosen | (1 << x), k + 1, forb | tried)
                tried |= 1 << x
    rec(list(em), 0, 0, 0)
    return res, t

def slack(n, E):
    return 3 * n + 2 * len(E) - 11 * tau(masks(E))

def induced(E, S):
    S = set(S)
    return [e for e in E if all(x in S for x in e)]

def components(verts, E):
    par = {v: v for v in verts}
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in E:
        for x in e[1:]:
            a, b = find(e[0]), find(x)
            if a != b: par[a] = b
    comp = {}
    for v in verts:
        comp.setdefault(find(v), []).append(v)
    return [sorted(c) for c in comp.values()]

def is_linear(E):
    return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2))

def vertex_critical_violator(n, E):
    if slack(n, E) >= 0:
        return False
    V = list(range(n))
    for k in range(n - 1, 0, -1):
        for S in itertools.combinations(V, k):
            F = induced(E, S)
            if 3 * k + 2 * len(F) - 11 * tau(masks(F)) < 0:
                return False
    return True

def check_theorem2(n, E, verbose=False):
    """returns list of failure strings (empty = all claims hold) and pattern statistics."""
    fails = []; stats = {}
    s = slack(n, E); tH = tau(masks(E))
    deg = [0] * n
    for e in E:
        for x in e: deg[x] += 1
    for v in range(n):
        if deg[v] != 3:
            continue
        vedges = [e for e in E if v in e]
        pairs = [tuple(sorted(x for x in e if x != v)) for e in vedges]
        G = [e for e in E if v not in e]
        rest = [x for x in range(n) if x != v]
        comps = components(rest, G)
        cid = {x: i for i, c in enumerate(comps) for x in c}
        r = len(comps)
        # L017 Thm 4 (ii),(iii) basics
        tG = tau(masks(G))
        if tG != tH - 1: fails.append(('tau(G) != tau(H)-1', v))
        cs = [3 * len(c) + 2 * len(induced(G, c)) - 11 * tau(masks(induced(G, c))) for c in comps]
        if any(len(c) == 1 for c in comps): fails.append(('isolated vertex in G', v))
        if sum(cs) != s + 2: fails.append(('component slacks do not add to s+2', v))
        # (*) : no minimum transversal of G meets all three pairs
        Ts, _ = all_min_transversals(masks(G), tG)
        pm = [sum(1 << x for x in p) for p in pairs]
        if any(all(T & q for q in pm) for T in Ts): fails.append(('(*) fails', v))
        inside = [cid[p[0]] == cid[p[1]] for p in pairs]
        comps_of_pairs = [set(cid[x] for x in p) for p in pairs]
        if r == 1:
            pat = 'a'
        else:
            # (i): no component contains two pairs
            for i in range(r):
                if sum(1 for p, ins in zip(pairs, inside) if ins and cid[p[0]] == i) >= 2:
                    fails.append(('two pairs inside one component (pattern c1/c2/d)', v))
            if r >= 3: fails.append(('r >= 3', v))
            nin = sum(inside)
            if nin == 0: pat = 'b'
            elif nin == 1: pat = 'f'
            elif nin == 2: pat = 'e'
            else: pat = 'other'
        stats[pat] = stats.get(pat, 0) + 1
        if pat == 'e':
            fails.append(('pattern (e) occurs', v))
        if pat == 'f' and r == 2:
            j = inside.index(True); c1 = cid[pairs[j][0]]; c2 = 1 - c1
            F1, F2 = comps[c1], comps[c2]
            if not (cs[c1] == 1 and cs[c2] == 0 and s == -1):
                fails.append(('pattern (f) slacks', v, cs, s))
            # tight sub-extensions H[V(F1)+v+d], H[V(F1)+v+f]
            split = [p for p in pairs if cid[p[0]] != cid[p[1]]]
            for p in split:
                dd = p[0] if cid[p[0]] == c2 else p[1]
                Y = F1 + [v, dd]
                if 3 * len(Y) + 2 * len(induced(E, Y)) - 11 * tau(masks(induced(E, Y))) != 0:
                    fails.append(('pattern (f) sub-extension not tight', v))
            # (iv): F2 single edge, or d,f pendants of F2 in different edges
            F2E = induced(G, F2)
            ds = [p[0] if cid[p[0]] == c2 else p[1] for p in split]
            if len(F2) == 3 and len(F2E) == 1:
                pass
            else:
                dF2 = {x: sum(1 for e in F2E if x in e) for x in ds}
                share = any(set(ds) <= set(e) for e in F2E)
                if not (dF2[ds[0]] == 1 and dF2[ds[1]] == 1 and not share):
                    fails.append(('pattern (f)(iv) fails', v))
        if pat == 'b' and r == 2:
            for i in range(2):
                att = sorted(p[0] if cid[p[0]] == i else p[1] for p in pairs)
                FE = induced(G, comps[i])
                if tuple(att) in {tuple(sorted(e)) for e in FE}:
                    if not (len(comps[i]) == 3 and len(FE) == 1):
                        fails.append(('(v): attachment triple is an edge but component not single edge', v))
                # (vi): tight component not a single edge: >= 2 attachment vertices of component-degree 1
                if cs[i] == 0 and not (len(comps[i]) == 3):
                    d1 = sum(1 for x in att if sum(1 for e in FE if x in e) == 1)
                    if d1 < 2: fails.append(('(vi) fails', v))
            if all(len(c) == 3 for c in comps) and not (n == 7 and len(E) == 5):
                fails.append(('both single edges but H not 7/5', v))
        # (vii): degree-2 co-vertex w in F, edge {w,p,q} of F: {w,p},{w,q} not co-transversal in F
        for p in pairs:
            for w in p:
                if deg[w] != 2: continue
                F = comps[cid[w]]; FE = induced(G, F)
                gw = [e for e in FE if w in e]
                if len(gw) != 1: fails.append(('(vii) degree', v, w)); continue
                TsF, tF = all_min_transversals(masks(FE))
                for x in gw[0]:
                    if x == w: continue
                    if any((T >> w) & 1 and (T >> x) & 1 for T in TsF):
                        fails.append(('(vii) fails', v, w, x))
                # equivalent form: no minimum transversal of F-w contains p or q
                FwE = induced(G, [x for x in F if x != w])
                TsFw, tFw = all_min_transversals(masks(FwE))
                if tFw != tF - 1: fails.append(('(vii) tau(F-w)', v, w))
                for x in gw[0]:
                    if x != w and any((T >> x) & 1 for T in TsFw):
                        fails.append(('(vii) F-w form fails', v, w, x))
                stats['vii'] = stats.get('vii', 0) + 1
    return fails, stats

def rand_linear(rnd, n, m):
    E = []; deg = [0] * n; tries = 0
    while len(E) < m and tries < 3000:
        tries += 1
        e = tuple(sorted(rnd.sample(range(n), 3)))
        if any(deg[x] >= 3 for x in e) or any(len(set(e) & set(f)) > 1 for f in E) or e in E:
            continue
        E.append(e)
        for x in e: deg[x] += 1
    return E

def relabel_union(pieces):
    """disjoint union of pieces (n_i, E_i); returns (n, E, offsets)."""
    n = 0; E = []; off = []
    for ni, Ei in pieces:
        off.append(n); E += [tuple(x + n for x in e) for e in Ei]; n += ni
    return n, E, off

def main():
    seed = int(sys.argv[1]); TR = int(sys.argv[2]); TT = int(sys.argv[3])
    rnd = random.Random(seed)
    print('== Part 1: F7 and the two (9,8,4) violators')
    F7 = (7, [(0, 1, 6), (0, 4, 5), (1, 2, 3), (2, 4, 6), (3, 5, 6)])
    V1 = (9, [(0, 1, 2), (0, 3, 4), (1, 6, 7), (2, 5, 8), (3, 5, 7), (3, 6, 8), (4, 5, 6), (4, 7, 8)])
    V2 = (9, [(0, 1, 4), (0, 2, 3), (1, 7, 8), (2, 5, 6), (3, 5, 8), (3, 6, 7), (4, 5, 7), (4, 6, 8)])
    for name, (n, E) in [('F7', F7), ('V1(9,8,4)', V1), ('V2(9,8,4)', V2)]:
        print(name, 'linear', is_linear(E), 'tau', tau(masks(E)), 'slack', slack(n, E),
              'vertex-critical violator', vertex_critical_violator(n, E))
        fails, stats = check_theorem2(n, E)
        print('   Theorem 2 checks: patterns', stats, 'failures', fails)
    print('== Part 2: random linear Delta<=3 connected graphs, n in 7..11')
    st = dict(graphs=0, viol=0, vc=0, pat={}, fails=0); seen = set()
    for t in range(TR):
        n = rnd.randint(7, 11); m = rnd.randint(n // 2 + 1, n)
        E = rand_linear(rnd, n, m)
        if len({x for e in E for x in e}) < n or len(components(range(n), E)) != 1:
            continue
        st['graphs'] += 1
        if slack(n, E) >= 0: continue
        st['viol'] += 1
        key = tuple(sorted(E))
        if key in seen: continue
        seen.add(key)
        if not vertex_critical_violator(n, E): continue
        st['vc'] += 1
        fails, stats = check_theorem2(n, E)
        for k, v in stats.items(): st['pat'][k] = st['pat'].get(k, 0) + v
        if fails:
            st['fails'] += 1; print('FAIL', n, E, fails)
    print(st)
    print('== Part 3: targeted two-piece constructions (patterns e, f, b, c1, c2, d)')
    st = dict(built=0, viol=0, vc=0, pat={}, fails=0, bypat={})
    for t in range(TT):
        n1 = rnd.randint(3, 7); n2 = rnd.randint(3, 7)
        E1 = rand_linear(rnd, n1, rnd.randint(1, n1 - 1)); E2 = rand_linear(rnd, n2, rnd.randint(1, n2 - 1))
        if len({x for e in E1 for x in e}) < n1 or len({x for e in E2 for x in e}) < n2: continue
        if len(components(range(n1), E1)) != 1 or len(components(range(n2), E2)) != 1: continue
        n, E, off = relabel_union([(n1, E1), (n2, E2)])
        v = n; n += 1
        deg = [0] * n
        for e in E:
            for x in e: deg[x] += 1
        A1 = [x for x in range(n1) if deg[x] <= 2]; A2 = [x for x in range(n1, n1 + n2) if deg[x] <= 2]
        pat = rnd.choice(['e', 'f', 'b', 'c1', 'c2', 'd'])
        try:
            if pat == 'e':
                P1 = rnd.sample(A1, 2); P2 = rnd.sample(A2, 2)
                e_ = rnd.choice([x for x in A1 if x not in P1]); f_ = rnd.choice([x for x in A2 if x not in P2])
                pairs = [P1, P2, [e_, f_]]
            elif pat == 'f':
                P1 = rnd.sample(A1, 2); c_, e_ = rnd.sample([x for x in A1 if x not in P1], 2); d_, f_ = rnd.sample(A2, 2)
                pairs = [P1, [c_, d_], [e_, f_]]
            elif pat == 'b':
                xs = rnd.sample(A1, 3); ys = rnd.sample(A2, 3)
                pairs = [[xs[i], ys[i]] for i in range(3)]
            elif pat == 'c1':
                P1 = rnd.sample(A1, 2); P2 = rnd.sample([x for x in A1 if x not in P1], 2)
                e_ = rnd.choice([x for x in A1 if x not in P1 + P2]); f_ = rnd.choice(A2)
                pairs = [P1, P2, [e_, f_]]
            elif pat == 'c2':
                P1 = rnd.sample(A1, 2); P2 = rnd.sample([x for x in A1 if x not in P1], 2); P3 = rnd.sample(A2, 2)
                pairs = [P1, P2, P3]
            else:
                # (d): three components; add a third piece
                n3 = rnd.randint(3, 6); E3 = rand_linear(rnd, n3, rnd.randint(1, n3 - 1))
                if len({x for e in E3 for x in e}) < n3 or len(components(range(n3), E3)) != 1: continue
                n, E, off = relabel_union([(n1, E1), (n2, E2), (n3, E3)]); v = n; n += 1
                deg = [0] * n
                for e in E:
                    for x in e: deg[x] += 1
                A1 = [x for x in range(n1) if deg[x] <= 2]; A2 = [x for x in range(n1, n1 + n2) if deg[x] <= 2]
                A3 = [x for x in range(n1 + n2, n1 + n2 + n3) if deg[x] <= 2]
                P1 = rnd.sample(A1, 2); P2 = rnd.sample([x for x in A1 if x not in P1], 2)
                pairs = [P1, P2, [rnd.choice(A2), rnd.choice(A3)]]
        except (ValueError, IndexError):
            continue
        if any(any(set(p) <= set(e) for e in E) for p in pairs): continue
        H = E + [tuple(sorted([v] + list(p))) for p in pairs]
        if not is_linear(H): continue
        st['built'] += 1
        if slack(n, H) >= 0: continue
        st['viol'] += 1
        if not vertex_critical_violator(n, H): continue
        st['vc'] += 1; st['bypat'][pat] = st['bypat'].get(pat, 0) + 1
        fails, stats = check_theorem2(n, H)
        for k, val in stats.items(): st['pat'][k] = st['pat'].get(k, 0) + val
        if fails:
            st['fails'] += 1; print('FAIL', pat, n, H, fails)
    print(st)

if __name__ == '__main__':
    main()
