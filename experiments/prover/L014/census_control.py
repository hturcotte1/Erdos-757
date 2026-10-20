"""(L014) Positive control with realizable patterns (non-vacuity of the lists): the AP hypergraphs of the 2,910 saturated extremal
14-point classes (data/census_n14_m12_classes.jsonl.gz, L004) and of the 54,243 realizable 12-point classes
(experiments/20261014-1005-census-dfs/results/realized_n12.json.gz, L002), recomputed from the point sets, must all lie in
cell(14,12,6,4) resp. cell(12,10,5,4) of this run, and those with maximum degree <= 3 in cell(14,12,6,3) resp. cell(12,10,5,3)
(canonical forms by bin/canon).  Prints the counts."""
import os, sys, json, gzip, itertools, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pyverify as pv
def found(key):
    return [l.rstrip('\n') for l in open(os.path.join(HERE, 'out', 'cells', 'cell_%d_%d_%d_D%d.txt' % key)) if l.startswith('FOUND:')]
def canon(lines, nv):
    r = subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(nv)], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True)
    out = r.stdout.splitlines(); assert len(out) == len(lines); return out
def pattern(A):
    A = sorted(A); idx = {a: i for i, a in enumerate(A)}
    return sorted((idx[a], idx[b], idx[c]) for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b)
for (n, m, t), recs in (((14, 12, 6), [json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')]),
                        ((12, 10, 5), json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt')))):
    pats = [pattern(r['set']) for r in recs]
    assert all(len(p) == m for p in pats)
    lines = ['FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in p) for p in pats]
    cf = canon(lines, n); deg = [pv.maxdeg(p) for p in pats]
    for D in (4, 3):
        cell = set(canon(found((n, m, t, D)), n))
        sel = [i for i in range(len(pats)) if deg[i] <= D]
        inn = sum(cf[i] in cell for i in sel); used = len(set(cf[i] for i in sel) & cell)
        print('(%d,%d,%d): %d realizable classes, %d with max degree <= %d; in cell(%d,%d,%d,%d) of this run: %d of them (%d of the %d classes of the list occur)'
              % (n, m, t, len(pats), len(sel), D, n, m, t, D, inn, used, len(cell)))
