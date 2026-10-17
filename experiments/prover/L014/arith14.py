"""(L014) Exact integer arithmetic used in the certificate (C1).
(a) the top branch of cell(23,21,10,3): degree range, t' and S' for every d, t';
(b) Henning-Yeo (K8) lower bounds h >= n - floor((5n+3(n-2))/17) and the 4/7 thresholds ceil(4n/7)-1 for 20 <= n <= 28;
(c) record cells (n, m, tau) with m <= n-2, tau <= m, 17 tau <= 5n+3m and h = n - tau <= ceil(4n/7)-1, for n <= 26, with I11 slack;
(d) f(24) = 14: HY gives h >= 14 at n = 24, and f(14) + f(10) = 8 + 6 = 14 (K1, K24/K29)."""
import math
from fractions import Fraction as Fr
n, m, t, D = 23, 21, 10, 3
print('(a) cell(23,21,10,3): 3m = %d, 2n = %d, so some vertex has degree >= 3; ceil(3m/n) = %d; d ranges over %s' % (3 * m, 2 * n, math.ceil(Fr(3 * m, n)), list(range(max(1, math.ceil(Fr(3 * m, n))), D + 1))))
for d in range(max(1, math.ceil(Fr(3 * m, n))), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        print('    d=%d t\'=%d: S\' = 3*%d + 2*%d - 11*%d = %d -> %s' % (d, tp, n - 1, m - d, tp, Sp, 'branch' if Sp >= 0 else 'impossible (components of H-w have <= 22 vertices, slack >= 0 by L011)'))
print('    I11 slack of (23,21,10): 3*23 + 2*21 - 11*10 = %d' % (69 + 42 - 110))
print('(b) n, HY lower bound for h (m <= n-2), 4/7 threshold ceil(4n/7)-1:')
for N in range(20, 29):
    tmax = (5 * N + 3 * (N - 2)) // 17; hy = N - tmax; thr = math.ceil(Fr(4 * N, 7)) - 1
    print('    n=%d: HY h >= %d (tau <= %d), beat 4/7 needs h <= %d: %s' % (N, hy, tmax, thr, 'excluded by HY' if hy > thr else 'not excluded by HY'))
print('(c) record cells (n, m, tau, I11 slack) for n <= 26 (HY-feasible, h <= ceil(4n/7)-1):')
for N in range(3, 27):
    thr = math.ceil(Fr(4 * N, 7)) - 1; tmin = N - thr
    cells = [(N, mm, tt, 3 * N + 2 * mm - 11 * tt) for mm in range(0, N - 1) for tt in range(tmin, mm + 1) if 17 * tt <= 5 * N + 3 * mm]
    if cells: print('    n=%d (h <= %d): %s' % (N, thr, cells))
print('(d) n=24: 9n+6 = %d, (9n+6)/17 = %s, ceil = %d; f(14)+f(10) = 8+6 = 14' % (9 * 24 + 6, Fr(9 * 24 + 6, 17), math.ceil(Fr(9 * 24 + 6, 17))))
print('    n=23: (9n+6)/17 = %s, ceil = %d (so h >= 13 at n=23 by K8; h = 13 means tau = 10)' % (Fr(9 * 23 + 6, 17), math.ceil(Fr(9 * 23 + 6, 17))))
print('    4/7 thresholds: n=23: ceil(92/7)-1 = %d; n=24: ceil(96/7)-1 = %d; n=25: ceil(100/7)-1 = %d' % (math.ceil(Fr(92, 7)) - 1, math.ceil(Fr(96, 7)) - 1, math.ceil(Fr(100, 7)) - 1))
