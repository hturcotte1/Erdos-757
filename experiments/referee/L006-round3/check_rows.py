"""Referee round 3, L006: stored rows vs census and quoted totals; choose rerun sample. Own code; imports nothing from the repo."""
import gzip, json, random, sys
ROOT = '/home/user/Erdos-757'
cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
rows = [json.loads(l) for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt')]
print('census entries', len(cen), 'rows', len(rows))
byc = {}
for r in rows:
    assert r['class'] not in byc, 'duplicate class %s' % r['class']
    byc[r['class']] = r
assert sorted(byc) == list(range(len(cen))), 'class ids not 0..N-1'
bad = [c for c in byc if byc[c]['set'] != sorted(cen[c]['set'])]
print('set mismatches', len(bad))
# census self-consistency (own recomputation of m and 4-point distances is done elsewhere)
assert all(len(e['set']) == 12 and e['h'] == 7 for e in cen)
assert all(len(e['edges']) == 10 for e in cen)
tot = dict(single=0, t1b=0, isect_pts=0, isect45=0, evaluated=0, n2ext=0)
mm = {k: [10**9, -1] for k in ('n_single_45', 'n_t1b_45', 'n_max_sidon', 't2_isect_pts', 'Px_size', 't1_pairs')}
anomalies = []
for c, r in byc.items():
    ok = (r['hA'] == 7 and r['t2_line_h'] == [9] and r['t2_lines'] == 36 and r['t2_isect_45'] == 0 and r['records'] == []
          and r['min_h'] == 9 and r['t2_precheck'] is False and r['in_all_max_sidon'] == []
          and r['hist'] == {'9': r['n_single_45'] + r['n_t1b_45'] + 36} and r['n_2ext'] == r['n_t1b_45'] + r['t2_isect_45'])
    if not ok: anomalies.append(c)
    tot['single'] += r['n_single_45']; tot['t1b'] += r['n_t1b_45']; tot['isect_pts'] += r['t2_isect_pts']
    tot['isect45'] += r['t2_isect_45']; tot['evaluated'] += sum(r['hist'].values()); tot['n2ext'] += r['n_2ext']
    for k in mm:
        mm[k][0] = min(mm[k][0], r[k]); mm[k][1] = max(mm[k][1], r[k])
print('row anomalies', len(anomalies), anomalies[:10])
print('totals', tot)
print('ranges', mm)
summ = json.load(open(ROOT + '/experiments/20261016-0330-ext12-all/summary.json'))
print('summary.json', summ)
assert summ['total_single_45'] == tot['single'] and summ['total_t1b_45'] == tot['t1b'] and summ['total_2ext_45'] == tot['n2ext']
assert summ['classes_processed'] == len(rows)
# quoted numbers in the proof
assert tot['single'] == 1887566 and tot['t1b'] == 51264727 and tot['isect_pts'] == 19247288 and tot['isect45'] == 0
assert 54243 * 36 == 1952748 and tot['evaluated'] == 55105041
assert mm['n_single_45'] == [21, 46] and mm['n_t1b_45'] == [424, 1395] and mm['n_max_sidon'] == [48, 63]
print('ALL QUOTED TOTALS/RANGES CONFIRMED')
# rerun sample, my own choice: extremes of each counter (first and last attaining class), last classes, a few early (pre-restart) ones,
# known classes (20392, 23942, 18917 per round 1; re-identified independently in rerun script), seeded random (seed 3141592)
pick = set()
for k in mm:
    for v in mm[k]:
        att = sorted(c for c, r in byc.items() if r[k] == v)
        pick.add(att[0]); pick.add(att[-1])
pick |= {54242, 54241, 54240, 27121, 3, 141, 277, 20392, 23942, 18917}
rnd = random.Random(3141592)
while len(pick) < 64:
    pick.add(rnd.randrange(len(cen)))
pick = sorted(pick)
json.dump(pick, open(ROOT + '/experiments/referee/L006-round3/rerun_ids.json', 'w'))
print('rerun ids (%d):' % len(pick), pick)
