"""Build the inputs G of one engine branch: usage build_inputs.py CELLDIR n m t d tp > inputs.txt
Decompositions of (n-1, m-d) with total slack S' = 3(n-1)+2(m-d)-11tp by the referee's decomp_ref.decomps; every multiset of
representatives (combinations with replacement for repeated types) from CELLDIR/cell_nK_mK_tK_D<d>.txt; components placed on
consecutive vertex blocks.  Output lines: 'k a1 b1 c1 ...'.  Per-decomposition counts on stderr."""
import sys, os, re, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp_ref import decomps
celldir = sys.argv[1]; n, m, t, d, tp = map(int, sys.argv[2:7])
Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
assert Sp >= 0
def load(k):
    if k == (1, 0, 0): return [[]]
    fn = os.path.join(celldir, 'cell_%d_%d_%d_D%d.txt' % (k[0], k[1], k[2], d))
    if not os.path.exists(fn): raise SystemExit('MISSING cell file %s' % fn)
    L = []; done = False
    for l in open(fn):
        if l.startswith('FOUND'): L.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
        if l.startswith('INFO') or l.startswith('SUMMARY'): done = True
    if not done: raise SystemExit('INCOMPLETE cell file %s' % fn)
    return L
total = 0
for dec in decomps(n - 1, m - d, Sp):
    groups = {}
    for c in dec: groups[c] = groups.get(c, 0) + 1
    gl = [(typ, load(typ), k) for typ, k in sorted(groups.items())]
    combos = [list(itertools.combinations_with_replacement(range(len(L)), k)) for (typ, L, k) in gl]
    cnt = 0
    for combo in itertools.product(*combos):
        es = []; off = 0
        for (typ, L, k), idxs in zip(gl, combo):
            for i in idxs:
                es += [tuple(v + off for v in e) for e in L[i]]; off += typ[0]
        assert off == n - 1
        print('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es)); cnt += 1
    total += cnt
    sys.stderr.write('  %s inputs %d\n' % (list(dec), cnt))
sys.stderr.write('branch (%d,%d,%d) d=%d tp=%d S\'=%d: %d decompositions, %d inputs\n' % (n, m, t, d, tp, Sp, len(decomps(n - 1, m - d, Sp)), total))
