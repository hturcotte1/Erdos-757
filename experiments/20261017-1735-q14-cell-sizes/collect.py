"""Builds results.json from out/cells (new cells), progress.tsv, samples.jsonl, ext22_progress.log."""
import json, os, re, hashlib
H = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(H, 'out', 'cells')
new = ['14_10_5', '11_9_4', '15_13_6', '17_11_6', '20_12_7', '18_14_7', '21_15_8', '19_17_8', '22_18_9', '23_21_10']
cells = {}
for k in new:
    p = os.path.join(C, 'cell_%s_D3.txt' % k)
    if not os.path.exists(p): cells[k] = None; continue
    info = {}; n = 0
    for l in open(p):
        if l.startswith('FOUND:'): n += 1
        if l.startswith('INFO '): info = json.loads(l[5:])
    br = [dict(d=b['d'], tp=b['tp'], inputs=b.get('inputs'), nodes=b.get('ext', {}).get('nodes'), hits_F7free=b.get('ext', {}).get('hits_F7free'), hits_in_C=b.get('hits_in_C')) for b in info.get('branches', []) if b.get('inputs')]
    cells[k] = dict(classes=n, secs=info.get('secs'), route=info.get('route'), connected_hits=info.get('connected_hits'), branches=br, labelled=info.get('labelled'),
                    sha256_16=hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16], bytes=os.path.getsize(p))
samples = [json.loads(l) for l in open(os.path.join(H, 'samples.jsonl'))]
prog = [l.rstrip('\n').split('\t') for l in open(os.path.join(H, 'progress.tsv'))]
json.dump(dict(cells=cells, progress=prog, samples=samples), open(os.path.join(H, 'results.json'), 'w'), indent=1)
print(json.dumps({k: (v and (v['classes'], v['secs'])) for k, v in cells.items()}))
