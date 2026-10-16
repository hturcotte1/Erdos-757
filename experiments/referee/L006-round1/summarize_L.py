import json, sys, gzip
rows = {r['class']: r for r in (json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz', 'rt'))}
rs = [json.loads(l) for l in open(sys.argv[1])]
want = [int(x) for x in open('/home/user/Erdos-757/experiments/referee/L006-round1/routeL_classes.txt').read().split(',')]
done = [r['tag'] for r in rs]
print('classes requested', len(want), 'done', len(rs), 'all requested done:', sorted(done) == sorted(want))
print('known sets included:', all(k in done for k in (20392, 23942, 18917)))
print('all A (4,5):', all(r['A_is_45'] for r in rs), ' h values:', sorted({r['h'] for r in rs}))
print('n_max_sidon equal to stored rows:', all(r['n_max_sidon'] == rows[r['tag']]['n_max_sidon'] for r in rs))
print('lines per T (min,max):', min(r['lines_per_T_min_max'][0] for r in rs), max(r['lines_per_T_min_max'][1] for r in rs))
print('deficient points total', sum(r['n_points'] for r in rs), 'per class min/max', min(r['n_points'] for r in rs), max(r['n_points'] for r in rs))
print('deficient (4,5) points total:', sum(r['n_points_45'] for r in rs))
cl = [r for r in rs if r['n_common_lines']]
print('classes with common deficient lines:', len(cl), 'total common lines', sum(r['n_common_lines'] for r in rs),
      'generic-(4,5) common lines:', sum(len(r['common_lines_generic_45']) for r in rs))
from collections import Counter
shape = Counter()
for r in rs:
    for a, b, c in r['common_lines']:
        shape[(a, b)] += 1
print('common line directions (a,b) of a*x+b*y=c:', dict(shape))
print('max secs', max(r['secs'] for r in rs), 'total secs', round(sum(r['secs'] for r in rs)))
for k in (20392, 23942, 18917):
    r = next(r for r in rs if r['tag'] == k)
    print('known class', k, {f: r[f] for f in ('h', 'n_max_sidon', 'n_common_lines', 'n_points', 'n_points_45', 'secs')})
