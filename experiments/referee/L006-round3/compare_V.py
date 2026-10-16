"""Summarize Route V and compare with (i) the authors' stored rows (n_max_sidon) and (ii) round-1 Route L on overlapping classes."""
import json, gzip, sys
from math import gcd
def norm(a, b, c):
    g = gcd(gcd(a, b), c); a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0): a, b, c = -a, -b, -c
    return (a, b, c)
V = [json.loads(l) for l in open(sys.argv[1])]
ids = json.load(open('routeV_ids.json'))
st = {}
for l in gzip.open('/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz', 'rt'):
    r = json.loads(l); st[r['class']] = r
L = {r['tag']: r for r in map(json.loads, open('../L006-round1/routeL_600.jsonl'))}
print('Route V classes done', len(V), 'of', len(ids), '; distinct', len({r['tag'] for r in V}))
print('k=7 for all:', all(r['k'] == 7 for r in V), '; n_maxT == stored n_max_sidon for all:', all(r['n_maxT'] == st[r['tag']]['n_max_sidon'] for r in V))
print('deficient points: total', sum(r['deficient_points'] for r in V), 'min/max', min(r['deficient_points'] for r in V), max(r['deficient_points'] for r in V))
print('deficient (4,5) points: total', sum(len(r['deficient_45_points']) for r in V))
cls = [r for r in V if r['common_lines']]
print('classes with common deficient lines', len(cls), '; lines', sum(len(r['common_lines']) for r in V),
      '; generically (4,5) lines', sum(len(r['common_lines_generic45']) for r in V))
from collections import Counter
shape = Counter()
for r in V:
    for c in r['common_lines']:
        a, b, _ = c['line']; shape[(a, b)] += 1
print('common line shapes (a,b) of a x + b y = c:', dict(shape), '; generic min ndist values', Counter(c['generic_min_ndist'] for r in V for c in r['common_lines']))
ov = [r for r in V if r['tag'] in L]
pt_eq = sum(1 for r in ov if r['deficient_points'] == L[r['tag']]['n_points'])
ln_eq = sum(1 for r in ov if {tuple(c['line']) for c in r['common_lines']} == {norm(*c) for c in L[r['tag']]['common_lines']})
print('overlap with round-1 Route L:', len(ov), 'classes; equal common-line sets', ln_eq, '; equal deficient-point counts', pt_eq)
diff = [(r['tag'], r['deficient_points'], L[r['tag']]['n_points'], len(r['common_lines'])) for r in ov if r['deficient_points'] != L[r['tag']]['n_points']]
print('point-count differences (class, V, L, #common lines):', diff[:20])
print('known classes:', [(r['tag'], r['deficient_points'], len(r['common_lines']), len(r['deficient_45_points'])) for r in V if r['tag'] in (20392, 23942, 18917)])
print('max secs', max(r['secs'] for r in V))
