"""For linear uncoverable triples (all of which contain an F7 copy in the slack<=1, m<=n-4 cells): which role does v play in the F7 copies,
how many of v's three edges does a copy use, and what is the smallest S' (containing the six vertices) with |S'|-e_F(S') <= 3.
usage: f7_roles.py cell K  (first K classes)"""
import sys, itertools, collections
from pyverify import all_covers_exact
cell, K = sys.argv[1], int(sys.argv[2])
lines = open('inputs/cell_%s.txt' % cell).read().split('\n')[:K]
roles = collections.Counter(); Ssz = collections.Counter(); nunc = 0; copies_per = collections.Counter(); nonlin = 0
for line in lines:
    a = list(map(int, line.split())); n, m, tau = a[:3]; E = [tuple(a[3+3*i:6+3*i]) for i in range(m)]
    Ts = all_covers_exact(E, tau); Tm = [sum(1 << v for v in T) for T in Ts]
    inE = set(); [inE.update(itertools.permutations(e, 2)) for e in E]
    pairs = [(a_, b_) for a_ in range(n) for b_ in range(a_+1, n) if (a_, b_) not in inE]
    # bitset of transversals meeting each pair
    mb = {p: sum(1 << i for i, t in enumerate(Tm) if t >> p[0] & 1 or t >> p[1] & 1) for p in pairs}
    Eset = set(frozenset(e) for e in E)
    def f7_copies(H):
        S = set(frozenset(e) for e in H); at = collections.defaultdict(list)
        for e in H:
            for x in e: at[x].append(e)
        res = []
        for c, es in at.items():
            for e1, e2, e3 in itertools.combinations(es, 3):
                p = [tuple(x for x in e if x != c) for e in (e1, e2, e3)]; a1, b1 = p[0]
                for x2, y2 in (p[1], p[1][::-1]):
                    for x3, y3 in (p[2], p[2][::-1]):
                        if len({c, a1, b1, x2, y2, x3, y3}) == 7 and frozenset((a1, x2, x3)) in S and frozenset((b1, y2, y3)) in S:
                            res.append(frozenset([e1, e2, e3, frozenset((a1, x2, x3)), frozenset((b1, y2, y3))]))
        return set(res)
    for p1, p2, p3 in itertools.combinations(pairs, 3):
        if len(set(p1) | set(p2) | set(p3)) < 6: continue
        if mb[p1] & mb[p2] & mb[p3]: continue
        nunc += 1; v = n; N = [frozenset((v, *p)) for p in (p1, p2, p3)]
        H = [frozenset(e) for e in E] + N; cps = f7_copies(H); copies_per[len(cps)] += 1
        for cp in cps:
            used = sum(1 for e in cp if e in N); roles['copy uses %d of the 3 new edges' % used] += 1
        W = set(p1) | set(p2) | set(p3); best = None
        for extra in range(0, 4):
            for X in itertools.combinations([x for x in range(n) if x not in W], extra):
                S = W | set(X); e = sum(1 for ed in E if set(ed) <= S)
                if len(S) - e <= 3: best = len(S); break
            if best: break
        Ssz[best] += 1
print(cell, 'classes', len(lines), 'uncoverable linear triples', nunc, 'F7 copies per triple', dict(copies_per), dict(roles), "min |S'| (S' contains the six vertices, |S'|-e<=3):", dict(Ssz))
