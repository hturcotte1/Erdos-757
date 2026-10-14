"""Patterns (rank order) of the known 12-point sets, computed from the definition; and their normalized form."""
import json, math
from math import gcd
sets = {
 "record_12": [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575],
 "12b_omega1": [0, 178, 198, 218, 227, 235, 272, 276, 287, 317, 356, 436],
 "12c_omega2": [-336, -168, -44, -24, -4, 0, 39, 44, 49, 80, 102, 160],
}
def pattern(A):
    A = sorted(A); idx = {v: i for i, v in enumerate(A)}
    E = []
    for a in range(len(A)):
        for c in range(a + 2, len(A)):
            s = A[a] + A[c]
            if s % 2 == 0 and s // 2 in idx: E.append((a, idx[s // 2], c))
    return sorted(E)
def norm(A):
    A = sorted(A); v = [x - A[0] for x in A]; g = 0
    for x in v: g = gcd(g, x)
    v = [x // g for x in v]; r = sorted(v[-1] - x for x in v)
    return min(v, r)
if __name__ == "__main__":
    for k, A in sets.items():
        E = pattern(A)
        print(" ".join("%d,%d,%d" % e for e in E), "#", k, norm(A))
