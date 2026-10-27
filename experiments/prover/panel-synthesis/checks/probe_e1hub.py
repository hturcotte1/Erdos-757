#!/usr/bin/env python3
"""Probe (not a verification): the E1-hub mechanism as a source of counterexamples to L021's KT^{L*}.
For each graph G' of the given stored cell lists with Delta <= 3 and A(G') <= 15, find every b-configuration
{a,b,c} (vertices of degree <= 2, not an edge, pairwise in no common minimum transversal), build
H = G' + E1-hub(a,b,c), keep H if it lies in C_3 (own membership code), and report A(H), DEF(H), P(H).
Uses L021's kt.py only for tau, minimum transversals and DEF (probe mode)."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/panel-synthesis/checks')
import kt
from check_k29 import linear, f7_free, p3_ok

pieces = [kt.Piece(p['edges'], p['name']) for p in json.load(open(
    '/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']]

def run(path):
    graphs = kt.read_cell(path)
    stats = dict(graphs=0, small_A=0, bconf=0, inC=0, negA=0, Pneg=0)
    for E in graphs:
        n = kt.nverts(E); m = len(E)
        deg = [0]*n
        for e in E:
            for x in e: deg[x] += 1
        if max(deg) > 3: continue
        stats['graphs'] += 1
        em = kt.masks(E); t = kt.tau_masks(em)
        A0 = kt.A_value(n, m, t)
        if A0 > 15: continue
        stats['small_A'] += 1
        T = kt.min_transversals(em, t)
        low = [x for x in range(n) if deg[x] <= 2]
        co = set()
        for x, y in itertools.combinations(low, 2):
            bxy = (1 << x) | (1 << y)
            if any((tr & bxy) == bxy for tr in T): co.add((x, y))
        Es = set(frozenset(e) for e in E)
        for a, b, c in itertools.combinations(low, 3):
            if (a, b) in co or (a, c) in co or (b, c) in co: continue
            if frozenset((a, b, c)) in Es: continue
            stats['bconf'] += 1
            v, x, y, z = n, n + 1, n + 2, n + 3
            EH = list(E) + [(x, y, z), (a, v, x), (b, v, y), (c, v, z)]
            nH = n + 4
            dH = [0]*nH
            for e in EH:
                for u in e: dH[u] += 1
            if max(dH) > 3 or not linear(EH) or not f7_free(EH, nH) or not p3_ok(EH, nH):
                continue
            stats['inC'] += 1
            tH = kt.tau_masks(kt.masks(EH))
            assert tH == t + 2, (path, E, a, b, c, tH, t)
            AH = kt.A_value(nH, len(EH), tH)
            if AH < 0:
                stats['negA'] += 1
                D = kt.deficiency(nH, EH, pieces, proper=False)
                P = AH + D
                print('  H', (nH, len(EH), tH), 'A', AH, 'DEF', D, 'P', P, 'from G\'', (n, m, t), 'A(G\')', A0,
                      'abc', (a, b, c), flush=True)
                if P < 0:
                    stats['Pneg'] += 1
                    print('  KT COUNTEREXAMPLE CANDIDATE', EH, flush=True)
    print(path.split('/')[-1], stats, flush=True)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        run(p)
