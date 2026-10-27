"""Referee #1 (L021): independent re-derivation of Theorem 7(i)-(iii) from the refereed cell lists
(extracted here from experiments/prover/L012/cells.tar.gz and L013/cells.tar.gz).
(1) candidate triples (n,m,tau), n<=27, for connected members of C_3 with A<0 (own enumeration);
(2) every listed graph re-verified: n, m, connected, in C, Delta<=3, tau by ILP;
(3) closure in increasing n with own copy search (VF2) and own DEF (CP-SAT); classification;
(4) pieces: brute-force minimum transversals, (L1), W, J_{1/6}, slack."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcore import *
HERE = os.path.dirname(os.path.abspath(__file__))
LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 24
cands = []
for n in range(1, 28):
    for m in range(0, n + 1):
        for t in range(0, m + 1):
            if n >= 2 and m > n - 2: continue           # (P3) with S = V
            if m == 0: continue                          # connected with A<0 needs an edge (A(K1)=27, A(empty)=0)
            if n > 2*m + 1: continue                     # connected
            if 3*m < n: continue                         # no isolated vertex
            if 3*n + 2*m - 11*t < 0: continue           # I11 (L016, n <= 27)
            if 17*t > 5*n + 3*m: continue               # Henning-Yeo K8
            if A_val(n, m, t) >= 0: continue
            cands.append((n, m, t))
print('candidate triples n<=27:', len(cands), ' n<=24:', sum(1 for c in cands if c[0] <= 24))
def find_list(n, m, t):
    for d in ('tar/cells', 'tar13/cells'):
        p = os.path.join(HERE, d, 'cell_%d_%d_%d_D3.txt' % (n, m, t))
        if os.path.exists(p): return p
    return None
pieces = []   # (name, n, edges, W)
summary = []
t0 = time.time()
for (n, m, t) in sorted(cands):
    if n > LIM: continue
    p = find_list(n, m, t)
    if p is None:
        print('NO D3 LIST for', (n, m, t)); summary.append(((n, m, t), 'NO LIST')); continue
    gs = parse_cell(p)
    A = A_val(n, m, t)
    irr = []; red_eq = 0; red_gt = 0
    for gi, g in enumerate(gs):
        assert nv(g) == n and len(g) == m and len(set(map(frozenset, g))) == m
        assert connected(n, g) and max(degrees(n, g)) <= 3 and in_C(n, g), (n, m, t, gi)
        assert tau_ilp(n, g) == t, (n, m, t, gi)
        copies = []
        for (pname, pn, pe, W) in pieces:
            if pn >= n: continue
            for U in induced_copies(n, g, pn, pe): copies.append((U, W))
        D, fam = DEF_ilp(n, g, copies)
        Dd = DEF_of_family(n, g, [copies[i] for i in fam])
        assert Dd == D, (D, Dd)
        if A + D < 0: irr.append(gi)
        elif A + D == 0: red_eq += 1
        else: red_gt += 1
    for gi in irr: pieces.append(('(%d,%d,%d)#%d' % (n, m, t, gi), n, gs[gi], -A))
    summary.append(((n, m, t), len(gs), len(irr), red_eq, red_gt))
    print('cell', (n, m, t), 'A', A, 'graphs', len(gs), 'irreducible', len(irr), 'reducible A+DEF=0:', red_eq, ' >0:', red_gt, '[%.0fs]' % (time.time() - t0), flush=True)
print('IRREDUCIBLE:', len(pieces), [p[0] for p in pieces])
# (4) pieces
bad = 0
for (pname, pn, pe, W) in pieces:
    tb, T = min_transversals_bf(pn, pe)
    U = 0
    for x in T: U |= x
    L1 = (U == (1 << pn) - 1)
    m_ = len(pe); s = 3*pn + 2*m_ - 11*tb
    J = 66*tb <= 19*pn + 12*m_
    ok = L1 and J and W == -A_val(pn, m_, tb) and W <= 16 and W <= 11*(pn - m_)
    bad += not ok
    print(pname, 'tau', tb, '#minT', len(T), 'L1', L1, 'W', W, 's', s, 'J1/6', J, 'W<=11(n-m)', W <= 11*(pn-m_), 'maxdeg', max(degrees(pn, pe)))
print('piece failures:', bad)
json.dump(dict(pieces=[dict(name=a, n=b, edges=c, W=d) for a, b, c, d in pieces], summary=summary),
          open(os.path.join(HERE, 'check1_pieces.json'), 'w'), indent=0)
