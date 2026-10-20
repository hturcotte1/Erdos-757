#!/usr/bin/env python3
"""Controls for r2_family.py's census method and for r3's 4-subset test: plant points that create
cross-copy relations / extra coincidences and verify they are detected.  Own code."""
import sys
sys.path.insert(0, ".")
from r2_family import build
from itertools import combinations

def census(I):
    Iset = set(I)
    classes = set()
    for p1 in I:
        for p2 in I:
            s = p1 + p2
            for p3 in I:
                p4 = s - p3
                if p4 in Iset and not ((p1 == p3 and p2 == p4) or (p1 == p4 and p2 == p3)):
                    a = tuple(sorted((p1, p2))); b = tuple(sorted((p3, p4)))
                    classes.add(tuple(sorted((a, b))))
    four = sum(1 for a, b in classes if len(set(a) | set(b)) == 4)
    return len(classes), four

def min_BB(I):
    m = 10 ** 9
    for B in combinations(I, 4):
        D = {a - b for a in B for b in B}
        if len(D) < m:
            m = len(D)
    return m

K = 3
copies, S, I = build(K)
print("baseline K=3: classes, four-point =", census(I), " min|B-B| =", min_BB(I))
# plant p = a + b - c with a in copy 0 interior, b in copy 2 interior, c in copy 3 interior
scale = 269 ** K
a = int(copies[0][1] * scale); b = int(copies[2][3] * scale); c = int(copies[3][4] * scale)
p = a + b - c
assert p not in set(I)
J = sorted(I + [p])
cl, four = census(J)
print("planted p=a+b-c: classes=%d four-point=%d min|B-B|=%d" % (cl, four, min_BB(J)))
# plant the midpoint of two points of different copies: creates a 3-AP across copies
q2 = int(copies[0][2] * scale) + int(copies[3][5] * scale)
if q2 % 2 == 0:
    q = q2 // 2
else:
    q = None
# alternative: reflection 2a - c (3-AP a as middle)
q = 2 * int(copies[1][2] * scale) - int(copies[3][6] * scale)
assert q not in set(I)
J2 = sorted(I + [q])
cl2, four2 = census(J2)
print("planted q=2a-c: classes=%d four-point=%d min|B-B|=%d" % (cl2, four2, min_BB(J2)))
print("small controls: min|B-B| for {1,2,3,5}:", min_BB([1, 2, 3, 5]), " for {0,1,3,7}:", min_BB([0, 1, 3, 7]))
ok = census(I) == (36, 0) and four >= 1 and cl > 36 and cl2 > 36 and min_BB([1, 2, 3, 5]) == 9 and min_BB([0, 1, 3, 7]) == 13
print("CONTROLS OK" if ok else "CONTROLS FAILED")
