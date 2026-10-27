#!/usr/bin/env python3
"""Referee #3 (round 2) independent checks for L017.  Written from scratch; imports nothing from e757/, judge/ or
experiments/prover/.  Exact integer arithmetic only.

tau is decided by an exact branch-and-bound hitting-set decision procedure `has_cover(edges, k)`
(branch on an uncovered edge e={a,b,c}: take a | exclude a, take b | exclude a,b, take c; edges shrink when vertices
are excluded; disjoint-edge lower bound).  Co-transversality of X is decided by Fact 0.4: tau(F-X) == tau(F)-|X|.

Part A  (Remark 13.2 Property (P); Theorem 4(v),(vi) incl. the new F_2 side of (vi)(f), on the 13 tight Delta<=3 classes)
Part B  (Theorem 4(iii),(iv) and Theorem 6(ii) converse for ARBITRARY degree-3 extensions of disjoint unions of real
         class-C components of slack 0/1: the (iv) condition, evaluated on the components, is compared with
         tau(H') == tau(G)+1 computed directly on H'; non-deficient distributions must give tau(H') == tau(G)).
Usage: check_r2.py A | B <trials> <seed>
"""
import sys, os, re, random, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = os.path.join(HERE, 'cells', 'cells')


def load(name):
    out = []
    for l in open(os.path.join(CELLS, name)):
        if l.startswith('FOUND:'):
            out.append([tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)])
    return out


def has_cover(edges, k):
    """exact: is there a vertex set of size <= k meeting every edge (edges: list of frozensets, may be of size < 3)?"""
    edges = [e for e in edges]
    if not edges:
        return True
    if k <= 0:
        return False
    for e in edges:
        if len(e) == 0:
            return False
    # forced vertices (singleton edges)
    for e in edges:
        if len(e) == 1:
            (x,) = tuple(e)
            return has_cover([f for f in edges if x not in f], k - 1)
    # lower bound: greedy disjoint edges
    used = set(); lb = 0
    for e in sorted(edges, key=len):
        if not (e & used):
            used |= e; lb += 1
            if lb > k:
                return False
    # branch on a shortest edge, vertices ordered by degree
    e = min(edges, key=len)
    deg = {}
    for f in edges:
        for x in f:
            deg[x] = deg.get(x, 0) + 1
    order = sorted(e, key=lambda x: -deg[x])
    excluded = set()
    for x in order:
        rest = []
        ok = True
        for f in edges:
            if x in f:
                continue
            g = f - excluded
            if not g:
                ok = False; break
            rest.append(g)
        if ok and has_cover(rest, k - 1):
            return True
        excluded.add(x)
    return False


def tau(edges):
    es = [frozenset(e) for e in edges]
    k = 0
    while not has_cover(es, k):
        k += 1
    return k


def minus(edges, X):
    X = set(X)
    return [e for e in edges if not (set(e) & X)]


def cotrans(edges, X, t):
    """X co-transversal in the graph with edge list `edges` and tau t  (Fact 0.4)."""
    return has_cover([frozenset(e) for e in minus(edges, X)], t - len(X))


def degs(edges, verts):
    d = {v: 0 for v in verts}
    for e in edges:
        for x in e:
            d[x] += 1
    return d


def share(edges, x, y):
    return int(any(x in e and y in e for e in edges))


