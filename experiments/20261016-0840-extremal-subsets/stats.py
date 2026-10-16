"""For every stored extremal (4,5)-class at n = 6..12: does it contain an extremal (n-2)-subset / (n-1)-subset?
Exact integer arithmetic.  A subset A\\X is extremal iff h(A\\X) = f(|A|-|X|) iff no 3-AP-free subset of A of size
f(|A|-|X|)+1 avoids X (h(A\\X) >= f always).  We enumerate all (f+1)-subsets of A that are 3-AP-free (bitmasks) and test
which X are transversals.  h(A) = f(n) itself is re-checked (no 3-AP-free (f(n)+1)-subset).
Usage: python3 stats.py [--out results.json] [--procs 2]"""
import gzip, itertools, json, glob, os, sys, time
from collections import Counter
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
F = {2: 2, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7}
SC = os.path.join(ROOT, 'experiments', '20261014-1430-small-counts', 'results')

_subs_cache = {}
def subsets_of_size(n, t):
    key = (n, t)
    if key not in _subs_cache:
        _subs_cache[key] = np.array([sum(1 << i for i in c) for c in itertools.combinations(range(n), t)], dtype=np.int64)
    return _subs_cache[key]

def ap_masks(s):
    """bitmasks of 3-APs of the sorted integer list s (a+c = 2b), exact."""
    n = len(s); pos = {v: i for i, v in enumerate(s)}; out = []
    for j in range(n):
        for i in range(j):
            k = pos.get(2 * s[j] - s[i])
            if k is not None and k > j:
                out.append((1 << i) | (1 << j) | (1 << k))
    return out

def indep_sets(n, t, edges):
    subs = subsets_of_size(n, t)
    bad = np.zeros(len(subs), dtype=bool)
    for e in edges:
        bad |= (subs & e) == e
    return subs[~bad]

def analyse(s):
    """returns (list of extremal deleted pairs, list of extremal deleted singles) as index tuples into sorted s."""
    s = sorted(s); n = len(s)
    edges = ap_masks(s)
    top = indep_sets(n, F[n] + 1, edges)
    assert len(top) == 0, ('h(A) > f(n)', s)
    I1 = indep_sets(n, F[n - 1] + 1, edges)
    singles = [x for x in range(n) if not np.any((I1 & (1 << x)) == 0)] if len(I1) else list(range(n))
    I2 = indep_sets(n, F[n - 2] + 1, edges)
    pairs = []
    for i, j in itertools.combinations(range(n), 2):
        p = (1 << i) | (1 << j)
        if len(I2) == 0 or not np.any((I2 & p) == 0):
            pairs.append((i, j))
    return pairs, singles

def sources():
    def load(path):
        d = json.load(gzip.open(path))
        return d if isinstance(d, list) else d['real']
    for n in range(6, 11):
        for m in range(1, n - 1):
            p = os.path.join(SC, f'n{n}_m{m}_real.json.gz')
            if os.path.exists(p):
                recs = load(p)
                if recs:
                    yield n, m, (m == n - 2), 'all realizable patterns, one integer representative each' if m < n - 2 else 'all saturated classes', recs
    for m in (6, 7, 8):
        yield 11, m, False, 'first 300 DFS-order patterns (sample), realizable ones, one integer rep each', load(os.path.join(SC, f'n11_m{m}_sample_real.json.gz'))
    yield 11, 9, True, 'all 466,961 saturated classes', None
    yield 12, 10, True, 'all 54,243 saturated classes', load(os.path.join(ROOT, 'experiments', '20261014-1005-census-dfs', 'results', 'realized_n12.json.gz'))

def n11_m9_iter():
    for p in sorted(glob.glob(os.path.join(SC, '..', 'n11', 'results', 'post', 'real_*.json.gz'))):
        for r in json.load(gzip.open(p))['real']:
            yield r

def work_chunk(sets):
    out = []
    for s in sets:
        pairs, singles = analyse(s)
        out.append((len(pairs), len(singles), pairs[:3], singles))
    return out

def run(procs=2):
    import multiprocessing as mp
    res = {}
    t0 = time.time()
    pool = mp.Pool(procs)
    for n, m, sat, desc, recs in sources():
        it = n11_m9_iter() if recs is None else iter(recs)
        allsets = [r['set'] for r in it]
        chunks = [allsets[i:i + 1000] for i in range(0, len(allsets), 1000)]
        outs = [o for part in pool.imap(work_chunk, chunks) for o in part]
        d2 = Counter(o[0] for o in outs); d1 = Counter(o[1] for o in outs)
        ex2 = next((i for i, o in enumerate(outs) if o[0] > 0), None)
        ex1 = next((i for i, o in enumerate(outs) if o[1] > 0), None)
        ent = dict(n=n, m=m, saturated=sat, source=desc, classes=len(outs),
                   with_ext_n2=sum(v for k, v in d2.items() if k > 0), dist_pairs={str(k): v for k, v in sorted(d2.items())},
                   with_ext_n1=sum(v for k, v in d1.items() if k > 0), dist_singles={str(k): v for k, v in sorted(d1.items())},
                   all_singles_extremal=(d1.get(n, 0) == len(outs)),
                   example_n2=None if ex2 is None else dict(set=allsets[ex2], deleted_pairs_idx=outs[ex2][2]),
                   example_n1=None if ex1 is None else dict(set=allsets[ex1], deleted_idx=outs[ex1][3]))
        res[f'n{n}_m{m}'] = ent
        print(f'n={n} m={m} classes={ent["classes"]} ext(n-2)={ent["with_ext_n2"]} ext(n-1)={ent["with_ext_n1"]} t={time.time()-t0:.0f}s', flush=True)
    return res

if __name__ == '__main__':
    out = 'results.json'; procs = 2
    a = sys.argv[1:]
    if '--out' in a: out = a[a.index('--out') + 1]
    if '--procs' in a: procs = int(a[a.index('--procs') + 1])
    res = run(procs)
    agg = {}
    for k, e in res.items():
        g = agg.setdefault(e['n'], dict(n=e['n'], f_n=F[e['n']], f_n_minus_1=F[e['n'] - 1], f_n_minus_2=F[e['n'] - 2],
                                        classes=0, with_ext_n2=0, with_ext_n1=0,
                                        saturated_classes=0, saturated_with_ext_n2=0, saturated_with_ext_n1=0))
        g['classes'] += e['classes']; g['with_ext_n2'] += e['with_ext_n2']; g['with_ext_n1'] += e['with_ext_n1']
        if e['saturated']:
            g['saturated_classes'] += e['classes']; g['saturated_with_ext_n2'] += e['with_ext_n2']; g['saturated_with_ext_n1'] += e['with_ext_n1']
    sr = json.load(open(os.path.join(ROOT, 'data', 'small_records.json')))['sets']
    recs = {}
    for k, v in sr.items():
        if len(v["set"]) > 12: continue
        pairs, singles = analyse(v['set'])
        recs[k] = dict(n=len(v['set']), h=v['h'], m=v['m'], n_ext_pairs=len(pairs), n_ext_singles=len(singles), pairs_idx=pairs[:5])
    json.dump(dict(F=F, per_source=res, per_size=[agg[n] for n in sorted(agg)], small_records=recs), open(out, 'w'), indent=1)
