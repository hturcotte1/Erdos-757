"""my_decomp.py -- referee's independent derivation of the violator cells and component decompositions used in
L018 Corollary 7.2 (n=28) and Remark 7.3 (n=29), and lookup of the component cells in the cell directories (read only).
Rules re-derived from L018: minimal counterexample => connected, Delta=3, slack in {-1,-2} (Thm 6(a)), HY 17 tau <= 5n+3m,
ceil((n-1)/2) <= m <= n-2; X-w for a degree-3 vertex w has 27 vertices, m-3 edges, tau-1, slack s+2, no isolated vertex,
at most 2 components (Thm 6(b')), each a connected member of C with Delta<=3 (n_i>=3, ceil((n_i-1)/2)<=m_i<=n_i-2, tau_i>=1,
slack_i>=0, HY).  No import from experiments/prover."""
import os, math, itertools, sys

CELLDIRS = ['/home/user/Erdos-757/experiments/referee/L018-round2/cells13/cells',  # refereed L013 lists (own extraction)
            '/home/user/Erdos-757/experiments/20261027-0300-tight-cells-d4/out/cells',
            '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells']

def lookup(n, m, t):
    for d in CELLDIRS:
        f = os.path.join(d, 'cell_%d_%d_%d_D3.txt' % (n, m, t))
        if os.path.exists(f):
            cnt = sum(1 for l in open(f) if l.startswith('FOUND'))
            tag = 'L013' if 'cells13' in d else 'UNREFEREED ' + d.split('/experiments/')[1].split('/')[0]
            return cnt, tag
    return None, 'NOT COMPUTED'

def comp_types(N, Smax):
    out = []
    for n in range(3, N + 1):
        for m in range(math.ceil((n - 1) / 2), n - 1):
            for t in range(1, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= Smax and 17 * t <= 5 * n + 3 * m:
                    out.append((n, m, t, s))
    return out

def decomps(N, M, S, rmax=2):
    P = comp_types(N, S)
    sols = []
    for r in range(1, rmax + 1):
        for combo in itertools.combinations_with_replacement(P, r):
            if sum(c[0] for c in combo) == N and sum(c[1] for c in combo) == M and sum(c[3] for c in combo) == S:
                sols.append(tuple((c[0], c[1], c[2]) for c in combo))
    return sols

def violator_cells(N):
    cells = []
    for m in range(math.ceil((N - 1) / 2), N - 1):
        for t in range(1, m + 1):
            s = 3 * N + 2 * m - 11 * t
            if s < 0 and 17 * t <= 5 * N + 3 * m:
                cells.append((N, m, t, s))
    return cells

if __name__ == '__main__':
    for N in [int(a) for a in sys.argv[1:]] or [28, 29]:
        print('==== n =', N)
        for (n, m, t, s) in violator_cells(N):
            if s <= -3:
                print('cell (%d,%d,%d) slack %d: excluded by Theorem 6(a) (slack <= -3)' % (n, m, t, s)); continue
            print('cell (%d,%d,%d) slack %d: X-w = (%d,%d,%d) slack %d; decompositions into <= 2 connected components:' % (n, m, t, s, n - 1, m - 3, t - 1, s + 2))
            for dec in decomps(n - 1, m - 3, s + 2):
                info = []
                void = False
                for c in dec:
                    cnt, tag = lookup(*c)
                    info.append('%s[%s %s]' % (c, cnt, tag))
                    if cnt == 0: void = True
                flag = 'VOID (empty component cell)' if void else 'REMAINS'
                if s == -2 and all(c in {(3, 1, 1), (10, 7, 4), (14, 12, 6), (17, 13, 7)} for c in dec):
                    flag += ' ; all components among the 13 known tight classes -> void by Thm 8 Steps 8.5-8.6 (7.2.4)'
                print('    ', ' + '.join(info), '->', flag)
