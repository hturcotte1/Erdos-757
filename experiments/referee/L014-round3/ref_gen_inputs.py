"""Referee (L014 round 3): rebuild the ext_d inputs of a recursion branch from the prover's cell lists, with own code.
usage: ref_gen_inputs.py CELLDIR n m t D OUT   (writes 'm a b c ...' lines for every branch d, t', every decomposition, in my own order)
Decompositions: own partition-first brute force (ref_decomp.py)."""
import sys, re, itertools, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref_decomp import decompositions_bf
celldir, n, m, t, D, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
def load(n_, m_, t_, D_):
    if (n_, m_) == (1, 0): return [[]]
    p = os.path.join(celldir, 'cell_%d_%d_%d_D%d.txt' % (n_, m_, t_, D_))
    if not os.path.exists(p): raise SystemExit('missing cell file %s' % p)
    reps = []; done = False
    for l in open(p):
        if l.startswith('FOUND:'):
            es = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
            assert len(es) == m_, (p, l)
            assert all(0 <= v < n_ for e in es for v in e)
            reps.append(es)
        if l.startswith('INFO '): done = True
    assert done, p
    return reps
out = open(outp, 'w'); total = 0
import math
for d in range(max(1, -(-3 * m // n)), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0 or tp < 0: continue
        decs = decompositions_bf(n - 1, m - d, Sp)
        for dec in decs:
            from collections import Counter
            cnt = Counter(dec); gl = []
            for typ, k in sorted(cnt.items()):
                cls = load(typ[0], typ[1], typ[2], d)
                gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), k))))
            c = 0
            for combo in itertools.product(*[g[2] for g in gl]):
                es = []; off = 0
                for (typ, cls, _), idxs in zip(gl, combo):
                    for i in idxs:
                        es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                assert off == n - 1 and len(es) == m - d
                out.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); c += 1
            print('d=%d tp=%d Sp=%d %s: %d inputs' % (d, tp, Sp, list(dec), c)); total += c
print('TOTAL', total)
