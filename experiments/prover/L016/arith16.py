"""(L016) Exact-integer arithmetic for certificate L016 (n = 27), written for this certificate (the same definitions as L013's arith13.py).
C = linear, F7-free 3-graphs with e(S) <= |S|-2 for |S| >= 2; s(H) = 3n + 2m - 11 tau (I11 slack).
(a) Violator cells at n = 27: (27, m, tau) with ceil(26/2) = 13 <= m <= 25 (connected, (P3)), 1 <= tau <= m, 17 tau <= 135 + 3m (K8),
    s < 0.  For a vertex of degree d (1 <= d <= m): I11 at 26 (L013) needs s - 3 - 2d >= 0 if tau(H-v) = tau and s + 8 - 2d >= 0 if
    tau(H-v) = tau - 1.  dmax = largest possible d; counting: 3m <= dmax * 27.
(b) The branches of the open cells: d from max(1, ceil(3m/n)) to dmax, t' in {tau-1, tau}, S' = 3(n-1) + 2(m-d) - 11 t' >= 0.
(c) Record cells (h <= ceil(4n/7) - 1, m <= n-2, tau <= m, K8) for 23 <= n <= 30 with their I11 slack.
(d) h >= n - floor((3n + 2(n-2))/11) [I11] and h >= n - floor((5n + 3(n-2))/17) [K8] for 23 <= n <= 30; tau bound at n = 27."""
def ceil_div(a, b): return -((-a) // b)
n = 27
print('(a) window table n=27 (m: 3n+2m, lo=floor((3n+2m)/11)+1, 5n+3m, hy=min(floor((5n+3m)/17), m)):')
cells = []
for m in range(ceil_div(n - 1, 2), n - 1):
    X, Y = 3 * n + 2 * m, 5 * n + 3 * m; lo = X // 11 + 1; hy = min(Y // 17, m)
    print('    m=%d: %d, %d, %d, %d%s' % (m, X, lo, Y, hy, '  <- lo <= hy' if lo <= hy else ''))
    for t in range(1, m + 1):
        if 17 * t > Y: continue
        s = X - 11 * t
        if s >= 0: continue
        same = [d for d in range(1, m + 1) if s - 3 - 2 * d >= 0]
        minus = [d for d in range(1, m + 1) if s + 8 - 2 * d >= 0]
        dmax = max(minus) if minus else 0
        assert not same and dmax == (s + 8) // 2 and lo <= t <= hy
        if 3 * m > dmax * n: st = 'EMPTY by counting (3m=%d > dmax*n=%d)' % (3 * m, dmax * n)
        else: st = 'OPEN (3m=%d <= dmax*n=%d)' % (3 * m, dmax * n)
        cells.append((n, m, t, s, dmax, st))
print('    violator cells (n,m,tau): slack, dmax = floor((s+8)/2), tau(H-v)=tau impossible for every d, status:')
for c in cells: print('    (%d,%d,%d) s=%d dmax=%d %s' % c)
op = [(c[0], c[1], c[2], c[4]) for c in cells if c[5].startswith('OPEN')]
print('    OPEN cells (n,m,tau,Delta):', op)
print('(b) branches of the open cells (d, t\', S\'):')
for (n_, m, t, D) in op:
    brs = []
    for d in range(max(1, ceil_div(3 * m, n_)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n_ - 1) + 2 * (m - d) - 11 * tp
            brs.append((d, tp, Sp, 'branch' if Sp >= 0 else 'no branch (S\'<0)'))
    print('    (%d,%d,%d,%d): ceil(3m/n)=%d; %s' % (n_, m, t, D, ceil_div(3 * m, n_), brs))
print('(c) record cells (beat 4/7: h <= ceil(4n/7)-1; m <= n-2, tau <= m, K8) and I11 slack, 23 <= n <= 30:')
for N in range(23, 31):
    hmax = ceil_div(4 * N, 7) - 1; tmin = N - hmax
    rc = [(N, m, t, 3 * N + 2 * m - 11 * t) for m in range(0, N - 1) for t in range(max(tmin, 0), m + 1) if 17 * t <= 5 * N + 3 * m]
    print('    n=%d: needs h <= %d; K8-feasible record cells (n,m,tau,s): %s; I11-allowed (s>=0): %s' % (N, hmax, rc, [r for r in rc if r[3] >= 0]))
print('(d) lower bounds for h: I11 with m <= n-2, and K8 alone:')
for N in range(23, 31):
    print('    n=%d: I11 %d, K8 %d' % (N, N - (5 * N - 4) // 11, N - (8 * N - 6) // 17))
print('    n=27, m <= 25: 11 tau <= 81 + 2m <= 131, floor(131/11) = %d, so h >= %d; ceil(4*27/7) - 1 = %d' % (131 // 11, 27 - 131 // 11, ceil_div(108, 7) - 1))
