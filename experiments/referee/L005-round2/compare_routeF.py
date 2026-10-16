import json, glob
loc = {}
for f in sorted(glob.glob('/home/user/Erdos-757/experiments/referee/L005-ext14-all-two-point-extensions/locus_all*.jsonl')):
    for l in open(f):
        r = json.loads(l); loc[r['class']] = r
R = [json.loads(l) for f in ['routeF_0.jsonl', 'routeF_1.jsonl'] for l in open(f)]
rows = {json.loads(l)['class']: json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261015-2340-ext14-all/results.jsonl')}
mis = []; nonzero_witnessed = []
for r in R:
    c = r['class']; L = loc[c]
    if r['n_D_points'] != L['n_isolated_pts'] or r['nS'] != L['nS'] or r['nS'] != rows[c]['n_max_sidon']:
        mis.append((c, r['n_D_points'], L['n_isolated_pts'], r['nS'], L['nS']))
    if r['whole']['witnessed']:
        nonzero_witnessed.append((c, r['whole']['witnessed'], L['whole']['other_with_witness'], r['whole_examples'][:1]))
summ = {'classes': len(R), 'distinct': len({r['class'] for r in R}),
        'selftest_points': sum(r['selftest_points'] for r in R), 'selftest_bad': sum(r['selftest_bad'] for r in R),
        'D_points_total': sum(r['n_D_points'] for r in R), 'D_points_range': [min(r['n_D_points'] for r in R), max(r['n_D_points'] for r in R)],
        'D_points_45': sum(r['n_D_points_45'] for r in R), 'flagged_whole': sum(len(r['whole']['flagged']) for r in R),
        'fraction_candidates': sum(r['n_fraction_candidates'] for r in R), 'candidates_total': sum(r['n_candidates'] for r in R),
        'mismatch_vs_round1_locus': mis, 'classes_with_witnessed_whole_lines': nonzero_witnessed,
        'cpu_secs': round(sum(r['secs'] for r in R), 1)}
json.dump(summ, open('routeF_summary.json', 'w'), indent=1)
print(json.dumps(summ, indent=1))
