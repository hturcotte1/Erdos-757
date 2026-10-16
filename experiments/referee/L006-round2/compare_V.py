"""Compare Route V (own code) with (i) the stored rows and (ii) the exact pair sets of the authors' unmodified process()
(want_pairs=True).  The authors' code is imported ONLY here, for the comparison."""
import gzip, json, sys, os
from fractions import Fraction as F
from multiprocessing import Pool
ROOT = '/home/user/Erdos-757'
sys.path.insert(0, ROOT + '/experiments/20261016-0330-ext12-all')
import extend12_all as E

def auth(item):
    idx, s = item
    r = E.process((idx, s), want_pairs=True)
    return idx, sorted(sorted(map(str, (F(v, 4) for v in p))) for p in r['_t1b']), [str(F(v, 4)) for v in sorted(r['_Px_ok'])], r['t2_isect_45']

if __name__ == '__main__':
    os.nice(5)
    cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
    rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt'))}
    V = [json.loads(l) for l in open(sys.argv[1])]
    with Pool(2) as pool:
        A = {i: (p, x, t) for i, p, x, t in pool.map(auth, [(r['class'], cen[r['class']]['set']) for r in V])}
    nok = 0; tot_pairs = 0; tot_gen = 0; fails = []
    for r in V:
        c = r['class']; st = rows[c]
        ap, apx, at2 = A[c]
        checks = {
            'hA=7': r['hA'] == 7 == st['hA'],
            'min_h=9': r['min_h'] == 9,
            'no deficient': r['n_deficient'] == 0,
            'cell ok h=9': r['cell'] == ['ok', 9],
            'genV45 = n_single_45': r['generic45_by_kind']['V'] == st['n_single_45'] == r['generic45_by_kind']['H'],
            'v45 = n_2ext': r['n_vertex45_unordered'] == st['n_2ext'] and r['n_vertex45_ordered'] == 2 * st['n_2ext'],
            'pair set equal': r['pairs45'] == sorted(ap) and at2 == 0,
            'single set equal': r['genV45'] == apx,
        }
        if all(checks.values()): nok += 1
        else: fails.append((c, {k: v for k, v in checks.items() if not v}))
        tot_pairs += r['n_vertex45_unordered']; tot_gen += sum(r['generic45_by_kind'].values())
    print(f'Route V vs stored rows and authors pair sets: {nok}/{len(V)} classes agree on every check')
    print('total (4,5) vertex pairs compared exactly:', tot_pairs, '; (4,5) generic line points evaluated:', tot_gen)
    hh = {}
    for r in V:
        for k, v in r['h_hist'].items(): hh[k] = hh.get(k, 0) + v
    print('h histogram over all evaluated (4,5) types (vertices ordered + generic line points):', hh)
    print('vertices tested:', sum(r['n_vertices'] for r in V), 'status:', {k: sum(r['vertex_status'].get(k, 0) for r in V) for k in ('ok', 'not45', 'nondistinct')})
    print('lines per class:', min(r['n_lines'] for r in V), '..', max(r['n_lines'] for r in V), '; pure-AP D lines:', sorted({r['pure_by_kind']['D'] for r in V}),
          '; generic-(4,5) D lines:', sorted({r['generic45_by_kind']['D'] for r in V}))
    print('secs per class:', min(r['secs'] for r in V), '..', max(r['secs'] for r in V))
    for f in fails[:10]: print('FAIL', f)
