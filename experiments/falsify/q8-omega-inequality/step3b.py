# 3-piece amalgam chains/trees (<=31 points): pieces glued at random vertices (each new piece glued to a random existing point)
import json, random, collections, time
from q8lib import *
from e757.anneal import is45_ints
d = json.load(open(os.path.join(HERE, '..', '..', '..', 'data', 'small_records.json')))['sets']
pieces = {k: d[k]['set'] for k in ['8', '10', '11', '12', '12b', '12c']}
rng = random.Random(77)
cases = []; meta = []; tried = 0
while len(cases) < 300 and tried < 20000:
    tried += 1
    names = [rng.choice(['12', '12b', '12c', '11', '10', '8', '12', '12b', '12c']) for _ in range(3)]
    tot = sum(len(pieces[k]) for k in names) - 2
    if tot > 31: continue
    pts = list(pieces[names[0]])
    for k in names[1:]:
        B = pieces[k]; x = rng.choice(pts); y = rng.choice(B); q = rng.choice([1, -1]) * rng.choice([3001, 4099, 6007, 8209, 12007, 20011])
        pts = sorted(set(pts) | {x + q * (b - y) for b in B})
    if len(pts) != tot or not is45_ints(pts): continue
    cases.append((len(cases), len(pts), masks_of(pts), 2, 20000, len(cases) + 1)); meta.append((names, pts))
print('built', len(cases), 'tried', tried, flush=True)
res = run_cases(cases, vcap=50)
tot = collections.Counter(); hist = collections.Counter()
for i, r in res.items():
    for k in ('states', 'violQ', 'violAct', 'violD4', 'eqQ'): tot[k] += r[k]
    for s, c in r['hist']['Q'].items(): hist[s] += c
print(dict(tot), 'min slack', min(hist), sorted(hist.items())[:5])
json.dump(dict(tot=dict(tot), hist_lowest=sorted(hist.items())[:8], n_cases=len(cases), meta=meta[:5]), open(os.path.join(HERE, 'step3b_results.json'), 'w'))
