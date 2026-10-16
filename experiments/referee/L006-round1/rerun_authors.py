"""Rerun the UNMODIFIED authors' process() from extend12_all.py on chosen classes; compare with stored rows (all fields except secs).
Also run process() on the three known sets as given in data/small_records.json (affine-invariant counters must match the census class rows)."""
import gzip, json, sys, os, random, hashlib, time
from multiprocessing import Pool
AUTH = '/home/user/Erdos-757/experiments/20261016-0330-ext12-all'
sys.path.insert(0, AUTH)
import extend12_all as E
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'
ROWS = '/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz'
def work(a):
    return E.process(a)
if __name__ == '__main__':
    os.nice(0)
    print('sha256 extend12_all.py', hashlib.sha256(open(os.path.join(AUTH, 'extend12_all.py'), 'rb').read()).hexdigest())
    cen = json.load(gzip.open(CENSUS, 'rt'))
    rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROWS, 'rt'))}
    pick = {20392, 23942, 18917, 0, 1, 7, 100, 199, 279, 12070, 25977, 34895}
    for k in ('n_single_45', 'n_t1b_45', 'n_max_sidon', 't2_isect_pts', 'Px_size', 't1_pairs'):
        vals = sorted(rows, key=lambda c: (rows[c][k], c))
        pick.add(vals[0]); pick.add(vals[-1])
    rng = random.Random(20261016)
    while len(pick) < 40:
        pick.add(rng.randrange(54243))
    pick = sorted(pick)
    print('classes', len(pick), pick)
    t0 = time.time()
    with Pool(3) as pool:
        res = pool.map(work, [(c, cen[c]['set']) for c in pick])
    ok = 0
    for r in res:
        st = rows[r['class']]
        a = {k: v for k, v in r.items() if k != 'secs'}
        b = {k: v for k, v in st.items() if k != 'secs'}
        same = json.loads(json.dumps(a)) == b
        ok += same
        if not same:
            print('MISMATCH', r['class'], {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)})
    print(f'rerun: {ok}/{len(res)} classes identical to stored rows (all fields except secs); {time.time()-t0:.1f}s')
    # known sets via --known path equivalent
    inv = ('hA', 'n_max_sidon', 't2_precheck', 'Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 't2_line_h', 't2_lines', 't2_isect_pts', 't2_isect_45', 'hist', 'min_h', 'records', 'n_2ext')
    km = {'12': 20392, '12b': 23942, '12c': 18917}
    for k, v in E.known_sets():
        r = E.process((k, v))
        st = rows[km[k]]
        print('known', k, 'class', km[k], 'invariant counters equal:', all(json.loads(json.dumps(r[f])) == st[f] for f in inv),
              {f: r[f] for f in ('n_max_sidon', 'n_single_45', 'n_t1b_45', 'Px_size', 't2_isect_pts', 'min_h')})
