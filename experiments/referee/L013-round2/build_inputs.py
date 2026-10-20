"""Referee: build the inputs of one engine branch from a cell directory, using the referee's own decompositions (decomp_ref).
Usage: build_inputs.py CELLDIR n m t d tp [--perm SEED] > inputs.txt   (format: 'k a b c a b c ...' on n-1 vertices)
Each input = disjoint union of one representative per component (multisets for repeated types); with --perm the vertex labels of
every input are permuted randomly (counts of extensions are labelling-invariant)."""
import sys, os, re, itertools, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp_ref import decomps
from collections import Counter
CD = sys.argv[1]; n, m, t, d, tp = map(int, sys.argv[2:7])
perm = None
if '--perm' in sys.argv: perm = random.Random(int(sys.argv[sys.argv.index('--perm') + 1]))
def load(typ):
    if typ == (1, 0, 0): return [[]]
    p = os.path.join(CD, 'cell_%d_%d_%d_D%d.txt' % (typ + (d,)))
    nn, mm, tt = typ
    if not os.path.exists(p):
        if mm == 0 or tt < 1 or tt > mm or nn > 2 * mm + 1 or mm > nn - 2 or 17 * tt > 5 * nn + 3 * mm: return []
        raise SystemExit('missing cell file ' + p)
    out = []; done = False
    for l in open(p):
        if l.startswith('FOUND:'): out.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
        if l.startswith('INFO'): done = True
    assert done
    return out
Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
assert Sp >= 0
cnt = 0; per = []
for dec in decomps(n - 1, m - d, Sp):
    c = Counter(dec); groups = []
    for typ in sorted(c): groups.append((typ, load(typ), c[typ]))
    choices = [list(itertools.combinations_with_replacement(range(len(L)), k)) for (typ, L, k) in groups]
    k0 = 0
    for combo in itertools.product(*choices):
        es = []; off = 0
        for (typ, L, k), idxs in zip(groups, combo):
            for i in idxs:
                es += [tuple(v + off for v in e) for e in L[i]]; off += typ[0]
        assert off == n - 1
        if perm is not None:
            pi = list(range(n - 1)); perm.shuffle(pi); es = [tuple(sorted(pi[v] for v in e)) for e in es]; perm.shuffle(es)
        print('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es)); k0 += 1
    per.append((list(dec), k0)); cnt += k0
sys.stderr.write('branch (%d,%d,%d) d=%d tp=%d Sp=%d decompositions=%d inputs=%d\n' % (n, m, t, d, tp, Sp, len(per), cnt))
for dec, k0 in per: sys.stderr.write('   %s %d\n' % (dec, k0))
