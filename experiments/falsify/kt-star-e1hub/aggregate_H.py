import json, glob, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hubs
reg = hubs.Registry(); by = collections.Counter(); minP = {}; inL = collections.Counter(); neg = 0
for f in ['main_others.jsonl'] + sorted(glob.glob('main_25_15_9.part*.jsonl')):
    for l in open(f):
        d = json.loads(l)
        if d['type'] != 'H': continue
        rec, new = reg.lookup(d['n'], [tuple(e) for e in d['H']])
        if not new: continue
        k = '(%d,%d,%d)' % (d['n'], d['m'], d['tau']); by[k] += 1
        minP[k] = min(minP.get(k, 99), d['P'])
        if d['piece']: inL[d['piece'].split('#')[0]] += 1
        elif d['Pp'] < 0 or d['P'] < 0: neg += 1
res = dict(distinct_hub_classes=sum(by.values()), by_cell=dict(by), minP=minP, hubs_in_Lstar=dict(inL), counterexamples=neg)
json.dump(res, open('hubs_global.json', 'w'), indent=1); print(json.dumps(res))
