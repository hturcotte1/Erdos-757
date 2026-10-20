"""Window cells for n = 21..23 and the record cells (h = ceil(4n/7)-1, tau = n-h) at n = 21, 22, 23: Henning-Yeo condition and I11 slack."""
def conn_cells(nmax):
    for n in range(3, nmax + 1):
        for m in range((n - 1 + 1) // 2, n - 1): yield n, m
for n, m in conn_cells(23):
    if n < 21: continue
    lo = (3*n + 2*m)//11 + 1; hy = (5*n + 3*m)//17; hi = min(hy, m)
    if lo <= hi: s = 3*n + 2*m - 11*lo; print('window', (n, m, lo), 'slack', s, 'deg bound', (s + 8)//2)
for n, h in [(21, 11), (22, 12), (23, 13)]:
    t = n - h
    for m in range(0, n - 1):
        if 17*t <= 5*n + 3*m:
            print('record cell n=%d h=%d tau=%d: HY needs m>=%d; I11 slack at each allowed m:' % (n, h, t, m), [(mm, 3*n + 2*mm - 11*t) for mm in range(m, n - 1)]); break
    else: print('record cell n=%d h=%d tau=%d: impossible by HY (m<=n-2)' % (n, h, t))
