"""Referee round 2, L017: independent enumeration of every cell list quoted in Theorem 6(i), 13.1, 13.3, 13.4, 13.5."""
import math
def conn_ok(n, m, t):
    return n >= 3 and math.ceil((n-1)/2) <= m <= n-2 and 1 <= t <= m and 17*t <= 5*n+3*m
def slack(n, m, t): return 3*n+2*m-11*t
print('Theorem 6(i): cells with s in {-1,-2}, m<=n-2, n<=2m+1, tau<=m, HY, 3m>=n:')
for N in (28, 29, 30):
    print('  N=%d:' % N, [(N, m, t, slack(N, m, t)) for m in range(1, N-1) for t in range(1, m+1) if slack(N, m, t) in (-1, -2) and conn_ok(N, m, t) and 3*m >= N])
tight = [(n, m, t) for n in range(3, 31) for m in range(1, n-1) for t in range(1, m+1) if slack(n, m, t) == 0 and conn_ok(n, m, t)]
print('13.1 tight connected cells n<=30:', tight)
print('      number with n<=26:', len([c for c in tight if c[0] <= 26]))
s1 = [(n, m, t) for n in range(3, 28) for m in range(1, n-1) for t in range(1, m+1) if slack(n, m, t) == 1 and conn_ok(n, m, t)]
print('13.3 slack-1 connected cells n<=27:', s1)
def decomps(N, M, S, smax):
    pieces = [(n, m, t) for n in range(3, N+1) for m in range(1, n-1) for t in range(1, m+1) if 0 <= slack(n, m, t) <= smax and conn_ok(n, m, t)]
    if S >= 3: pieces.append((1, 0, 0))
    sols = set()
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S: sols.add(tuple(sorted(chosen))); return
        if i == len(pieces) or n > N or m > M or s > S: return
        pn, pm, pt = pieces[i]; ps = slack(pn, pm, pt); k = 0
        while n + k*pn <= N and m + k*pm <= M and s + k*ps <= S:
            rec(i+1, n+k*pn, m+k*pm, s+k*ps, chosen + [(pn, pm, pt)]*k); k += 1
    rec(0, 0, 0, 0, [])
    return sorted(sols)
print('13.4 decompositions of (28,24) with total slack 0:', decomps(28, 24, 0, 0))
print('13.3(i) decompositions of (27,m-3) for the two n=28 cells, slack s+2, components with slack<=1:')
for (m, s) in ((18, -1), (23, -2)):
    ds = decomps(27, m-3, s+2, 1)
    print('   (28,%d) s=%d: %d decompositions; those with r<=3:' % (m, s, len(ds)), [d for d in ds if len(d) <= 3])
print('13.5(i) tight connected cells with 26 vertices:', [c for c in tight if c[0] == 26])
for (N, m) in ((28, 18), (28, 23)):
    sols = [(n1, n2, n3) for n1 in range(N+1) for n2 in range(N+1) for n3 in range(N+1) if n1+n2+n3 == N and n1+2*n2+3*n3 == 3*m]
    print('13.5(ii) (%d,%d): all (n1,n2,n3):' % (N, m), sols, '; n1-n3 =', sorted(set(a-c for a, b, c in sols)))
