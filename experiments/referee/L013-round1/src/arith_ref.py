"""Referee L013 round 1: independent arithmetic (exact integers).
(a) violator cells for n=3..27: connected (n >= 3, n <= 2m+1), m <= n-2, 1 <= tau <= m, K8 (17 tau <= 5n+3m), 11 tau > 3n+2m.
    For each: slack s, degree analysis over d=1..m for tau(H-v) in {tau, tau-1} using I11 at n-1, counting 3m <= Dmax*n.
    Also the same WITHOUT K8 (to show what K8 contributes to the window).
(b) record cells (beat 4/7) n=23..30 and their I11 status.
(c) I11 implied h-bound vs HY bound.
(d) Remark 4 degree analysis for (23,21,10) and (25,23,11)."""
import math
def viol(nmin, nmax, useK8=True):
    out = []
    for n in range(nmin, nmax + 1):
        for m in range(1, n - 1):            # m <= n-2
            if n > 2 * m + 1: continue       # connected
            for t in range(1, m + 1):
                if useK8 and 17 * t > 5 * n + 3 * m: continue
                s = 3 * n + 2 * m - 11 * t
                if s < 0: out.append((n, m, t, s))
    return out
def degree_analysis(n, m, t):
    """possible degrees d of a vertex v of a violator (n,m,t) given I11 on H-v (n-1 vertices, m-d edges, tau' in {t-1,t})."""
    same = [d for d in range(1, m + 1) if 11 * t <= 3 * (n - 1) + 2 * (m - d)]
    drop = [d for d in range(1, m + 1) if 11 * (t - 1) <= 3 * (n - 1) + 2 * (m - d)]
    return same, drop
print("(a) violator cells n=23..27 (with K8):")
cells = viol(23, 27)
for (n, m, t, s) in cells:
    same, drop = degree_analysis(n, m, t)
    D = max(drop) if drop else 0
    assert not same
    assert D == (s + 8) // 2, (n, m, t, s, D)
    status = 'OPEN' if 3 * m <= D * n else 'EMPTY(count %d > %d)' % (3 * m, D * n)
    print("  (%d,%d,%d) s=%d  tau(H-v)=tau possible for d in %s; Dmax=%d floor((s+8)/2)=%d; 3m=%d D*n=%d -> %s" % (n, m, t, s, same, D, (s + 8) // 2, 3 * m, D * n, status))
print("  number:", len(cells))
from collections import Counter
c = Counter((n, m) for (n, m, t, s) in cells)
print("  (n,m) with two violating tau:", [k for k, v in c.items() if v > 1])
print("  n<=22 window cells (with K8):", len(viol(3, 22)), "; two-tau pairs:", [k for k, v in Counter((n, m) for (n, m, t, s) in viol(3, 22)).items() if v > 1])
noK8 = viol(23, 26, useK8=False)
extra = [x for x in noK8 if x not in cells]
print("(a') WITHOUT K8 the window at n=23..26 would contain %d cells, %d more than with K8; the extra ones:" % (len(noK8), len(extra)))
for x in extra: print("   ", x)
print("(b) record cells (h <= ceil(4n/7)-1, m <= n-2, tau <= m, K8):")
for n in range(17, 31):
    hmax = math.ceil(4 * n / 7) - 1; tmin = n - hmax
    rc = [(m, t) for m in range(1, n - 1) for t in range(tmin, m + 1) if 17 * t <= 5 * n + 3 * m]
    ok = [(m, t, 3 * n + 2 * m - 11 * t) for (m, t) in rc if 11 * t <= 3 * n + 2 * m]
    print("  n=%d: hmax=%d record cells %s; I11-allowed %s" % (n, hmax, rc, ok))
print("(c) n - floor((5n-4)/11) vs n - floor((8n-6)/17):")
for n in range(20, 31):
    print("  n=%d: I11 %d  HY %d" % (n, n - (5 * n - 4) // 11, n - (8 * n - 6) // 17))
print("(d) Remark 4 cells:")
for (n, m, t) in [(23, 21, 10), (25, 23, 11)]:
    s = 3 * n + 2 * m - 11 * t
    same, drop = degree_analysis(n, m, t)
    print("  (%d,%d,%d) s=%d tau(H-v)=tau possible d: %s ; tau(H-v)=tau-1 possible d: %s" % (n, m, t, s, same, drop))
