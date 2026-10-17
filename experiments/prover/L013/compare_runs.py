"""(L013, prover) Compare the prover's cell directory with other cell directories (the worker's runs, L012's cells.tar.gz), cell by cell:
class counts AND the sets of canonical representatives (all lists are canonical forms printed by the same nauty-based `canon`, so equal
classes give identical edge lists).  Also compares counts with a TSV table (n m tau Delta classes ...), if given.
Usage: python3 compare_runs.py MYDIR NAME1=DIR1 [NAME2=DIR2 ...] [tsv:NAME=FILE]"""
import sys, os, re, json
INFOS = {}
def load(cd):
    out = {}; INFOS[cd] = {}
    for fn in os.listdir(cd):
        mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
        if not mm: continue
        L = open(os.path.join(cd, fn)).read().splitlines()
        if not any(l.startswith('INFO ') for l in L): continue
        out[tuple(map(int, mm.groups()))] = frozenset(l.strip() for l in L if l.startswith('FOUND:'))
        INFOS[cd][tuple(map(int, mm.groups()))] = json.loads([l for l in L if l.startswith('INFO ')][0][5:])
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
    # branch counters of common recursion cells (isomorphism invariants of the computation: equal lists give equal inputs and counters)
    KEYS = ('graphs', 'bad_tau', 'tg_too_small', 'searched', 'max_min_covers', 'nodes', 'hits_F7free', 'hits_in_C')
    nb = 0; bd = []
    for k in common:
        a, b = INFOS[sys.argv[1]][k], INFOS[cd][k]
        if a['route'] != b['route']: bd.append((k, 'route', a['route'], b['route'])); continue
        if a['route'] != 'recurse': continue
        A = [(x['d'], x['tp'], x['Sp'], x['decompositions'], x['inputs'], tuple(x.get('ext', {}).get(q) for q in KEYS)) for x in a['branches']]
        Bb = [(x['d'], x['tp'], x['Sp'], x['decompositions'], x['inputs'], tuple(x.get('ext', {}).get(q) for q in KEYS)) for x in b['branches']]
        nb += len(A)
        if A != Bb or a.get('connected_hits') != b.get('connected_hits'): bd.append((k, A, Bb))
    print('   recursion branches compared: %d; differences (d, tp, S\', decompositions, inputs, ext counters, connected hits): %s' % (nb, bd[:5]))
