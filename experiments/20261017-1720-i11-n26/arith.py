"""Exact-integer arithmetic for I11 (11 tau <= 3n + 2m) on the class C at n = 26, 27.
Minimal violator H (n vertices, slack s = 3n+2m-11 tau < 0) is connected (slack additive over components, isolated vertex slack 3,
components with fewer vertices satisfy I11 by induction).  Deleting a vertex v of degree d >= 1 gives (n-1, m-d, tau') with
tau' in {tau-1, tau} in C; I11 at n-1 requires slack >= 0:
   slack(H-v) = s - 3 - 2d + 11 (tau - tau').
tau' = tau needs s >= 3 + 2d > 0: impossible.  tau' = tau-1 needs d <= floor((s+8)/2) =: dmax (also for every v, so Delta <= dmax).
Counting: 3m <= Delta * n."""
import sys, json
def violator_cells(n):
    out = []
    for m in range(1, n - 1):
        if n > 2 * m + 1: continue                      # connected with m edges
        for t in range(1, m + 1):
            if 17 * t > 5 * n + 3 * m: continue         # K8
            s = 3 * n + 2 * m - 11 * t
            if s < 0: out.append((n, m, t, s))
    return out
def analyse(n):
    res = []
    for (n_, m, t, s) in violator_cells(n):
        dmax = (s + 8) // 2
        r = dict(n=n, m=m, tau=t, slack=s, dmax=dmax)
        r['tau_same_possible_degrees'] = [d for d in range(1, m + 1) if s - 3 - 2 * d >= 0]
        if dmax < 1: r['status'] = 'excluded: no admissible degree (dmax<1)'
        elif 3 * m > dmax * n: r['status'] = 'excluded by counting: 3m=%d > dmax*n=%d' % (3 * m, dmax * n)
        else: r['status'] = 'OPEN: Delta <= %d (3m=%d <= %d)' % (dmax, 3 * m, dmax * n)
        r['remainders'] = []
        if r['status'].startswith('OPEN'):
            for d in range(1, dmax + 1):
                mm, tt = m - d, t - 1
                sl = 3 * (n - 1) + 2 * mm - 11 * tt
                r['remainders'].append(dict(d=d, cell=(n - 1, mm, tt), slack=sl,
                    HY_ok=(17 * tt <= 5 * (n - 1) + 3 * mm), P3_ok=(mm <= n - 3)))
        res.append(r)
    return res
if __name__ == '__main__':
    allres = {}
    for n in (26, 27):
        print('=== n = %d: violator cells (n, m, tau), slack s<0, K8 window, connected ===' % n)
        R = analyse(n); allres[n] = R
        for r in R:
            print('(%d,%d,%d) slack %d: tau(H-v)=tau possible for degrees %s; tau(H-v)=tau-1 needs d <= %d; %s' %
                  (r['n'], r['m'], r['tau'], r['slack'], r['tau_same_possible_degrees'] or 'none', r['dmax'], r['status']))
            for q in r['remainders']:
                print('      degree %d: H-v = (%d,%d,%d) slack %d%s%s' % (q['d'], *q['cell'], q['slack'], '' if q['HY_ok'] else ' [violates K8]', '' if q['P3_ok'] else ' [violates P3: m<=n-3]'))
        print('open cells n=%d: %s' % (n, [(r['m'], r['tau'], r['dmax']) for r in R if r['status'].startswith('OPEN')]))
    json.dump({str(k): v for k, v in allres.items()}, open('arith_results.json', 'w'), indent=1)
