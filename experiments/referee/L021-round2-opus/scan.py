"""Own re-enumeration of the candidate triples of L021 7.1 (n <= 27)."""
c = []
for n in range(3, 28):
    for m in range(1, n):
        for t in range(0, n + 1):
            if n > 2 * m + 1 or 3 * m < n or m > n - 2 and not (n == 3 and m == 1):
                continue
            s = 3 * n + 2 * m - 11 * t
            A = 27 * n + 35 * m - 132 * t
            if s >= 0 and 17 * t <= 5 * n + 3 * m and A < 0:
                c.append((n, m, t))
print(len(c), "candidate triples;", sum(1 for x in c if x[0] <= 24), "with n <= 24")
print("n >= 25:", [x for x in c if x[0] >= 25])
