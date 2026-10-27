"""L020: patterns (b) and (f) in reverse.  For F (cell list, Delta<=3, slack 3 expected) compute all NC pairs among vertices
of degree <= 2; b-configurations {x1,x2,x3} (pairwise NC, not an edge) are glued to E_1 = {y1,y2,y3} by v with edges
{v,x_j,y_j}; f-configurations ({a,b};{c,e}) (a,b not in an edge, four cross NC pairs) are glued to every tight partner X
with an NC pair {d,f} (E_1 and the (10,7,4) classes, Delta<=3) by {v,a,b},{v,c,d},{v,e,f} and {v,a,b},{v,c,f},{v,e,d}.
Results in C with Delta<=3 and tau = tau(F)+tau(X)+1 are near-tight graphs (slack s(F)-2).
Usage: python3 build_bf.py <F-list> <out.json> [sample_size(0=all) seed [partner lists...]]"""
import sys, json, itertools, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any, in_C
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'

def nc_data(n, es):
    deg = hyp.degrees(n, es)
    Ts, t = hyp.all_min_transversals(hyp.masks(es))
    cov = [0] * n
    for T in Ts:
        mm = T
        while mm:
            b = mm & -mm; mm ^= b; cov[b.bit_length() - 1] |= T
    A = [x for x in range(n) if deg[x] <= 2]
    NC = {x: set(y for y in A if y != x and not (cov[x] >> y) & 1) for x in A}
    share = set(frozenset(q) for e in es for q in itertools.combinations(e, 2))
    return t, A, NC, share

def main(fpath, out, k=None, seed=1, plist=None):
    Fs = [(n, es) for (n, es) in read_any(fpath) if max(hyp.degrees(n, es)) <= 3]
    if k:
        random.seed(seed); Fs = random.sample(Fs, min(k, len(Fs)))
    plist = plist or [I + 'cell_3_1_1.txt', I + 'cell_10_7_4.txt']
    partners = [(n, es) for p in plist for (n, es) in read_any(p) if max(hyp.degrees(n, es)) <= 3]
    Pdat = []
    for (nx, ex) in partners:
        tx, Ax, NCx, shx = nc_data(nx, ex)
        prs = sorted(set(tuple(sorted((x, y))) for x in Ax for y in NCx[x]))
        if prs: Pdat.append((nx, ex, tx, prs))
    print('partners with an NC pair:', [(p[0], len(p[3])) for p in Pdat], 'F graphs:', len(Fs), flush=True)
    res = []; nb = nf = 0
    for i, (n, es) in enumerate(Fs):
        t, A, NC, share = nc_data(n, es)
        s = 3 * n + 2 * len(es) - 11 * t
        eset = set(frozenset(e) for e in es)
        bconf = [(x, y, z) for x, y, z in itertools.combinations(A, 3) if y in NC[x] and z in NC[x] and z in NC[y] and frozenset((x, y, z)) not in eset]
        fconf = []
        for a, b in itertools.combinations(A, 2):
            if frozenset((a, b)) in share: continue
            for c, e in itertools.combinations(sorted(NC[a] & NC[b]), 2):
                if c not in (a, b) and e not in (a, b): fconf.append((a, b, c, e))
        nb += bool(bconf); nf += bool(fconf)
        builds = []
        for (x1, x2, x3) in bconf:
            builds.append((3, 1, [(n, n + 1, n + 2)], [(n + 3, x1, n), (n + 3, x2, n + 1), (n + 3, x3, n + 2)], n + 4))
        for (a, b, c, e) in fconf:
            for (nx, ex, tx, prs) in Pdat:
                for (d, f) in prs:
                    for (dd, ff) in ((d, f), (f, d)):
                        off = n; v = n + nx
                        builds.append((nx, tx, [tuple(off + y for y in g) for g in ex], [(v, a, b), (v, c, off + dd), (v, e, off + ff)], n + nx + 1))
        for (nx, tx, eX, ev, N) in builds:
            E = list(es) + eX + ev
            if max(hyp.degrees(N, E)) > 3 or not in_C(N, E): continue
            tK = hyp.tau(N, E)
            if tK == t + tx + 1:
                res.append(dict(n=N, m=len(E), tau=tK, slack=3 * N + 2 * len(E) - 11 * tK, edges=E, src=i))
        if bconf or fconf:
            print('F', i, (n, len(es), t, 'slack', s), 'b-conf', len(bconf), 'f-conf', len(fconf), 'near-tight results so far', len(res), flush=True)
    print('F with b-conf', nb, 'with f-conf', nf, 'of', len(Fs), '; near-tight graphs built:', len(res),
          sorted(set((r['n'], r['m'], r['tau'], r['slack']) for r in res)), flush=True)
    json.dump(res, open(out, 'w'))

if __name__ == '__main__':
    k = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != '0' else None
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    main(sys.argv[1], sys.argv[2], k, seed, sys.argv[5:] or None)
