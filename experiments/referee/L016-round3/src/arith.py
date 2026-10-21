# Referee L016 round 3: own re-derivation of Steps 1-3, the branches, the record cells n<=30, and f(27)>=16. Exact integers only.
from math import ceil, floor
def window(n):
    cells = []
    for m in range(1, n - 1):            # (P3): m <= n-2
        if n > 2 * m + 1: continue        # connected with m >= 1 edges: n <= 2m+1
        lo = (3 * n + 2 * m) // 11 + 1    # violator: 11 tau > 3n+2m
        hy = min((5 * n + 3 * m) // 17, m)   # K8 and tau <= m
        for t in range(lo, hy + 1):
            cells.append((n, m, t, 3 * n + 2 * m - 11 * t))
    return cells
n = 27
print("m: 3n+2m lo 5n+3m hy")
for m in range(13, 26):
    lo = (3*n+2*m)//11+1; hy = min((5*n+3*m)//17, m)
    print(m, 3*n+2*m, lo, 5*n+3*m, hy, "VIOLATOR" if lo <= hy else "")
cells = window(27)
print("violator cells (n,m,tau,slack):", cells)
assert [(c[1], c[2], c[3]) for c in cells] == [(13,10,-3),(14,10,-1),(18,11,-4),(19,11,-2),(23,12,-5),(24,12,-3),(25,12,-1)]
# degree bound: H-v has 26 vertices, I11 holds there (L013): 0 <= 3*26 + 2(m-d) - 11 tau'
open_cells = []
for (n, m, t, s) in cells:
    dmax = None
    for d in range(1, m + 1):
        ok_same = 3*26 + 2*(m-d) - 11*t >= 0
        assert not ok_same, (n, m, t, d)   # tau(H-v) = tau impossible
        if 3*26 + 2*(m-d) - 11*(t-1) >= 0: dmax = d
    assert dmax == (s + 8) // 2, (n, m, t, s, dmax)
    # counting: sum of degrees 3m <= dmax * n
    feasible = 3 * m <= dmax * n
    print("cell", (n, m, t), "slack", s, "dmax", dmax, "3m=%d <= %d*%d=%d" % (3*m, dmax, n, dmax*n), "OPEN" if feasible else "EMPTY by counting")
    if feasible: open_cells.append((n, m, t, dmax))
print("OPEN cells:", open_cells)
assert open_cells == [(27,13,10,2),(27,14,10,3),(27,18,11,2),(27,19,11,3),(27,25,12,3)]
# branches of the engine for each open cell: d from ceil(3m/n) to D, t' in {t-1,t}, S' = 3(n-1)+2(m-d)-11t' >= 0
for (n, m, t, D) in open_cells:
    br = []
    for d in range(ceil(3*m/n), D + 1):
        for tp in (t - 1, t):
            Sp = 3*(n-1) + 2*(m-d) - 11*tp
            if Sp >= 0: br.append((d, tp, Sp))
    print("branches of", (n, m, t, D), ":", br)
# branches of the chain cells
for (n, m, t, D) in [(26,22,11,3),(25,19,10,3),(24,16,9,3)]:
    br = []
    for d in range(ceil(3*m/n), D + 1):
        for tp in (t - 1, t):
            Sp = 3*(n-1) + 2*(m-d) - 11*tp
            if Sp >= 0: br.append((d, tp, Sp))
    print("branches of", (n, m, t, D), ":", br)
# f(27) >= 16
print("f(27) lower bound from I11: 27 - floor((81+2*25)/11) =", 27 - (81 + 50) // 11)
assert 27 - (81 + 50) // 11 == 16
# record cells for 23 <= n <= 30: beating 4/7 needs h <= ceil(4n/7)-1, tau >= n-h; K8-feasible with m <= n-2
print("record cells (n,m,tau) with K8 feasibility and I11 slack:")
for n in range(23, 31):
    hneed = -(-4*n // 7) - 1
    tneed = n - hneed
    k8 = n - (8*n - 6) // 17       # K8 lower bound on h with m <= n-2
    i11 = n - (5*n - 4) // 11      # I11 lower bound on h with m <= n-2 (if I11 holds at n)
    cellsn = []
    for m in range(1, n - 1):
        for t in range(tneed, m + 1):
            if 17*t <= 5*n + 3*m:
                cellsn.append((m, t, 3*n + 2*m - 11*t))
    print(" n=%d h_needed<=%d tau>=%d  K8 h>=%d  I11 h>=%d  K8-feasible record cells (m,tau,I11slack): %s" % (n, hneed, tneed, k8, i11, cellsn))
