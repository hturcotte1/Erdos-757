"""choose the classes for the rerun of the authors' code: 24 seeded-random + A_base (2440) + extremes of each counter"""
import json, random
rows = [json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261015-2340-ext14-all/results.jsonl')]
rng = random.Random(20261016)
pick = set(rng.sample(range(len(rows)), 24))
pick.add(2440)
ext = {}
for key in ('Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 'n_max_sidon', 't2_isect_pts'):
    lo = min(rows, key=lambda r: (r[key], r['class']))['class']
    hi = max(rows, key=lambda r: (r[key], -r['class']))['class']
    ext[key] = (lo, hi)
    pick.add(lo); pick.add(hi)
pick.add(0); pick.add(len(rows) - 1)
print(json.dumps({'extremes': ext, 'classes': sorted(pick)}))
