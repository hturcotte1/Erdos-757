"""(D1) with H - v = F (L024 Step 6.1, C3 part 0): for every piece F of L*, all sets of three pairwise disjoint pairs
of vertices of F-degree <= 2, no pair inside an edge of F, such that no minimum transversal of F meets all three
pairs (Claim B for {F}); count raw and up to Aut(F); test F + v in C_3 (P3 must fail: n - m drops by 2)."""
from itertools import combinations
import pattern_a_ref as R
from rlib import degs, in_C3

raw = 0; orb = 0; inc3 = 0
for name, (n, E) in R.P.items():
    t, mts = R.MT[name]
    d = degs(n, E)
    inedge = set(p for e in E for p in combinations(e, 2))
    pairs = [(a, b) for a, b in combinations(range(n), 2) if d[a] <= 2 and d[b] <= 2 and (a, b) not in inedge]
    pm = {p: (1 << p[0]) | (1 << p[1]) for p in pairs}
    sols = []
    for A, B, C in combinations(pairs, 3):
        a, b, c = pm[A], pm[B], pm[C]
        if a & b or a & c or b & c:
            continue
        if not any((T & a) and (T & b) and (T & c) for T in mts):
            sols.append((A, B, C))
    R.orbits(name)
    auts = R.AUT[name]
    canon = set()
    for s in sols:
        best = None
        for g in auts:
            img = tuple(sorted(tuple(sorted((g[x], g[y]))) for x, y in s))
            if best is None or img < best:
                best = img
        canon.add(best)
    k_in = 0
    for s in sols:
        EH = list(E) + [tuple(sorted((n, x, y))) for x, y in s]
        if in_C3(n + 1, EH):
            k_in += 1
    raw += len(sols); orb += len(canon); inc3 += k_in
    if sols:
        print(name, 'raw', len(sols), 'up to Aut', len(canon), 'in C3', k_in)
print('PART0 raw', raw, 'up to Aut', orb, 'in C3', inc3)
