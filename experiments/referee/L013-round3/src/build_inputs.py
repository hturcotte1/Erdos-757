"""build_inputs.py n m t D d tp cellsdir [decomp-filter]: inputs of the engine branch (d, tp) of cell (n,m,t,D), rebuilt from the
cell files in cellsdir with MY decomposition generator: every decomposition of (n-1, m-d) with total slack S' = 3(n-1)+2(m-d)-11 tp,
every multiset of representatives (combinations with replacement per type), components on consecutive vertex blocks.
Prints 'k a b c ...' lines; per-decomposition counts to stderr."""
import sys, os, re, itertools, math
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp_lib import my_decomps
n, m, t, D, d, tp = map(int, sys.argv[1:7]); cells = sys.argv[7]
Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
assert Sp >= 0 and max(1, math.ceil(3 * m / n)) <= d <= D and tp in (t - 1, t)
def load(key):
    if key[:2] == (1, 0): return [[]]
    p = os.path.join(cells, 'cell_%d_%d_%d_D%d.txt' % key)
    if not os.path.exists(p): sys.exit('missing cell file %s' % p)
    reps = []
    for l in open(p):
        if l.startswith('FOUND:'): reps.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
    return reps
total = 0
for dec in sorted(my_decomps(n - 1, m - d, Sp)):
    cnt = {}
    for ty in dec: cnt[ty] = cnt.get(ty, 0) + 1
    groups = [(ty, load((ty[0], ty[1], ty[2], d)), k) for ty, k in sorted(cnt.items())]
    size = 1
    for ty, cls, k in groups: size *= comb(len(cls) + k - 1, k)
    print('DECOMP', list(dec), 'inputs', size, file=sys.stderr); total += size
    if size == 0: continue
    for combo in itertools.product(*[itertools.combinations_with_replacement(range(len(cls)), k) for ty, cls, k in groups]):
        es = []; off = 0
        for (ty, cls, k), idxs in zip(groups, combo):
            for i in idxs:
                es += [tuple(v + off for v in e) for e in cls[i]]; off += ty[0]
        assert off == n - 1 and len(es) == m - d
        print('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
print('TOTAL inputs', total, file=sys.stderr)
