import os, math
import plan2, model
from model import *
orig = lambda k: os.path.exists(os.path.join(plan2.CELLS, 'cell_%d_%d_%d_D%d.txt' % k))
out = []
def st(k, est):
    if orig(k): return 'old:%d' % KNOWN[k]
    if k in KNOWN: return 'now:%d' % KNOWN[k]
    return 'NEW~%d' % est.get(k, 0)
for nm in ('n28', 'n29rec', 'n29full', 'rec25'):
    seen = build(tops_for(nm)); est, cost = evaluate(seen)
    out.append('=== target %s tops %s' % (nm, tops_for(nm)))
    for k in tops_for(nm):
        v = seen[k]; n, m, t, D = k
        out.append('top %s slack %d: %d branches' % (k, 3*n+2*m-11*t, len(v['branches'])))
        for b in v['branches']:
            items = []
            tot = 0.0
            for dec in b['decs']:
                if dec['comps'] is None: continue
                sz = 1.0
                for ck, kk in dec['comps']:
                    c = KNOWN.get(ck, est.get(ck, 0.0)); sz *= ncomb(c, kk)
                tot += sz
                items.append((sz, '+'.join('%dx%s[%s]' % (kk, ck[:3], st(ck, est)) for ck, kk in dec['comps']) or 'isolated only'))
            items.sort(key=lambda x: -x[0])
            out.append('   branch d=%d tau\'=%d remainder (%d,%d) slack %d: %d decompositions, inputs ~%.0f; largest: %s' % (b['d'], b['tp'], n-1, m-b['d'], b['Sp'], b['ndec'], tot, '; '.join('%s=%.0f' % (x[1], x[0]) for x in items[:3])))
open('branches.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out)[:6000])
