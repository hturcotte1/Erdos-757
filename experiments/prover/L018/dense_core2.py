"""dense_core2.py -- for the low-slack (slack <= 5) census graphs with no (Red) pair of size <= 5 (from
redk5_free_graphs.txt.gz, n >= 9), describe H - Z for every minimum (Red) set Z, and test the exactness identity
value(Z) = slack(H) - slack(H - Z) - 11*(tau(H-Z) + tau(E_Z) - tau(H)).  Exact integers."""
import gzip, itertools, collections
from hg import TauCache, tau_of
def parse(line):
    t = line.split(); m = int(t[0]); return [tuple(map(int, x.split('.'))) for x in t[1:1+m]]
def comps(E, V):
    par = {v: v for v in V}
    def f(v):
        while par[v] != v: par[v] = par[par[v]]; v = par[v]
        return v
    for e in E:
        a, b, c = e; par[f(a)] = f(b); par[f(b)] = f(c)
    cs = collections.defaultdict(lambda: [set(), 0])
    for v in V: cs[f(v)][0].add(v)
    for e in E: cs[f(e[0])][1] += 1
    return sorted((len(s), k) for s, k in cs.values())
fn = '/home/user/Erdos-757/experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz'
summary = collections.Counter(); allexact = True; ng = 0
for line in gzip.open(fn, 'rt'):
    if line.startswith('#'): continue
    E = parse(line); n = 1 + max(max(e) for e in E); m = len(E)
    if n < 9: continue
    tH = tau_of(E); s = 3*n + 2*m - 11*tH
    if s > 5: continue
    ng += 1
    tc = TauCache(E); inc = [0]*n
    for i, e in enumerate(E):
        for v in e: inc[v] |= 1 << i
    red = []
    for Z in range(1, (1 << n) - 1):
        F = 0
        for v in range(n):
            if Z >> v & 1: F |= inc[v]
        val = 3*bin(Z).count('1') + 2*bin(F).count('1') - 11*tc.tau(F)
        if val >= 0: red.append((bin(Z).count('1'), Z, F, val))
    k = min(r[0] for r in red)
    kinds = collections.Counter()
    for (sz, Z, F, val) in red:
        if sz != k: continue
        V2 = [v for v in range(n) if not Z >> v & 1]
        E2 = [E[i] for i in range(m) if not F >> i & 1]
        t2 = tau_of(E2) if E2 else 0
        s2 = 3*len(V2) + 2*len(E2) - 11*t2
        gap = t2 + tc.tau(F) - tH
        exact = (val == s - s2 - 11*gap)
        allexact &= exact
        kinds[(tuple(comps(E2, V2)), s2, gap)] += 1
    desc = '; '.join('H-Z components (n,m)=%s slack(H-Z)=%d gap=%d: %d sets' % (c, s2, g, cnt) for (c, s2, g), cnt in sorted(kinds.items()))
    print('(%d,%d,%d) slack %d, min |Z| = %d: %s' % (n, m, tH, s, k, desc))
    summary[(n, m, s, k)] += 1
print('graphs:', ng, 'identity value = slack(H) - slack(H-Z) - 11*gap holds for all listed Z:', allexact)
print(sorted(summary.items()))
