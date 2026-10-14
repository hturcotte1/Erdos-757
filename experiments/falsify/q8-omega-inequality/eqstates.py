import json, collections
from q8lib import *
d = json.load(open(os.path.join(HERE, '..', '..', '..', 'data', 'small_records.json')))['sets']
out = {}
for key in ['14', '12', '12b', '12c']:
    A = d[key]['set']; n = len(A)
    r = run_cases([(1, n, masks_of(A), 3, 0, 0)], vcap=10**7, printeq=True)[1]
    full = (1 << n) - 1
    byD = collections.Counter(); ex = []
    for line in r['eq']:
        f = dict(x.split('=') for x in line.split())
        D = int(f['D']); S = int(f['S'])
        byD[bin(D).count('1')] += 1
        if D == 0 or bin(D).count('1') == 1: ex.append((decode(D, A), int(f['tau']), int(f['e1']), int(f['e2'])))
    out[key] = dict(S_full_states=r['states'], eq_total=r['eqQ'], eq_by_Dsize=dict(byD), eq_examples_Dle1=ex[:20], slack_hist_Sfull=None)
    print(key, r['states'], r['eqQ'], dict(sorted(byD.items())), [e for e in ex if not e[0]])
json.dump(out, open('eqstates_results.json', 'w'), default=str)
