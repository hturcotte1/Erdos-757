"""Candidate cells (n,m,tau) of connected members of C with slack 0 or 1 and n <= 26:
3n+2m-11tau in {0,1}, ceil((n-1)/2) <= m <= n-2 (connected; (P3) with S=V), tau <= m,
and, for Delta <= 3, m <= 3*tau.  Also report which are excluded only by K8 (17 tau <= 5n+3m)."""
out = {0: [], 1: []}
for n in range(1, 27):
    for m in range(0, n - 1):
        if m >= 1 and n > 2 * m + 1:
            continue
        if m == 0 and n != 1:
            continue
        for t in range(0, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if s not in (0, 1):
                continue
            if m > 3 * t:
                continue
            k8 = 17 * t <= 5 * n + 3 * m
            out[s].append((n, m, t, k8))
for s in (0, 1):
    print('slack', s, 'cells (n,m,tau, K8 ok):')
    for c in out[s]:
        print('  ', c)
