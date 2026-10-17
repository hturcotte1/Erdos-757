"""cells_table.tsv for the NEW cells only (not in seed_cells.txt) of out/cells, plus results.json."""
import os, json, re
from collect import table
HERE = os.path.dirname(os.path.abspath(__file__))
seeded = set(open(os.path.join(HERE, 'seed_cells.txt')).read().split())
rows = table(os.path.join(HERE, 'out', 'cells'))
new = [r for r in rows if 'cell_%d_%d_%d_D%d.txt' % r['cell'] not in seeded]
with open('cells_table.tsv', 'w') as f:
    f.write('n\tm\ttau\tDelta\tclasses\troute\tsecs\tbad_tau\n')
    for r in new: f.write('\t'.join(map(str, list(r['cell']) + [r['classes'], r['route'], r['secs'], r['bad_tau']])) + '\n')
top = [json.loads(l) for l in open(os.path.join(HERE, 'results_cells.jsonl'))]
res = dict(top_level=top, new_cells=new, total_bad_tau=sum(r['bad_tau'] for r in new), n_new=len(new), n_seeded=len(seeded))
json.dump(res, open('results.json', 'w'), indent=1)
print(len(new), 'new cells; seeded', len(seeded), '; total bad_tau', res['total_bad_tau'], '; nonempty new cells with n>=23:', [r['cell'] for r in new if r['cell'][0] >= 23 and r['classes']])
