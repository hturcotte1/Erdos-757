"""Exact integer enumeration of the arithmetic cells used in certificate L007.
Window cells: (n,m) with 3<=n<=NMAX, m<=n-2, n<=2m+1 (connected), and a tau with
   11 tau > 3n+2m (I11 violated), 17 tau <= 5n+3m (Henning-Yeo), tau <= m.
Slack-0 cells: connected (n,m,tau) with 3n+2m = 11 tau, m<=n-2, n<=2m+1, tau<=m, 17tau<=5n+3m.
Slack-1 cells likewise with 3n+2m-11tau = 1 (used only in the n=16 remark).
Also lists the cells that satisfy 3n+2m = 11 tau but fail n<=2m+1 (disconnected)."""
import sys
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
print("window cells (n,m): lo=floor((3n+2m)/11)+1, hi=min(floor((5n+3m)/17), m)")
win = []
for n in range(3, NMAX + 1):
    for m in range(0, n - 1):           # m <= n-2
        if n > 2 * m + 1:                # connected needs n <= 2m+1
            continue
        lo = (3 * n + 2 * m) // 11 + 1
        hy = (5 * n + 3 * m) // 17
        hi = min(hy, m)
        if lo <= hi:
            win.append((n, m, lo, hi))
            print("  (%d,%d): 3n+2m=%d, lo=%d; 5n+3m=%d, floor/17=%d; m=%d; taus %s"
                  % (n, m, 3*n+2*m, lo, 5*n+3*m, hy, m, list(range(lo, hi + 1))))
print("window cells:", [(n, m, lo) for n, m, lo, hi in win])
for s in (0, 1):
    print("slack-%d connected cells (n<=%d):" % (s, NMAX))
    out = []; disc = []
    for n in range(1, NMAX + 1):
        for m in range(0, n + 1):
            r = 3 * n + 2 * m - s
            if r % 11:
                continue
            t = r // 11
            ok_basic = (m <= n - 2) and t <= m and 17 * t <= 5 * n + 3 * m
            if not ok_basic:
                continue
            if n <= 2 * m + 1:
                out.append((n, m, t))
            else:
                disc.append((n, m, t))
    print("   connected:", out)
    print("   satisfy all but n<=2m+1 (hence disconnected):", disc)
# modular form: 3n+2m == 0 mod 11  <=>  m == 4n mod 11 (2^{-1}=6, -3*6=-18=4 mod 11)
assert all(((3*n + 2*((4*n) % 11)) % 11) == 0 for n in range(50))
print("m == 4n (mod 11) for slack 0:", [(n, (4*n) % 11, (n-1+1)//2, n-2) for n in range(3, 14)])
