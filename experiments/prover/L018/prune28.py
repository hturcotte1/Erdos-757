"""prune28.py -- consequences of L018 (Theorems 2, 6(a),(b'), 8-data) for the window-cell induction at n = N0 (default 28, 29):
assuming I11 on C for all n < N0, every member X of a violator cell (N0, m, t) (slack < 0, Delta <= 3) is a minimal counterexample, so
  (R1) slack(X) in {-1,-2}                                   [Theorem 6(a)]
  (R2) Delta(X) = 3: only the branch d = 3 remains             [Theorem 2, Lemma 0.3(d)]
  (R3) tau(X - w) = t - 1, slack(X - w) = slack(X) + 2         [Theorem 6(a)]
  (R4) X - w has at most 2 components, no isolated vertex      [Theorem 6(b), (b')]
  (R5) if slack(X) = -2 and every component is one of the 13 known tight classes, the decomposition is void
       [Theorem 8, Steps 8.5-8.6, whose case analysis uses only the data of Step 8.3 for the components].
Lists every violator cell, every (d=3) decomposition of X - w allowed by (R1)-(R4), and marks (R5).  Component cells are looked up
in the cell directories given (read only).  Exact integer arithmetic; decompositions by the slack-sum generator (as decomp22.gen1)."""
import sys, os, glob
CELLDIRS = ['/home/user/Erdos-757/experiments/prover/L018/cells13/cells',   # refereed L013 lists (extracted from ../L013/cells.tar.gz), searched first
            '/home/user/Erdos-757/experiments/20261027-0300-tight-cells-d4/out/cells',
            '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells',
            '/home/user/Erdos-757/experiments/20261027-0235-cost-n28-n29/out/cells',
            '/home/user/Erdos-757/experiments/20261017-2150-i11-n27/out/cells']
def known(n, m, t, D=3):
    for d in CELLDIRS:
        f = os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
        if os.path.exists(f):
            src = 'L013' if 'L018/cells13' in d else 'unrefereed:' + d.split('/experiments/')[1].split('/')[0]
            return '%d %s' % (sum(1 for l in open(f) if l.startswith('FOUND')), src)
    return None
def conn_cells(nmax):
    for n in range(3, nmax + 1):
        for m in range(n // 2, n - 1):
            yield n, m
def slack_cells(nmax, smax):
    return [(n, m, t, 3*n + 2*m - 11*t) for n, m in conn_cells(nmax) for t in range(0, m + 1)
            if 0 <= 3*n + 2*m - 11*t <= smax and 17*t <= 5*n + 3*m and t >= 1]
def decomps(N, M, S, rmax):
    P = slack_cells(N, S); sols = []
    def rec(i, n, m, s, ch):
        if len(ch) > rmax: return
        if n == N and m == M and s == S: sols.append(tuple(ch)); return
        if i == len(P): return
        pn, pm, pt, ps = P[i]; k = 0
        while n + k*pn <= N and m + k*pm <= M and s + k*ps <= S and len(ch) + k <= rmax:
            rec(i + 1, n + k*pn, m + k*pm, s + k*ps, ch + [(pn, pm, pt)]*k); k += 1
    rec(0, 0, 0, 0, [])
    return sols
TIGHT_KNOWN = {(3, 1, 1), (10, 7, 4), (14, 12, 6), (17, 13, 7)}
for N0 in [int(a) for a in sys.argv[1:]] or [28, 29]:
    print('=== n =', N0)
    for m in range(N0 // 2, N0 - 1):
        for t in range(1, m + 1):
            s = 3*N0 + 2*m - 11*t
            if s >= 0 or 17*t > 5*N0 + 3*m: continue
            if s <= -3:
                print('cell (%d,%d,%d) slack %d: VOID by (R1)' % (N0, m, t, s)); continue
            Sp = s + 2
            decs = decomps(N0 - 1, m - 3, Sp, 2)
            print('cell (%d,%d,%d) slack %d: d=3 only (R2), X-w = (%d,%d) slack %d, %d decompositions with <= 2 components:' % (N0, m, t, s, N0 - 1, m - 3, Sp, len(decs)))
            for dec in decs:
                tags = []
                if s == -2 and all(c in TIGHT_KNOWN for c in dec):
                    tags.append('VOID by (R5)')
                cnts = [known(*c) for c in dec]
                if any(c is not None and c.split()[0] == '0' for c in cnts): tags.append('VOID: empty component cell')
                st = ' + '.join('%s[%s]' % (c, '?' if k is None else k) for c, k in zip(dec, cnts))
                print('     ', st, '  ', '; '.join(tags) if tags else 'REMAINS')
