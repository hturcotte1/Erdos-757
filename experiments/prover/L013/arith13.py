"""(L013, prover) Exact-integer arithmetic for certificate L013 (written from scratch; no import of the worker's or L011/L012 scripts).
C = linear, F7-free 3-graphs with e(S) <= |S|-2 for |S| >= 2.  s(H) = 3n + 2m - 11 tau (I11 slack).
(a) Violator cells: (n, m, tau) with a connected member possible a priori: n >= 3, n <= 2m+1 (connected), m <= n-2 (P3 with S = V),
    1 <= tau <= m, 17 tau <= 5n + 3m (K8), and s < 0.  For every degree d = 1..m of a vertex v: slack of H - v is s - 3 - 2d if
    tau(H-v) = tau and s + 8 - 2d if tau(H-v) = tau - 1; with I11 at n-1 both must be >= 0 to be possible.  dmax = largest possible d.
    Counting: sum of degrees 3m <= dmax * n.  Cells with dmax < 1 or 3m > dmax*n are empty; the others are 'OPEN' (to be enumerated).
(b) Record cells (beat 4/7): h = n - tau <= ceil(4n/7) - 1, m <= n-2, tau <= m, K8; and which of them I11 allows (s >= 0).
(c) Lower bounds for h implied by I11 (with m <= n-2) and by K8 alone, n = 3..30.
(d) Degree bounds in the I11-allowed record cells (23,21,10) and (25,23,11) from I11 at n-1."""
from fractions import Fraction
def ceil_div(a, b): return -((-a) // b)
def violator_cells(n):
    out = []
    for m in range(1, n - 1):
        if n > 2 * m + 1: continue
        for t in range(1, m + 1):
            if 17 * t > 5 * n + 3 * m: continue
            s = 3 * n + 2 * m - 11 * t
            if s >= 0: continue
            same = [d for d in range(1, m + 1) if s - 3 - 2 * d >= 0]
            minus = [d for d in range(1, m + 1) if s + 8 - 2 * d >= 0]
            poss = sorted(set(same) | set(minus)); dmax = max(poss) if poss else 0
            assert not same and dmax == ((s + 8) // 2 if s + 8 >= 2 else 0)
            if dmax < 1: st = 'EMPTY (dmax < 1)'
            elif 3 * m > dmax * n: st = 'EMPTY by counting (3m=%d > dmax*n=%d)' % (3 * m, dmax * n)
            else: st = 'OPEN (3m=%d <= dmax*n=%d)' % (3 * m, dmax * n)
            out.append(dict(n=n, m=m, tau=t, s=s, dmax=dmax, tau_same_degrees=same, status=st,
                            rests=[(d, (n - 1, m - d, t - 1), s + 8 - 2 * d) for d in range(1, dmax + 1)]))
    return out
if __name__ == '__main__':
    print('(a) violator cells (n, m, tau): slack s, dmax, status; rests (d, (n-1, m-d, tau-1), slack of H - v)')
    tot_nm = set(); tot = 0
    for n in range(3, 23):
        for c in violator_cells(n): tot += 1; tot_nm.add((n, c['m']))
    print('    n <= 22: %d violator cells (n,m,tau), %d distinct (n,m)  [L011 Step 1: 29 window cells with n <= 22]' % (tot, len(tot_nm)))
    two = [(n, m) for (n, m) in sorted(tot_nm) if sum(1 for c in violator_cells(n) if c['m'] == m) > 1]
    print('    (n,m) with more than one violating tau, n <= 22:', two)
    open_cells = {}
    for n in range(23, 28):
        cs = violator_cells(n)
        two = [m for m in set(c['m'] for c in cs) if sum(1 for c in cs if c['m'] == m) > 1]
        print('  n=%d: %d violator cells; (n,m) with more than one violating tau: %s' % (n, len(cs), two))
        for c in cs:
            print('    (%d,%d,%d) s=%d dmax=%d tau(H-v)=tau possible for d in %s; %s' % (c['n'], c['m'], c['tau'], c['s'], c['dmax'], c['tau_same_degrees'], c['status']))
            if c['status'].startswith('OPEN'): print('        rests:', c['rests'])
        open_cells[n] = [(c['n'], c['m'], c['tau'], c['dmax']) for c in cs if c['status'].startswith('OPEN')]
        print('  OPEN cells n=%d (n,m,tau,Delta):' % n, open_cells[n])
    print('(b) record cells (h <= ceil(4n/7)-1, m <= n-2, tau <= m, K8) and their I11 slack, n <= 30:')
    for n in range(3, 31):
        hmax = ceil_div(4 * n, 7) - 1; tmin = n - hmax
        rc = [(m, t, 3 * n + 2 * m - 11 * t) for m in range(0, n - 1) for t in range(max(tmin, 0), m + 1) if 17 * t <= 5 * n + 3 * m]
        if rc: print('    n=%d (h<=%d): %s ; I11-allowed: %s' % (n, hmax, [(m, t) for m, t, s in rc], [(n, m, t, s) for m, t, s in rc if s >= 0]))
    print('(c) lower bounds h >= n - floor((3n+2(n-2))/11) [I11, m <= n-2] and h >= n - floor((5n+3(n-2))/17) [K8], n = 3..30:')
    for n in range(3, 31):
        a = n - (5 * n - 4) // 11; b = n - (8 * n - 6) // 17
        print('    n=%d: I11 %d, K8 %d%s' % (n, a, b, '' if a == b else '  <-- differ'))
    print('(d) degree bounds in the I11-allowed record cells, from I11 at n-1:')
    for (n, m, t) in [(23, 21, 10), (25, 23, 11)]:
        s = 3 * n + 2 * m - 11 * t
        ds = [d for d in range(1, m + 1) if (3 * (n - 1) + 2 * (m - d) - 11 * t >= 0) or (3 * (n - 1) + 2 * (m - d) - 11 * (t - 1) >= 0)]
        same = [d for d in range(1, m + 1) if 3 * (n - 1) + 2 * (m - d) - 11 * t >= 0]
        print('    (%d,%d,%d) s=%d: possible degrees %s (tau(H-v)=tau possible for %s); so Delta <= %d and tau(H-v) = %d for every v'
              % (n, m, t, s, ds, same, max(ds), t - 1))
