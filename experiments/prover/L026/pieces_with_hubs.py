#!/usr/bin/env python3
"""L026 check C4: which of the 32 pieces of L* contain an E1-hub (v; x,y,z; a,b,c) with d(x)=d(y)=d(z)=2,
and for those, is the outer triple a b-configuration of G'_F = F - {v,x,y,z}?  Reports the cell of G'_F,
its number of components and the degrees of a, b, c in G'_F.  Own code."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L

def hubs_in(n, E):
    d = L.degs(n, E)
    inc = [[] for _ in range(n)]
    for i, e in enumerate(E):
        for x in e: inc[x].append(i)
    Es = set(tuple(sorted(e)) for e in E)
    out = []
    for v in range(n):
        if d[v] != 3: continue
        es = [E[i] for i in inc[v]]
        # choose for each edge at v which co-vertex is the E1 vertex
        for choice in itertools.product(*[[tuple(u for u in e if u != v)] for e in es]):
            for perm in itertools.product((0, 1), repeat=3):
                xyz = [choice[k][perm[k]] for k in range(3)]
                abc = [choice[k][1 - perm[k]] for k in range(3)]
                if tuple(sorted(xyz)) in Es and all(d[u] == 2 for u in xyz):
                    out.append((v, tuple(xyz), tuple(abc)))
    return out

def main():
    pieces = L.load_pieces()
    for P in pieces:
        n, E = P.n, P.E
        hs = hubs_in(n, E)
        res = collections.Counter()
        for v, xyz, abc in hs:
            S = [u for u in range(n) if u != v and u not in xyz]
            idx = {u: i for i, u in enumerate(S)}
            Gp = L.induced(E, S)
            ng = len(S)
            a, b, c = (idx[u] for u in abc)
            t = L.tau(Gp) if Gp else 0
            T = L.all_min_transversals(Gp, t) if Gp else [0]
            nc = all(not any((tr >> p) & 1 and (tr >> q) & 1 for tr in T) for p, q in ((a, b), (a, c), (b, c)))
            comps = len(L.components(ng, Gp))
            dg = L.degs(ng, Gp)
            res[((ng, len(Gp), t), 'components', comps, 'b-config', nc, 'outer degrees', tuple(sorted((dg[a], dg[b], dg[c]))))] += 1
        print(P.name, 'W', P.W, 'hubs', len(hs), dict(res), flush=True)

if __name__ == '__main__':
    main()
