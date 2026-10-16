"""Referee round 3: rerun the AUTHORS' extend_all.process (unmodified, loaded by path) on a sample of classes
chosen by this referee, and compare every output field except 'secs' with the stored row of results.jsonl.
Usage: python3 rerun_authors.py OUT.json"""
import gzip, importlib.util, json, os, random, sys, time
from multiprocessing import Pool

ROOT = '/home/user/Erdos-757'
EXP = os.path.join(ROOT, 'experiments', '20261015-2340-ext14-all')
spec = importlib.util.spec_from_file_location('extend_all', os.path.join(EXP, 'extend_all.py'))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)

FIXED = [2440, 729, 857, 960, 1951, 2437, 2879, 1524, 2564, 2096, 2621, 1631, 1007, 235, 2892, 2697, 226]
rng = random.Random(20261016)
RAND = sorted(rng.sample([i for i in range(2910) if i not in FIXED], 14))
CLASSES = FIXED + RAND

def work(a):
    try: os.nice(10)
    except Exception: pass
    return E.process(a)

def main():
    out = sys.argv[1]
    sets = {}
    with gzip.open(os.path.join(ROOT, 'data', 'census_n14_m12_classes.jsonl.gz'), 'rt') as f:
        for i, line in enumerate(f):
            if i in CLASSES: sets[i] = json.loads(line)['set']
    stored = {}
    for line in open(os.path.join(EXP, 'results.jsonl')):
        r = json.loads(line)
        if r['class'] in sets: stored[r['class']] = r
    t0 = time.time(); mism = []; rows = []
    with Pool(2) as pool:
        for r in pool.imap_unordered(work, [(i, sets[i]) for i in CLASSES]):
            st = stored[r['class']]
            keys = (set(r) | set(st)) - {'secs'}
            bad = [k for k in sorted(keys) if r.get(k) != st.get(k)]
            if bad: mism.append((r['class'], bad))
            rows.append({k: r[k] for k in ('class', 'hA', 'n_max_sidon', 'Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45',
                                           't2_lines', 't2_line_h', 't2_isect_pts', 't2_isect_45', 'min_h', 'records')})
            print(r['class'], 'ok' if not bad else ('MISMATCH', bad), r['secs'], flush=True)
    rows.sort(key=lambda r: r['class'])
    json.dump({'classes': CLASSES, 'random_part': RAND, 'mismatches': mism, 'rows': rows,
               'wall': round(time.time() - t0, 1)}, open(out, 'w'), indent=1)
    print('classes', len(CLASSES), 'mismatches', mism, 'wall', round(time.time() - t0, 1))
    # also the --abase-test literal set
    r = E.process((0, [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]))
    print('abase-test', {k: r[k] for k in ('Px_size','n_single_45','t1_pairs','n_t1b_45','t2_lines','t2_line_h','t2_isect_pts','t2_isect_45','n_max_sidon','min_h','hist')})

if __name__ == '__main__':
    main()
