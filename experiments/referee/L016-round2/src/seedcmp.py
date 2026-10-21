"""compare the lists in the prover's cellsF with the refereed seeds (L013, L014 tarballs) as sets of FOUND lines; list the files
of cellsF that are not refereed seeds (should be run A's 45 + run F's 4)."""
import os, sys, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = '/home/user/Erdos-757/experiments/prover/L016/out/cellsF'
def fset(p):
    reps, info = rlib.read_cell(p); return frozenset(tuple(sorted(e)) for e in map(tuple, [tuple(x) for x in reps])) if False else frozenset(tuple(map(tuple, r)) for r in reps), len(reps), info is not None
seeds = {}
for d in ['out/seeds13/cells', 'out/seeds14/cells', 'out/seeds14']:
    for p in glob.glob(os.path.join(rlib.R, d, 'cell_*.txt*')):
        k = os.path.basename(p).replace('.gz', '')
        s = fset(p)
        if k in seeds and seeds[k][0] != s[0]: print('SEED CONFLICT', k)
        seeds[k] = s
print('distinct refereed seed lists:', len(seeds))
nonseed = []; mism = 0
for p in sorted(glob.glob(os.path.join(CF, 'cell_*.txt'))):
    k = os.path.basename(p)
    if k in seeds:
        s = fset(p)
        if s[0] != seeds[k][0]: mism += 1; print('MISMATCH with seed', k)
    else: nonseed.append(k)
print('cellsF files:', len(glob.glob(os.path.join(CF, 'cell_*.txt'))), 'seed lists identical except', mism, '; non-seed files:', len(nonseed))
listA = open('/home/user/Erdos-757/experiments/prover/L016/listA.txt').read().split()
keysA = set('cell_%s_%s_%s_D%s.txt' % tuple(x.split(',')) for x in listA)
print('listA keys:', len(keysA), ' non-seed files = listA + 4 heavy:', set(nonseed) == keysA | {'cell_24_16_9_D3.txt', 'cell_25_19_10_D3.txt', 'cell_26_22_11_D3.txt', 'cell_27_25_12_D3.txt'})
print('non-seed files:', ' '.join(nonseed))
