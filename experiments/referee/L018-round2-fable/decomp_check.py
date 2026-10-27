"""Corollary 7.2 bookkeeping, re-derived: violator cells at n=28 (slack<0, 14<=m<=26), those with
slack in {-1,-2}; decompositions of (27, m-3, tau-1) into <=2 connected parts with slacks >=0
summing to slack(X)+2, each part (n_i,m_i,tau_i) with n_i>=3, ceil((n_i-1)/2)<=m_i<=n_i-2,
tau_i>=1.  Run twice: with and without the Henning-Yeo filter 17 tau <= 5n+3m, to test whether HY
is load-bearing (DEPENDS ON says HY is 'Not used'; 7.2.1/7.2.2 mention it)."""
from math import ceil


def hy(n, m, t):
    return 17 * t <= 5 * n + 3 * m


def parts(n, use_hy):
    out = []
    for m in range(ceil((n - 1) / 2), n - 1):
        for t in range(1, n + 1):
            s = 3 * n + 2 * m - 11 * t
            if s < 0:
                continue
            if use_hy and not hy(n, m, t):
                continue
            out.append((n, m, t, s))
    return out


def decomps(n, m, t, target, use_hy):
    res = []
    for (n1, m1, t1, s1) in parts(n, use_hy):
        if m1 == m and t1 == t and s1 == target:
            res.append(((n1, m1, t1),))
    for n1 in range(3, n - 2):
        n2 = n - n1
        if n2 < 3 or n1 > n2:
            continue
        for (a, m1, t1, s1) in parts(n1, use_hy):
            for (b, m2, t2, s2) in parts(n2, use_hy):
                if m1 + m2 == m and t1 + t2 == t and s1 + s2 == target:
                    res.append(((n1, m1, t1), (n2, m2, t2)))
    return res


for use_hy in (True, False):
    print(f'=== HY filter {"ON" if use_hy else "OFF"} ===')
    n = 28
    viol = []
    for m in range(14, 27):
        for t in range(1, 29):
            s = 3 * n + 2 * m - 11 * t
            if s < 0 and (not use_hy or hy(n, m, t)):
                viol.append((m, t, s))
    print('violator cells (m,tau,slack):', viol)
    for (m, t, s) in viol:
        if s in (-1, -2):
            d = decomps(27, m - 3, t - 1, s + 2, use_hy)
            print(f'  (28,{m},{t}) slack {s}: X-w of type (27,{m - 3},{t - 1}) slack {s + 2}; decompositions (<=2 parts):')
            for dd in d:
                print('     ', ' + '.join(str(x) for x in dd))
    # n = 29 (Remark 7.3), assuming I11 for n<=28
    n = 29
    for m in range(14, 28):
        for t in range(1, 30):
            s = 3 * n + 2 * m - 11 * t
            if s in (-1, -2) and (not use_hy or hy(n, m, t)):
                d = decomps(28, m - 3, t - 1, s + 2, use_hy)
                print(f'  (29,{m},{t}) slack {s}: decompositions:', '; '.join(' + '.join(str(x) for x in dd) for dd in d))
