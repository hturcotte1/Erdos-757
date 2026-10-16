"""Driver: Route V on a list of census classes with 2 processes; JSONL output."""
import json, gzip, sys, random
from multiprocessing import Pool
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L006-round3')
import route_V as R
cen = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
def job(i): return R.route_V(cen[i]['set'], i)
if __name__ == '__main__':
    ids = json.load(open(sys.argv[1])); out = sys.argv[2]
    with Pool(2) as pool, open(out, 'w') as fo:
        for r in pool.imap_unordered(job, ids, chunksize=1):
            fo.write(json.dumps(r) + '\n'); fo.flush()
    print('done', len(ids))
