"""Abstract dataset tuples. usage: build_abstract.py census|witnesses|fresh|census_all500"""
import random, time, glob
from common import *
which = sys.argv[1]
def emit(path, rows):
    with gzip.open(path, 'wt') as f:
        for r in rows: f.write(json.dumps(r) + '\n')
def process(items, mode, param, src):
    # items: list of (name, n, edges)
    out = []
    for s in range(0, len(items), 1000):
        ch = items[s:s + 1000]
        res = run_tuples([(i, n, [mask(e) for e in E], mode, param) for i, (name, n, E) in enumerate(ch)])
        for i, (name, n, E) in enumerate(ch):
            out.append(dict(src=src, name=name, n=n, m=len(E), edges=E, tuples=res[i]))
    return out
t0 = time.time()
if which == 'census':
    L = [json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
    rows = process([(f'c{i}', 12, e) for i, e in enumerate(L)], 1, 2, 'census')
    emit('abstract_census_tuples.jsonl.gz', rows)
elif which == 'census_all500':
    L = [json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
    random.seed(757); idx = random.sample(range(len(L)), 500)
    rows = process([(f'c{i}', 12, L[i]) for i in idx], 3, 0, 'census_all500')
    emit('abstract_census_all500_tuples.jsonl.gz', rows)
elif which == 'witnesses':
    W = json.load(open('/home/user/Erdos-757/experiments/20261014-0500-slack-landscape/witnesses.json'))
    items = []
    for kind, d in W.items():
        for k, w in d.items():
            items.append((f'{kind}:{k}', w['n'], w['edges']))
    rows = process(items, 1, 2, 'witness')
    emit('abstract_witness_tuples.jsonl.gz', rows)
elif which == 'fresh':
    rows = []
    for f in sorted(glob.glob('fresh_*.json')):
        g = json.load(open(f))
        rows += process([(f"{g['cls']}_{g['n']}_{g['m']}_{g['T']}#{i}", g['n'], e) for i, e in enumerate(g['sols'])], 1, 2, 'fresh_' + g['cls'])
        print(f, g['status'], len(g['sols']))
    emit('abstract_fresh_tuples.jsonl.gz', rows)
print(which, len(rows), 'hypergraphs', round(time.time() - t0, 1), 's')
