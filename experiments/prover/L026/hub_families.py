#!/usr/bin/env python3
"""L026 exploration (not a proof step): for every b-configuration hub H = G' (+) (a,b,c) found in the given
cells (connected Delta<=3 G' with A(G') <= 15), list ALL optimal L*-families of H (value DEF(H)), and report
whether an optimal family has a member containing the hub vertex v / the hub edge {x,y,z}, the member
names, |E*|, and how many members meet {a,b,c}.  Own code (ownlib)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L

pieces = L.load_pieces()

def optimal_families(n, E):
    em = L.emasks(E)
    copies = []
    for P in pieces:
        for Wm in L.induced_copies(P, n, E):
            copies.append((Wm, P.W, P.m, P.name))
    best = [0]; fams = []
    def bd(U):
        return sum(1 for f in em if f & U)
    def rec(i, U, gain, fam):
        obj = gain - 35 * bd(U)
        if obj > best[0]: best[0] = obj; fams.clear()
        if obj == best[0] and fam: fams.append(list(fam))
        ub = obj + sum(c[1] for c in copies[i:] if not c[0] & U)
        if ub < best[0]: return
        for j in range(i, len(copies)):
            Wm, w, mP, name = copies[j]
            if Wm & U: continue
            fam.append((Wm, name)); rec(j + 1, U | Wm, gain + w + 35 * mP, fam); fam.pop()
    rec(0, 0, 0, [])
    return best[0], fams

def run(path, limit):
    graphs = L.read_found(path)
    stats = collections.Counter()
    shown = 0
    for E in graphs:
        n = L.nv(E); m = len(E); d = L.degs(n, E)
        if max(d) > 3 or len(L.components(n, E)) != 1: continue
        t = L.tau(E)
        if L.A_val(n, m, t) > 15: continue
        T = L.all_min_transversals(E, t)
        low = [x for x in range(n) if d[x] <= 2]
        Es = set(tuple(sorted(e)) for e in E)
        for a, b, c in itertools.combinations(low, 3):
            if (a, b, c) in Es: continue
            if any(tr & ((1 << p) | (1 << q)) == ((1 << p) | (1 << q)) for tr in T for p, q in ((a, b), (a, c), (b, c))):
                continue
            nH, EH = L.hub(n, E, a, b, c)
            D, fams = optimal_families(nH, EH)
            v = n; hubmask = sum(1 << u for u in range(n, n + 4))
            kinds = set()
            for fam in fams:
                U = 0
                for Wm, name in fam: U |= Wm
                vin = any((Wm >> v) & 1 for Wm, _ in fam)
                xyz_in = any(((Wm >> (n + 1)) & 7) == 7 for Wm, _ in fam)
                names = tuple(sorted(name for _, name in fam))
                kinds.add((vin, xyz_in, names))
            stats[('some optimal family has a member containing v', any(k[0] for k in kinds))] += 1
            stats[('every optimal family has a member containing v', all(k[0] for k in kinds))] += 1
            if shown < limit:
                shown += 1
                print('  G\'', (n, m, t), 'abc', (a, b, c), 'DEF(H)', D, 'optimal families (v in a member, xyz in a member, names):',
                      sorted(kinds), flush=True)
    print(path.split('/')[-1], dict(stats), flush=True)

if __name__ == '__main__':
    lim = int(sys.argv[1])
    for p in sys.argv[2:]:
        run(p, lim)
