"""L003 round 3: n <= 5 part of the Statement, exact/symbolic. No repo imports."""
from fractions import Fraction as Fr
from itertools import combinations
def is45(X): return all(len({b - a, c - a, d - a, c - b, d - b, d - c}) >= 5 for a, b, c, d in combinations(X, 4))
def sidon(S):
    d = [b - a for a, b in combinations(S, 2)]; return len(d) == len(set(d))
def hmax(X):
    for k in range(len(X), 0, -1):
        if any(sidon(S) for S in combinations(X, k)): return k
def aps(X):
    s = set(X); return [(a, (a + c) / 2, c) for a, c in combinations(sorted(X), 2) if (a + c) / 2 in s]
# points as linear forms (a, b) = a + b*x
fams = {4: [(0, 0), (1, 0), (2, 0), (0, 1)], 5: [(0, 0), (1, 0), (2, 0), (0, 1), (0, 3)]}
for n, P in fams.items():
    dist = [((P[j][0] - P[i][0], P[j][1] - P[i][1]), (i, j)) for i, j in combinations(range(n), 2)]
    ident, roots = [], []
    for (d1, p1), (d2, p2) in combinations(dist, 2):
        if d1 == d2: ident.append((p1, p2))
        elif d1[1] != d2[1]: roots.append(Fr(d2[0] - d1[0], d1[1] - d2[1]))
    # order: consecutive differences positive for x > 4 (linear forms, check at 4 and slope)
    order_ok = all((P[i + 1][0] - P[i][0]) + (P[i + 1][1] - P[i][1]) * 4 >= 0 and (P[i + 1][1] - P[i][1]) >= 0 for i in range(n - 1))
    print("n=%d identical coincidences %s; max root of other coincidences %s; order for x>4: %s" % (n, ident, max(roots), order_ok))
    for x in (Fr(41, 10), 5, 6, 17, Fr(1001, 3)):
        X = sorted(a + b * Fr(x) for a, b in P)
        print("   x=%s 45=%s APs=%s h=%d" % (x, is45(X), [(str(a), str(b), str(c)) for a, b, c in aps(X)], hmax(X)))
# f(4) >= 3 and f(5) >= 4: every linear 3-graph on 4 or 5 vertices has transversal number <= 1
for n in (4, 5):
    triples = list(combinations(range(n), 3)); worst = 0; fams_ = 0
    for mask in range(1, 1 << len(triples)):
        E = [triples[i] for i in range(len(triples)) if mask >> i & 1]
        if any(len(set(a) & set(b)) >= 2 for a, b in combinations(E, 2)): continue
        fams_ += 1
        tau = next(t for t in range(n + 1) if any(all(set(e) & set(T) for e in E) for T in combinations(range(n), t)))
        worst = max(worst, tau)
    print("n=%d: %d nonempty linear 3-graphs, max tau = %d -> h = n - tau >= %d for weak Sidon sets" % (n, fams_, worst, n - worst))
# n = 3: h({a<b<c}) = 2 iff b-a = c-b (AP), so extremal 3-sets are exactly the 3-APs = one affine class
print("n=3: {0,1,2} h=%d, {0,1,3} h=%d" % (hmax([0, 1, 2]), hmax([0, 1, 3])))
