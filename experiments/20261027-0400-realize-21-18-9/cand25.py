import sys, json, re, os, random
from rexact import *
os.environ['CELLDIR'] = 'work/cells'; os.environ['ENGINELOG'] = '/dev/null'
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0300-tight-cells-d4/src')
import engine
D = '/home/user/Erdos-757/experiments/falsify/i11-structure-lemmas/'
A = json.load(open(D + 'tight_25_23_11_candidates.json'))['graphs']; B = json.load(open(D + 'verified_tight_25_23_11_candidates.json'))['graphs']
assert [g['edges'] for g in A] == [g['edges'] for g in B], 'files differ'
def line(es): return 'FOUND: ' + ' '.join('(%d,%d,%d)' % tuple(e) for e in es)
cls21 = engine.cell(21, 18, 9, 4); keys21 = engine.canon_lines([line(e) for e in cls21], 21)
out = []
for gi, g in enumerate(A):
    E = [tuple(e) for e in g['edges']]; n = g['n']
    sols, st = decide(E, n, find_all=True)
    r = dict(name=g['from'], n=n, m=len(E), realizable=bool(sols), realizable_labellings=len(sols), nodes=st['nodes'], prunes=st['prunes'], secs=st['secs'])
    if sols:
        iv = explicit_point(sols[0], n, random.Random(0)); r['set'] = iv
    sub = [e for e in E if all(v <= 20 for v in e)]
    k = engine.canon_lines([line(sub)], 21)[0]
    r['sub21_edges'] = len(sub); r['sub21_iso_class_index'] = keys21.index(k) if k in keys21 else None
    out.append(r); print(r['name'], r['realizable'], st['nodes'], st['prunes'], st['secs'], 'sub21 class', r['sub21_iso_class_index'], flush=True)
json.dump(out, open('results_25_23_11_candidates.json', 'w'), indent=1)
