import sys, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from t3_check import check_vertex
L = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
summary = {}
for i, c in enumerate(L):
    n, m, t, es = c['n'], c['m'], c['tau'], [tuple(e) for e in c['edges']]
    s = hg.slack(n, m, t); d = hg.degrees(n, es)
    per = {}
    for v in range(n):
        if d[v] == 3:
            st = {}
            fails, pat, cells, ny = check_vertex(n, es, t, s, v, st)
            key = pat + ':' + '+'.join('(%d,%d,%d)' % x[:3] for x in sorted(cells))
            per[key] = per.get(key, 0) + 1
    k = tuple(sorted(per.items()))
    summary[k] = summary.get(k, 0) + 1
    print(i, per, flush=True)
print('distinct per-class pattern profiles:')
for k, v in summary.items():
    print(v, k)
