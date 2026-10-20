import sys, os, json, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref_decomp import decompositions_bf
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L014')
os.environ['CELLDIR'] = '/home/user/Erdos-757/experiments/referee/L014-round3/out/cells/cells'
os.environ['ENGINELOG'] = '/home/user/Erdos-757/experiments/referee/L014-round3/out/engine_dummy.log'
import engine   # comparison only: engine.decompositions vs my brute force on every branch of my tree
nb = 0; diff = 0
for l in open('out/tree_mine.txt'):
    if not l.startswith('BRANCH'): continue
    (key, d, tp, Sp, nd) = eval(l[7:])
    n, m, t, D = key
    mine = set(decompositions_bf(n - 1, m - d, Sp)); eng = set(tuple(sorted(x)) for x in engine.decompositions(n - 1, m - d, Sp))
    nb += 1
    if mine != eng: diff += 1; print('DIFF', key, d, tp, Sp, mine ^ eng)
print('branches compared', nb, 'different', diff)
# INFO lines of all 145 cell files: classes, routes, bad_tau
celldir = os.environ['CELLDIR']; tot = 0; nd = 0; nr = 0; badtau = 0; calls = 0; files = 0; problems = 0
for fn in sorted(os.listdir(celldir)):
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
    if not mm: continue
    n, m, t, D = map(int, mm.groups()); files += 1
    lines = open(os.path.join(celldir, fn)).read().splitlines()
    found = [x for x in lines if x.startswith('FOUND:')]; info = [x for x in lines if x.startswith('INFO ')]
    assert len(info) == 1 and len(found) + 1 == len(lines), fn
    inf = json.loads(info[0][5:]); tot += len(found)
    for x in found:
        es = [tuple(map(int, y.split(','))) for y in re.findall(r'\((\d+,\d+,\d+)\)', x)]
        if len(es) != m or any(v < 0 or v >= n for e in es for v in e): problems += 1
    if inf['route'] == 'direct': nd += 1
    else:
        nr += 1
        for br in inf['branches']:
            if 'ext' in br: calls += 1; badtau += br['ext'].get('bad_tau', 0)
print('cell files', files, 'direct', nd, 'recurse', nr, 'classes', tot, 'ext_d branch calls', calls, 'total bad_tau', badtau, 'label/edge-count problems', problems)
# direct keys with n >= 20 in my tree
import ast
