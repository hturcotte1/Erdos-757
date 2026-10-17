"""Referee (L013 round 2) arithmetic, written from scratch.  Exact integers only.
Scans ALL (n, m, tau) with 0 <= m <= n, 0 <= tau <= n (no a-priori window), then applies the constraints one by one:
  C-membership necessary conditions for a CONNECTED member with m >= 1:  n >= 3, n <= 2m+1, m <= n-2, 1 <= tau <= m, 17 tau <= 5n+3m.
  violator: s = 3n+2m-11tau < 0.
Degree analysis with I11 assumed at n-1 (for H-v, any H-v in C):  slack(H-v) = 3(n-1)+2(m-d)-11 tau' >= 0, tau' in {tau-1, tau}.
Counting: 3m <= Delta * n."""
import math, sys
def cells(n):
    out = []
    for m in range(0, n + 1):
        for t in range(0, n + 1):
            if not (n >= 3 and m >= 1 and n <= 2 * m + 1 and m <= n - 2 and 1 <= t <= m and 17 * t <= 5 * n + 3 * m): continue
            s = 3 * n + 2 * m - 11 * t
            if s >= 0: continue
            dpos_same = [d for d in range(0, m + 1) if 3 * (n - 1) + 2 * (m - d) - 11 * t >= 0]
            dpos_minus = [d for d in range(0, m + 1) if 3 * (n - 1) + 2 * (m - d) - 11 * (t - 1) >= 0]
            # d = 0 only possible for isolated vertex; a connected graph with m>=1 has min degree >= 1
            dpos = sorted(set(d for d in dpos_same + dpos_minus if d >= 1))
            dmax = max(dpos) if dpos else 0
            status = 'OPEN' if dmax >= 1 and 3 * m <= dmax * n else 'EMPTY'
            out.append((n, m, t, s, dmax, [d for d in dpos_same if d >= 1], status, 3 * m, dmax * n))
    return out
tot = 0; nm = set()
for n in range(1, 23):
    for c in cells(n): tot += 1; nm.add((n, c[1]))
print('n<=22: violator cells', tot, 'distinct (n,m)', len(nm))
for n in range(23, 28):
    cs = cells(n)
    print('n=%d: %d violator cells' % (n, len(cs)))
    for c in cs:
        print('   (%d,%d,%d) s=%d dmax=%d floor((s+8)/2)=%d tau(H-v)=tau possible for d=%s; 3m=%d dmax*n=%d -> %s' % (c[0], c[1], c[2], c[3], c[4], (c[3] + 8) // 2, c[5], c[7], c[8], c[6]))
# per (n,m): number of violating tau
for n in range(3, 28):
    from collections import Counter
    cnt = Counter(c[1] for c in cells(n))
    two = [m for m, k in cnt.items() if k > 1]
    if two: print('n=%d (n,m) with two violating tau:' % n, two)
# record cells: h = n - tau <= ceil(4n/7) - 1  (beat 4/7), m <= n-2, tau <= m, K8 ; I11-allowed if s >= 0
print('record cells (any m incl. disconnected), n=17..30:')
for n in range(17, 31):
    hmax = -((-4 * n) // 7) - 1
    rc = [(m, t, 3 * n + 2 * m - 11 * t) for m in range(0, n - 1) for t in range(0, m + 1) if n - t <= hmax and 17 * t <= 5 * n + 3 * m]
    print('  n=%d hmax=%d HY-feasible (m,tau,s): %s' % (n, hmax, rc))
# Remark 3: h >= n - floor((3n + 2m)/11) with m <= n-2 ; K8: h >= n - floor((5n+3m)/17)
for n in range(20, 31):
    a = n - (3 * n + 2 * (n - 2)) // 11; b = n - (5 * n + 3 * (n - 2)) // 17
    print('  n=%d I11 bound %d  HY bound %d %s' % (n, a, b, '' if a == b else 'DIFFER'))
# Remark 4(b): (25,23,11): degrees
for (n, m, t) in [(23, 21, 10), (25, 23, 11)]:
    s = 3 * n + 2 * m - 11 * t
    same = [d for d in range(1, m + 1) if 3 * (n - 1) + 2 * (m - d) - 11 * t >= 0]
    minus = [d for d in range(1, m + 1) if 3 * (n - 1) + 2 * (m - d) - 11 * (t - 1) >= 0]
    print('  record cell (%d,%d,%d) s=%d: tau(H-v)=tau possible for d in %s; tau-1 for d in %s' % (n, m, t, s, same, minus))
