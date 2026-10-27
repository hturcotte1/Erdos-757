"""(L023) Exact integer arithmetic of Theorem 1, the branches of the top key and Corollary 5."""
from math import ceil, floor
n = 25
print('(a) K8 at n=25: 17*tau <= 5n + 3m <= 125 + 3*23 = %d, so tau <= %d, h >= %d' % (125 + 69, (125 + 69) // 17, 25 - (125 + 69) // 17))
print('    4/7 threshold at n=25: h <= ceil(100/7) - 1 = %d' % (ceil(100 / 7) - 1))
for m in range(0, 24):
    s = 3 * n + 2 * m - 11 * 11
    if 17 * 11 <= 5 * n + 3 * m: print('    tau = 11 allowed by K8 with m = %d; I11 slack 75 + 2m - 121 = %d' % (m, s))
print('(b) degree bound: v of degree d, H - v: 24 vertices, 23 - d edges, tau(H-v) in {10, 11}')
for d in range(1, 8):
    for tp in (10, 11):
        ok = 11 * tp <= 72 + 2 * (23 - d)
        print('    d=%d tau(H-v)=%d: 11*%d = %d <= 72 + 2*(23-%d) = %d ? %s' % (d, tp, tp, 11 * tp, d, 72 + 2 * (23 - d), ok))
print('(c) top key (25,23,11,4): d from ceil(3*23/25) = %d to 4' % ceil(69 / 25))
for d in (3, 4):
    for tp in (10, 11):
        print('    d=%d tp=%d S\' = 3*24 + 2*(23-%d) - 11*%d = %d' % (d, tp, d, tp, 72 + 2 * (23 - d) - 11 * tp))
print('(d) Corollary 5: records need h <= ceil(4n/7) - 1; K8 bound h >= n - floor((5n + 3(n-2))/17)')
for N in range(23, 31):
    thr = ceil(4 * N / 7) - 1; hy = N - (5 * N + 3 * (N - 2)) // 17; i11 = N - (3 * N + 2 * (N - 2)) // 11
    print('    n=%d: record needs h <= %d; K8 gives h >= %d (%s); I11 (if it held) h >= %d; ceil(n/2)+2 = %d' % (N, thr, hy, 'excluded' if hy > thr else 'not excluded by K8', i11, ceil(N / 2) + 2))
print('    Henning-Yeo bound at n=25: n - floor((8n-6)/17) = %d' % (25 - (8 * 25 - 6) // 17))