def partA():
    files = [('cell_3_1_1_D3.txt', 3), ('cell_10_7_4_D3.txt', 10), ('cell_14_12_6_D3.txt', 14), ('cell_17_13_7_D3.txt', 17)]
    tot_graphs = 0; types_all = {}; fail = []
    for fn, n in files:
        for gi, E in enumerate(load(fn)):
            tot_graphs += 1
            V = list(range(n)); m = len(E); t = tau(E); s = 3 * n + 2 * m - 11 * t
            assert s == 0, (fn, gi, s)
            d = degs(E, V)
            assert max(d.values()) <= 3 and min(d.values()) >= 1
            # vertex form of (U): every vertex co-transversal (s=0 < 3+2d)
            for x in V:
                if not cotrans(E, [x], t):
                    fail.append(('vertex', fn, gi, x))
            for x, y in itertools.combinations(V, 2):
                if cotrans(E, [x, y], t):
                    continue
                sig = share(E, x, y); dx, dy = sorted((d[x], d[y]))
                types_all.setdefault((fn, (dx, dy, sig)), 0); types_all[(fn, (dx, dy, sig))] += 1
                # pair lemma: 2|boundary| <= s+5 = 5
                bd = d[x] + d[y] - sig
                if 2 * bd > s + 5:
                    fail.append(('pairlemma', fn, gi, x, y))
                # Property (P) for classes with >= 10 vertices
                if n >= 10 and d[x] <= 2 and d[y] <= 2 and not (sig == 1 and (dx, dy) == (1, 2)):
                    fail.append(('P', fn, gi, x, y, dx, dy, sig))
                # Theorem 4(vi)(f), F_2 side, on attachment-eligible vertices (F-degree 1 or 2):
                if d[x] <= 2 and d[y] <= 2:
                    if d[x] == 2 and d[y] == 2:
                        fail.append(('vi_f_F2_both2', fn, gi, x, y))
                    if (d[x] == 2 or d[y] == 2) and sig != 1:
                        fail.append(('vi_f_F2_sigma', fn, gi, x, y))
    print('PART A: tight Delta<=3 graphs checked:', tot_graphs)
    for k in sorted(types_all):
        print('   non-co-transversal pair type', k, types_all[k])
    print('PART A failures:', len(fail), fail[:10])


def comp_lib():
    lib = []  # (name, slack, edges, n)
    for fn, n, s in [('cell_3_1_1_D3.txt', 3, 0), ('cell_10_7_4_D3.txt', 10, 0), ('cell_14_12_6_D3.txt', 14, 0),
                     ('cell_17_13_7_D3.txt', 17, 0), ('cell_8_5_3_D3.txt', 8, 1), ('cell_12_10_5_D3.txt', 12, 1),
                     ('cell_15_11_6_D3.txt', 15, 1)]:
        for gi, E in enumerate(load(fn)):
            lib.append(('%s#%d' % (fn[5:-7], gi), s, E, n))
    return lib


