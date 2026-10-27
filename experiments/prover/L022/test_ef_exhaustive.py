"""Exhaustive exercise of the identities behind Theorem 2(ii)-(iv) of L022.
Pieces F1, F2 from {E_1, the two (8,5,3) classes, the five (10,7,4) classes, the first 8 (12,10,5) classes} (stored lists).
For EVERY pattern-(e) and pattern-(f) choice of three disjoint pairs (attachment vertices of piece-degree <= 2; an inside pair
not inside an edge), decide (*) [no minimum transversal of F1 u F2 meets the three pairs, i.e. tau(H) = tau(F1)+tau(F2)+1]
from the lists of all minimum transversals of the pieces (bitmasks, hyp.all_min_transversals); for every configuration
satisfying (*), compute tau DIRECTLY (branch and bound on the edge list, independent of the transversal lists) for H and
for the sub-extensions H[Y] and check:
  (*) itself: tau(H) = tau(F1) + tau(F2) + 1;
  (e) s(H[V(F1)+v+f]) = s(F1)-1 and s(H[V(F2)+v+e]) = s(F2)-1;
  (f) s(H[V(F1)+v+d]) = s(F1)-1 = s(H[V(F1)+v+f]);
  (f) with {d,f,z} an edge of F2 and F2 not that single edge: s(H[V(F1)+v+d+f+z]) = s(F1)-2.
usage: python3 test_ef_exhaustive.py"""
import itertools
import lib22  # sets sys.path for hyp
from hyp import tau_masks, masks, all_min_transversals

INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_%s.txt'
pieces = []
for c, lim in [('3_1_1', 9), ('8_5_3', 9), ('10_7_4', 9), ('12_10_5', 8)]:
    for i, l in enumerate(open(INP % c)):
        if i >= lim:
            break
        t = list(map(int, l.split()))
        if t:
            pieces.append((c + '#' + str(i), t[0], [tuple(t[3 + 3 * j:6 + 3 * j]) for j in range(t[1])]))


def tau(E):
    return tau_masks(masks(E)) if E else 0


def sl(S, E):
    S = set(S)
    F = [e for e in E if all(x in S for x in e)]
    return 3 * len(S) + 2 * len(F) - 11 * tau(F)


info = []
for name, n, E in pieces:
    Ts, t = all_min_transversals(masks(E))
    d = [0] * n
    for e in E:
        for x in e:
            d[x] += 1
    info.append((name, n, E, Ts, t, d, 3 * n + 2 * len(E) - 11 * t))

TAB = {}
def tables(k):
    if k in TAB:
        return TAB[k]
    name, n, E, Ts, t, d, s_ = info[k]
    mP = {}; mPx = {}; c2 = {}
    for P in itertools.combinations(range(n), 2):
        mP[P] = any((T >> P[0]) & 1 or (T >> P[1]) & 1 for T in Ts)
        for x in range(n):
            mPx[(P, x)] = any(((T >> P[0]) & 1 or (T >> P[1]) & 1) and (T >> x) & 1 for T in Ts)
        c2[P] = any((T >> P[0]) & 1 and (T >> P[1]) & 1 for T in Ts)
    TAB[k] = (mP, mPx, c2)
    return TAB[k]


def meets(T, P):
    return any((T >> x) & 1 for x in P)


cnt = dict(e_conf=0, e_star=0, f_conf=0, f_star=0, fz_checked=0, fail=0)
for k1, k2 in itertools.product(range(len(info)), repeat=2):
    (n1_, n1, E1, T1s, t1, d1, s1), (n2_, n2, E2, T2s, t2, d2, s2) = info[k1], info[k2]
    mP1, mPx1, c21 = tables(k1); mP2, mPx2, c22 = tables(k2)
    A1 = [x for x in range(n1) if d1[x] <= 2]
    A2 = [x for x in range(n2) if d2[x] <= 2]
    in1 = lambda p: any(set(p) <= set(g) for g in E1)
    in2 = lambda p: any(set(p) <= set(g) for g in E2)
    E2s = [tuple(x + n1 for x in e) for e in E2]
    v = n1 + n2
    V1 = list(range(n1))
    V2 = list(range(n1, n1 + n2))
    # pattern (e): P1 in F1, e in F1; P2 in F2, f in F2
    for P1 in itertools.combinations(A1, 2):
        if in1(P1):
            continue
        okP1 = mP1[P1]
        for e in A1:
            if e in P1:
                continue
            ok1 = mPx1[(P1, e)]
            for P2 in itertools.combinations(A2, 2):
                if in2(P2):
                    continue
                okP2 = mP2[P2]
                for f in A2:
                    if f in P2:
                        continue
                    cnt['e_conf'] += 1
                    # (*) fails iff some T1, T2 with T1 meeting P1, T2 meeting P2 and (e in T1 or f in T2)
                    if ok1 and okP2:
                        continue
                    if okP1 and mPx2[(P2, f)]:
                        continue
                    cnt['e_star'] += 1
                    H = E1 + E2s + [(v,) + P1, (v, P2[0] + n1, P2[1] + n1), (v, e, f + n1)]
                    good = (tau(H) == t1 + t2 + 1 and sl(V1 + [v, f + n1], H) == s1 - 1
                            and sl(V2 + [v, e], H) == s2 - 1)
                    if not good:
                        cnt['fail'] += 1
                        print('FAIL e', n1_, n2_, P1, e, P2, f, flush=True)
    # pattern (f): P1 in F1; c, e in F1; d, f in F2
    for P1 in itertools.combinations(A1, 2):
        if in1(P1):
            continue
        okP1 = mP1[P1]
        rest = [x for x in A1 if x not in P1]
        for c, e in itertools.combinations(rest, 2):
            okc = mPx1[(P1, c)] or mPx1[(P1, e)]
            for dd, f in itertools.combinations(A2, 2):
                okdf = c22[(dd, f)]
                for (cc, ee) in ((c, e), (e, c)):
                    cnt['f_conf'] += 1
                    if okc:
                        continue
                    if okP1 and okdf:
                        continue
                    cnt['f_star'] += 1
                    H = E1 + E2s + [(v,) + P1, (v, cc, dd + n1), (v, ee, f + n1)]
                    good = (tau(H) == t1 + t2 + 1 and sl(V1 + [v, dd + n1], H) == s1 - 1
                            and sl(V1 + [v, f + n1], H) == s1 - 1)
                    g = [x for x in E2 if dd in x and f in x]
                    if g and n2 != 3:
                        z = [x for x in g[0] if x not in (dd, f)][0]
                        cnt['fz_checked'] += 1
                        good = good and sl(V1 + [v, dd + n1, f + n1, z + n1], H) == s1 - 2
                    if not good:
                        cnt['fail'] += 1
                        print('FAIL f', n1_, n2_, P1, cc, ee, dd, f, flush=True)
print(cnt)
