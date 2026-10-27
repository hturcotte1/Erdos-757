"""Numerical test of the combinatorial core of L024 Lemma 2 (independent of minimal counterexamples):
pieces F_1..F_k of L* (disjoint copies), k+1 'edges' (vertex sets each meeting V(X), with at most 2 vertices in any one
piece, as for edges of E*), Claim E on every nonempty subfamily Y (at least |Y|+1 of the edges meet V(Y)), and one rich
piece  ==>  minimum transversals T_F exist whose union meets every edge (i.e. Claim B FAILS).
Also records, for families with no rich piece, how often the conclusion fails (to see the test has teeth)."""
import random, sys
from itertools import combinations, product
import pattern_a_ref as R

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
names = list(R.P.keys())
rich = [x for x in names if x in R.RICH]
viol = 0; tested_rich = 0; tested_poor = 0; poor_B = 0
for it in range(N):
    k = random.randint(1, 3)
    withrich = random.random() < 0.6
    fam = [random.choice(names) for _ in range(k)]
    if withrich:
        fam[random.randrange(k)] = random.choice(rich)
    offs, nG = [], 0
    for nm in fam:
        offs.append(nG); nG += R.P[nm][0]
    mts = [[T << offs[i] for T in R.MT[nm][1]] for i, nm in enumerate(fam)]
    piece_of = []
    for i, nm in enumerate(fam):
        piece_of += [i] * R.P[nm][0]
    edges = []
    for _ in range(k + 1):
        while True:
            sz = random.randint(1, 3)
            S = random.sample(range(nG), sz)
            cnt = {}
            for x in S:
                cnt[piece_of[x]] = cnt.get(piece_of[x], 0) + 1
            if max(cnt.values()) <= 2:
                break
        edges.append(sum(1 << x for x in S))
    pm = [sum(1 << x for x in range(offs[i], offs[i] + R.P[nm][0])) for i, nm in enumerate(fam)]
    # Claim E for all nonempty subfamilies
    claimE = True
    for r in range(1, k + 1):
        for Y in combinations(range(k), r):
            vy = 0
            for i in Y:
                vy |= pm[i]
            if sum(1 for e in edges if e & vy) < r + 1:
                claimE = False
    if not claimE:
        continue
    # does some union of minimum transversals meet every edge?
    cover = False
    full = (1 << len(edges)) - 1
    pats = []
    for i in range(k):
        s = set()
        for T in mts[i]:
            p = 0
            for j, e in enumerate(edges):
                if T & e:
                    p |= 1 << j
            s.add(p)
        pats.append(s)
    for ps in product(*pats):
        acc = 0
        for p in ps:
            acc |= p
        if acc == full:
            cover = True
            break
    if any(x in R.RICH for x in fam):
        tested_rich += 1
        if not cover:
            viol += 1
            print('LEMMA 2 VIOLATION', fam, [bin(e) for e in edges])
    else:
        tested_poor += 1
        poor_B += (not cover)
print('tested (Claim E holds) with rich piece', tested_rich, 'violations', viol,
      '| without rich piece', tested_poor, 'of which Claim B holds', poor_B)
