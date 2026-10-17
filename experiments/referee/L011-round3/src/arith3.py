"""Referee L011 round 3: exact-integer re-derivation of every arithmetic statement of the certificate (window cells, degree
bounds, counting, slack cells, decompositions by brute force incl. the isolated vertex, record cells, Remark 4), compared with
the lists written in results/proofs/L011-f22-equals-13.md (hardcoded below)."""
from math import ceil
from collections import Counter
def slack(n, m, t): return 3 * n + 2 * m - 11 * t
def k8(n, m, t): return 17 * t <= 5 * n + 3 * m
# ---- Step 1: window cells (connected violator: m>=1, n<=2m+1, m<=n-2; lo = least violating tau; hy = min(K8, m))
def windows(nmax, useK8=True):
    out = []
    for n in range(3, nmax + 1):
        for m in range(1, n - 1):
            if n > 2 * m + 1: continue
            lo = (3 * n + 2 * m) // 11 + 1
            hy = min((5 * n + 3 * m) // 17, m) if useK8 else m
            if lo <= hy: out.append((n, m, lo, hy))
    return out
W = windows(22)
print('window cells n<=22:', len(W), '(certificate: 29)')
W2122 = [(n, m, lo, hy) for (n, m, lo, hy) in W if n >= 21]
print('n=21,22 window cells (n,m,lo,hy,slack):', [(n, m, lo, hy, slack(n, m, lo)) for n, m, lo, hy in W2122])
cert_cells = {(21, 11, 8): -3, (21, 12, 8): -1, (21, 16, 9): -4, (21, 17, 9): -2, (22, 15, 9): -3, (22, 16, 9): -1, (22, 20, 10): -4}
mine = {(n, m, lo): slack(n, m, lo) for n, m, lo, hy in W2122}
assert all(lo == hy for n, m, lo, hy in W2122), 'lo != hy somewhere'
print('  equals certificate list with slacks:', mine == cert_cells)
# the rows printed in Step 1
for n in (21, 22):
    ms = list(range(n // 2, n - 1))
    print('  n=%d m=%d..%d: 3n+2m=' % (n, ms[0], ms[-1]), [3 * n + 2 * m for m in ms], 'lo=', [(3 * n + 2 * m) // 11 + 1 for m in ms],
          'floor((5n+3m)/17)=', [(5 * n + 3 * m) // 17 for m in ms])
# ---- Step 2: degree bounds, by testing every d and both candidate values of tau(H-v)
print('Step 2 degree bounds (cell: feasible tau(H-v) values, max d):')
for (n, m, t), s in cert_cells.items():
    feas = {}
    for d in range(0, m + 1):
        for tp in (t - 1, t):
            if 11 * tp <= 3 * (n - 1) + 2 * (m - d): feas.setdefault(tp, []).append(d)
    dmax = max(max(v) for v in feas.values())
    print('  %s s=%d: tau(H-v) in %s, d<=%d, floor((s+8)/2)=%d, K8 max tau=%d, 3m=%d, 2n=%d%s' % ((n, m, t), s, sorted(feas), dmax, (s + 8) // 2,
          min((5 * n + 3 * m) // 17, m), 3 * m, 2 * n, '  COUNTING-IMPOSSIBLE' if 3 * m > 2 * n and dmax <= 2 else ''))
    assert sorted(feas) == [t - 1] and dmax == (s + 8) // 2
# robustness: without K8, every violating (n,m,tau) at n=21,22 with degree bound >= 2 must be one of the seven cells
extra = []
for n in (21, 22):
    for m in range(1, n - 1):
        if n > 2 * m + 1: continue
        for t in range((3 * n + 2 * m) // 11 + 1, m + 1):
            s = slack(n, m, t); dmax = (s + 8) // 2
            if dmax >= 2 and (n, m, t) not in cert_cells: extra.append((n, m, t, s, dmax))
print('violating cells at n=21,22 WITHOUT K8 having degree bound >= 2 and not in the list:', extra)
# ---- Step 0.7: slack cells (connected, n<=21), with and without K8
def slack_cells(nmax, smax, useK8=True):
    out = []
    for n in range(3, nmax + 1):
        for m in range(1, n - 1):
            if n > 2 * m + 1: continue
            for t in range(0, m + 1):
                s = slack(n, m, t)
                if 0 <= s <= smax and (k8(n, m, t) or not useK8): out.append((n, m, t, s))
    return out
cert_slack = {0: [(3,1,1),(10,7,4),(13,8,5),(14,12,6),(16,9,6),(17,13,7),(19,10,7),(20,14,8),(21,18,9)],
              1: [(8,5,3),(11,6,4),(12,10,5),(14,7,5),(15,11,6),(17,8,6),(18,12,7),(19,16,8),(21,13,8)],
              2: [(6,3,2),(9,4,3),(10,8,4),(13,9,5),(16,10,6),(17,14,7),(19,11,7),(20,15,8),(21,19,9)],
              3: [(8,6,3),(11,7,4),(14,8,5),(15,12,6),(17,9,6),(18,13,7),(19,17,8),(20,10,7),(21,14,8)]}
for useK8 in (True, False):
    sc = slack_cells(21, 3, useK8)
    ok = all(sorted(c[:3] for c in sc if c[3] == s) == sorted(cert_slack[s]) for s in range(4))
    print('slack cells n<=21 (K8=%s) equal certificate 0.7 lists:' % useK8, ok)
# ---- decompositions: brute force over multisets of pieces (connected cells with slack <= S, n <= N, plus the isolated vertex (1,0,0) slack 3)
def decomps(N, M, S, useK8=True):
    pieces = [(n, m, t, s) for (n, m, t, s) in slack_cells(N, S, useK8)] + [(1, 0, 0, 3)]
    sols = set()
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S: sols.add(tuple(sorted(chosen))); return
        if i == len(pieces) or n > N or m > M or s > S: return
        pn, pm, pt, ps = pieces[i]; k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, chosen + [(pn, pm, pt)] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sorted(sols)
# second, slack-free formulation: multisets of component types (n_i,m_i,t_i) (connected: m>=1, n<=2m+1, m<=n-2, t<=m; or (1,0,0))
# with sum n = N, sum m = M, sum t = T, every piece with slack >= 0 (I11 below N) -- no use of the slack value of the pieces
def decomps2(N, M, T, useK8=True):
    types = [(1, 0, 0)] + [(n, m, t) for n in range(3, N + 1) for m in range(1, n - 1) if n <= 2 * m + 1 for t in range(0, m + 1)
                           if slack(n, m, t) >= 0 and (k8(n, m, t) or not useK8)]
    sols = set()
    def rec(i, n, m, t, chosen):
        if n == N and m == M and t == T: sols.add(tuple(sorted(chosen))); return
        if i == len(types) or n > N or m > M or t > T: return
        pn, pm, pt = types[i]; k = 0
        while n + k * pn <= N and m + k * pm <= M and t + k * pt <= T:
            rec(i + 1, n + k * pn, m + k * pm, t + k * pt, chosen + [(pn, pm, pt)] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sorted(sols)
AP = (3, 1, 1); I = (1, 0, 0)
cert_dec = {
 (20, 9, 1): [[AP]*4 + [(8,5,3)], [AP]*3 + [(11,6,4)], [AP]*2 + [(14,7,5)], [AP, (17,8,6)]],
 (19, 11, 2): [[AP]*3 + [(10,8,4)], [AP]*2 + [(13,9,5)], [AP, (6,3,2), (10,7,4)], [AP, (8,5,3), (8,5,3)], [AP, (16,10,6)], [(6,3,2), (13,8,5)],
               [(8,5,3), (11,6,4)], [(9,4,3), (10,7,4)], [(19,11,7)]],
 (20, 14, 0): [[(20,14,8)], [AP, (17,13,7)], [AP, AP, (14,12,6)], [(10,7,4), (10,7,4)]],
 (20, 10, 3): [[I, (19,10,7)], [I, AP, (16,9,6)], [I, AP, AP, (13,8,5)], [I, AP, AP, AP, (10,7,4)], [(20,10,7)], [AP, (17,9,6)], [AP, AP, (14,8,5)],
               [AP]*3 + [(11,7,4)], [AP]*4 + [(8,6,3)], [AP, AP, (6,3,2), (8,5,3)], [AP, (6,3,2), (11,6,4)], [(6,3,2), (14,7,5)], [AP, (9,4,3), (8,5,3)], [(9,4,3), (11,6,4)]],
 (21, 13, 1): [[(21,13,8)], [AP, (18,12,7)], [AP, AP, (15,11,6)], [AP]*3 + [(12,10,5)], [(10,7,4), (11,6,4)], [(8,5,3), (13,8,5)], [AP, (8,5,3), (10,7,4)]],
}
for (N, M, S), lst in cert_dec.items():
    T = (3 * N + 2 * M - S) // 11; assert (3 * N + 2 * M - S) % 11 == 0
    cert = sorted(tuple(sorted(x)) for x in lst)
    a, b, c = decomps(N, M, S), decomps2(N, M, T), decomps(N, M, S, useK8=False)
    print('decompositions of (%d,%d) slack %d (tau %d): brute force %d, slack-free %d, no-K8 %d; equal to certificate list (%d): %s' %
          (N, M, S, T, len(a), len(b), len(c), len(cert), a == cert and b == cert and c == cert))
    if a != cert: print('   MINE:', a, '\n   CERT:', cert)
# L009/L010 check lists quoted in C1
for (N, M, S, expect) in [(17, 9, 3, 10), (18, 12, 1, 4), (19, 10, 0, 4), (16, 10, 2, 5), (13, 9, 2, 2)]:
    print('  check (%d,%d) slack %d: %d decompositions (certificate says %d)' % (N, M, S, len(decomps(N, M, S)), expect))
# ---- Step 12.2 / Remark 5: record cells
cert_rec = {23: [(21,10,1)], 25: [(23,11,0)], 30: [(27,13,1),(28,13,3)], 32: [(29,14,0),(30,14,2)], 34: [(32,15,1)], 36: [(34,16,0)],
            37: [(33,16,1),(34,16,3),(35,16,5)], 39: [(35,17,0),(36,17,2),(37,17,4)]}
hyonly = {}; i11ok = {}
for n in range(3, 41):
    hmax = ceil(4 * n / 7) - 1; tmin = n - hmax
    hy = [(m, t) for m in range(0, n - 1) for t in range(tmin, m + 1) if k8(n, m, t)]
    cells = [(m, t, slack(n, m, t)) for m, t in hy if slack(n, m, t) >= 0]
    if hy: hyonly[n] = hy
    if cells: i11ok[n] = cells
print('K8-feasible record cells for n<=22:', {n: v for n, v in hyonly.items() if n <= 22}, '(certificate: 16:(13,7),(14,7); 18:(16,8); 20:(18,9); 22:(20,10))')
print('I11-allowed record cells n<=40 equal Remark 5:', i11ok == cert_rec, '; n with none for 23<=n<=40:', [n for n in range(23, 41) if n not in i11ok])
# Remark 4
print('Remark 4: n=21 tau=9 cells with I11 slack>=0 and K8:', [(m, slack(21, m, 9), k8(21, m, 9)) for m in range(10, 20) if slack(21, m, 9) >= 0],
      '; floor(101/11)=', 101 // 11, 'floor(162/17)=', 162 // 17)
# Step 12.1
print('Step 12.1: 11 tau <= 66 + 2*20 = 106 -> tau <= %d -> h >= %d' % (106 // 11, 22 - 106 // 11))
