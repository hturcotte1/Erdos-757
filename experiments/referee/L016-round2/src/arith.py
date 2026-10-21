"""Referee's own arithmetic for L016 (exact integers)."""
from math import ceil, floor, comb
N = 27
print('== Step 1: violator cells at n = 27 (connected, n <= 2m+1, m <= n-2, 1 <= tau <= m, 17 tau <= 5n+3m, s = 3n+2m-11tau < 0)')
viol = []
for m in range(1, N - 1):
    if N > 2 * m + 1: continue
    for t in range(1, m + 1):
        if 17 * t > 5 * N + 3 * m: continue
        s = 3 * N + 2 * m - 11 * t
        if s < 0: viol.append((N, m, t, s))
for v in viol: print('  violator cell', v)
print('== Step 2: degree bound. For v of degree d: H-v has 26 vertices, m-d edges, tau(H-v) in {tau-1, tau}; I11 at 26 needs')
print('   78 + 2(m-d) - 11 tau(H-v) >= 0.')
opn = []
for (n, m, t, s) in viol:
    ok_d = []
    for d in range(0, m + 1):
        for tp in (t - 1, t):
            if 3 * (n - 1) + 2 * (m - d) - 11 * tp >= 0:
                assert tp == t - 1, ('tau(H-v)=tau possible', n, m, t, d)
                ok_d.append(d)
    dmax = max(ok_d) if ok_d else None
    assert dmax == (s + 8) // 2, (dmax, (s + 8) // 2)
    cnt_ok = 3 * m <= dmax * n
    print('  (%d,%d,%d) s=%d: dmax=%s = floor((s+8)/2)=%d ; counting 3m=%d <= dmax*n=%d : %s' % (n, m, t, s, dmax, (s + 8) // 2, 3 * m, dmax * n, cnt_ok))
    if cnt_ok: opn.append((n, m, t, dmax))
print('OPEN cells', opn)
print('== Step 4: branches of the open cells and of the chain')
def br(n, m, t, D):
    out = []
    for d in range(max(1, ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            out.append((d, tp, Sp, 'OK' if Sp >= 0 else 'neg'))
    return out
for key in opn + [(26, 22, 11, 3), (25, 19, 10, 3), (24, 16, 9, 3)]:
    print('  ', key, br(*key))
print('== Theorem 2 / Corollary 3')
print('  n=27: m <= 25, 11 tau <= 81 + 2*25 = %d -> tau <= %d -> h >= %d' % (81 + 50, (81 + 50) // 11, 27 - (81 + 50) // 11))
print('  beating 4/7 at n=27 needs h <= ceil(4*27/7)-1 =', ceil(4 * 27 / 7) - 1)
print('  record cells (n, m, tau) for 23 <= n <= 30 with K8 feasibility (h = n - tau <= ceil(4n/7)-1, m <= n-2):')
for n in range(23, 31):
    hneed = ceil(4 * n / 7) - 1; tneed = n - hneed
    cells = []
    for m in range(0, n - 1):
        for t in range(tneed, m + 1):
            if 17 * t <= 5 * n + 3 * m:
                cells.append((n, m, t, 3 * n + 2 * m - 11 * t))
    hy = n - (8 * n - 6) // 17; i11 = n - (5 * n - 4) // 11
    print('   n=%d h_needed<=%d: K8-feasible record cells (n,m,tau,I11 slack): %s ; HY bound h>=%d, I11 bound h>=%d' % (n, hneed, cells, hy, i11))
