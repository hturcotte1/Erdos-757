"""Rerun the authors' unmodified extend_all.process on a referee-chosen sample; compare with stored rows."""
import gzip, importlib.util, json, random, sys, time
ROOT = '/home/user/Erdos-757'
EXP = ROOT + '/experiments/20261015-2340-ext14-all'
spec = importlib.util.spec_from_file_location('extend_all', EXP + '/extend_all.py')
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
rows = {}
for line in open(EXP + '/results.jsonl'):
    r = json.loads(line); rows[r['class']] = r
census = [json.loads(l)['set'] for l in gzip.open(ROOT + '/data/census_n14_m12_classes.jsonl.gz', 'rt')]
R = list(rows.values())
pick = {2440}
pick.add(max(R, key=lambda r: r['t1_pairs'])['class'])
pick.add(max(R, key=lambda r: r['n_t1b_45'])['class'])
pick.add(min(R, key=lambda r: r['n_t1b_45'])['class'])
pick.add(max(R, key=lambda r: r['secs'])['class'])
rng = random.Random(1016)
pick |= set(rng.sample(range(2910), 9))
pick = sorted(pick)
print('picked', pick, flush=True)
bad = 0
for idx in pick:
    t = time.time()
    r = E.process((idx, census[idx]))
    st = rows[idx]
    diff = [k for k in st if k != 'secs' and st[k] != r.get(k)]
    if diff: bad += 1
    print(idx, 'n_t1b_45', r['n_t1b_45'], 't1_pairs', r['t1_pairs'], 'isect', r['t2_isect_pts'], 'min_h', r['min_h'], 'diff', diff, f'{time.time()-t:.1f}s', flush=True)
print('classes with differences:', bad)
