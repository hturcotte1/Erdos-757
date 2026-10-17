# Referee round 2: arithmetic of Steps 0.3, 1, 2, 4.1, 7, Remark 5; brute-force decompositions (decomp_bf, no HY) compared with
# the routes, Step 8 and every recursive branch recorded in the prover's cell files.
import json, glob, os, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp_bf import decomps
print('== Step 1 / 0.3 (n=23, tau=10)')
n, t = 23, 10
for m in range(15, 22):
    hy = 17 * t <= 5 * n + 3 * m
    feas = [(d, tp) for d in range(0, 9) for tp in (9, 10) if 11 * tp <= 66 + 2 * (m - d) and m - d >= 0]
    dmax = max([d for d, tp in feas], default=None)
    print('  m=%d HY=%s feasible (d,tau(H-v))=%s max d=%s 3m<=dmax*n: %s H-slack=%d' % (m, hy, feas, dmax, dmax is not None and 3 * m <= dmax * n, 3*n+2*m-11*t))
print('  without HY, m with 3m <= n*(m-17):', [m for m in range(1, 22) if m - 17 >= 1 and 3 * m <= (m - 17) * n])
sols = [(a, b, c) for a in range(24) for b in range(24) for c in range(24) if a + b + c == 23 and a + 2 * b + 3 * c == 63]
print('  Delta<=3 degree vectors (n1,n2,n3):', sols, 'min n3 =', min(s[2] for s in sols))
print('== decompositions (brute force, no HY)')
for (N, M, S) in [(22, 17, 1), (22, 18, 3), (22, 19, 5)]:
    ds = decomps(N, M, S); print('  (%d,%d) slack %d: %d %s' % (N, M, S, len(ds), ds))
cdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'cells_x', 'cells')
nb = bad = miss = ncell = 0
for fn in sorted(glob.glob(cdir + '/cell_*.txt')):
    info = None
    for l in open(fn):
        if l.startswith('INFO '): info = json.loads(l[5:])
    key = tuple(int(x) for x in os.path.basename(fn)[5:-4].replace('D', '').split('_')); nn, mm, tt, DD = key; ncell += 1
    if info is None: print('NO INFO', key); bad += 1; continue
    if info.get('route') != 'recurse': continue
    got = {(b['d'], b['tp']): b for b in info['branches']}
    want = [(d, tp) for d in range(max(1, math.ceil(3 * mm / nn)), DD + 1) for tp in (tt - 1, tt) if tp >= 0 and 3 * (nn - 1) + 2 * (mm - d) - 11 * tp >= 0]
    if set(got) != set(want): miss += 1; print('BRANCH SET DIFFERS', key, sorted(got), want)
    for (d, tp) in want:
        if (d, tp) not in got: continue
        b = got[(d, tp)]; nb += 1; Sp = 3 * (nn - 1) + 2 * (mm - d) - 11 * tp
        theirs = sorted(tuple(sorted(tuple(x) for x in dec)) for dec, size in b['dec'])
        if decomps(nn - 1, mm - d, Sp) != theirs or b['Sp'] != Sp: bad += 1; print('DECOMP MISMATCH', key, d, tp)
print('  cell files %d, recursive branches checked %d, mismatches %d, branch-set differences %d' % (ncell, nb, bad, miss))
rc = [(a, m, tt, 3 * a + 2 * m - 11 * tt) for a in range(23, 41) for m in range(0, a - 1) for tt in range(a - (math.ceil(4 * a / 7) - 1), m + 1)
      if 17 * tt <= 5 * a + 3 * m and 11 * tt <= 3 * a + 2 * m]
print('== Remark 5 record cells (23<=n<=40):', rc)
