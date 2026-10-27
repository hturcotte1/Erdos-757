# Cell arithmetic used in L022 Corollary 3' and N4' (exact integers).
def cells(N, slacks):
    out = []
    for m in range(-(-(N - 1) // 2), N - 1):          # ceil((N-1)/2) <= m <= N-2
        for t in range(1, m + 1):
            s = 3 * N + 2 * m - 11 * t
            if s in slacks and 17 * t <= 5 * N + 3 * m and 3 * m >= N:
                out.append((N, m, t, s))
    return out
print('violator cells n=30 (s in {-1,-2}):', cells(30, {-1, -2}))
for (N, m, t, s) in cells(30, {-1, -2}):
    n1, m1, t1 = N - 1, m - 3, t - 1
    print('  H-v cell', (n1, m1, t1), 'slack', 3 * n1 + 2 * m1 - 11 * t1,
          'connected possible (n<=2m+1):', n1 <= 2 * m1 + 1,
          '| max vertices of a disconnected G with r<=3 comps:', 2 * m1 + 3)
print('connected slack-1 cells with 27 vertices:', cells(27, {1}))
print('connected tight cells with 27 vertices:', cells(27, {0}))
print('connected tight cells n<=26:', [c[:3] for n in range(3, 27) for c in cells(n, {0})])
print('connected slack-1 cells n<=26:', [c[:3] for n in range(3, 27) for c in cells(n, {1})])
