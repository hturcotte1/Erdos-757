"""Compare ATE (referee, independent) with the authors' enumeration, as SETS of unordered pairs {x,y} (original scale).
Authors' pairs are regenerated with their own functions (extend_all.candidates / ndist), replicating their T1 loop.
Also compares ATE counts with the stored results.jsonl rows."""
import importlib.util, itertools, json, sys
from fractions import Fraction as Fr
EXP = '/home/user/Erdos-757/experiments/20261015-2340-ext14-all'
spec = importlib.util.spec_from_file_location('extend_all', EXP + '/extend_all.py')
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
stored = {}
for line in open(EXP + '/results.jsonl'):
    r = json.loads(line); stored[r['class']] = r
rows = []
for fn in sys.argv[1:]:
    rows += [json.loads(l) for l in open(fn)]
allok = True
for r in rows:
    if r.get('control'): continue
    c = r['class']; st = stored[c]
    A = [4 * a for a in st['set']]
    tr = list(itertools.combinations(A, 3)); pr = list(itertools.combinations(A, 2))
    single = lambda v: all(E.ndist((v,) + q) >= 5 for q in tr)
    Pxok = [x for x in sorted(E.candidates(A)) if single(x)]
    auth = set()
    for x in Pxok:
        for y in E.candidates(sorted(A + [x])):
            if single(y) and all(E.ndist((x, y) + q) >= 5 for q in pr):
                auth.add((min(Fr(x, 4), Fr(y, 4)), max(Fr(x, 4), Fr(y, 4))))
    mine = {(Fr(p), Fr(q)) for p, q in r['pairs45']}
    vert45 = r['line_reps']['G-vert']['is45']
    ok = (mine == auth and len(mine) == st['n_t1b_45'] + st['t2_isect_45'] and vert45 == st['n_single_45']
          and r['hA'] == st['hA'] == 8 and r['n_deficits'] == 0)
    allok &= ok
    print(c, 'ATE pairs', len(mine), 'authors regenerated', len(auth), 'stored n_t1b_45', st['n_t1b_45'],
          'equal sets', mine == auth, '| ATE vert G lines (4,5)', vert45, 'stored n_single_45', st['n_single_45'], '| OK' if ok else '| FAIL')
print('ALL OK' if allok else 'SOME FAIL')
