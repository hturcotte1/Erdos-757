"""Referee recomputation (independent of decomp.py) of: window cells n<=16, the n=16 degree argument,
slack-0/1 connected cells n<=15 (with and without the Henning-Yeo filter), and all decompositions of (15,11) with total slack 1.
Exact integer arithmetic only."""
from itertools import product
def connected_range(n):
    # connected 3-graph with m>=1 edges: n <= 2m+1 ; (P3): m <= n-2
    return [m for m in range(1, n-1) if n <= 2*m+1]
print("Window cells (some tau with 11 tau > 3n+2m, 17 tau <= 5n+3m, tau <= m):")
for n in range(3, 17):
    row = []
    for m in connected_range(n):
        taus = [t for t in range(0, m+1) if 11*t > 3*n+2*m and 17*t <= 5*n+3*m]
        if taus: row.append((n, m, taus))
    if row: print("  n=%d:" % n, row)
# n=16 degree argument
print("n=16, tau>=7: HY-feasible (m,tau):", [(m, t) for m in range(0, 15) for t in range(7, 15) if 17*t <= 80+3*m and t <= m])
for m in (13, 14):
    # tau(H-v)>=6 and 11 tau(H-v) <= 45 + 2(m-d)
    dmax = max(d for d in range(0, 20) if 66 <= 45 + 2*(m-d))
    print("  m=%d: d(v) <= %d ; max degree sum 16*%d = %d vs 3m = %d" % (m, dmax, dmax, 16*dmax, 3*m),
          "; tau(H-v) values allowed:", [t for t in range(6, 10) if 11*t <= 45+2*(m-0)])
# slack cells
def slack_cells(use_hy):
    out = {}
    for n in range(3, 16):
        for m in connected_range(n):
            for t in range(0, m+1):
                s = 3*n+2*m-11*t
                if s in (0, 1) and (not use_hy or 17*t <= 5*n+3*m):
                    out.setdefault(s, []).append((n, m, t))
    return out
for hy in (True, False):
    sc = slack_cells(hy)
    print("slack cells (HY filter=%s): s=0:" % hy, sc[0], " s=1:", sc[1])
# decompositions of (15,11) total slack 1 (components: isolated vertex slack 3, or connected slack-0/1 cells); with and without HY
def decomp(N, M, S, pieces):
    sols = []
    def rec(i, n, m, s, ch):
        if (n, m, s) == (N, M, S): sols.append(ch); return
        if i == len(pieces) or n > N or m > M or s > S: return
        p = pieces[i]
        k = 0
        while n + k*p[0] <= N and m + k*p[1] <= M and s + k*p[3] <= S:
            rec(i+1, n+k*p[0], m+k*p[1], s+k*p[3], ch + [p[:3]]*k); k += 1
    rec(0, 0, 0, 0, [])
    return sols
for hy in (True, False):
    sc = slack_cells(hy)
    pieces = [c+(0,) for c in sc[0]] + [c+(1,) for c in sc[1]] + [(1, 0, 0, 3)]
    print("decompositions of (15,11) total slack 1 (HY filter=%s):" % hy, decomp(15, 11, 1, pieces))
