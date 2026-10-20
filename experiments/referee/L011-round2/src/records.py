"""Referee L011 r2: Corollary 3 / Remark 4 / Remark 5 arithmetic.  Record cell: h <= ceil(4n/7)-1, i.e. tau >= n-ceil(4n/7)+1,
with m <= n-2, tau <= m and K8 (17 tau <= 5n+3m); I11 slack s = 3n+2m-11tau."""
from fractions import Fraction
import math
def ceil47(n): return -((-4 * n) // 7)
print("== K8-allowed record cells, 3 <= n <= 40 (m, tau, I11 slack)")
for n in range(3, 41):
    cells = [(m, t, 3*n + 2*m - 11*t) for m in range(0, n - 1) for t in range(n - ceil47(n) + 1, m + 1) if 17*t <= 5*n + 3*m]
    if cells:
        ok = [c for c in cells if c[2] >= 0]
        print(n, "ceil(4n/7)=%d" % ceil47(n), "K8 cells:", [(m, t) for (m, t, s) in cells], "| I11-allowed:", [(n, m, t, s) for (m, t, s) in ok])
print("== f values vs ceil(4n/7):", [(n, ceil47(n)) for n in (16, 18, 20, 22)])
# Remark 4
print("== n=21: max tau by I11 over m<=19:", max((63 + 2*m) // 11 for m in range(0, 20)), "; tau=9 needs m >=", min(m for m in range(0, 20) if 99 <= 63 + 2*m),
      "; K8 max tau:", max((105 + 3*m) // 17 for m in range(0, 20)))
for m in (18, 19): print("   (21,%d,9): slack %d, K8 %d <= %d" % (m, 63 + 2*m - 99, 153, 105 + 3*m))
print("== Theorem 2: n=22, m<=20: tau <=", max((66 + 2*m) // 11 for m in range(0, 21)), "-> h >=", 22 - max((66 + 2*m) // 11 for m in range(0, 21)))
print("   13/22 >= 4/7:", Fraction(13, 22) >= Fraction(4, 7), " 12/22 < 4/7:", Fraction(12, 22) < Fraction(4, 7))
