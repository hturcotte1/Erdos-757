import json, re, os, hashlib, glob
HERE = os.path.dirname(os.path.abspath(__file__))
def h(p):
    L = [l.rstrip('\n') for l in open(p) if l.startswith('FOUND:')]; return hashlib.md5('\n'.join(sorted(L)).encode()).hexdigest(), len(L)
rows = []
for l in open(os.path.join(HERE, 'progress.tsv')).read().splitlines()[1:]:
    f = l.split('\t')
    if not f[0].startswith('(') or len(f) < 8: continue
    if not f[1].isdigit(): continue
    rows.append(dict(cell=f[0], classes=int(f[1]), inputs=f[2], nodes=f[3], seconds=f[4], bad_tau=f[5], hits_in_C=f[6], route=f[7], utc=f[8] if len(f) > 8 else ''))
with open(os.path.join(HERE, 'cells_table.tsv'), 'w') as o:
    o.write('cell\tclasses\tinputs\tnodes\tseconds\tbad_tau\thits_in_C\troute\tutc\n')
    for r in rows: o.write('\t'.join(str(r[k]) for k in ['cell','classes','inputs','nodes','seconds','bad_tau','hits_in_C','route','utc']) + '\n')
# independent recomputation from refereed seeds
cmp = {}
for ks in open(os.path.join(HERE, 'ref2_keys.txt')).read().split():
    k = tuple(map(int, ks.split(',')))
    a = os.path.join(HERE, 'out/cells/cell_%d_%d_%d_D%d.txt' % k); b = os.path.join(HERE, 'out/cells_ref2/cell_%d_%d_%d_D%d.txt' % k)
    if os.path.exists(b) and not os.path.islink(b): cmp[ks] = 'SAME (%d classes)' % h(b)[1] if h(a) == h(b) else 'DIFFERENT'
    else: cmp[ks] = 'not finished'
need = json.load(open(os.path.join(HERE, 'needed_cells.json')))
res = {'tags': '[verified-here] as an UNREFEREED computation (exact integer/combinatorial)',
       'n28': {'violator_cells_required': need['n28']['tops'], 'all_empty': need['n28']['all_violator_tops_empty'], 'closure_cells': len(need['n28']['closure']), 'closure': need['n28']['closure']},
       'n29': {'violator_cells_required': need['n29']['tops'], 'all_empty': need['n29']['all_violator_tops_empty'], 'closure_cells': len(need['n29']['closure']), 'closure': need['n29']['closure']},
       'record_cell_25_23_11': {'cell(25,23,11,4)': 6, 'cell(25,23,11,3)': 0, 'realizable': 0, 'realize': 'realize_rec.txt: 6 graphs, 325400 assignments, 21831 distinct-valued, 0 realizations; min_extra_APs 8'},
       'f19_cells': {'cell(19,17,8,5)': 785127, 'by max degree': {'3': 29898, '4': 667007, '5': 88222}, 'cell(19,16,8,4)': 956, 'cell(18,12,7,5)': 0},
       'cell_21_19_9_D4': 31268,
       'independent_recomputation_from_refereed_seeds': cmp,
       'computed_cells': rows}
json.dump(res, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
print(len(rows), 'rows;', {k: v for k, v in cmp.items() if not v.startswith('SAME')})
