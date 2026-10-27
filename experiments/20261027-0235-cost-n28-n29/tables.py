import json, math, os
import plan2
import model
from model import *
orig_exists = lambda k: os.path.exists(os.path.join(plan2.CELLS, 'cell_%d_%d_%d_D%d.txt' % k))
names = ('n28', 'n29rec', 'n29full', 'rec25')
scen = {'central': dict(mult_y=1, mult_npi=1, rate=1e6), 'low': dict(mult_y=1 / 2.7, mult_npi=1 / 3, rate=3e6), 'high': dict(mult_y=2.7, mult_npi=3, rate=1e6)}
res = {}
for nm in names:
    seen = build(tops_for(nm)); res[nm] = dict(seen=seen)
    for sc, kw in scen.items(): res[nm][sc] = evaluate(seen, **kw)
cells = {}
for nm in names:
    for k in res[nm]['seen']:
        cells.setdefault(k, set()).add(nm)
tops = {nm: tops_for(nm) for nm in names}
lines = ['cell\tslack\tstatus\tclasses(exact or est)\tinputs_est\tcore_h_low\tcore_h_central\tcore_h_high\ttargets']
rec = []
for k in sorted(cells, key=lambda k: (k[0], k[1], k[3])):
    nm0 = sorted(cells[k])[0]; seen = res[nm0]['seen']
    s = 3 * k[0] + 2 * k[1] - 11 * k[2]
    if orig_exists(k): status = 'EXISTING (L012-L016 lists)'; cl = KNOWN.get(k); cs = [0, 0, 0]
    elif k in KNOWN: status = 'COMPUTED here/by d4 worker'; cl = KNOWN[k]; cs = [0, 0, 0]
    else:
        status = 'NEW (estimated)'; est, cost = res[nm0]['central']; cl = round(est[k], 1)
        cs = [res[nm0][sc][1][k] / 3600 for sc in ('low', 'central', 'high')]
    inp = ''
    if status.startswith('NEW'):
        # inputs estimate from the central evaluation
        est, cost = res[nm0]['central']; ts = 0.0
        for b in seen[k]['branches']:
            for dec in b['decs']:
                if dec['comps'] is None: continue
                sz = 1.0
                for ck, kk in dec['comps']:
                    c = KNOWN.get(ck, est.get(ck, 0.0)); sz *= ncomb(c, kk)
                ts += sz
        inp = '%.0f' % ts
    if status.startswith('NEW') or k in set(sum(tops.values(), [])):
        lines.append('\t'.join(map(str, [k, s, status, cl, inp, '%.3f' % cs[0], '%.3f' % cs[1], '%.3f' % cs[2], ','.join(sorted(cells[k]))])))
        rec.append(dict(cell=list(k), slack=s, status=status, classes=cl, inputs=inp, core_hours=dict(low=cs[0], central=cs[1], high=cs[2]), targets=sorted(cells[k])))
open('cells_table.tsv', 'w').write('\n'.join(lines) + '\n')
json.dump(rec, open('cells_table.json', 'w'), indent=1)
print(len(rec), 'rows')
