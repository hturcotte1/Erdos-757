"""prover's 167 cell files vs L012's cells.tar.gz and the worker's final directory: identical sets of FOUND lines?"""
import os, glob
def found(fn): return sorted(l.strip() for l in open(fn) if l.startswith('FOUND'))
P = 'out/prover_cells/cells'
for name, D in [('L012', 'out/l012cells/cells'), ('worker-n26-final', '/home/user/Erdos-757/experiments/20261017-1720-i11-n26/out/cells'), ('worker-n26-tar', 'out/w26cells')]:
    if not os.path.isdir(D): print(name, 'missing'); continue
    common = same = 0; diffs = []
    for fn in glob.glob(os.path.join(D, 'cell_*.txt')):
        b = os.path.basename(fn); pf = os.path.join(P, b)
        if not os.path.exists(pf): continue
        common += 1
        if found(fn) == found(pf): same += 1
        else: diffs.append(b)
    print('%s: files %d, common %d, identical %d, differing %s' % (name, len(glob.glob(os.path.join(D, 'cell_*.txt'))), common, same, diffs))
