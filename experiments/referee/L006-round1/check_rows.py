"""Referee L006: integrity check of stored per-class rows vs census and the claimed totals.
No import of e757 or of the authors' code."""
import gzip, json, sys, hashlib
from collections import Counter
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'
ROWS = '/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz'
JL = '/home/user/Erdos-757/experiments/20261016-0330-ext12-all/results.jsonl'
cen = json.load(gzip.open(CENSUS, 'rt'))
rows = [json.loads(l) for l in gzip.open(ROWS, 'rt')]
print('census', len(cen), 'rows', len(rows))
cls = Counter(r['class'] for r in rows)
assert len(cls) == len(rows) == len(cen) == 54243, 'count'
assert set(cls) == set(range(54243)), 'class ids'
bad = 0
tot = Counter()
mins = {}
for r in rows:
    c = r['class']
    if sorted(r['set']) != sorted(cen[c]['set']): bad += 1
    assert r['hA'] == 7
    assert r['t2_line_h'] == [9] and r['t2_lines'] == 36
    assert r['t2_isect_45'] == 0 and r['records'] == [] and r['min_h'] == 9
    assert list(r['hist'].keys()) == ['9'], r['hist']
    assert r['hist']['9'] == r['n_single_45'] + r['n_t1b_45'] + 36, (c, r['hist'], r['n_single_45'], r['n_t1b_45'])
    assert r['n_2ext'] == r['n_t1b_45']
    assert r['t2_precheck'] is False and r['in_all_max_sidon'] == []
    for k in ('n_single_45', 'n_t1b_45', 't2_isect_pts', 'Px_size', 't1_pairs', 'n_max_sidon'):
        tot[k] += r[k]
        lo, hi = mins.get(k, (10**18, -1))
        mins[k] = (min(lo, r[k]), max(hi, r[k]))
print('set mismatches vs census:', bad)
print('totals:', dict(tot))
print('min/max:', mins)
print('total evaluated values (T1a+T1b+T2 lines):', tot['n_single_45'] + tot['n_t1b_45'] + 36 * len(rows))
# compare with uncompressed results.jsonl (git-ignored), if present
try:
    jl = [json.loads(l) for l in open(JL)]
    print('results.jsonl lines', len(jl), 'distinct classes', len({r['class'] for r in jl}))
    d1 = {r['class']: json.dumps({k: v for k, v in r.items() if k != 'secs'}, sort_keys=True) for r in rows}
    d2 = {r['class']: json.dumps({k: v for k, v in r.items() if k != 'secs'}, sort_keys=True) for r in jl}
    print('rows == results.jsonl (ignoring secs):', d1 == d2)
    print('first 285 classes in results.jsonl order:', [r['class'] for r in jl[:285]][:20], '... max of first 280:', max(r['class'] for r in jl[:280]), 'sorted first280 == range?', sorted(r['class'] for r in jl[:280]) == list(range(280)))
except FileNotFoundError:
    print('results.jsonl not present')