def partB(trials, seed):
    rng = random.Random(seed)
    lib = comp_lib()
    tight = [c for c in lib if c[1] == 0]; slack1 = [c for c in lib if c[1] == 1]
    small_tight = [c for c in tight if c[3] <= 10]
    stats = {}; fails = []
    done = 0; attempts = 0
    while done < trials and attempts < 50 * trials:
        attempts += 1
        r = rng.choice([1, 1, 2, 2, 2, 3, 3])
        comps = []
        use_s1 = rng.random() < 0.5
        for i in range(r):
            if use_s1 and i == 0:
                comps.append(rng.choice(slack1))
            else:
                comps.append(rng.choice(small_tight if (r == 3 or rng.random() < 0.5) else tight))
        if sum(c[3] for c in comps) > 34:
            continue
        # build G
        E = []; off = 0; compof = {}; Ecomp = []
        for ci, (name, s, ce, n) in enumerate(comps):
            ce2 = [tuple(v + off for v in e) for e in ce]
            E += ce2; Ecomp.append((ce2, list(range(off, off + n))))
            for v in range(off, off + n):
                compof[v] = ci
            off += n
        NG = off; dG = degs(E, range(NG))
        elig = [v for v in range(NG) if dG[v] in (1, 2)]
        # three disjoint pairs, not inside an edge of G, every component met
        ok = False
        for _ in range(200):
            if len(elig) < 6:
                break
            six = rng.sample(elig, 6)
            P = [tuple(six[0:2]), tuple(six[2:4]), tuple(six[4:6])]
            if any(share(E, a, b) and any(a in e and b in e for e in E) for a, b in P):
                continue
            if any(any(a in e and b in e for e in E) for a, b in P):
                continue
            met = set(compof[x] for p in P for x in p)
            if len(met) != r:
                continue
            ok = True; break
        if not ok:
            continue
        done += 1
        v = NG
        H = E + [(v,) + p for p in P]
        tG = sum(tau(ce) for ce, _ in Ecomp)
        tH = tau(H)
        assert tG <= tH <= tG + 1
        star = (tH == tG + 1)
        # Hall deficiency of the distribution
        Npair = [set(compof[x] for x in p) for p in P]
        def has_sdr():
            for perm in itertools.permutations(range(r), 3) if r >= 3 else []:
                if all(perm[j] in Npair[j] for j in range(3)):
                    return True
            return False
        deficient = not has_sdr()
        if not deficient:
            key = ('nondeficient', r)
            stats[key] = stats.get(key, [0, 0]); stats[key][0] += 1; stats[key][1] += int(star)
            if star:
                fails.append(('nondeficient_star', [c[0] for c in comps], P))
            continue
        # co-transversality oracle on components (Fact 0.4)
        ctau = [tau(ce) for ce, _ in Ecomp]
        def ct(X):
            ci = compof[X[0]]; assert all(compof[x] == ci for x in X)
            return cotrans(Ecomp[ci][0], X, ctau[ci])
        inside = [len(Npair[j]) == 1 for j in range(3)]
        cond = None; pat = None
        if r == 1:
            pat = 'a'
            cond = not any(ct([x, y, z]) for x in P[0] for y in P[1] for z in P[2])
        elif r == 2:
            sp = [j for j in range(3) if not inside[j]]
            ins = [j for j in range(3) if inside[j]]
            if len(sp) == 3:
                pat = 'b'
                X1 = [next(x for x in P[j] if compof[x] == 0) for j in range(3)]
                Y1 = [next(x for x in P[j] if compof[x] == 1) for j in range(3)]
                cond = (not any(ct([a, b]) for a, b in itertools.combinations(X1, 2)) and
                        not any(ct([a, b]) for a, b in itertools.combinations(Y1, 2)))
            elif len(sp) == 0:
                # {1,1,2} type: two pairs in one component, third in the other  -> (c2)
                pat = 'c2'
                c0 = [j for j in range(3) if compof[P[j][0]] == 0]; c1 = [j for j in range(3) if compof[P[j][0]] == 1]
                two = c0 if len(c0) == 2 else c1
                cond = not any(ct([x, y]) for x in P[two[0]] for y in P[two[1]])
            elif len(sp) == 1:
                cs = [compof[P[j][0]] for j in ins]
                if cs[0] == cs[1]:
                    pat = 'c1'
                    cond = not any(ct([x, y]) for x in P[ins[0]] for y in P[ins[1]])
                else:
                    pat = 'e'
                    j3 = sp[0]
                    # pair inside F_A together with the vertex of P3 in F_A, and symmetrically
                    cond = True
                    for j in ins:
                        cA = compof[P[j][0]]
                        z = next(x for x in P[j3] if compof[x] == cA)
                        if any(ct([x, z]) for x in P[j]):
                            cond = False
            else:  # len(sp) == 2: pattern (f)
                pat = 'f'
                j1 = ins[0]; cA = compof[P[j1][0]]; cB = 1 - cA
                ce_ = [next(x for x in P[j] if compof[x] == cA) for j in sp]
                df_ = [next(x for x in P[j] if compof[x] == cB) for j in sp]
                cond = (not any(ct([x, y]) for x in P[j1] for y in ce_)) and (not ct(df_))
        else:  # r == 3, deficient: two pairs inside one component, the third split over the other two -> (d)
            pat = 'd'
            ins = [j for j in range(3) if inside[j]]
            assert len(ins) == 2 and compof[P[ins[0]][0]] == compof[P[ins[1]][0]], (P, Npair)
            cond = not any(ct([x, y]) for x in P[ins[0]] for y in P[ins[1]])
        key = (pat, r)
        stats.setdefault(key, [0, 0, 0])
        stats[key][0] += 1; stats[key][1] += int(star); stats[key][2] += int(cond == star)
        if cond != star:
            fails.append(('equiv', pat, [c[0] for c in comps], P, cond, star))
        if star:
            sG = sum(3 * c[3] + 2 * len(c[2]) - 11 * tt for c, tt in zip(comps, ctau))
            sH = 3 * (NG + 1) + 2 * len(H) - 11 * tH
            if sH != sG - 2:
                fails.append(('slack', pat, sG, sH))
    print('PART B: extensions tested:', done, 'attempts', attempts)
    for k in sorted(stats):
        print('   ', k, 'count,star,(agree)' , stats[k])
    print('PART B failures:', len(fails), fails[:5])


if __name__ == '__main__':
    if sys.argv[1] == 'A':
        partA()
    else:
        partB(int(sys.argv[2]), int(sys.argv[3]))
