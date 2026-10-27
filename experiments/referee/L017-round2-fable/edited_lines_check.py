# Independent one-line checks of the two edited inequalities (referee round 2, L017).
# (1) Theorem 4(vi), pattern (f), F_2 side: from d'(d)+d'(f)-sigma <= 2 with d' in {1,2}, sigma in {0,1}.
ok = True
for dd in (1, 2):
    for df in (1, 2):
        for sg in (0, 1):
            if dd + df - sg <= 2:
                deg3 = (dd == 2) + (df == 2)
                # claim: at most one of d,f has H-degree 3 (d'=2), and if one does then sigma = 1
                if deg3 > 1 or (deg3 == 1 and sg != 1):
                    ok = False
                    print("VIOLATION", dd, df, sg)
print("Theorem 4(vi)(f) F_2 side:", "OK" if ok else "FAIL")
# (2) Remark 13.2, Property (P) on E_1 = one edge {0,1,2}: tau = 1, every pair has degrees (1,1),
# shares the edge, and lies in no common minimum transversal -> all three pairs are exceptions.
from itertools import combinations
V = [0, 1, 2]; E = [frozenset(V)]
tau = min(k for k in range(4) if any(all(set(T) & e for e in E) for T in combinations(V, k)))
minT = [set(T) for T in combinations(V, tau) if all(set(T) & e for e in E)]
exc = [p for p in combinations(V, 2) if not any(set(p) <= T for T in minT)]
print("E_1: tau =", tau, "; pairs with no common minimum transversal:", exc,
      "; degrees all 1, all share the edge -> not exempt by the (1,2) clause -> exceptions:", len(exc))
# (3) Attribution arithmetic: HY Thm 14 at k=3; Chvatal-Hanson at Delta=3; 4.6(a) equivalence.
k = 3
print("HY Thm14 k=3 coefficients:", k*(k*k-3), (k-2)*(k+1), (k-1)**2, k-1, "-> 18 tau <= 4n+4m+2")
from fractions import Fraction as Fr
print("Chvatal-Hanson Delta=3: |E| <= 3nu+floor(nu/2) <= 7nu/2 -> 3|E| <=", Fr(21,2), "nu < 11 nu for nu>=1")
for n in range(3, 12):
    for m in range(1, n):
        if 3*m <= 2*n:
            lhs = 11*(4*n+4*m+2) <= 18*(3*n+2*m); rhs = 8*m+22 <= 10*n
            assert lhs == rhs
print("4.6(a) equivalence 11(4n+4m+2)<=18(3n+2m) <=> 8m+22<=10n: OK; fails only for n<=4 with 3m<=2n:",
      [(n, m) for n in range(3, 8) for m in range(1, n) if 3*m <= 2*n and not (8*m+22 <= 10*n)])
