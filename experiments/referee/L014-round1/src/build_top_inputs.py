"""Referee L014 r1: rebuild the inputs of the top branch (d=3, t'=9, S'=3) of cell(23,21,10,3) from the prover's cell files,
independently of engine.py/gen_inputs.py.  Decompositions are given explicitly (re-derived by hand in the review and by
src/decomp_bf.py).  Usage: python3 build_top_inputs.py CELLDIR > inputs.txt ; counts to stderr."""
import sys, re, itertools
CD = sys.argv[1]
def load(n, m, t, D=3):
    if (n, m, t) == (1, 0, 0): return [[]]
    reps = []; info = False
    with open('%s/cell_%d_%d_%d_D%d.txt' % (CD, n, m, t, D)) as f:
        for l in f:
            if l.startswith('FOUND:'):
                es = [tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]
                assert len(es) == m, (n, m, t, l)
                assert all(0 <= v < n for e in es for v in e)
                reps.append(es)
            elif l.startswith('INFO'): info = True
    assert info, 'incomplete cell file'
    return reps
DECS = [[(22, 18, 9)], [(21, 18, 9), (1, 0, 0)], [(10, 8, 4), (12, 10, 5)], [(8, 6, 3), (14, 12, 6)], [(3, 1, 1), (19, 17, 8)]]
tot = 0
for dec in DECS:
    lists = [load(*t) for t in dec]       # all types distinct within each decomposition: plain product
    assert len(set(dec)) == len(dec)
    cnt = 0
    for combo in itertools.product(*lists):
        es = []; off = 0
        for typ, g in zip(dec, combo):
            es += [(a + off, b + off, c + off) for (a, b, c) in g]; off += typ[0]
        assert off == 22 and len(es) == 18
        print(len(es), ' '.join('%d %d %d' % e for e in es)); cnt += 1
    print('DEC', dec, 'sizes', [len(x) for x in lists], 'inputs', cnt, file=sys.stderr); tot += cnt
print('TOTAL inputs', tot, file=sys.stderr)
