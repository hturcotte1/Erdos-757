"""Markdown table of all connected cells (n,m), 3<=n<=NMAX, ceil((n-1)/2)<=m<=n-2:
lo = floor((3n+2m)/11)+1 (least tau violating I11), hy = floor((5n+3m)/17) (Henning-Yeo max tau), hi = min(hy, m).
A cell is a window cell iff lo <= hi."""
import sys
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 13
rows = []
for n in range(3, NMAX + 1):
    cells = []
    for m in range((n - 1 + 1) // 2, n - 1):
        if n > 2 * m + 1: continue
        lo = (3*n + 2*m) // 11 + 1; hy = (5*n + 3*m) // 17; hi = min(hy, m)
        cells.append("m=%d: lo=%d, hy=%d%s" % (m, lo, hy, "  **WINDOW tau=%s**" % ",".join(map(str, range(lo, hi+1))) if lo <= hi else ""))
    rows.append("| %d | %s |" % (n, "; ".join(cells)))
print("| n | cells (m: lo = floor((3n+2m)/11)+1, hy = floor((5n+3m)/17)) |\n|---|---|")
print("\n".join(rows))
