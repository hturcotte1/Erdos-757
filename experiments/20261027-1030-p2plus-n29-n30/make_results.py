"""Collect results of the run: python3 make_results.py   (reads out/progress.jsonl, out/cells/cell_<target>.txt)"""
import json, os, re, gzip, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import parse, analyze
TARGETS = [(29,23,12,3), (30,27,13,3)]
prog = [json.loads(l) for l in open('out/progress.jsonl')] if os.path.exists('out/progress.jsonl') else []
done = {tuple(p['cell']): p for p in prog}
res = dict(targets={}, new_cells=[dict(cell=p['cell'], classes=p['classes'], secs=p['secs']) for p in prog])
os.makedirs('lists', exist_ok=True)
for t in TARGETS:
    f = 'out/cells/cell_%d_%d_%d_D%d.txt' % t
    if t not in done or not os.path.exists(f):
        res['targets'][str(t)] = dict(status='NOT COMPUTED (timeout / not reached)'); continue
    cls = [parse(l) for l in open(f) if l.startswith('FOUND')]
    rs = [analyze(e) for e in cls]
    hist = {}
    for r in rs: hist[r['n_deg1']] = hist.get(r['n_deg1'], 0) + 1
    res['targets'][str(t)] = dict(status='COMPLETE', classes=len(cls), secs=done[t]['secs'], n_deg1_hist=dict(sorted(hist.items())),
        pendant_b_total=sum(r['pendant_b'] for r in rs), classes_with_pendant_b=sum(1 for r in rs if r['pendant_b']),
        deg_hists=sorted({json.dumps(r['deg_hist']) for r in rs}),
        ge3=[dict(edges=cls[i], n_deg1=rs[i]['n_deg1'], deg1=rs[i]['deg1']) for i in range(len(rs)) if rs[i]['n_deg1'] >= 3])
    with gzip.open('lists/cell_%d_%d_%d_D%d.txt.gz' % t, 'wt') as g:
        g.write(open(f).read())
json.dump(res, open('results.json', 'w'), indent=1)
print(json.dumps(res['targets'], indent=1)[:3000])
