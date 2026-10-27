#!/usr/bin/env python3
"""L026 check C2: reproduce the judge's E1-hub probe with own code and test the L026 lemmas on every hub.
For every connected Delta<=3 graph G' of the given stored cell lists with A(G') <= 15:
  - all b-configurations {a,b,c} (degree <= 2, not an edge, pairwise in no common minimum transversal);
  - H = G' (+) (a,b,c); check tau(H) = tau(G') + 2 (Lemma 1), H in C_3 (Lemma 2), A(H) = A(G') - 16;
  - record: are a, b, c each co-transversal in G' (Prop. 8(b) predicts yes in a minimal counterexample,
    here only reported), adjacency of the pairs, the fold H° = G' + v + z + {v,a,b} + {v,z,c} for every
    non-adjacent ordered split ({a,b} | c): H° in C_3 (Lemma 2(b)), tau(H°) = tau(G') + 1, A(H°) = A(H)+8,
    P(H°) >= 0, DEF(H°) <= 10 (Lemma 5);
  - P(H) = A(H) + DEF(H), DEF(G') <= 16 and DEF(G') <= 10 if n(G') >= 11 (Lemma 5, G' connected).
Usage: python3 check_hubs.py <cell files ...>"""
import sys, itertools, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L

pieces = L.load_pieces()

def run(path):
    graphs = L.read_found(path)
    st = dict(graphs=0, smallA=0, bconf=0, hubs_inC=0, Pneg=0, tau_formula_fail=0, inC_fail=0,
              lemma5_fail=0, nonco_vertex=0, folds=0, fold_fail=0, AH=[], case=[])
    for E in graphs:
        n = L.nv(E); m = len(E); d = L.degs(n, E)
        if max(d) > 3: continue
        if len(L.components(n, E)) != 1: continue
        st['graphs'] += 1
        t = L.tau(E); A0 = L.A_val(n, m, t)
        D0 = L.DEF(n, E, pieces)
        if D0 > 16 or (n >= 11 and D0 > 10): st['lemma5_fail'] += 1
        if A0 > 15: continue
        st['smallA'] += 1
        T = L.all_min_transversals(E, t)
        low = [x for x in range(n) if d[x] <= 2]
        cov = 0
        for tr in T: cov |= tr
        co = set()
        for x, y in itertools.combinations(low, 2):
            bm = (1 << x) | (1 << y)
            if any(tr & bm == bm for tr in T): co.add((x, y))
        Es = set(tuple(sorted(e)) for e in E)
        adj = set()
        for e in E:
            for p in itertools.combinations(sorted(e), 2): adj.add(p)
        for a, b, c in itertools.combinations(low, 3):
            if (a, b) in co or (a, c) in co or (b, c) in co: continue
            if (a, b, c) in Es: continue
            st['bconf'] += 1
            nH, EH = L.hub(n, E, a, b, c)
            if not L.in_C3(nH, EH): st['inC_fail'] += 1; continue
            st['hubs_inC'] += 1
            tH = L.tau(EH)
            if tH != t + 2: st['tau_formula_fail'] += 1
            AH = L.A_val(nH, len(EH), tH)
            assert AH == A0 - 16
            DH = L.DEF(nH, EH, pieces)
            PH = AH + DH
            if PH < 0: st['Pneg'] += 1
            st['AH'].append(AH)
            nonco = [w for w in (a, b, c) if not (cov >> w) & 1]
            if nonco: st['nonco_vertex'] += 1
            # folds
            for (p, q, r) in ((a, b, c), (a, c, b), (b, c, a)):
                if (min(p, q), max(p, q)) in adj: continue
                v, z = n, n + 1
                Ef = list(E) + [(v, p, q), (v, z, r)]
                nf = n + 2
                inC = L.in_C3(nf, Ef)
                tf = L.tau(Ef)
                Af = L.A_val(nf, len(Ef), tf)
                Df = L.DEF(nf, Ef, pieces)
                st['folds'] += 1
                if not inC or tf != t + 1 or Af != AH + 8 or Af + Df < 0 or Df > 10:
                    st['fold_fail'] += 1
                    print('  FOLD ANOMALY', (n, m, t), (p, q, r), inC, tf, Af, Df, flush=True)
            pairs_adj = sum(1 for (p, q) in ((a, b), (a, c), (b, c)) if (min(p, q), max(p, q)) in adj)
            print('  hub', (n, m, t), 'abc', (a, b, c), 'degs', (d[a], d[b], d[c]), 'adjacent pairs', pairs_adj,
                  'A(H)', AH, 'DEF(H)', DH, 'P(H)', PH, 'non-co-transversal among a,b,c:', nonco, flush=True)
    st['AH'] = sorted(set(st['AH']))
    del st['case']
    print(path.split('/')[-1], json.dumps(st), flush=True)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        run(p)
