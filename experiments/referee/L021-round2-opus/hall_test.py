"""Adversarial test of the Hall exchange in L021 Step 3.4 (and of the set identity
E*_H(S) = N_B(S) used in 8.1). Random host 3-graphs: vertex-disjoint 'members' (random
connected 3-graphs on 3..8 vertices) plus outside vertices plus random extra edges that
meet the members and lie inside no member. For X* = all members and EVERY nonempty
S subset of E*(X*) with |N_B(S)| < |S|: check E*(X') subset of E*(X*) minus S for X' = X* minus N_B(S),
the strict decrease of |E*| - |X|, and that X' empty forces |X*| < |S|. Also check, for
every subfamily S' of X*, that E*_H(S') equals the set of E*(X*)-edges meeting V(S')."""
import random, sys
from itertools import combinations

rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300


def estar(edges, members, fam):
    V = set().union(*[members[i] for i in fam]) if fam else set()
    return {j for j, e in enumerate(edges)
            if set(e) & V and not any(set(e) <= members[i] for i in fam)}


nS = nfam = 0
for tr in range(trials):
    k = rng.randint(1, 5)
    members, edges, nxt = [], [], 0
    for _ in range(k):
        sz = rng.randint(3, 8)
        vs = list(range(nxt, nxt + sz)); nxt += sz
        members.append(set(vs))
        # a connected random 3-graph on vs: chain of triples
        cover = {vs[0]}
        while len(cover) < sz:
            a = rng.choice(sorted(cover))
            rest = [v for v in vs if v not in cover]
            b = rest[0]
            c = rng.choice([v for v in vs if v not in (a, b)])
            edges.append(tuple(sorted((a, b, c)))); cover |= {a, b, c}
    outside = list(range(nxt, nxt + rng.randint(0, 6))); nxt += len(outside)
    allv = list(range(nxt))
    for _ in range(rng.randint(0, 2 * k + 2)):
        e = tuple(sorted(rng.sample(allv, 3)))
        if any(set(e) <= M for M in members) or not any(set(e) & M for M in members):
            continue
        edges.append(e)
    fam = list(range(k))
    Es = sorted(estar(edges, members, fam))
    if len(Es) > 12:
        continue
    N = {j: {i for i in fam if set(edges[j]) & members[i]} for j in Es}
    base = len(Es) - len(fam)
    # identity E*_H(S') = {e in E*(X*) : e meets V(S')} for every subfamily S'
    for r in range(1, k + 1):
        for Sp in combinations(fam, r):
            lhs = estar(edges, members, list(Sp))
            rhs = {j for j in Es if N[j] & set(Sp)}
            assert lhs == rhs, (lhs, rhs)
            nfam += 1
    for r in range(1, len(Es) + 1):
        for S in combinations(Es, r):
            NS = set().union(*[N[j] for j in S])
            if len(NS) >= len(S):
                continue
            nS += 1
            Xp = [i for i in fam if i not in NS]
            if not Xp:
                assert len(fam) < len(S)
                continue
            EXp = estar(edges, members, Xp)
            assert EXp <= set(Es) - set(S)
            assert len(EXp) - len(Xp) < base
print(f"trials={trials} Hall-violating S checked={nS} subfamilies checked={nfam}: ALL OK")
