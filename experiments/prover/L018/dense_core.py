"""dense_core.py -- for the census graphs whose smallest (Red) set Z has |Z| >= 6 and slack <= 5,
list all minimum-size (Red) pairs (Z, T) and describe them (exact)."""
import gzip, sys, itertools, collections
from hg import TauCache, tau_of, degrees
def parse(line):
    t = line.split(); m = int(t[0])
    return [tuple(map(int, x.split('.'))) for x in t[1:1+m]]
def analyse(E, maxlist=3):
    n = 1 + max(max(e) for e in E); m = len(E)
    tc = TauCache(E)
    inc = [0]*n
    for i, e in enumerate(E):
        for v in e: inc[v] |= 1 << i
    tau = tc.tau((1 << m) - 1)
    s = 3*n + 2*m - 11*tau
    d = [bin(inc[v]).count('1') for v in range(n)]
    red = []
    best = None
    for Z in range(1, (1 << n) - 1):
        F = 0
        for v in range(n):
            if Z >> v & 1: F |= inc[v]
        val = 3*bin(Z).count('1') + 2*bin(F).count('1') - 11*tc.tau(F)
        if val >= 0:
            red.append((bin(Z).count('1'), Z, val, F))
    red.sort()
    return n, m, tau, s, d, red
def tset(E, F):
    """a minimum transversal of the edge subset F"""
    edges = [E[i] for i in range(len(E)) if F >> i & 1]
    t = tau_of(edges)
    V = sorted(set(v for e in edges for v in e))
    for T in itertools.combinations(V, t):
        if all(any(v in e for v in T) for e in edges):
            return T
if __name__ == '__main__':
    fn = '/home/user/Erdos-757/experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz'
    for line in gzip.open(fn, 'rt'):
        if line.startswith('#'): continue
        E = parse(line)
        n = 1 + max(max(e) for e in E)
        if n < 11: 
            if n != 9: continue
        m = len(E)
        tau = tau_of(E); s = 3*n + 2*m - 11*tau
        if s > 5: continue
        n, m, tau, s, d, red = analyse(E)
        k = red[0][0]
        mins = [r for r in red if r[0] == k]
        print('GRAPH n=%d m=%d tau=%d slack=%d degs=%s  #Red=%d  min|Z|=%d (#min=%d)' % (n, m, tau, s, ''.join(map(str, d)), len(red), k, len(mins)))
        print('   edges', ' '.join('%d.%d.%d' % e for e in E))
        for (sz, Z, val, F) in mins[:4]:
            Zl = [v for v in range(n) if Z >> v & 1]
            out = [v for v in range(n) if not Z >> v & 1]
            T = tset(E, F)
            print('   Z=%s (V-Z=%s) e(Z)=%d tau=%d value=%d T=%s  deg(V-Z)=%s' % (Zl, out, bin(F).count('1'), len(T), val, list(T), [d[v] for v in out]))
        sys.stdout.flush()
