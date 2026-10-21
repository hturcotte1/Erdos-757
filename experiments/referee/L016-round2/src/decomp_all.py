"""For every list in cellsF with route 'recurse': own branches and own brute-force decompositions (isolated vertices included)
compared with the INFO line (branch set, decomposition set, per-decomposition input counts from the stored lists)."""
import sys, os, glob, re, json
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = '/home/user/Erdos-757/experiments/prover/L016/out/cellsF'
sizes = {}
def L(n, m, t, D):
    if (n, m) == (1, 0): return 1
    k = (n, m, t, D)
    if k not in sizes:
        p = rlib.cell_path(CF, n, m, t, D)
        sizes[k] = sum(1 for l in open(p) if l.startswith('FOUND:')) if os.path.exists(p) else None
    return sizes[k]
nfiles = nrec = nbr = ndec = bad = 0
for p in sorted(glob.glob(os.path.join(CF, 'cell_*.txt'))):
    n, m, t, D = map(int, re.findall(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)', p)[0]); nfiles += 1
    info = None
    for l in open(p):
        if l.startswith('INFO '): info = json.loads(l[5:])
    if info is None: print('NO INFO', p); bad += 1; continue
    if info.get('route') != 'recurse': continue
    nrec += 1
    mybr = [(d, tp) for (d, tp, Sp) in rlib.branches(n, m, t, D)]
    theirbr = [(b['d'], b['tp']) for b in info['branches']]
    if sorted(mybr) != sorted(theirbr): print('BRANCH SET DIFFERS', (n, m, t, D), mybr, theirbr); bad += 1
    for b in info['branches']:
        nbr += 1; d, tp = b['d'], b['tp']; Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        mine = rlib.my_decomps(n - 1, m - d, Sp)
        theirs = sorted(tuple(sorted(tuple(x) for x in dec)) for dec, size in b['dec'])
        ndec += len(mine)
        if mine != theirs: print('DECOMP DIFFERS', (n, m, t, D), d, tp, len(mine), len(theirs)); bad += 1; continue
        for dec, size in b['dec']:
            groups = {}
            for c in dec: groups[tuple(c)] = groups.get(tuple(c), 0) + 1
            cnt = 1; missing = False
            for tpk, k in groups.items():
                s = L(tpk[0], tpk[1], tpk[2], d)
                if s is None: missing = True; break
                cnt *= comb(s + k - 1, k)
            if missing:
                # a type without a list file: allowed only if the engine treats the key as trivially empty
                if size != 0: print('MISSING LIST but size', size, (n, m, t, D), dec); bad += 1
                else: print('  note: no file for a type in', (n, m, t, D), 'd', d, dec, '(size 0 in INFO)')
                continue
            if cnt != size: print('SIZE DIFFERS', (n, m, t, D), dec, cnt, size); bad += 1
print('SUMMARY files=%d recursion_lists=%d branches=%d decompositions=%d problems=%d' % (nfiles, nrec, nbr, ndec, bad))
