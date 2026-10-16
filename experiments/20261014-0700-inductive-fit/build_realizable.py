"""Realizable dataset: record sets (all 3^n states) + random saturated realizable sets n=12,14 (|D|<=2)."""
import random, time
from common import *
from e757.core import KNOWN, ap_edges
from e757.anneal import random_linear_map, evaluate
from e757.saturated import to_integers
def hyp(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [tuple(sorted((idx[a], idx[b], idx[c]))) for a, b, c in ap_edges(A)]
recs = {}
for k, v in KNOWN.items():
    A = v if isinstance(v, (list, tuple)) else v.get('set', v)
    recs[k] = sorted(A)
for k, v in json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets'].items():
    recs['rec' + k] = sorted(v['set'])
# dedupe by set
seen = {}
for k, A in recs.items():
    seen.setdefault(tuple(A), k)
recs = {k: list(A) for A, k in seen.items()}
print('record sets:', {k: len(A) for k, A in recs.items()})
rows = []
for k, A in recs.items():
    E = hyp(A); n = len(A)
    t = time.time()
    r = run_tuples([(0, n, [mask(e) for e in E], 0, 0)])[0]
    print(k, n, len(E), 'distinct tuples', len(r), round(time.time() - t, 1), flush=True)
    rows.append(dict(src='record', name=k, n=n, m=len({e[1] for e in E}), edges=E, set=A, tuples=r))
rng = random.Random(757)
for n in (12, 14):
    got = 0; tries = 0
    while got < 300:
        tries += 1
        mp = random_linear_map(n, rng); ev = evaluate(mp)
        if not ev['is45']: continue
        A = sorted(to_integers(ev['vals'])); E = hyp(A)
        r = run_tuples([(0, n, [mask(e) for e in E], 1, 2)])[0]
        rows.append(dict(src=f'rand{n}', name=f'rand{n}_{got}', n=n, m=len({e[1] for e in E}), edges=E, set=A, tuples=r)); got += 1
    print('random', n, got, 'of', tries, flush=True)
with gzip.open('realizable_tuples.jsonl.gz', 'wt') as f:
    for r in rows: f.write(json.dumps(r) + '\n')
