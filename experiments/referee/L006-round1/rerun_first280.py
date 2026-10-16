"""Rerun the unmodified authors' process() on classes 0..279 (produced by the first, old-code run) and compare with stored rows."""
import gzip, json, sys, os, time
from multiprocessing import Pool
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261016-0330-ext12-all')
import extend12_all as E
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'
ROWS = '/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz'
if __name__ == '__main__':
    cen = json.load(gzip.open(CENSUS, 'rt'))
    rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROWS, 'rt'))}
    pick = list(range(280))
    t0 = time.time()
    with Pool(3) as pool:
        res = pool.map(E.process, [(c, cen[c]['set']) for c in pick], chunksize=4)
    bad = [r['class'] for r in res if json.loads(json.dumps({k: v for k, v in r.items() if k != 'secs'})) != {k: v for k, v in rows[r['class']].items() if k != 'secs'}]
    print(f'classes 0..279: {len(res) - len(bad)}/{len(res)} identical to stored rows; mismatches: {bad}; {time.time() - t0:.1f}s')
