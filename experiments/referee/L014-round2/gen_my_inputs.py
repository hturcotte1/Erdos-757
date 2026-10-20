"""Referee L014 round 2: build the inputs G = X - w of one recursion branch from the prover's cell lists (files only read),
with MY decompositions (arith_decomp.decomps_bf).  Output lines 'N M a b c ...' for bin/myext.
usage: python3 gen_my_inputs.py CELLDIR n m t D d tp OUTFILE"""
import sys, os, re, itertools
from math import ceil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arith_decomp import decomps_bf, slack
def load_cell(celldir, n, m, t, D):
    if (n, m, t) == (1, 0, 0): return [[]]
    fn = os.path.join(celldir, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    if not os.path.exists(fn): raise SystemExit('missing cell file ' + fn)
    reps = []; info = False
    for l in open(fn):
        if l.startswith('FOUND:'):
            es = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
            assert len(es) == m and all(0 <= v < n for e in es for v in e), (fn, l)
            assert sorted(set(v for e in es for v in e)) == list(range(n)), ('rep does not use all vertices', fn, l)
            reps.append(es)
        elif l.startswith('INFO '): info = True
    assert info, ('incomplete cell file', fn)
    return reps
if __name__ == '__main__':
    celldir = sys.argv[1]; n, m, t, D, d, tp = map(int, sys.argv[2:8]); outf = sys.argv[8]
    Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
    assert Sp >= 0 and ceil(3 * m / n) <= d <= D
    decs = decomps_bf(n - 1, m - d, Sp, True)
    total = 0
    with open(outf, 'w') as fo:
        for dec in decs:
            groups = {}
            for c in dec: groups[c] = groups.get(c, 0) + 1
            gl = []
            for typ in sorted(groups):
                cls = load_cell(celldir, typ[0], typ[1], typ[2], d)
                gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), groups[typ]))))
            cnt = 0
            for combo in itertools.product(*[g[2] for g in gl]):
                es = []; off = 0
                for (typ, cls, _), idxs in zip(gl, combo):
                    for i in idxs:
                        es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                assert off == n - 1 and len(es) == m - d
                fo.write('%d %d ' % (n - 1, len(es)) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
            print('DEC', list(dec), 'sizes', [len(g[1]) for g in gl], 'inputs', cnt)
            total += cnt
    print('BRANCH key', (n, m, t, D), 'd=%d tp=%d Sp=%d decompositions=%d inputs=%d' % (d, tp, Sp, len(decs), total))
