"""lemma_tests.py -- falsification tests (exact) for the lemmas of L018 on census data.
(U1) one-vertex lemma: F in C, x with d(x)>=1, slack(F) < 3+2d(x)  ==> x lies in a minimum transversal of F.
(U2) two-vertex lemma: slack(F) < 2|E_{x,x'}| - 5 ==> x, x' lie in a common minimum transversal.
(TP) tight connected graphs with a pendant vertex x in e={x,p,q}: d(p)=d(q)=2, K-{x,p} connected with slack 1.
(CL) closure form (Theorem 1): has (Red) pair  <=>  exists T: [cl(T) != V and w(T) >= 0] or [cl(T) = V and w(T) >= 3]
     (checked against the brute-force Z-formulation on census graphs n <= 10, all T).
Census graphs: experiments/20261027-0230-red-config/out/cls_*.txt (connected, class C, Delta<=3)."""
import glob, itertools, collections, sys
from hg import tau_of, TauCache
def load(n):
    G = []
    for fn in sorted(glob.glob('/home/user/Erdos-757/experiments/20261027-0230-red-config/out/cls_%d_*.txt' % n)):
        for line in open(fn):
            t = line.split()
            if not t: continue
            if t[0] == 'C': t = t[1:]
            m = int(t[0]); G.append([tuple(map(int, x.split('.'))) for x in t[1:1+m]])
    return G
def mintrans_all(E, n):
    """all minimum transversals (as frozensets)"""
    t = tau_of(E)
    V = range(n)
    out = []
    for T in itertools.combinations(V, t):
        s = set(T)
        if all(s & set(e) for e in E): out.append(frozenset(T))
    return t, out
def deg(E, n):
    d = [0]*n
    for e in E:
        for v in e: d[v] += 1
    return d
def components(E, n, removed=()):
    rem = set(removed); par = {v: v for v in range(n) if v not in rem}
    def f(v):
        while par[v] != v: par[v] = par[par[v]]; v = par[v]
        return v
    for e in E:
        if rem & set(e): continue
        a, b, c = e; par[f(a)] = f(b); par[f(b)] = f(c)
    return len(set(f(v) for v in par))
stats = collections.Counter()
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
for n in range(3, NMAX + 1):
    for E in load(n):
        m = len(E); d = deg(E, n)
        t, MT = mintrans_all(E, n)
        s = 3*n + 2*m - 11*t
        inmt = set().union(*MT) if MT else set()
        # U1
        for x in range(n):
            if d[x] >= 1 and s < 3 + 2*d[x]:
                stats['U1 tested'] += 1
                assert x in inmt, ('U1 FAILS', E, x)
        # U2
        for x, y in itertools.combinations(range(n), 2):
            sh = any(x in e and y in e for e in E)
            Exy = d[x] + d[y] - sh
            if s < 2*Exy - 5:
                stats['U2 tested'] += 1
                assert any(x in T and y in T for T in MT), ('U2 FAILS', E, x, y)
        # TP
        if s == 0 and m > 1:
            for x in range(n):
                if d[x] != 1: continue
                e = [f for f in E if x in f][0]
                p, q = [v for v in e if v != x]
                assert d[p] == 2 and d[q] == 2, ('TP degree FAILS', E, x)
                for pp in (p, q):
                    E2 = [f for f in E if x not in f and pp not in f]
                    n2 = n - 2
                    # relabel
                    keep = [v for v in range(n) if v not in (x, pp)]
                    idx = {v: i for i, v in enumerate(keep)}
                    E2r = [tuple(idx[v] for v in f) for f in E2]
                    s2 = 3*n2 + 2*len(E2r) - 11*tau_of(E2r)
                    c2 = components(E2r, n2)
                    stats['TP tested'] += 1
                    assert s2 == 1 and c2 == 1, ('TP FAILS', E, x, pp, s2, c2)
        # CL (closure form) for n <= 9
        if n <= 9 and n >= 5:
            tc = TauCache(E); inc = [0]*n
            for i, e in enumerate(E):
                for v in e: inc[v] |= 1 << i
            red_Z = False
            for Z in range(1, (1 << n) - 1):
                F = 0
                for v in range(n):
                    if Z >> v & 1: F |= inc[v]
                if 3*bin(Z).count('1') + 2*bin(F).count('1') - 11*tc.tau(F) >= 0: red_Z = True; break
            red_T = False
            for T in range(1, 1 << n):
                ET = 0
                for v in range(n):
                    if T >> v & 1: ET |= inc[v]
                cl = [v for v in range(n) if (inc[v] & ~ET) == 0]
                w = 3*len(cl) + 2*bin(ET).count('1') - 11*bin(T).count('1')
                if (len(cl) < n and w >= 0) or (len(cl) == n and w >= 3): red_T = True; break
            stats['CL tested'] += 1
            assert red_Z == red_T, ('CL FAILS', E)
    print('n=%d done' % n, dict(stats)); sys.stdout.flush()
print('ALL TESTS PASSED', dict(stats))
