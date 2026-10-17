import json, collect, os
from arith import analyse
rows = collect.table('out/cells'); rows25 = collect.table('out/cells25')
def jl(p): return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
top = jl('results_cells.jsonl'); top25 = jl('results_cells_n25.jsonl'); xc = jl('crosscheck_results.jsonl')
known = {k: next(r['classes'] for r in rows if r['cell'] == k) for k in [(12, 10, 5, 3), (10, 7, 4, 3)]}
res = dict(
  arithmetic={str(n): analyse(n) for n in (23, 24, 25)},
  engine_top_cells_n23_n24=top, engine_bonus_n25=top25,
  cells_touched_n23_n24=[dict(cell=list(r['cell']), classes=r['classes'], route=r['route'], secs=r['secs'], bad_tau=r['bad_tau']) for r in rows],
  cells_touched_n25_bonus_count=len(rows25), bad_tau_total=sum(r['bad_tau'] for r in rows) + sum(r['bad_tau'] for r in rows25),
  known_counts=dict((str(k), v) for k, v in known.items()), known_counts_expected={'(12, 10, 5, 3)': 149, '(10, 7, 4, 3)': 4},
  crosscheck=xc,
  conclusions={'I11 holds on C for n = 23': 'YES' if all(t['classes'] == 0 for t in top if t['cell'][0] == 23) else 'NO',
               'I11 holds on C for n = 24': 'YES' if all(t['classes'] == 0 for t in top if t['cell'][0] == 24) else 'NO',
               'I11 holds on C for n = 25 (bonus)': 'YES' if len(top25) == 3 and all(t['classes'] == 0 for t in top25) else 'UNDECIDED'})
json.dump(res, open('results.json', 'w'), indent=1)
print(json.dumps(res['conclusions']), res['known_counts'], 'bad_tau_total', res['bad_tau_total'], 'crosschecks', [(c['cell'], c['equal']) for c in xc])
