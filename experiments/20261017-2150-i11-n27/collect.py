"""Collect the cell results (progress.tsv + out/cells) into results.json and cells_table.tsv."""
import os, json, re, glob
H = os.path.dirname(os.path.abspath(__file__)); cells = {}
seed = set(open(os.path.join(H, 'seed_cells.txt')).read().split())
for p in sorted(glob.glob(os.path.join(H, 'out', 'cells', 'cell_*.txt'))):
    b = os.path.basename(p); n, m, t, D = map(int, re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt', b).groups())
    if b in seed: continue
    cnt = 0; info = {}
    for l in open(p):
        if l.startswith('FOUND:'): cnt += 1
        if l.startswith('INFO '): info = json.loads(l[5:])
    inputs = sum(x.get('inputs', 0) for x in info.get('branches', [])); bad = sum(x.get('ext', {}).get('bad_tau', 0) for x in info.get('branches', []))
    nodes = sum(x.get('ext', {}).get('nodes', 0) for x in info.get('branches', []))
    cells['(%d,%d,%d,%d)' % (n, m, t, D)] = dict(classes=cnt, secs=info.get('secs'), route=info.get('route'), inputs=inputs, bad_tau=bad, ext_nodes=nodes)
json.dump(dict(new_cells=cells, n_new=len(cells)), open(os.path.join(H, 'results.json'), 'w'), indent=1)
with open(os.path.join(H, 'cells_table.tsv'), 'w') as f:
    f.write('cell\tclasses\tsecs\troute\tinputs\tbad_tau\text_nodes\n')
    for k, v in sorted(cells.items(), key=lambda kv: eval(kv[0])): f.write('\t'.join(map(str, [k, v['classes'], v['secs'], v['route'], v['inputs'], v['bad_tau'], v['ext_nodes']])) + '\n')
print(len(cells), 'new cells')
