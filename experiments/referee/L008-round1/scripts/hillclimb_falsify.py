"""Referee falsification attempt (heuristic, not a proof): local search in the ABSTRACT class O+ (linear, F7-free, P3) for
n in {14,15,16}, m in {n-3, n-2}, maximizing 11*tau - (3n+2m) (an I11 violation if > 0; at n = 16 a tau >= 7 would refute
Theorem 1).  Moves: replace one edge by a random triple keeping (P1)-(P3).  Exact tau by branching."""
import random, itertools, sys, time
def tau(E):
    def rec(es, k):
        if not es: return True
        if k == 0: return False
        e = es[0]
        return any(rec([f for f in es if v not in f], k - 1) for v in e)
    k = 0
    while not rec(E, k): k += 1
    return k
def linear_ok(E):
    seen = set()
    for e in E:
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen.add(p)
    return True
def f7(E):
    es = set(frozenset(e) for e in E); inc = {}
    for e in E:
        for v in e: inc.setdefault(v, []).append(frozenset(e))
    for p, L in inc.items():
        for a, b, c in itertools.combinations(L, 3):
            ra, rb, rc = sorted(a - {p}), sorted(b - {p}), sorted(c - {p})
            for i in (0, 1):
                for j in (0, 1):
                    if frozenset((ra[0], rb[i], rc[j])) in es and frozenset((ra[1], rb[1 - i], rc[1 - j])) in es: return True
    return False
def p3(E):
    ms = [sum(1 << v for v in e) for e in E]; m = len(ms); U = [0] * (1 << m)
    for F in range(1, 1 << m):
        low = (F & -F).bit_length() - 1; U[F] = U[F & (F - 1)] | ms[low]
        if bin(U[F]).count('1') < bin(F).count('1') + 2: return False
    return True
def ok(E): return linear_ok(E) and not f7(E) and p3(E)
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
best_overall = {}
T_END = time.time() + float(sys.argv[2] if len(sys.argv) > 2 else 120)
while time.time() < T_END:
    n = rng.choice([14, 15, 16]); m = rng.choice([n - 3, n - 2])
    E = []
    while len(E) < m:
        e = tuple(sorted(rng.sample(range(n), 3)))
        if ok(E + [e]): E.append(e)
        if len(E) < m and rng.random() < 0.001: E = []
    t = tau(E); score = 11 * t - (3 * n + 2 * m)
    for it in range(300):
        i = rng.randrange(m); e = tuple(sorted(rng.sample(range(n), 3)))
        F = E[:i] + E[i + 1:] + [e]
        if not ok(F): continue
        t2 = tau(F); s2 = 11 * t2 - (3 * n + 2 * m)
        if s2 >= score: E, t, score = F, t2, s2
    key = (n, m); b = best_overall.get(key)
    if b is None or score > b[0]: best_overall[key] = (score, t, E)
    if score > 0 or (n == 16 and t >= 7): print('VIOLATION', n, m, t, E); break
for k in sorted(best_overall): print('n=%d m=%d best 11tau-(3n+2m) = %d (tau=%d)' % (k[0], k[1], best_overall[k][0], best_overall[k][1]))
