"""Referee L013 round 3: independent decomposition generator and audit of every recursion branch recorded in the prover's cell files.
Type = isolated vertex (1,0,0) [slack 3] or connected (p,m,t): p>=3, p<=2m+1, m<=p-2, 1<=t<=m, 17t<=5p+3m, slack 3p+2m-11t>=0.
Generator: dynamic enumeration over types in a fixed order, choosing multiplicities (non-decreasing type index), with exact sums N, M, S.
For each recursion cell file: (i) branch set == {(d,tp): ceil(3m/n)<=d<=D, tp in {t-1,t}, S'>=0}; (ii) decomposition list == mine;
(iii) inputs == prod C(|cell|+k-1, k) from the cell files in the same directory; (iv) ext_d counters bad_tau==0, graphs==inputs.
Also: cell count, total classes, counts vs cells_table.tsv, set-equality of representatives with the worker dirs and L012's lists."""
import sys, os, re, json, math, glob, tarfile, io
from math import comb
CELLS = sys.argv[1]
def types_all(N, S):
    T = []
    if S >= 3: T.append((1, 0, 0))
    for p in range(3, N + 1):
        for m in range(1, p - 1):
            if p > 2 * m + 1: continue
            for t in range(1, m + 1):
                s = 3 * p + 2 * m - 11 * t
                if 0 <= s <= S and 17 * t <= 5 * p + 3 * m: T.append((p, m, t))
    return T
def my_decomps(N, M, S):
    T = types_all(N, S); res = set()
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S: res.add(tuple(sorted(chosen))); return
        if i >= len(T) or n > N or m > M or s > S: return
        p = T[i]; sp = 3 * p[0] + 2 * p[1] - 11 * p[2]
        # multiplicity k >= 0 of type i
        k = 0
        while n + k * p[0] <= N and m + k * p[1] <= M and s + k * sp <= S:
            rec(i + 1, n + k * p[0], m + k * p[1], s + k * sp, chosen + [p] * k); k += 1
    rec(0, 0, 0, 0, [])
    return res
def parse_cell(path):
    reps = []; info = None
    for l in open(path):
        if l.startswith('FOUND:'): reps.append(tuple(sorted(tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l))))
        elif l.startswith('INFO '): info = json.loads(l[5:])
    return reps, info
