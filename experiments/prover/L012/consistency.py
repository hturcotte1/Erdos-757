"""(L012) Consistency checks of the engine's cell lists (canonical forms by bin/canon):
 (1) every one of the 2,910 saturated extremal 14-point census classes (L004, data/census_n14_m12_classes.jsonl.gz) has an AP pattern
     isomorphic to a member of cell(14,12,6,4), and every one of the 54,243 realizable 12-point classes (L002,
     experiments/20261014-1005-census-dfs/results/realized_n12.json.gz) to a member of cell(12,10,5,4);
 (2) the Delta<=3 cells equal (as sets of isomorphism classes) the prover's labelled lists of L008-L011."""
import sys, json, gzip, subprocess, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
def canon(lines, nv):
    if not lines: return []
    return subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(nv)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
def cellset(key):
    L = [l for l in open(os.path.join(HERE, 'out', 'cells', 'cell_%d_%d_%d_D%d.txt' % key)) if l.startswith('FOUND:')]
    return set(canon([l.strip() for l in L], key[0]))
def fileset(path, tag, nv, gz=False):
    op = gzip.open if gz else open
    L = [l.strip() for l in op(path, 'rt') if l.startswith(tag + ':')]
    return set(canon(L, nv)), len(L)
res = {}
c14 = cellset((14, 12, 6, 4)); recs = [json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')]
k14 = canon(['FOUND: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in r['edges']) for r in recs], 14)
res['census14'] = dict(classes=len(recs), in_cell=sum(k in c14 for k in k14), distinct_patterns=len(set(k14)), cell_size=len(c14))
c12 = cellset((12, 10, 5, 4)); recs = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
k12 = canon(['FOUND: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in r['edges']) for r in recs], 12)
res['census12'] = dict(classes=len(recs), in_cell=sum(k in c12 for k in k12), distinct_patterns=len(set(k12)), cell_size=len(c12))
P = '/home/user/Erdos-757/experiments/prover/'
checks = [((14, 12, 6, 3), P + 'L011/out/filt_T14.txt', 'SURVIVOR'), ((17, 13, 7, 3), P + 'L011/out/filt_T17.txt', 'SURVIVOR'),
          ((15, 11, 6, 3), P + 'L011/out/filt_15_11_6.txt', 'SURVIVOR'), ((12, 10, 5, 3), P + 'L011/out/filt_12_10_5.txt', 'SURVIVOR'),
          ((10, 8, 4, 3), P + 'L011/out/filt_10_8_4.txt', 'SURVIVOR'), ((13, 9, 5, 3), P + 'L011/out/filt_13_9_5.txt', 'SURVIVOR'),
          ((16, 10, 6, 3), P + 'L011/out/filt_16_10_6.txt', 'SURVIVOR'), ((11, 7, 4, 3), P + 'L011/out/filt_11_7_4.txt', 'SURVIVOR'),
          ((14, 8, 5, 3), P + 'L011/out/filt_14_8_5.txt', 'SURVIVOR'), ((8, 6, 3, 3), P + 'L011/out/filt_8_6_3.txt', 'SURVIVOR'),
          ((9, 4, 3, 3), P + 'L011/out/filt_9_4_3.txt', 'SURVIVOR'), ((10, 7, 4, 3), P + 'L011/out/filt_10_7_4.txt', 'SURVIVOR'),
          ((8, 5, 3, 3), P + 'L011/out/filt_8_5_3.txt', 'SURVIVOR'), ((6, 3, 2, 3), P + 'L011/out/filt_6_3_2.txt', 'SURVIVOR')]
res['labelled_lists'] = []
for key, path, tag in checks:
    a = cellset(key); b, nlab = fileset(path, tag, key[0])
    res['labelled_lists'].append(dict(cell=key, engine_classes=len(a), labelled=nlab, labelled_classes=len(b), equal=a == b))
for key in [(19, 11, 7, 3), (20, 14, 8, 3), (21, 13, 8, 4), (18, 12, 7, 4)]:
    p = os.path.join(HERE, 'out', 'cells', 'cell_%d_%d_%d_D%d.txt' % key)
    res.setdefault('empty_cells', []).append(dict(cell=key, classes=len(cellset(key)) if os.path.exists(p) else None))
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(HERE, 'consistency_output.json'), 'w'), indent=1)
