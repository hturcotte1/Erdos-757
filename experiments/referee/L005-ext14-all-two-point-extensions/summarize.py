"""Summaries of the two full referee runs (Route C: cases_all.jsonl, Route L: locus_all.jsonl) against the authors' results.jsonl."""
import json
from collections import Counter
stored = {json.loads(l)['class']: json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261015-2340-ext14-all/results.jsonl')}
# Route C
rc = {}
for l in open('cases_all.jsonl'):
    r = json.loads(l)
    rc[r['class']] = r
keys = ('Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 't2_isect_pts', 't2_isect_45', 'n_max_sidon')
mism = [c for c, r in rc.items() if any(r[k] != stored[c][k] for k in keys)]
defi = [c for c, r in rc.items() if r['t1a_deficient'] or r['t1b_deficient'] or r['universal'] or r['t2_isect_def'] or r['hA'] != 8]
hist = Counter()
for r in rc.values():
    for k, v in r['t1b_hist'].items():
        hist[k] += v
out = {'routeC_classes': len(rc), 'routeC_ids_complete': sorted(rc) == list(range(2910)),
       'routeC_counter_mismatches_vs_stored': len(mism), 'routeC_classes_with_any_deficiency': len(defi),
       'routeC_sums': {k: sum(r[k] for r in rc.values()) for k in keys},
       'routeC_t1b_h_histogram': dict(hist),
       'routeC_cpu_secs': round(sum(r['secs'] for r in rc.values()))}
# Route L
rl = {}
dup_mismatch = 0
import os
for fn in ('locus_all.jsonl', 'locus_all_b.jsonl', 'locus_all_c.jsonl'):
    if not os.path.exists(fn):
        continue
    for l in open(fn):
        r = json.loads(l)
        if r['class'] in rl:
            a = dict(rl[r['class']]); b = dict(r); a.pop('secs'); b.pop('secs')
            if a != b:
                dup_mismatch += 1
        rl[r['class']] = r
# a real problem would be: h != 8, a whole line of D without a symbolic non-(4,5) witness (flagged), or a (4,5) isolated point
anom = [c for c, r in rl.items() if r['h'] != 8 or r['whole']['flagged'] or r['n_pts_45'] != 0
        or r['whole']['excluded_X=a'] != 14 or r['whole']['excluded_Y=a'] != 14 or r['whole']['excluded_X=Y'] != 1]
# benign: extra whole lines (beyond the 29 excluded ones) that carry a symbolic witness (every point non-(4,5))
extra = {c: [r['n_whole'], r['whole']['other_with_witness'], r['whole_witness_examples']] for c, r in rl.items()
         if r['whole']['other_with_witness']}
out['routeL_classes_with_extra_witnessed_whole_lines'] = extra
iso = [r['n_isolated_pts'] for r in rl.values()]
out.update({'routeL_duplicate_rows_disagreeing': dup_mismatch, 'routeL_classes': len(rl), 'routeL_ids_complete': sorted(rl) == list(range(2910)),
            'routeL_anomalies': len(anom), 'routeL_isolated_points_range': [min(iso), max(iso)],
            'routeL_isolated_points_total': sum(iso), 'routeL_pts45_total': sum(r['n_pts_45'] for r in rl.values()),
            'routeL_nS_matches_stored': all(r['nS'] == stored[c]['n_max_sidon'] for c, r in rl.items()),
            'routeL_selftested_classes': sum(1 for c in rl if c % 97 == 0),
            'routeL_cpu_secs': round(sum(r['secs'] for r in rl.values())),
            'abase_2440': {k: rl[2440][k] for k in ('nS', 'n_whole', 'n_isolated_pts', 'n_pts_45')} if 2440 in rl else None})
print(json.dumps(out, indent=1))
json.dump(out, open('summary.json', 'w'), indent=1)