files = sorted(glob.glob(os.path.join(CELLS, 'cell_*.txt')))
cells = {}
for f in files:
    n, m, t, D = map(int, re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt', os.path.basename(f)).groups())
    cells[(n, m, t, D)] = parse_cell(f)
print('cells:', len(cells), 'total classes:', sum(len(r) for r, _ in cells.values()),
      'direct:', sum(1 for r, i in cells.values() if i['route'] == 'direct'), 'recursion:', sum(1 for r, i in cells.values() if i['route'] == 'recurse'),
      'nonempty:', sum(1 for r, _ in cells.values() if r))
# duplicates inside a cell file
dups = sum(len(r) - len(set(r)) for r, _ in cells.values()); print('duplicate representatives inside files:', dups)
problems = 0; nbr = 0; ndec = 0; ninputs = 0
for key, (reps, info) in sorted(cells.items()):
    n, m, t, D = key
    if info['route'] != 'recurse': continue
    exp_br = set()
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp >= 0: exp_br.add((d, tp, Sp))
    got_br = set((b['d'], b['tp'], b['Sp']) for b in info['branches'])
    if exp_br != got_br: problems += 1; print('BRANCH SET MISMATCH', key, exp_br, got_br)
    for b in info['branches']:
        nbr += 1; d, tp, Sp = b['d'], b['tp'], b['Sp']
        mine = my_decomps(n - 1, m - d, Sp)
        theirs = set(tuple(sorted(tuple(x) for x in dec)) for dec, size in b['dec'])
        ndec += len(mine)
        if mine != theirs: problems += 1; print('DECOMP MISMATCH', key, (d, tp), 'mine-theirs', mine - theirs, 'theirs-mine', theirs - mine)
        tot = 0
        for dec, size in b['dec']:
            cnt = {}
            for x in dec: cnt[tuple(x)] = cnt.get(tuple(x), 0) + 1
            prod = 1
            for typ, k in cnt.items():
                if typ == (1, 0, 0): c = 1
                else:
                    ck = (typ[0], typ[1], typ[2], d)
                    if ck not in cells: problems += 1; print('MISSING COMPONENT CELL', ck, 'for', key); c = 0
                    else: c = len(cells[ck][0])
                prod *= comb(c + k - 1, k)
            if prod != size: problems += 1; print('INPUT COUNT MISMATCH', key, dec, prod, size)
            tot += prod
        ninputs += tot
        if tot != b['inputs']: problems += 1; print('BRANCH INPUT TOTAL MISMATCH', key, b)
        if tot > 0:
            e = b.get('ext', {})
            if e.get('bad_tau', -1) != 0 or e.get('graphs') != tot or e.get('searched') != tot:
                problems += 1; print('EXT COUNTER PROBLEM', key, b)
print('recursion branches audited:', nbr, 'decompositions (mine):', ndec, 'inputs total:', ninputs, 'problems:', problems)
# top-level table check against certificate text (12 cells)
top = [(23,13,9,2),(23,14,9,3),(23,20,10,3),(24,12,9,2),(24,13,9,3),(24,18,10,3),(25,16,10,2),(25,17,10,3),(25,22,11,3),(26,14,10,2),(26,15,10,3),(26,21,11,3)]
for key in top:
    reps, info = cells[key]
    print('TOP', key, 'classes', len(reps), [(b['d'], b['tp'], b['Sp'], len(b['dec']), b['inputs'], b.get('ext', {}).get('hits_F7free'), b.get('hits_in_C')) for b in info['branches']], 'connected_hits', info.get('connected_hits'))
# cells_table.tsv counts
tsv = {}
for l in open(os.path.join(os.path.dirname(CELLS.rstrip('/')), '..', 'cells_table.tsv')):
    p = l.rstrip('\n').split('\t')
    if p[0] == 'n': continue
    tsv[tuple(map(int, p[:4]))] = int(p[4])
print('cells_table.tsv rows:', len(tsv), 'count agreement with files:', all(tsv.get(k) == len(r) for k, (r, _) in cells.items()) and set(tsv) == set(cells))
# comparisons with other directories (sets of sorted edge lists per cell)
def load_dir(d):
    out = {}
    for f in glob.glob(os.path.join(d, 'cell_*.txt')):
        k = tuple(map(int, re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt', os.path.basename(f)).groups()))
        out[k] = parse_cell(f)
    return out
def load_tar(tp, sub):
    out = {}
    with tarfile.open(tp) as tf:
        for mem in tf.getmembers():
            mm = re.match(r'.*cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', mem.name)
            if not mm: continue
            k = tuple(map(int, mm.groups())); reps = []; info = None
            for l in io.TextIOWrapper(tf.extractfile(mem)):
                if l.startswith('FOUND:'): reps.append(tuple(sorted(tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l))))
                elif l.startswith('INFO '): info = json.loads(l[5:])
            out[k] = (reps, info)
    return out
R = '/home/user/Erdos-757/experiments/'
others = {'W26dir': load_dir(R + '20261017-1720-i11-n26/out/cells'), 'W2324dir': load_dir(R + '20261017-1645-i11-n23-n24/out/cells'),
          'W25tar': load_tar(R + '20261017-1645-i11-n23-n24/cells25.tar.gz', ''), 'L012tar': load_tar(R + 'prover/L012/cells.tar.gz', ''),
          'L013tar': load_tar(R + 'prover/L013/cells.tar.gz', '')}
for name, oc in others.items():
    common = set(oc) & set(cells); diffs = [k for k in common if set(oc[k][0]) != set(cells[k][0])]
    # also compare as exact strings (canonical forms identical?)
    exact = [k for k in common if oc[k][0] != cells[k][0]]
    print('%s: cells %d, common %d, representative-set differences %d, list-order/exact differences %d, only-in-other %d' % (name, len(oc), len(common), len(diffs), len(exact), len(set(oc) - set(cells))))
