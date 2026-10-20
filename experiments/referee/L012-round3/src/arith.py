"""Referee L012 round 3: independent arithmetic.
(1) Step 0.3 / Step 1: cells with h = 13 at n = 23, degree bounds from I11 at n = 22, slacks.
(2) Brute-force decomposition lists (isolated vertices included) for (22,17;1), (22,18;3), (22,19;5), and for every
    branch (n-1, m-d, S') recorded in the prover's cell files (INFO json), compared with the engine's lists.
(3) Remark 5 record cells for n <= 40.
Component types: connected members of C with n_K vertices, m_K edges, tau_K: constraints used (all valid for connected members of C):
  1 <= m_K <= n_K - 2 (P3), n_K <= 2 m_K + 1 (connected), 1 <= tau_K <= m_K, 17 tau_K <= 5 n_K + 3 m_K (K8), 0 <= slack (I11, n_K <= 22).
  The isolated vertex (1,0,0) has slack 3.  No other constraint (in particular no degree constraint)."""
import json, glob, os, sys, itertools, math
from functools import lru_cache
def slack(t): return 3 * t[0] + 2 * t[1] - 11 * t[2]
def types_upto(nmax, smax, use_hy=True):
    T = [(1, 0, 0)]
    for n in range(3, nmax + 1):
        for m in range(1, n - 1):
            if n > 2 * m + 1: continue
            for t in range(1, m + 1):
                if use_hy and 17 * t > 5 * n + 3 * m: continue
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= smax: T.append((n, m, t))
    return T
def decomps(N, M, S, use_hy=True):
    """all multisets of types (n,m,tau) (isolated vertices allowed) with sum n = N, sum m = M, total slack = S, every slack in [0,S]."""
    T = sorted(types_upto(N, S, use_hy)); res = set()
    def rec(i, n, m, s, ch):
        if n == N and m == M and s == S: res.add(tuple(sorted(ch))); return
        if n >= N or i == len(T): return
        for j in range(i, len(T)):
            t = T[j]
            if n + t[0] <= N and m + t[1] <= M and s + slack(t) <= S: rec(j, n + t[0], m + t[1], s + slack(t), ch + [t])
    rec(0, 0, 0, 0, [])
    return res
print('== (1) n = 23, h = 13: tau = 10')
n, tau = 23, 10
ms = [m for m in range(1, n - 1) if 17 * tau <= 5 * n + 3 * m]
print('m range allowed by P3 and K8:', ms)
for m in ms:
    s = 3 * n + 2 * m - 11 * tau
    # H - v: 22 vertices, m-d edges, tau' in {tau-1, tau}; I11 at 22: 11 tau' <= 66 + 2(m-d)
    dmax = None; t10 = []
    for d in range(0, m + 1):
        if 11 * 10 <= 66 + 2 * (m - d): t10.append(d)
        if 11 * 9 <= 66 + 2 * (m - d): dmax = d
    print(' m=%d: slack(H)=%d; degrees allowing tau(H-v)=10: %s; max degree %d (3m=%d vs 2n=%d -> %s); slack(H-v) for d=dmax: %d'
          % (m, s, t10, dmax, 3 * m, 2 * n, 'impossible' if 3 * m > dmax * n else 'ok', 66 + 2 * (m - dmax) - 99))
# degree count for Delta<=3, saturated: n1+n2+n3=23, n1+2n2+3n3=63
sols = [(n1, n2, n3) for n1 in range(24) for n2 in range(24) for n3 in range(24) if n1 + n2 + n3 == 23 and n1 + 2 * n2 + 3 * n3 == 63]
print(' Delta<=3 degree patterns (n1,n2,n3) with no isolated vertex: min n3 =', min(s[2] for s in sols), 'max n3 =', max(s[2] for s in sols))
print('== (2) decompositions (with HY / without HY)')
for (N, M, S) in [(22, 17, 1), (22, 18, 3), (22, 19, 5)]:
    a = decomps(N, M, S, True); b = decomps(N, M, S, False)
    print(' (%d,%d) slack %d: %d decompositions (no-HY: %d, equal=%s)' % (N, M, S, len(a), len(b), a == b))
    for x in sorted(a): print('    ', list(x))
# all engine branches from the cell files
celldir = sys.argv[1] if len(sys.argv) > 1 else 'out/cells'
nb = 0; bad = 0
for fn in sorted(glob.glob(os.path.join(celldir, 'cell_*.txt'))):
    key = tuple(int(x) for x in os.path.basename(fn)[5:-4].replace('D', '').split('_'))
    nn, mm, tt, D = key
    for l in open(fn):
        if l.startswith('INFO'):
            info = json.loads(l[5:])
            if info.get('route') != 'recurse': continue
            # every (d, tp) with S' >= 0 must be present
            expect = set()
            for d in range(max(1, math.ceil(3 * mm / nn)), D + 1):
                for tp in (tt - 1, tt):
                    Sp = 3 * (nn - 1) + 2 * (mm - d) - 11 * tp
                    if Sp >= 0 and tp >= 0: expect.add((d, tp))
            got = set((br['d'], br['tp']) for br in info['branches'])
            if expect != got: bad += 1; print('  BRANCH SET MISMATCH', key, expect, got)
            for br in info['branches']:
                d, tp, Sp = br['d'], br['tp'], br['Sp']
                mine = decomps(nn - 1, mm - d, Sp)
                theirs = set(tuple(sorted(tuple(c) for c in dec)) for dec, size in br['dec'])
                nb += 1
                if mine != theirs:
                    bad += 1; print('  DECOMP MISMATCH', key, 'd=%d tp=%d Sp=%d' % (d, tp, Sp), 'mine-theirs', mine - theirs, 'theirs-mine', theirs - mine)
print(' engine branches checked: %d, mismatches: %d' % (nb, bad))
print('== (3) record cells n <= 40 (h <= ceil(4n/7)-1, m <= n-2, tau <= m, K8, I11 slack >= 0)')
for nn in range(3, 41):
    hmax = math.ceil(4 * nn / 7) - 1; tmin = nn - hmax
    cells = [(nn, mm, t, 3 * nn + 2 * mm - 11 * t) for mm in range(0, nn - 1) for t in range(tmin, mm + 1) if 17 * t <= 5 * nn + 3 * mm and 11 * t <= 3 * nn + 2 * mm]
    if cells: print('  n=%d:' % nn, cells)
