"""Referee L012 round 3: inputs for one recursion branch of a cell, built from MY brute-force decompositions and the prover's lower
cell lists (consistency with the engine's INFO is checked by arith.py).  cell (n,m,t,D), branch d: G = X - w has (n-1, m-d), tau' = t-1
(the only branch with S' >= 0 for the cells treated here; asserted), components with max degree <= d from cells cell_*_D{d}.
Usage: python3 build_branch_inputs.py n m t D d celldir > inputs"""
import sys, os, re, itertools, math
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L012-round3/src')
from arith import decomps
n, m, t, D, d = map(int, sys.argv[1:6]); celldir = sys.argv[6]
assert math.ceil(3 * m / n) <= d <= D
tp = t - 1; Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
assert Sp >= 0 and 3 * (n - 1) + 2 * (m - d) - 11 * t < 0, 'only the tp = t-1 branch is handled here'
decs = sorted(decomps(n - 1, m - d, Sp))
print('# cell', (n, m, t, D), 'branch d=%d tp=%d Sp=%d' % (d, tp, Sp), 'decompositions', len(decs), file=sys.stderr)
def load(typ):
    if typ == (1, 0, 0): return [[]]
    fn = os.path.join(celldir, 'cell_%d_%d_%d_D%d.txt' % (typ[0], typ[1], typ[2], d))
    if not os.path.exists(fn): print('# MISSING cell file', fn, file=sys.stderr); return None
    return [[tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in open(fn) if l.startswith('FOUND:')]
out = []
for dec in decs:
    groups = {}
    for typ in dec: groups[typ] = groups.get(typ, 0) + 1
    gl = []
    ok = True
    for typ, k in sorted(groups.items()):
        reps = load(typ)
        if reps is None: ok = False; break
        gl.append((typ, reps, list(itertools.combinations_with_replacement(range(len(reps)), k))))
    if not ok: continue
    cnt = 0
    for combo in itertools.product(*[g[2] for g in gl]):
        es = []; off = 0
        for (typ, reps, _), idxs in zip(gl, combo):
            for i in idxs: es += [tuple(v + off for v in e) for e in reps[i]]; off += typ[0]
        assert off == n - 1
        out.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es)); cnt += 1
    print('#  ', list(dec), 'inputs', cnt, file=sys.stderr)
print('# total inputs', len(out), file=sys.stderr)
print('\n'.join(out))
