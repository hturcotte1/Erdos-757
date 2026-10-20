"""Referee L013 round 3: independent arithmetic (written from the definitions, no prover code).
(1) violator cells n = 23..27: connected (n <= 2m+1), 1 <= tau <= m <= n-2, K8 17 tau <= 5n+3m, slack 3n+2m-11 tau < 0;
(2) degree bound from I11 at n-1 applied to H - v (tau' in {tau-1, tau}); (3) counting 3m <= dmax*n;
(4) Remark 3/4/5 arithmetic: record cells, lower bounds, degree bounds in (23,21,10) and (25,23,11)."""
import math
def violators(n):
    out = []
    for m in range(1, n - 1):            # m <= n-2
        if n > 2 * m + 1: continue       # connected
        for t in range(1, m + 1):
            if 17 * t > 5 * n + 3 * m: continue
            s = 3 * n + 2 * m - 11 * t
            if s < 0: out.append((n, m, t, s))
    return out
def degree_analysis(n, m, t, s):
    ok_same, ok_less = [], []
    for d in range(1, m + 1):
        n1, m1 = n - 1, m - d
        # H - v in C with n-1 vertices and m-d edges; I11 at n-1
        if 11 * t <= 3 * n1 + 2 * m1: ok_same.append(d)
        if 11 * (t - 1) <= 3 * n1 + 2 * m1: ok_less.append(d)
    return ok_same, ok_less
print("== (1)-(3) violator cells, degree bounds, counting ==")
summary = {}
for n in range(23, 28):
    V = violators(n)
    nm = {}
    for (n_, m, t, s) in V: nm.setdefault(m, []).append(t)
    multi = {m: ts for m, ts in nm.items() if len(ts) > 1}
    print("n=%d: %d violator cells; (m -> taus): %s; multiple taus: %s" % (n, len(V), nm, multi))
    opens, excl = [], []
    for (n_, m, t, s) in V:
        same, less = degree_analysis(n, m, t, s)
        dmax = max(less) if less else 0
        assert not same, (n, m, t, same)
        assert dmax == (s + 8) // 2, (n, m, t, s, dmax)
        if 3 * m > dmax * n: excl.append((n, m, t, s, dmax))
        else: opens.append((n, m, t, dmax))
        print("   (%d,%d,%d) s=%d: tau(H-v)=tau possible for d in %s; dmax(tau-1)=%d; 3m=%d vs dmax*n=%d -> %s" %
              (n, m, t, s, same, dmax, 3 * m, dmax * n, "EXCLUDED" if 3 * m > dmax * n else "OPEN"))
    summary[n] = (opens, excl)
    print("   OPEN:", opens); print("   EXCLUDED by counting:", [(a, b, c) for (a, b, c, _, _) in excl])
print("\n== check against certificate Step 1-3 ==")
cert_open = [(23,13,9,2),(23,14,9,3),(23,20,10,3),(24,12,9,2),(24,13,9,3),(24,18,10,3),(25,16,10,2),(25,17,10,3),(25,22,11,3),(26,14,10,2),(26,15,10,3),(26,21,11,3)]
cert_excl = [(23,19,10),(24,17,10),(25,15,10),(25,21,11),(26,19,11),(26,20,11)]
mine_open = [c for n in range(23, 27) for c in summary[n][0]]
mine_excl = [(a, b, c) for n in range(23, 27) for (a, b, c, _, _) in summary[n][1]]
print("open cells equal:", sorted(mine_open) == sorted(cert_open), "excluded equal:", sorted(mine_excl) == sorted(cert_excl))
print("n=27 open:", summary[27][0], "excluded:", [(a,b,c) for (a,b,c,_,_) in summary[27][1]])
print("\n== n <= 22 window cells (L011 Step 1 says 29 cells, one tau each) ==")
W = [c for n in range(3, 23) for c in violators(n)]
print("count:", len(W), "distinct (n,m):", len(set((c[0], c[1]) for c in W)))
print("\n== Remark 3: lower bounds from I11 (m<=n-2) vs K8 (m<=n-2) ==")
for n in range(23, 28):
    i11 = n - (5 * n - 4) // 11; hy = n - (8 * n - 6) // 17
    print("  n=%d: I11 h>=%d, K8 h>=%d %s" % (n, i11, hy, "" if i11 == hy else "<-- differ"))
print("f(25) <= f(11)+f(14) = 7+8 = 15; f(23) <= f(9)+f(14)=6+8=14 (K1)")
print("\n== Remark 3/4: record cells n=23..27 (h <= ceil(4n/7)-1, m <= n-2, tau <= m, K8) and I11 slack ==")
for n in range(23, 28):
    hmax = math.ceil(4 * n / 7) - 1; tmin = n - hmax
    cells = [(m, t, 3 * n + 2 * m - 11 * t) for m in range(0, n - 1) for t in range(tmin, m + 1) if 17 * t <= 5 * n + 3 * m]
    print("  n=%d h<=%d tau>=%d: %s; I11-allowed: %s" % (n, hmax, tmin, cells, [c for c in cells if c[2] >= 0]))
print("\n== Remark 4(b): (25,23,11): degrees d with tau(H-v)=11 / =10 allowed by I11 at 24 ==")
for (n, m, t) in [(23, 21, 10), (25, 23, 11)]:
    same, less = degree_analysis(n, m, t, 3 * n + 2 * m - 11 * t)
    print("  (%d,%d,%d) s=%d: tau(H-v)=tau for d in %s; tau(H-v)=tau-1 for d in %s" % (n, m, t, 3*n+2*m-11*t, same, less))
print("\n== Remark 5 arithmetic: (27,25,12): S' for d=3, t'=11 and t'=12; (26,22,11): d=3, t'=10 ==")
for (n, m, t, d) in [(27, 25, 12, 3), (26, 22, 11, 3), (23, 21, 10, 3)]:
    print("  (%d,%d,%d) ceil(3m/n)=%d; d=%d: S'(t-1)=%d, S'(t)=%d" % (n, m, t, math.ceil(3 * m / n), d, 3*(n-1)+2*(m-d)-11*(t-1), 3*(n-1)+2*(m-d)-11*t))
