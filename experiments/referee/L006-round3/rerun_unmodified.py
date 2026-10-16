"""Referee round 3, L006: rerun the authors' UNMODIFIED process() (byte-identical copy, sha256 checked) on my chosen classes and compare with stored rows."""
import gzip, json, hashlib, sys, os, time
from fractions import Fraction as F
from multiprocessing import Pool
ROOT = '/home/user/Erdos-757'
HERE = os.path.dirname(os.path.abspath(__file__))
h1 = hashlib.sha256(open(HERE + '/authors_extend12_all.py', 'rb').read()).hexdigest()
h2 = hashlib.sha256(open(ROOT + '/experiments/20261016-0330-ext12-all/extend12_all.py', 'rb').read()).hexdigest()
assert h1 == h2 == 'b4600c1e2966e76aaa1a8a38f36c811cf5ef495ec36d1bbe6a71f7b53d968db0', (h1, h2)
sys.path.insert(0, HERE)
import authors_extend12_all as E

def nf(S):
    S = sorted(S); a, b = S[0], S[-1]
    f1 = tuple(F(s - a, b - a) for s in S)
    f2 = tuple(sorted(F(b - s, b - a) for s in S))
    return min(f1, f2)

def run(item):
    return E.process(item)

if __name__ == '__main__':
    cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
    rows = {}
    for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt'):
        r = json.loads(l); rows[r['class']] = r
    # identify the known sets' classes with my own affine normal form (reflection included)
    known = json.load(open(ROOT + '/data/small_records.json'))['sets']
    nfidx = {}
    for i, e in enumerate(cen):
        k = nf(e['set']); assert k not in nfidx, 'two census classes equivalent'; nfidx[k] = i
    print('census classes pairwise inequivalent:', len(nfidx))
    kid = {}
    for name in ('12', '12b', '12c'):
        kid[name] = nfidx.get(nf(known[name]['set'])); print('known', name, known[name]['set'], '-> class', kid[name])
    ids = json.load(open(HERE + '/rerun_ids.json'))
    assert all(v in ids for v in kid.values())
    t0 = time.time()
    items = [(i, cen[i]['set']) for i in ids] + [(name, known[name]['set']) for name in ('12', '12b', '12c')]
    with Pool(2) as pool:
        res = pool.map(run, items, chunksize=1)
    mism = []
    for r in res:
        if isinstance(r['class'], str): continue
        s = rows[r['class']]
        a = {k: v for k, v in r.items() if k != 'secs'}; b = {k: v for k, v in s.items() if k != 'secs'}
        if json.loads(json.dumps(a)) != b: mism.append(r['class'])
    print('reran', sum(1 for r in res if not isinstance(r['class'], str)), 'census classes; mismatches vs stored rows:', mism)
    keys = ('n_max_sidon', 'n_single_45', 'n_t1b_45', 'Px_size', 't2_isect_pts', 't1_pairs', 'min_h', 't2_line_h', 't2_isect_45')
    for r in res:
        if isinstance(r['class'], str):
            s = rows[kid[r['class']]]
            print('known set', r['class'], {k: r[k] for k in keys}, '| same invariant counters as its census class', kid[r['class']], ':',
                  all(r[k] == s[k] for k in keys))
    print('secs', round(time.time() - t0, 1))
