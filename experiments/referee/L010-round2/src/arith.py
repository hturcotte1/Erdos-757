"""Referee L010 round 2: arithmetic of Steps 1-3, 5.2, 5.3, 6.3 re-derived from scratch (exact integers only).
Cells (n,m,tau); slack s = 3n+2m-11tau; HY: 17tau <= 5n+3m.  A connected component with m>=1 edges has
3 <= n <= 2m+1, and (P3) gives m <= n-2; the only component with m=0 is an isolated vertex (1,0,0), slack 3."""
from math import ceil
def slack(n, m, t): return 3*n + 2*m - 11*t
def hy_ok(n, m, t): return 17*t <= 5*n + 3*m

print("== Step 1: window cells (violator H connected by 0.3, so ceil((n-1)/2) <= m <= n-2; tau >= lo, tau <= min(hy, m))")
allwin = []
for n in range(3, 23):
    for m in range(1, n - 1):
        if n > 2*m + 1: continue
        lo = (3*n + 2*m)//11 + 1; hy = (5*n + 3*m)//17
        if lo <= min(hy, m):
            for t in range(lo, min(hy, m) + 1): allwin.append((n, m, t, slack(n, m, t)))
for n in (19, 20, 21, 22):
    rows = []
    for m in range(ceil((n-1)/2), n - 1):
        lo = (3*n + 2*m)//11 + 1; hy = (5*n + 3*m)//17
        rows.append((m, lo, hy))
    print(" n=%d rows (m, lo, hy):" % n, rows)
    print("   window cells:", [(c, s) for c in allwin for s in [c[3]] if c[0] == n])
print(" number of window cells with n <= 20:", sum(1 for c in allwin if c[0] <= 20))
print(" all window cells n<=20:", [c[:3] for c in allwin if c[0] <= 20])

print("== Step 2: degree bounds from 11 tau(H-v) <= 3(N-1) + 2(m-d) with tau(H-v) >= tau-1 (exact, by trying d)")
for (n, m, t, s) in [c for c in allwin if c[0] in (19, 20)]:
    # tau(H-v) in {t-1, t}; t is impossible iff 11t > 3(n-1)+2(m-d) for every d>=0, i.e. 11t > 3(n-1)+2m
    t_imposs = 11*t > 3*(n-1) + 2*m
    dmax = max([d for d in range(0, m+1) if 11*(t-1) <= 3*(n-1) + 2*(m-d)], default=None)
    hyt = (5*n + 3*m)//17
    print(" (%d,%d,%d) s=%d: tau(H-v)=tau forbidden: %s; d <= %s; HY tau <= %d (5n+3m=%d); sum d = %d vs 2n = %d, 3n = %d"
          % (n, m, t, s, t_imposs, dmax, hyt, 5*n+3*m, 3*m, 2*n, 3*n))

def cells(nmax, mmax, kmax, use_hy):
    C = [(1, 0, 0)] if 3 <= kmax else []
    for n in range(3, nmax + 1):
        for m in range(1, min(mmax, n - 2) + 1):
            if n > 2*m + 1: continue
            for t in range(1, m + 1):
                s = slack(n, m, t)
                if 0 <= s <= kmax and (hy_ok(n, m, t) or not use_hy): C.append((n, m, t))
    return C
print("== slack cells n<=19 (connected cells n>=3 plus the isolated vertex), with HY / without HY")
for k in range(4):
    a = [c for c in cells(19, 19, 3, True) if slack(*c) == k]; b = [c for c in cells(19, 19, 3, False) if slack(*c) == k]
    print(" slack %d: %s ; identical without HY: %s" % (k, a, a == b))

def decomps(n, m, k, use_hy):
    C = sorted(c for c in cells(n, m, k, use_hy))
    out = []
    def rec(i, n0, m0, k0, cur):
        if n0 == 0 and m0 == 0 and k0 == 0: out.append(list(cur)); return
        for j in range(i, len(C)):
            c = C[j]; s = slack(*c)
            if c[0] <= n0 and c[1] <= m0 and s <= k0:
                cur.append(c); rec(j, n0 - c[0], m0 - c[1], k0 - s, cur); cur.pop()
    rec(0, n, m, k, [])
    return out
print("== decompositions (all multisets of cells, isolated vertex allowed)")
for (n, m, k) in [(18, 12, 1), (17, 9, 3), (19, 10, 0), (16, 9, 0), (17, 13, 0), (16, 10, 2), (13, 9, 2)]:
    d1 = decomps(n, m, k, True); d2 = decomps(n, m, k, False)
    print(" (%d,%d) slack %d: %d decompositions (identical without HY: %s)" % (n, m, k, len(d1), d1 == d2))
    for d in d1: print("    ", d, " tau sum", sum(c[2] for c in d))

print("== Without HY: cells at n=19,20 with s<0 that survive the degree lemma (d <= floor((s+8)/2), need >= 0) and counting")
for n in (19, 20):
    for m in range(ceil((n-1)/2), n - 1):
        for t in range((3*n + 2*m)//11 + 1, m + 1):
            s = slack(n, m, t); dmax = (s + 8)//2
            if dmax < 0: continue                      # no vertex can exist
            if 3*m > n*dmax: continue                  # sum of degrees too large
            print("  survives without HY: (%d,%d,%d) s=%d dmax=%d HY-ok=%s" % (n, m, t, s, dmax, hy_ok(n, m, t)))
