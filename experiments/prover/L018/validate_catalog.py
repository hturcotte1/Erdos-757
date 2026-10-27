"""validate_catalog.py -- independent check of the radius-2 pendant catalog (Theorem 3) on the census (n <= NMAX):
for every pendant vertex y of every census graph such that NO (Red) pair (Z,T) has Z inside the ball B_2(y)
(computed directly in the graph), verify that the configuration at y is (P-tree-2) or (P-tri-2) exactly as described
in the certificate.  Also count how often each configuration type occurs at all (reducible or not)."""
import glob, itertools, collections, sys
from hg import TauCache
def load(n):
    for fn in sorted(glob.glob('/home/user/Erdos-757/experiments/20261027-0230-red-config/out/cls_%d_*.txt' % n)):
        for line in open(fn):
            t = line.split()
            if not t: continue
            if t[0] == 'C': t = t[1:]
            m = int(t[0]); yield [tuple(map(int, x.split('.'))) for x in t[1:1+m]]
def conf_type(E, n, y, d, edges_at):
    e0 = edges_at[y][0]; a, b = [v for v in e0 if v != y]
    if d[a] != 2 or d[b] != 2: return 'other'
    A = [f for f in edges_at[a] if f != e0][0]; B = [f for f in edges_at[b] if f != e0][0]
    ball = {y, a, b} | set(A) | set(B)
    common = set(A) & set(B)
    second = []
    for u in sorted((set(A) | set(B)) - {a, b}):
        need = 2 if u not in common else 3
        if d[u] != need: return 'other'
        for f in edges_at[u]:
            if f != A and f != B: second.append((u, f))
    fs = [f for _, f in second]
    if len(set(fs)) != len(fs): return 'other'
    for u, f in second:
        if (set(f) & ball) != {u}: return 'other'
    if not common and len(second) == 4: return 'P-tree-2'
    if len(common) == 1 and len(second) == 3: return 'P-tri-2'
    return 'other'
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
cnt = collections.Counter()
for n in range(5, NMAX + 1):
    for E in load(n):
        d = [0]*n; edges_at = [[] for _ in range(n)]; inc = [0]*n
        for i, e in enumerate(E):
            for v in e: d[v] += 1; edges_at[v].append(e); inc[v] |= 1 << i
        pend = [v for v in range(n) if d[v] == 1]
        if not pend: continue
        tc = TauCache(E)
        nb = [set() for _ in range(n)]
        for e in E:
            for v in e: nb[v] |= set(e)
        for y in pend:
            ball = {y}; front = {y}
            for r in range(2):
                new = set()
                for u in front: new |= nb[u]
                new -= ball; ball |= new; front = new
            ball = sorted(ball)
            red = False
            for k in range(1, len(ball) + 1):
                for Z in itertools.combinations(ball, k):
                    if len(Z) == n: continue
                    F = 0
                    for z in Z: F |= inc[z]
                    if 3*len(Z) + 2*bin(F).count('1') - 11*tc.tau(F) >= 0: red = True; break
                if red: break
            ty = conf_type(E, n, y, d, edges_at)
            cnt[(ty, 'locally-reducible' if red else 'locally-IRREDUCIBLE')] += 1
            if not red:
                assert ty in ('P-tree-2', 'P-tri-2'), ('CATALOG VIOLATION', n, E, y, ty)
    print('n=%d' % n, sorted(cnt.items())); sys.stdout.flush()
print('VALIDATION PASSED: every radius-2-irreducible pendant is of type P-tree-2 or P-tri-2')
