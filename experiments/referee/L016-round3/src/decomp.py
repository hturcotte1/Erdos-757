# Referee L016 round 3: brute-force decompositions of (n', m') with total slack S' into component types.
# Types: isolated vertex (1,0,0) slack 3; connected (a,b,t): a>=3, 1<=b<=a-2 (P3), a<=2b+1, 1<=t<=b, 17t<=5a+3b (K8), s=3a+2b-11t>=0 (I11 below 27).
import sys
def types_for(nmax, mmax):
    T = [(1, 0, 0, 3)]
    for a in range(3, nmax + 1):
        for b in range(1, min(a - 2, mmax) + 1):
            if a > 2 * b + 1: continue
            for t in range(1, b + 1):
                if 17 * t > 5 * a + 3 * b: continue
                s = 3 * a + 2 * b - 11 * t
                if s < 0: continue
                T.append((a, b, t, s))
    return T
def decompositions(n, m, S):
    T = types_for(n, m); res = []
    def rec(i, n, m, S, cur):
        if n == 0:
            if m == 0 and S == 0: res.append(tuple(cur))
            return
        if m < 0 or S < 0: return
        for j in range(i, len(T)):
            a, b, t, s = T[j]
            if a <= n and b <= m and s <= S:
                cur.append((a, b, t)); rec(j, n - a, m - b, S - s, cur); cur.pop()
    rec(0, n, m, S, [])
    return sorted(res)
if __name__ == '__main__':
    cases = [("(27,13,10,2) d=2 t'=9", 26, 11, 1), ("(27,14,10,3) d=2 t'=9", 26, 12, 3), ("(27,14,10,3) d=3 t'=9", 26, 11, 1),
             ("(27,18,11,2) d=2 t'=10", 26, 16, 0), ("(27,19,11,3) d=3 t'=10", 26, 16, 0), ("(27,25,12,3) d=3 t'=11", 26, 22, 1),
             ("(26,22,11,3) d=3 t'=10", 25, 19, 3), ("(25,19,10,3) d=3 t'=9", 24, 16, 5), ("(24,16,9,3) d=2 t'=8", 23, 14, 9), ("(24,16,9,3) d=3 t'=8", 23, 13, 7)]
    for name, n, m, S in cases:
        D = decompositions(n, m, S)
        print(name, "-> (%d,%d) slack %d: %d decompositions" % (n, m, S, len(D)))
        if len(D) <= 20:
            for d in D: print("   ", list(d))
