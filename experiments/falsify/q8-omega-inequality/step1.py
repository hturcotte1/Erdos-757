import json, time
from q8lib import *
d = json.load(open(os.path.join(HERE, '..', '..', '..', 'data', 'small_records.json')))['sets']
out = {}
for key in ['8', '10', '11', '12', '12b', '12c', '14']:
    A = d[key]['set']; n = len(A)
    t = time.time()
    r = run_cases([(1, n, masks_of(A), 0, 0, 0)], vcap=100)[1]
    r['time'] = time.time() - t; r['n'] = n; r['A'] = A
    out[key] = r
    print(key, n, {k: v for k, v in r.items() if k in ('states', 'violQ', 'violAct', 'violD4', 'eqQ', 'time')},
          'minQ', min(r['hist']['Q']), 'minA', min(r['hist']['A']), 'minD4', min(r['hist']['D']), flush=True)
json.dump(out, open(os.path.join(HERE, 'step1_results.json'), 'w'))
