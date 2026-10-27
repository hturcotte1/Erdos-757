"""Collect results.json from out/cells (INFO lines) and gzip the class lists of the new cells."""
import os, json, re, gzip, glob, tarfile
H = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(H, 'out', 'cells'); S = os.path.join(H, 'cells_seed')
TARGETS = ['17_13_7_D4', '20_14_8_D4', '21_18_9_D4', '24_19_10_D4', '27_20_11_D3']
def info(fn):
    n = 0; inf = None
    for l in open(fn):
        if l.startswith('FOUND:'): n += 1
        elif l.startswith('INFO '): inf = json.loads(l[5:])
    return n, inf
res = {'targets': {}, 'new_cells': {}}; new = []
for fn in sorted(glob.glob(C + '/cell_*.txt')):
    b = os.path.basename(fn)
    if os.path.exists(os.path.join(S, b)): continue
    key = b[5:-4]; n, inf = info(fn); new.append(fn)
    rec = dict(classes=n, route=inf.get('route'), secs=inf.get('secs'))
    if inf.get('route') == 'recurse':
        rec['branches'] = [dict(d=br['d'], tp=br['tp'], Sp=br['Sp'], decompositions=br['decompositions'], inputs=br['inputs'], dec=br['dec'],
                                nodes=br.get('ext', {}).get('nodes'), hits_F7free=br.get('ext', {}).get('hits_F7free'), hits_in_C=br.get('hits_in_C'), bad_tau=br.get('ext', {}).get('bad_tau'))
                           for br in inf['branches']]
        rec['connected_hits'] = inf.get('connected_hits')
    else: rec['enum'] = inf.get('enum')
    res['new_cells'][key] = rec
    if key in TARGETS: res['targets'][key] = rec
with tarfile.open(os.path.join(H, 'cells_new.tar.gz'), 'w:gz') as t:
    for fn in new: t.add(fn, arcname='cells_new/' + os.path.basename(fn))
os.makedirs(os.path.join(H, 'lists'), exist_ok=True)
for k in TARGETS:
    fn = os.path.join(C, 'cell_%s.txt' % k)
    if os.path.exists(fn):
        with open(fn, 'rb') as f, gzip.open(os.path.join(H, 'lists', 'cell_%s.txt.gz' % k), 'wb') as g: g.write(f.read())
res['n_new_cells'] = len(new)
json.dump(res, open(os.path.join(H, 'results.json'), 'w'), indent=1, default=str)
print('new cells', len(new), 'targets', {k: v['classes'] for k, v in res['targets'].items()})
