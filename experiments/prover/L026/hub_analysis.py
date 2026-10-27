"""L026 C7: structure of the stored E1-hubs (own code, ownlib.py only), testing Lemma 9 and the
minimality-free parts of Theorem 10 and recording the quantities that Theorem 10 constrains in a
minimal counterexample (stored hubs are NOT counterexamples: all have P(H) >= 0).
For every connected Delta<=3 graph G' (A(G') <= 15) of the given lists and every b-configuration {a,b,c}:
  * Lemma 9 on G', H, every fold and every component of H - a: the optimal family of a connected
    graph with DEF > 0 is a single piece or covers all vertices with (p-1)/2 connectors of size 3;
  * DEF(G'), A(G'), adjacency/degree pattern, the folds (A = A(H)+8) and their DEF,
    merges of non-adjacent pairs with d-sum <= 3 (blocked?), the components of H - a for outer
    vertices of G'-degree 2 (alpha/beta of Theorem 10(e)), and whether the optimal family of H has a
    member containing v.
Usage: python3 hub_analysis.py <cell files ...>"""
import sys, itertools, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L
pieces = L.load_pieces()
PW = {p.name: p for p in pieces}

def lemma9_ok(n, E, fam, D):
    """fam: list of (mask, name) attaining DEF D > 0 of the CONNECTED graph (n,E)."""
    if D <= 0: return True
    p = len(fam)
    U = 0
    for (Wm, nm) in fam: U |= Wm
    if p == 1 and U == (1 << n) - 1: return True
    if p % 2 == 0 or U != (1 << n) - 1: return False
    inside = 0
    for (Wm, nm) in fam: inside += PW[nm].m
    em = L.emasks(E)
    conn = [f for f in em if not any(f & Wm == f for (Wm, nm) in fam)]
    if len(conn) != (p - 1) // 2: return False
    for f in conn:
        hit = sum(1 for (Wm, nm) in fam if f & Wm)
        if hit != 3: return False
    return True

def defam(n, E):
    if not E: return 0, []
    return L.DEF(n, E, pieces, want=True)

def comp_graphs(n, E):
    out = []
    for C in L.components(n, E):
        Ei = L.induced(E, C)
        out.append((C, len(C), Ei))
    return out

def merge(n, E, x, y):
    lab = {}; k = 0
    for u in range(n):
        if u == y: continue
        lab[u] = k; k += 1
    lab[y] = lab[x]
    return n - 1, [tuple(sorted(lab[u] for u in e)) for e in E]

stats = dict(graphs=0, hubs=0, lemma9_checked=0, lemma9_fail=0, defG_pos=0, folds=0, folds_def_pos=0,
             merges_tested=0, merges_inC3=0, deg2_outer=0, alpha=0, beta=0, neither=0, famH_has_v=0,
             AH={}, pattern={})

