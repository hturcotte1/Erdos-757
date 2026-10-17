"""(L013, prover) Compare the prover's cell directory with other cell directories (the worker's runs, L012's cells.tar.gz), cell by cell:
class counts AND the sets of canonical representatives (all lists are canonical forms printed by the same nauty-based `canon`, so equal
classes give identical edge lists).  Also compares counts with a TSV table (n m tau Delta classes ...), if given.
Usage: python3 compare_runs.py MYDIR NAME1=DIR1 [NAME2=DIR2 ...] [tsv:NAME=FILE]"""
import sys, os, re, json
def load(cd):
    out = {}
    for fn in os.listdir(cd):
        mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
        if not mm: continue
        L = open(os.path.join(cd, fn)).read().splitlines()
        if not any(l.startswith('INFO ') for l in L): continue
        out[tuple(map(int, mm.groups()))] = frozenset(l.strip() for l in L if l.startswith('FOUND:'))
    return out
mine = load(sys.argv[1]); print('mine: %d cells (%s)' % (len(mine), sys.argv[1]))
for arg in sys.argv[2:]:
    if arg.startswith('tsv:'):
        name, fn = arg[4:].split('=', 1); rows = {}
        for l in open(fn):
            p = l.split('\t')
            if p[0] == 'n': continue
            rows[tuple(map(int, p[:4]))] = int(p[4])
        common = sorted(set(rows) & set(mine)); diff = [(k, len(mine[k]), rows[k]) for k in common if len(mine[k]) != rows[k]]
        print('%s (table %s): %d cells, %d common with mine; count differences: %s; only in table: %s' % (name, fn, len(rows), len(common), diff, sorted(set(rows) - set(mine))))
        continue
    name, cd = arg.split('=', 1); other = load(cd)
    common = sorted(set(other) & set(mine))
    cdiff = [(k, len(mine[k]), len(other[k])) for k in common if len(mine[k]) != len(other[k])]
    sdiff = [k for k in common if mine[k] != other[k]]
    print('%s (%s): %d cells, %d common with mine; count differences: %s; representative-set differences: %s; only in %s: %d; only in mine: %d'
          % (name, cd, len(other), len(common), cdiff, sdiff, name, len(set(other) - set(mine)), len(set(mine) - set(other))))
    if len(set(other) - set(mine)) <= 40: print('   only in %s: %s' % (name, sorted(set(other) - set(mine))))
