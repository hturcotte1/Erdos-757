"""L026 C12: shape (j1) (all outer vertices of G'-degree 1) among the stored hubs, against Theorem 12(k):
the bounds tau(G')-2 <= tau(R) <= tau(G')-1 (minimality-free), and, when tau(R) = tau(G')-2, that every
vertex of W is avoided in R (minimality-free consequence of the b-configuration); records the shared-edge
case and the components of R with positive DEF.  Usage: python3 j1_check.py <cell files ...>"""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L
pieces = L.load_pieces()
st = dict(j1=0, shared=0, bound_fail=0, drop2=0, drop1=0, W_avoided_fail=0)
for f in sys.argv[1:]:
    for E in L.read_found(f):
        n = L.nv(E); m = len(E); d = L.degs(n, E)
        if max(d) > 3 or len(L.components(n, E)) != 1: continue
        t0 = L.tau(E)
        if L.A_val(n, m, t0) > 15: continue
        T = L.all_min_transversals(E, t0)
        co = set()
        for tr in T:
            vs = [i for i in range(n) if tr >> i & 1]
            for pr in itertools.combinations(vs, 2): co.add(pr)
        Es = set(tuple(sorted(e)) for e in E)
        ones = [u for u in range(n) if d[u] == 1]
        for a, b, c in itertools.combinations(ones, 3):
            if (a, b) in co or (a, c) in co or (b, c) in co or (a, b, c) in Es: continue
            nH, EH = L.hub(n, E, a, b, c)
            if not L.in_C3(nH, EH): continue
            st['j1'] += 1
            g = {t: [e for e in E if t in e][0] for t in (a, b, c)}
            shared = len(set(map(tuple, g.values()))) < 3
            if shared: st['shared'] += 1
            Rv = [u for u in range(n) if u not in (a, b, c)]
            ER = L.induced(E, Rv)
            tR = L.tau(ER)
            if not (t0 - 2 <= tR <= t0 - 1): st['bound_fail'] += 1; print('BOUND FAIL', E, (a, b, c))
            W = set(u for t in (a, b, c) for u in g[t] if u not in (a, b, c))
            if tR == t0 - 2:
                st['drop2'] += 1
                TR = L.all_min_transversals(ER, tR)
                cov = 0
                for tr in TR: cov |= tr
                if any(cov >> Rv.index(u) & 1 for u in W): st['W_avoided_fail'] += 1; print('W FAIL', E, (a, b, c))
            else:
                st['drop1'] += 1
            comps = [(len(C), L.DEF(len(C), L.induced(ER, C), pieces)) for C in L.components(len(Rv), ER) if L.induced(ER, C)]
            print('j1 hub', (n, m, t0), (a, b, c), 'shared' if shared else 'disjoint', 'tau(R)-tau(G\')', tR - t0, 'R components (n, DEF):', comps, flush=True)
print('TOTAL', st)
