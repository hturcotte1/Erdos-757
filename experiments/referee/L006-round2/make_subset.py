"""Pick rerun classes for referee round 2: random (own seed) + near-extreme stress classes, avoiding round-1 classes."""
import gzip, json, random, hashlib
ROOT = '/home/user/Erdos-757'
cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt'))}
r1 = set(range(280))
for f in ('routeL_classes.txt', 'routeC_classes.txt'):
    r1 |= {int(t) for t in open(ROOT + '/experiments/referee/L006-round1/' + f).read().replace('\n', ',').split(',') if t.strip()}
r1 |= {0, 1, 7, 100, 199, 279, 418, 6457, 8742, 11223, 11415, 12070, 15115, 16812, 18917, 19428, 20392, 23942, 25237, 25977, 26883,
       29101, 30076, 30954, 30965, 33737, 34495, 34895, 35897, 36474, 36745, 38437, 43511, 44635, 46367, 47725, 48192, 48213, 54136, 54241}
print('round-1 classes to avoid:', len(r1))
seed = int.from_bytes(hashlib.sha256(b'L006 referee round 2, 2026-10-16').digest()[:8], 'big')
rng = random.Random(seed)
pool = [c for c in range(len(cen)) if c not in r1]
pick = set(rng.sample(pool, 400))
stress = set()
for k in ('n_single_45', 'n_t1b_45', 't2_isect_pts', 'n_max_sidon', 'Px_size', 't1_pairs', 'secs'):
    order = sorted(rows, key=lambda c: (rows[c][k], c))
    lo = [c for c in order if c not in r1][:3]; hi = [c for c in order[::-1] if c not in r1][:3]
    stress |= set(lo) | set(hi)
stress |= {280, 281, 282, 283, 54240, 54242}
pick |= stress
pick = sorted(pick)
print('picked', len(pick), 'stress', sorted(stress))
json.dump(pick, open(ROOT + '/experiments/referee/L006-round2/rerun_ids.json', 'w'))
with gzip.open(ROOT + '/experiments/referee/L006-round2/rerun_subset.json.gz', 'wt') as f:
    json.dump([cen[c] for c in pick], f)