def run(path):
    graphs = L.read_found(path) or L.read_flat(path)
    t0 = time.time()
    for E in graphs:
        n = L.nv(E); m = len(E); d = L.degs(n, E)
        if max(d) > 3 or len(L.components(n, E)) != 1: continue
        t = L.tau(E); A0 = L.A_val(n, m, t)
        if A0 > 15: continue
        stats['graphs'] += 1
        T = L.all_min_transversals(E, t)
        low = [x for x in range(n) if d[x] <= 2]
        co = set()
        for x, y in itertools.combinations(range(n), 2):
            bm = (1 << x) | (1 << y)
            if any(tr & bm == bm for tr in T): co.add((x, y))
        Es = set(tuple(sorted(e)) for e in E)
        adj = [set() for _ in range(n)]
        for e in E:
            for u in e:
                for w in e:
                    if u != w: adj[u].add(w)
        DG, famG = None, None
        for a, b, c in itertools.combinations(low, 3):
            if (a, b) in co or (a, c) in co or (b, c) in co or (a, b, c) in Es: continue
            nH, EH = L.hub(n, E, a, b, c)
            if not L.in_C3(nH, EH): continue
            if DG is None:
                DG, famG = defam(n, E)
                stats['lemma9_checked'] += 1
                if not lemma9_ok(n, E, famG, DG): stats['lemma9_fail'] += 1; print('L9FAIL G', E)
            stats['hubs'] += 1
            tH = t + 2
            assert L.tau(EH) == tH
            AH = A0 - 16
            DH, famH = defam(nH, EH)
            stats['lemma9_checked'] += 1
            if not lemma9_ok(nH, EH, famH, DH): stats['lemma9_fail'] += 1; print('L9FAIL H', EH)
            v = n
            if any(Wm >> v & 1 for (Wm, nm) in famH): stats['famH_has_v'] += 1
            stats['AH'][AH] = stats['AH'].get(AH, 0) + 1
            if DG > 0: stats['defG_pos'] += 1
            sig = {(p, q): (q in adj[p]) for p, q in ((a, b), (a, c), (b, c))}
            key = (tuple(sorted((d[a], d[b], d[c]))), sum(sig.values()))
            stats['pattern'][str(key)] = stats['pattern'].get(str(key), 0) + 1
            line = dict(G=(n, m, t), abc=(a, b, c), degs=(d[a], d[b], d[c]), adjpairs=sum(sig.values()),
                        AG=A0, DEFG=DG, AH=AH, DEFH=DH, folds=[], merges=[], deg2=[])
            # folds
            for (p, q, r) in ((a, b, c), (a, c, b), (b, c, a)):
                if q in adj[p]: continue
                vv, zz = n, n + 1
                Ef = list(E) + [(vv, p, q), (vv, zz, r)]
                nf = n + 2
                assert L.in_C3(nf, Ef)
                tf = L.tau(Ef); Af = L.A_val(nf, len(Ef), tf)
                assert tf == t + 1 and Af == AH + 8
                Df, famf = defam(nf, Ef)
                stats['folds'] += 1; stats['lemma9_checked'] += 1
                if not lemma9_ok(nf, Ef, famf, Df): stats['lemma9_fail'] += 1; print('L9FAIL fold', Ef)
                if Df > 0: stats['folds_def_pos'] += 1
                line['folds'].append(((p, q, r), Df, len(famf)))
            # merges for d-sum <= 3, non-adjacent
            for (p, q) in ((a, b), (a, c), (b, c)):
                if q in adj[p] or d[p] + d[q] > 3: continue
                stats['merges_tested'] += 1
                n2, E2 = merge(n, E, p, q)
                ok = L.in_C3(n2, E2)
                why = 'inC3' if ok else ('commonnbr' if adj[p] & adj[q] else ('F7' if L.is_linear(E2) and L.has_F7(n2, E2) else ('P3' if L.is_linear(E2) else 'nonlinear')))
                if ok:
                    stats['merges_inC3'] += 1
                    t2 = L.tau(E2); A2 = L.A_val(n2, len(E2), t2); D2 = L.DEF(n2, E2, pieces)
                    assert t2 == t
                    why += ' A=%d DEF=%d' % (A2, D2)
                line['merges'].append(((p, q), why))
            # degree-2 outer vertices: components of H - a
            for w in (a, b, c):
                if d[w] != 2: continue
                stats['deg2_outer'] += 1
                keep = [u for u in range(nH) if u != w]
                Ew = L.induced(EH, keep)
                comps = comp_graphs(len(keep), Ew)
                vi = keep.index(v)
                res = []
                hubpos = None; otherpos = False
                for (C, nc, Ec) in comps:
                    if len(Ec) == 0: res.append(('K1', 0)); continue
                    Dc, famc = defam(nc, Ec)
                    stats['lemma9_checked'] += 1
                    if not lemma9_ok(nc, Ec, famc, Dc): stats['lemma9_fail'] += 1; print('L9FAIL comp', Ec)
                    ishub = vi in C
                    res.append(('hub' if ishub else 'other', nc, Dc, len(famc)))
                    if Dc > 0:
                        if ishub: hubpos = True
                        else: otherpos = True
                if hubpos: stats['alpha'] += 1
                elif otherpos: stats['beta'] += 1
                else: stats['neither'] += 1
                line['deg2'].append((w, res))
            print(json.dumps(line), flush=True)
    print('#', path.split('/')[-1], 'done [%ds]' % (time.time() - t0), flush=True)

if __name__ == '__main__':
    for f in sys.argv[1:]: run(f)
    print('STATS', json.dumps(stats))
