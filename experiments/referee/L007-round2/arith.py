"""Referee L007 round 2: independent arithmetic for Steps 1, 3, 4 (no code reused).
Everything is exact integer arithmetic. For each connected cell (n,m) (n>=3, n<=2m+1, m<=n-2),
we enumerate tau directly (no floor formulas) and list the tau values with 11 tau > 3n+2m (I11 violated),
17 tau <= 5n+3m (K8 allowed) and tau <= m."""
import itertools
win = []
for n in range(3, 17):
    for m in range(0, n - 1):
        if n > 2 * m + 1:
            continue
        taus = [t for t in range(0, m + 1) if 11 * t > 3 * n + 2 * m and 17 * t <= 5 * n + 3 * m]
        if taus:
            win.append((n, m, taus))
print("window cells (n,m,[taus]) n<=16:", win)
# Slack-0 connected cells n<=13, enumerated over all m and tau (no modular shortcut)
s0 = [(n, m, t) for n in range(1, 14) for m in range(0, n + 1) for t in range(0, m + 1)
      if 3 * n + 2 * m == 11 * t and m <= n - 2 and n <= 2 * m + 1]
print("slack-0 connected cells n<=13 (no tau<=m/K8 filter needed):", s0)
s0d = [(n, m, t) for n in range(1, 14) for m in range(0, n + 1) for t in range(0, n + 1)
       if 3 * n + 2 * m == 11 * t and m <= n - 2 and n > 2 * m + 1]
print("slack-0 but disconnected-only (n>2m+1):", s0d)
# Step 4.4: partitions of 13 into parts of sizes in {3,10,13} (component sizes of slack-0 components)
sizes = sorted({n for n, m, t in s0})
parts = set()
def rec(rem, mn, cur):
    if rem == 0:
        parts.add(tuple(cur)); return
    for s in sizes:
        if s >= mn and s <= rem:
            rec(rem - s, s, cur + [s])
rec(13, 0, [])
print("component-size multisets summing to 13:", sorted(parts))
# Step 3: Lemma A at H-v: 11*tau(H-v) <= 3*13 + 2*(11-d) with tau(H-v)>=5
print("degrees d allowed by 55 <= 61-2d:", [d for d in range(0, 12) if 11 * 5 <= 39 + 2 * (11 - d)])
print("tau(H-v) values allowed (>=5, 11t<=61):", [t for t in range(5, 14) if 11 * t <= 61])
# d3 >= ? : sum of degrees 33, max degree 3
print("min number of degree-3 vertices:", min(d3 for d3 in range(0, 15) if 3 * d3 + 2 * (14 - d3) >= 33))
# Step 8.3: K8 at n=14, tau=6 -> m >= ?
print("m allowed by 17*6 <= 5*14+3m, m<=12:", [m for m in range(0, 13) if 17 * 6 <= 70 + 3 * m])
# Step 6.1 slack of (14,11,tau>=6)
print("s(14,11,6) =", 42 + 22 - 66)
# K24 lower bounds used in 8.4: f(14)>=8, f(15)>=9 from K8 with m<=n-2
for n in (14, 15):
    tmax = max(t for t in range(n + 1) if 17 * t <= 5 * n + 3 * (n - 2))
    print("n=%d: tau <= %d so h >= %d" % (n, tmax, n - tmax))
