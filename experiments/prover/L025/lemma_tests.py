"""L025 lemma tests on the stored data (own code: hyp25.py).  Every assertion is a statement proved in
results/proofs/L025-e1hub-lemma-i11-form.md; the script checks it on every stored class (or on a stated sample).
Usage: python3 lemma_tests.py <test> [cells...]
  tests: hub      Theorem 1: tau(G (+) (a,b,c)) formula and membership in C, for triples of vertices of degree <= 2
         nc       Proposition 6 / pair lemma recheck, identification lemma (Lemma 4), K' gadget (Lemma 3.2), e-gadget (Lemma 2.2)
         crit     edge-criticality and (Red) facts on near-tight graphs (Lemma 3.1)
"""
import sys, random, time
from itertools import combinations
from hyp25 import *

NEAR = [(3,1,1),(10,7,4),(14,12,6),(17,13,7),(8,5,3),(12,10,5),(15,11,6),(19,16,8),(22,17,9),(26,22,11)]
SL2 = [(6,3,2),(9,4,3),(10,8,4),(13,9,5),(16,10,6),(20,15,8)]

def classes(cells, maxD=3):
    for (n, m, t) in cells:
        for k, (n0, m0, t0, E) in enumerate(load_cell(n, m, t)):
            h = Hyp(E, range(n0))
            if h.maxdeg() > maxD:
                continue
            yield (n, m, t), k, h

def two_of(h, a, b, c):
    ba, bb, bc = h.bit(a), h.bit(b), h.bit(c)
    for T in h.min_transversals():
        if ((T & ba) and (T & bb)) or ((T & ba) and (T & bc)) or ((T & bb) and (T & bc)):
            return True
    return False

def test_hub(cells, per_class=40, seed=1):
    rnd = random.Random(seed); cnt = 0; bad = 0
    for cell, k, h in classes(cells):
        low = [v for v in h.V if h.deg[v] <= 2]
        trs = list(combinations(low, 3))
        rnd.shuffle(trs)
        edges = set(frozenset(e) for e in h.E)
        for (a, b, c) in trs[:per_class]:
            E2, V2 = oplus(h.E, h.V, a, b, c)
            h2 = Hyp(E2, V2)
            pred = h.tau() + (1 if two_of(h, a, b, c) else 2)
            inC = h2.in_C()
            isedge = frozenset((a, b, c)) in edges
            cnt += 1
            if h2.tau() != pred or inC != (not isedge):
                bad += 1
                print('MISMATCH', cell, k, (a, b, c), h2.tau(), pred, inC, isedge)
    print('hub test: triples', cnt, 'mismatches', bad)

def common_nb(h, p, q):
    nb = neighbours(h.E, h.V)
    return bool(nb[p] & nb[q])

