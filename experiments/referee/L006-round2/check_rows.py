"""Referee round 2: integrity of data/ext12_all_rows.jsonl.gz versus the census and the proof's totals.
Own code; no imports of e757 or the authors' scripts."""
import gzip, json, sys
from itertools import combinations
ROOT = '/home/user/Erdos-757'
cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
rows = [json.loads(l) for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt')]
print('census entries', len(cen), 'rows', len(rows))
ids = [r['class'] for r in rows]
assert sorted(ids) == list(range(len(cen))), 'class ids not a permutation of 0..N-1'
byid = {r['class']: r for r in rows}
bad = 0
for i, c in enumerate(cen):
    r = byid[i]
    if sorted(r['set']) != sorted(c['set']): bad += 1
print('set mismatches', bad)
# per-row invariants
def chk(cond, msg, cnt={}):
    if not cond: cnt[msg] = cnt.get(msg, 0) + 1
    return cnt
fails = {}
for r in rows:
    for cond, msg in [(r['hA'] == 7, 'hA'), (r['t2_line_h'] == [9], 't2_line_h'), (r['t2_lines'] == 36, 't2_lines'),
                      (r['t2_isect_45'] == 0, 't2_isect_45'), (r['records'] == [], 'records'), (r['min_h'] == 9, 'min_h'),
                      (r['t2_precheck'] is False, 'precheck'), (r['in_all_max_sidon'] == [], 'core'),
                      (list(r['hist'].keys()) == ['9'], 'histkeys'),
                      (r['hist'].get('9') == r['n_single_45'] + r['n_t1b_45'] + 36, 'histcount'),
                      (r['n_2ext'] == r['n_t1b_45'] + r['t2_isect_45'], 'n_2ext'), (len(r['set']) == 12, 'n12')]:
        if not cond: fails[msg] = fails.get(msg, 0) + 1
print('per-row invariant failures', fails)
tot = lambda k: sum(r[k] for r in rows)
mm = lambda k: (min(r[k] for r in rows), max(r[k] for r in rows))
print('total n_single_45', tot('n_single_45'), 'range', mm('n_single_45'))
print('total n_t1b_45', tot('n_t1b_45'), 'range', mm('n_t1b_45'))
print('total t2_isect_pts', tot('t2_isect_pts'), 'range', mm('t2_isect_pts'))
print('total t2_isect_45', tot('t2_isect_45'))
print('n_max_sidon range', mm('n_max_sidon'), 'Px_size range', mm('Px_size'), 't1_pairs total', tot('t1_pairs'))
print('T2 line hypergraphs', tot('t2_lines'), '= 54243*36 ->', 54243 * 36)
print('evaluated values (hist sum)', sum(sum(r['hist'].values()) for r in rows))
print('summary.json:', json.load(open(ROOT + '/experiments/20261016-0330-ext12-all/summary.json')))
# census-side: each set (4,5) and h=7 with my own Sidon-definition code on a sample (full pass done by round 1)
