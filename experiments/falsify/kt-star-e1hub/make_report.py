#!/usr/bin/env python3
import json, glob, os, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))
inv = json.load(open('inventory.json'))
cells = {}
PARTS = sorted(glob.glob('main_25_15_9.part*.jsonl'))
for f in ['main_others.jsonl'] + PARTS:
    for l in open(f):
        d = json.loads(l)
        if d['type'] == 'cell':
            if d['cell'] in cells and f in PARTS:
                c = cells[d['cell']]
                for x in ('graphs', 'bconf_labelled', 'graphs_with_bconf', 'hub_classes_new', 'hub_inC', 'notinT_low_vertices'): c[x] += d[x]
                for kk, vv in d['hubs_by_cell'].items(): c['hubs_by_cell'][kk] = c['hubs_by_cell'].get(kk, 0) + vv
                c['minP'] = min(c['minP'], d['minP']) if c['minP'] is not None and d['minP'] is not None else (c['minP'] if d['minP'] is None else d['minP'])
            else: cells[d['cell']] = d
Hs = []
for f in ['main_others.jsonl'] + PARTS:
    if os.path.exists(f):
        for l in open(f):
            d = json.loads(l)
            if d['type'] == 'H': Hs.append(d)
res = dict(main=dict(cells={}, total_graphs=0, total_bconf=0, total_hub_classes_in_C3=0, min_P=None, hits=0))
M = res['main']
rows = []
for k in sorted(inv, key=lambda k: eval(k)):
    v = inv[k]; c = cells.get(k)
    if not v['count']: continue
    if c is None: rows.append((k, v['A'], v['D'], v['count'], 'NOT RUN')); continue
    M['cells'][k] = {x: c.get(x) for x in ('A', 'D', 'graphs', 'bconf_labelled', 'graphs_with_bconf', 'hub_classes_new', 'hub_inC', 'hubs_by_cell', 'minP', 'minPp_nonpiece', 'notinT_low_vertices')}
    M['total_graphs'] += c['graphs']; M['total_bconf'] += c['bconf_labelled']; M['total_hub_classes_in_C3'] += c['hub_inC']
    if c['minP'] is not None and (M['min_P'] is None or c['minP'] < M['min_P']): M['min_P'] = c['minP']
    rows.append((k, c['A'], c['D'], c['graphs'], c['bconf_labelled'], c['graphs_with_bconf'], c['hub_inC'], c['hubs_by_cell'], c['minP']))
M['empty_or_zero_graph_cells'] = [k for k in inv if not inv[k]['count']]
def stat(f):
    return json.load(open(f)) if os.path.exists(f) else None
res['iterate_level2'] = [stat(f) for f in sorted(glob.glob('iter2*.jsonl.stats.json'))]
res['fhub'] = stat('fhub.jsonl.stats.json')
res['unions_vext'] = [stat(f) for f in sorted(glob.glob('uv_*.stats.json'))]
res['union_small'] = 'see union_small.log'
json.dump(res, open('results.json', 'w'), indent=1)
with open('cell_table.md', 'w') as f:
    f.write('| cell (n,m,tau) | A | list D | classes scanned | b-configs (labelled) | classes with b-config | hubs in C_3 (iso classes) | hub cells | min P |\n|---|---|---|---|---|---|---|---|---|\n')
    for r in rows: f.write('| ' + ' | '.join(str(x) for x in r) + ' |\n')
    f.write('\nCells in the stored lists with A<=15 and zero classes (empty or no connected Delta<=3 member): %s\n' % ', '.join(M['empty_or_zero_graph_cells']))
print(json.dumps({k: v for k, v in M.items() if k != 'cells'}, indent=1))
