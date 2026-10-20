"""Referee: compare the referee engine's cells (out/mycells, labelg canonical forms) with the prover's cells (re-canonicalised by labelg)."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import myengine as E
mine = {}
for fn in os.listdir(E.OUT):
    mt = re.match(r'mycell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
    if mt: mine[tuple(map(int, mt.groups()))] = E.load(tuple(map(int, mt.groups())))
prov = {}
for fn in os.listdir(E.PROVER):
    mt = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
    if mt: prov[tuple(map(int, mt.groups()))] = [E.parse_edges(l) for l in open(os.path.join(E.PROVER, fn)) if l.startswith('FOUND:')]
diff = []; rec = 0; recclasses = 0
import json
for k in sorted(mine):
    if mine[k] is None: continue
    info = json.loads([l for l in open(os.path.join(E.OUT, 'mycell_%d_%d_%d_D%d.txt' % k)) if l.startswith('INFO ')][0][5:])
    if k not in prov: diff.append(('only mine', k, len(mine[k]))); continue
    pc = sorted(E.canon(k[0], k[1], prov[k]))
    if pc != sorted(mine[k]): diff.append(('DIFFERENT', k, len(mine[k]), len(pc)))
    if info['route'] == 'recursion': rec += 1; recclasses += len(mine[k])
onlyp = sorted(set(prov) - set(k for k in mine if mine[k] is not None))
print('mine %d cells (%d by my recursion, %d classes in them), prover %d cells, cells only in prover: %d %s, differences: %d' % (
    sum(1 for k in mine if mine[k] is not None), rec, recclasses, len(prov), len(onlyp), onlyp[:20], len(diff)))
for d in diff: print('  ', d)
