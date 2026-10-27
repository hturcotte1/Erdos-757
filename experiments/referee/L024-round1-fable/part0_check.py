"""Referee check of L024 C3 part 0 (Step 6.1, case (D1) with H - v = F): for every piece F of L* and every vertex v joined to F
by three edges whose six co-vertices all lie in F (three disjoint pairs of F-vertices of F-degree <= 2, no pair inside an edge of F),
count the configurations satisfying Claim B (no minimum transversal of F meets all three pairs) and test F + v for C_3.
Certificate: 74 Claim-B configurations, 0 in C_3.  Pairs are counted as unordered triples {P1,P2,P3} (no automorphism reduction
is applied here; the certificate's count is per labelled configuration as well, see pattern_a.py part 0 -- we report both the raw
count and the count up to Aut(F))."""
import sys, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L024-round1-fable')
from ref_lib import *
import networkx as nx
from networkx.algorithms import isomorphism as iso
t0 = time.time()
pieces = load_pieces()
tot_raw = 0; tot_orb = 0; tot_c3 = 0
for P in pieces:
    n, E = P['n'], P['edges']
    t = tau_brute(n, E); mts = min_transversals_brute(n, E, t); d = degrees(n, E)
    low = [x for x in range(n) if d[x] <= 2]
    inside = set()
    for e in E:
        for a, b in itertools.combinations(sorted(e), 2): inside.add((a, b))
    pairs = [(a, b) for a, b in itertools.combinations(low, 2) if (a, b) not in inside]
    hit = {}
    for p in pairs:
        bits = 0
        for i, T in enumerate(mts):
            if p[0] in T or p[1] in T: bits |= 1 << i
        hit[p] = bits
    sols = []
    for i, p1 in enumerate(pairs):
        for j in range(i + 1, len(pairs)):
            p2 = pairs[j]
            if set(p1) & set(p2): continue
            h12 = hit[p1] & hit[p2]
            for k in range(j + 1, len(pairs)):
                p3 = pairs[k]
                if set(p3) & (set(p1) | set(p2)): continue
                if h12 & hit[p3] == 0: sols.append((p1, p2, p3))
    # orbits under Aut(F): canonical form via networkx isomorphism between the extended graphs is expensive; use the automorphism group
    G = incidence_graph(n, E); nm = iso.categorical_node_match('kind', -1)
    auts = [tuple(phi[('v', x)][1] for x in range(n)) for phi in iso.GraphMatcher(G, G, node_match=nm).isomorphisms_iter()]
    seen = set(); norb = 0
    for s in sols:
        key = frozenset(frozenset(p) for p in s)
        if key in seen: continue
        norb += 1
        for a in auts:
            seen.add(frozenset(frozenset(a[x] for x in p) for p in s))
    c3 = 0
    for s in sols:
        EH = E + [tuple(sorted(p + (n,))) for p in s]
        ok, why = in_C3(n + 1, EH)
        if ok: c3 += 1; print('IN C3:', P['name'], s)
    tot_raw += len(sols); tot_orb += norb; tot_c3 += c3
    print(P['name'], 'claim-B configs (raw)', len(sols), 'up to Aut(F)', norb, '|Aut|', len(auts), 'in C3', c3, f'[{time.time()-t0:.0f}s]', flush=True)
print('TOTAL raw', tot_raw, 'up to Aut', tot_orb, 'in C3', tot_c3)
