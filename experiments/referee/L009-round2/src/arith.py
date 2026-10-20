"""Referee L009 round 2: independent re-derivation of all arithmetic of the certificate (exact integers only).
(a) window cells n<=18 (connected range ceil((n-1)/2)<=m<=n-2, and also the full range 0<=m<=n-2 for comparison);
(b) connected cells with slack 0,1,2 for n<=17 (no Henning-Yeo restriction; then with HY, to see whether HY matters);
(c) decompositions of the four targets into multisets of connected slack cells and isolated vertices (my own recursion);
(d) vertex-deletion degree bounds: for a graph in cell (n,m,tau), which degrees d(v) and which tau(H-v) in {tau-1,tau}
    are compatible with I11 at n-1 (for Lemma R cells: with I11 at 16 resp. 13)."""
from itertools import count
def s(n, m, t): return 3*n + 2*m - 11*t
def hy(n, m, t): return 17*t <= 5*n + 3*m
print("(a) window cells: 11 tau > 3n+2m, tau <= m, 17 tau <= 5n+3m")
for full in (False, True):
    W = []
    for n in range(1, 19):
        lo_m = 0 if full else (n - 1 + 1)//2
        for m in range(lo_m, max(n - 1, 0)):   # m <= n-2
            ts = [t for t in range(0, m + 1) if s(n, m, t) < 0 and hy(n, m, t)]
            if ts: W.append((n, m, ts, [s(n, m, t) for t in ts]))
    print("  full m-range" if full else "  connected m-range", len(W), W)
    # also: without HY, which cells n in {17,18} would have violators (to see where K8 is load-bearing)
print("  without HY (n=17,18):", [(n, m, [t for t in range(m+1) if s(n,m,t) < 0]) for n in (17, 18) for m in range((n)//2, n-1) if any(s(n,m,t) < 0 for t in range(m+1))])
print("(b) connected slack cells n<=17")
cells = {}
for withhy in (False, True):
    L = {0: [], 1: [], 2: []}
    for n in range(3, 18):
        for m in range((n)//2, n - 1):       # ceil((n-1)/2) = n//2 for integers
            assert m == m and (n - 1 + 1)//2 == n//2
            for t in range(0, m + 1):
                v = s(n, m, t)
                if v in L and (not withhy or hy(n, m, t)): L[v].append((n, m, t))
    print("  HY imposed" if withhy else "  no HY", L)
    if not withhy: cells = L
def decomp(N, M, S, maxn):
    pieces = [(1, 0, 0, 3)] + [(n, m, t, sl) for sl in (0, 1, 2) for (n, m, t) in cells[sl] if n <= maxn]
    pieces.sort()
    out = []
    def rec(i, n, m, sl, acc):
        if n == N and m == M and sl == S: out.append(tuple(acc)); return
        if i >= len(pieces) or n >= N: return
        p = pieces[i]
        # choose multiplicity k >= 0 of piece i
        k = 0
        while n + k*p[0] <= N and m + k*p[1] <= M and sl + k*p[3] <= S:
            rec(i + 1, n + k*p[0], m + k*p[1], sl + k*p[3], acc + [p[:3]]*k); k += 1
    rec(0, 0, 0, 0, [])
    return out
print("(c) decompositions (components: connected slack cells with <= maxn vertices, isolated vertex slack 3)")
for (N, M, S, maxn, why) in [(16, 9, 0, 16, "H-v, H in (17,12,7)"), (17, 13, 0, 17, "H-v, H in (18,16,8)"),
                             (16, 10, 2, 16, "T-w, T in (17,13,7)"), (13, 9, 2, 13, "T-w, T in (14,12,6)")]:
    print("  (%d,%d) slack %d [%s]:" % (N, M, S, why), decomp(N, M, S, maxn))
# sanity: slack of the target graph
print("  target slacks:", s(16,9,6), s(17,13,7), s(16,10,6), s(13,9,5))
print("(d) deletion degree bounds (tau(H-v) in {tau-1,tau}, I11 at n-1: 11 tau' <= 3(n-1)+2(m-d))")
for (n, m, t, dmax_hyp) in [(17, 12, 7, None), (18, 11, 7, None), (18, 16, 8, None), (17, 13, 7, 3), (14, 12, 6, 3), (18, 10, 7, None)]:
    allowed = {}
    for d in range(0, m + 1):
        tps = [tp for tp in (t - 1, t) if 11*tp <= 3*(n-1) + 2*(m - d)]
        if tps: allowed[d] = tps
    D = max(allowed) if allowed else None
    Dh = D if dmax_hyp is None else min(D, dmax_hyp)
    d3min = 3*m - 2*n if Dh == 3 else None
    print("  cell (%d,%d,%d): allowed d -> tau(H-v): %s ; max degree %s%s ; #deg-3 >= %s" % (n, m, t, allowed, D,
          "" if dmax_hyp is None else " (hypothesis Delta<=3)", d3min))
    if Dh == 3:
        print("     after deleting a degree-3 vertex: (n,m,tau') =", [(n-1, m-3, tp, s(n-1, m-3, tp)) for tp in allowed[3]])
# HY consequences used: (17,12): tau<=7; (18,10),(18,11): tau<=7; (18,m<=16): tau<=8 and tau=8 => m=16
print("HY: (17,12) max tau", (85+36)//17, "; (18,10)", (90+30)//17, "; (18,11)", (90+33)//17,
      "; (18,16)", (90+48)//17, "; tau=8 needs m >=", min(m for m in range(0,17) if 17*8 <= 90+3*m))
print("I11-only version of 4.1 (no HY): tau(H)>=8, every v: tau(H-v)>=7, 77 <= 51+2(m-d) => d <= m-13; sum d = 3m <= 18(m-13) => m >=", min(m for m in range(0,17) if 3*m <= 18*(m-13)) if any(3*m <= 18*(m-13) for m in range(0,17)) else None)
