def types_all(N, S):
    T = []
    if S >= 3: T.append((1, 0, 0))
    for p in range(3, N + 1):
        for m in range(1, p - 1):
            if p > 2 * m + 1: continue
            for t in range(1, m + 1):
                s = 3 * p + 2 * m - 11 * t
                if 0 <= s <= S and 17 * t <= 5 * p + 3 * m: T.append((p, m, t))
    return T
def my_decomps(N, M, S):
    T = types_all(N, S); res = set()
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S: res.add(tuple(sorted(chosen))); return
        if i >= len(T) or n > N or m > M or s > S: return
        p = T[i]; sp = 3 * p[0] + 2 * p[1] - 11 * p[2]; k = 0
        while n + k * p[0] <= N and m + k * p[1] <= M and s + k * sp <= S:
            rec(i + 1, n + k * p[0], m + k * p[1], s + k * sp, chosen + [p] * k); k += 1
    rec(0, 0, 0, 0, [])
    return res
