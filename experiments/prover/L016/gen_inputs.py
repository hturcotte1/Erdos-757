"""(L014) python3 gen_inputs.py n m t D OUTFILE [TAGFILE]
Writes the ext_d input lines of every branch of the recursion cell (n,m,t,D) exactly as engine.recurse / stream.recurse build them
(same branches, engine.decompositions, component lists engine.cell(.., d) loaded from CELLDIR (must exist: nothing is computed),
combinations_with_replacement, product in sorted-type order, consecutive vertex blocks).  Prints per branch/decomposition the sizes.
If TAGFILE is given, writes one line per input: its decomposition index and the class indices (for stratified sampling)."""
import os, sys, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
def no_compute(*a): raise RuntimeError('cell missing in CELLDIR: %s' % (a,))
engine.direct = no_compute; engine.recurse = no_compute
n, m, t, D = map(int, sys.argv[1:5]); out = open(sys.argv[5], 'w'); tagf = open(sys.argv[6], 'w') if len(sys.argv) > 6 else None
total = 0
for d in range(max(1, math.ceil(3 * m / n)), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0 or tp < 0: continue
        decs = engine.decompositions(n - 1, m - d, Sp)
        for di, dec in enumerate(decs):
            groups = {}
            for c in dec: groups[c] = groups.get(c, 0) + 1
            gl = []
            for typ, k in sorted(groups.items()):
                cls = engine.cell(typ[0], typ[1], typ[2], d)
                gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), k))))
            cnt = 0
            for combo in itertools.product(*[g[2] for g in gl]):
                es = []; off = 0
                for (typ, cls, _), idxs in zip(gl, combo):
                    for i in idxs:
                        es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                assert off == n - 1
                out.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
                if tagf: tagf.write('d=%d tp=%d dec=%d %s\n' % (d, tp, di, ' '.join(str(list(x)) for x in combo)))
            print('branch d=%d tp=%d S=%d decomposition %d %s: %d inputs' % (d, tp, Sp, di, list(dec), cnt)); total += cnt
print('TOTAL inputs', total)
