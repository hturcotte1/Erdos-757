"""Referee L014 r1: build the extension inputs of every branch of a recursion cell (n,m,t,D) from the prover's lower cell files,
with own branches/decompositions (decomp_bf.decs) -- no engine.py.  Writes OUTPREFIX_d<d>_tp<tp>.txt ("m a b c ..." lines) and
prints per-branch counts.  Usage: python3 build_inputs.py CELLDIR n m t D OUTPREFIX"""
import sys, re, math, itertools, os
from collections import Counter
sys.argv, args = sys.argv[:3], sys.argv[1:]
CD, n, m, t, D, OP = args[0], int(args[1]), int(args[2]), int(args[3]), int(args[4]), args[5]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decomp_bf.py')).read().split('from math import comb')[0]
exec(src.replace('CD = sys.argv[1]', 'CD = %r' % CD))
def load(nn, mm, tt, DD):
    if (nn, mm, tt) == (1, 0, 0): return [[]]
    fn = '%s/cell_%d_%d_%d_D%d.txt' % (CD, nn, mm, tt, DD)
    reps = []; done = False
    for l in open(fn):
        if l.startswith('FOUND:'):
            es = [tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]; assert len(es) == mm; reps.append(es)
        elif l.startswith('INFO'): done = True
    assert done
    return reps
for d in range(max(1, math.ceil(3 * m / n)), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0 or tp < 0: continue
        fn = '%s_d%d_tp%d.txt' % (OP, d, tp); tot = 0
        with open(fn, 'w') as out:
            for dec in decs(n - 1, m - d, Sp):
                c = Counter(dec); groups = []
                for typ in sorted(c):
                    L = load(typ[0], typ[1], typ[2], d)
                    groups.append((typ, L, list(itertools.combinations_with_replacement(range(len(L)), c[typ]))))
                cnt = 0
                for combo in itertools.product(*[g[2] for g in groups]):
                    es = []; off = 0
                    for (typ, L, _), idxs in zip(groups, combo):
                        for i in idxs:
                            es += [(a + off, b + off, cc + off) for (a, b, cc) in L[i]]; off += typ[0]
                    assert off == n - 1 and len(es) == m - d
                    out.write('%d %s\n' % (len(es), ' '.join('%d %d %d' % e for e in es))); cnt += 1
                tot += cnt
        print('BRANCH', (n, m, t, D), 'd=%d tp=%d Sp=%d decompositions=%d inputs=%d file=%s' % (d, tp, Sp, len(decs(n - 1, m - d, Sp)), tot, fn))