def test_nc(cells, near=True):
    t0 = time.time()
    stats = dict(nc=0, nc_nonadj=0, ident_ok=0, ident_inC=0, kprime=0, egad=0, egad_tight=0)
    blocks = {}
    for cell, k, h in classes(cells):
        s = h.slack(); tau = h.tau()
        cp = h.co_pairs()
        low = [v for v in h.V if h.deg[v] <= 2]
        allv = h.V
        # NC pairs among all vertices (any degree)
        ncp = [frozenset(p) for p in combinations(allv, 2) if frozenset(p) not in cp]
        for p in ncp:
            x, y = tuple(p)
            stats['nc'] += 1
            # Proposition 6 (pair lemma form) for vertices of degree <= 2 in near-tight graphs
            if near and h.deg[x] <= 2 and h.deg[y] <= 2:
                E2, V2 = delete(h.E, h.V, {x, y}); h2 = Hyp(E2, V2)
                dpart = h.deg[x] + h.deg[y] - (1 if p in h.sig else 0)
                assert h2.tau() == tau - 1, (cell, k, p)
                assert h2.slack() == s + 5 - 2 * dpart, (cell, k, p)
            # identification lemma
            if p in h.sig or common_nb(h, x, y):
                continue
            stats['nc_nonadj'] += 1
            E2, V2 = identify(h.E, h.V, x, y); h2 = Hyp(E2, V2)
            assert h2.tau() == tau, ('ident tau', cell, k, p)
            assert h2.slack() == s - 3, ('ident slack', cell, k, p)
            stats['ident_ok'] += 1
            inC = h2.in_C()
            if inC:
                stats['ident_inC'] += 1
                if near:
                    print('!!! identification of an NC pair of a near-tight graph lies in C:', cell, k, p)
            else:
                reason = []
                if not linear(h2.E): reason.append('nonlinear')
                if has_f7(h2.E): reason.append('F7')
                if not p3(h2.E, h2.V): reason.append('P3')
                key = (cell, tuple(sorted((h.deg[x], h.deg[y]))), tuple(reason))
                blocks[key] = blocks.get(key, 0) + 1
        ncset = set(ncp)
        # K' gadget and e-gadget: r with {p,r},{q,r} NC, p,q non-adjacent, p,q,r distinct
        for r in allv:
            partners = [u for u in allv if u != r and frozenset((u, r)) in ncset]
            for p, q in combinations(partners, 2):
                if frozenset((p, q)) in h.sig:
                    continue
                # e-gadget: G + {w,p,q} + {w,z,r}
                N = max(h.V) + 1; w, z = N, N + 1
                E3 = h.E + [tuple(sorted((w, p, q))), tuple(sorted((w, z, r)))]
                h3 = Hyp(E3, h.V + [w, z])
                assert h3.tau() == tau + 1, ('egad tau', cell, k, (r, p, q))
                assert h3.slack() == s - 1
                assert h3.in_C(), ('egad C', cell, k)
                stats['egad'] += 1
                if s == 0:
                    stats['egad_tight'] += 1
                    print('!!! e-configuration in a tight graph:', cell, k, (r, p, q))
                # K' gadget: (G - r) + {w,p,q}
                E4, V4 = delete(h.E, h.V, {r}); E4 = E4 + [tuple(sorted((N, p, q)))]
                h4 = Hyp(E4, V4 + [N])
                assert h4.tau() == tau, ('kprime tau', cell, k, (r, p, q))
                assert h4.slack() == s + 2 - 2 * h.deg[r], ('kprime slack', cell, k)
                assert h4.in_C(), ('kprime C', cell, k)
                stats['kprime'] += 1
                if near and h.deg[r] >= 2:
                    print('!!! K-prime gadget violates I11:', cell, k, (r, p, q))
    print('nc test', cells, stats, 'time %.1f' % (time.time() - t0))
    for key, v in sorted(blocks.items()):
        print('   identification blocked:', key, v)

def test_crit(cells):
    cnt = 0
    for cell, k, h in classes(cells):
        tau = h.tau()
        for g in h.E:
            E2 = [e for e in h.E if e != g]
            assert Hyp(E2, h.V).tau() == tau - 1, ('edge not critical', cell, k, g)
        pend = [v for v in h.V if h.deg[v] == 1]
        if h.n > 3:
            for x in pend:
                e = [f for f in h.E if x in f][0]
                for u in e:
                    if u != x:
                        assert h.deg[u] >= 2, ('pendant neighbour of degree 1', cell, k)
            # no vertex in two edges containing pendants (distinct pendant edges)
            pe = {}
            for x in pend:
                e = [f for f in h.E if x in f][0]
                for u in e:
                    if u != x:
                        pe.setdefault(u, set()).add(e)
            for u, es in pe.items():
                assert len(es) <= 1, ('vertex in two pendant edges', cell, k, u)
        cnt += 1
    print('crit test: classes', cnt, 'all edges critical; pendant facts hold')

if __name__ == '__main__':
    which = sys.argv[1]
    cells = NEAR
    if len(sys.argv) > 2 and sys.argv[2] == 'slack2':
        cells = SL2
    if which == 'hub':
        test_hub(cells)
    elif which == 'nc':
        test_nc(cells, near=(cells is NEAR))
    elif which == 'crit':
        test_crit(cells)
