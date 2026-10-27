"""pendant_census.py -- for every census graph (connected, class C, Delta<=3) with a pendant vertex:
is there a (Red) pair (Z,T) with Z inside the radius-2 ball of some pendant vertex?  For the graphs where no pendant
has such a local pair, record the graph and its smallest (Red) set (exact)."""
import sys, collections, itertools
from hg import TauCache
def parse_cls(line):
    t = line.split()
    if t[0] == 'C': t = t[1:]
    m = int(t[0]); return [tuple(map(int, x.split('.'))) for x in t[1:1+m]]
def analyse(E, n):
    m = len(E)
    inc = [0]*n; nb = [set() for _ in range(n)]
    for i, e in enumerate(E):
        for v in e:
            inc[v] |= 1 << i
            nb[v] |= set(e)
    d = [bin(inc[v]).count('1') for v in range(n)]
    pend = [v for v in range(n) if d[v] == 1]
    if not pend: return None
    tc = TauCache(E)
    full = (1 << n) - 1
    def val(Zs):
        F = 0
        for v in Zs: F |= inc[v]
        return 3*len(Zs) + 2*bin(F).count('1') - 11*tc.tau(F)
    for y in pend:
        ball = {y}; front = {y}
        for r in range(RAD):
            new = set()
            for u in front: new |= nb[u]
            new -= ball; ball |= new; front = new
        ball = sorted(ball)
        for k in range(1, len(ball)+1):
            for Z in itertools.combinations(ball, k):
                if len(Z) == n: continue
                if val(Z) >= 0:
                    return ('local', y, Z)
    # no local pair: smallest Red Z globally
    for k in range(1, n):
        for Z in itertools.combinations(range(n), k):
            if val(Z) >= 0:
                return ('global', k, Z)
    return ('redfree',)
RAD = 2
if __name__ == "__main__":
    import glob
    res = collections.Counter(); bad = []
    RAD = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    globals()["RAD"] = RAD
    NMIN = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    for n in range(NMIN, int(sys.argv[1]) + 1):
        for fn in sorted(glob.glob('/home/user/Erdos-757/experiments/20261027-0230-red-config/out/cls_%d_*.txt' % n)):
            for line in open(fn):
                if not line.strip(): continue
                E = parse_cls(line)
                r = analyse(E, n)
                if r is None: continue
                res[(n, r[0])] += 1
                if r[0] != 'local':
                    bad.append((n, len(E), r, E))
        print('n=%d' % n, {k: v for k, v in res.items() if k[0] == n}); sys.stdout.flush()
    print("graphs with a pendant vertex but no radius-%d-local (Red) pair at any pendant:" % RAD, len(bad))
    for (n, m, r, E) in bad:
        dd = collections.Counter(v for e in E for v in e)
        print(n, m, r, 'degs', ''.join(str(dd[v]) for v in range(n)), ' '.join('%d.%d.%d' % e for e in E))
