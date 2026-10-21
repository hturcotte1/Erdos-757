# mkinputs.py n m t D CELLDIR [d tp]: own input builder for the recursion cell (n,m,t,D): for each branch (d, t') and each decomposition
# (own decomp.py), the product of the class lists (combinations with replacement for repeated types), consecutive vertex blocks. Lines "m a b c ...".
import sys, os, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp import decompositions
n, m, t, D = map(int, sys.argv[1:5]); celldir = sys.argv[5]
only = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else None
def load(nk, mk, tk, d):
    if (nk, mk, tk) == (1, 0, 0): return [[]]
    if (nk, mk, tk) == (3, 1, 1): return [[(0, 1, 2)]]
    p = '%s/cell_%d_%d_%d_D%d.txt' % (celldir, nk, mk, tk, d)
    if not os.path.exists(p): raise SystemExit('MISSING LIST ' + p)
    cls = []
    for line in open(p):
        if line.startswith('FOUND'):
            cls.append([tuple(map(int, x.strip('()').split(','))) for x in line.split()[1:]])
    return cls
total = 0
for d in range(max(1, math.ceil(3 * m / n)), D + 1):
    for tp in (t - 1, t):
        if only and (d, tp) != only: continue
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0: continue
        for dec in decompositions(n - 1, m - d, Sp):
            groups = {}
            for c in dec: groups[c] = groups.get(c, 0) + 1
            gl = []
            for typ, k in sorted(groups.items()):
                cls = load(typ[0], typ[1], typ[2], d)
                gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), k))))
            cnt = 0
            for combo in itertools.product(*[g[2] for g in gl]):
                es = []; off = 0
                for (typ, cls, _), idxs in zip(gl, combo):
                    for i in idxs:
                        es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                assert off == n - 1 and len(es) == m - d
                sys.stdout.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
            sys.stderr.write('branch d=%d tp=%d S=%d %s: %d inputs\n' % (d, tp, Sp, list(dec), cnt)); total += cnt
sys.stderr.write('TOTAL inputs %d\n' % total)
