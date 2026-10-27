"""Exhaustive exercise of the identities behind Theorem 2(ii),(iii) of L022: for pieces F1, F2 in
{E_1, the two (8,5,3) classes, the five (10,7,4) classes} and EVERY pattern-(e) / pattern-(f) choice of three disjoint pairs
(attachment vertices of piece-degree <= 2; an inside pair not inside an edge), whenever (*) holds
(tau(H) = tau(F1)+tau(F2)+1, H = F1 + F2 + v + the three edges) check
  (e): s(H[V(F1)+v+f]) = s(F1)-1 and s(H[V(F2)+v+e]) = s(F2)-1;   (f): s(H[V(F1)+v+d]) = s(F1)-1 = s(H[V(F1)+v+f]).
Exact.  usage: python3 test_ef_exhaustive.py"""
import itertools
import lib22
from hyp import tau_masks, masks
INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_%s.txt'
pieces = []
for c in ['3_1_1', '8_5_3', '10_7_4']:
    for l in open(INP % c):
        t = list(map(int, l.split()))
        if t: pieces.append((c, t[0], [tuple(t[3 + 3 * i:6 + 3 * i]) for i in range(t[1])]))
def tau(E): return tau_masks(masks(E)) if E else 0
def sl(S, E):
    S = set(S); F = [e for e in E if all(x in S for x in e)]
    return 3 * len(S) + 2 * len(F) - 11 * tau(F)
cnt = dict(e_conf=0, f_conf=0, e_star=0, f_star=0, fail=0)
for (c1, n1, E1), (c2, n2, E2) in itertools.product(pieces, repeat=2):
    E2s = [tuple(x + n1 for x in e) for e in E2]; v = n1 + n2
    t1, t2 = tau(E1), tau(E2)
    s1, s2 = sl(range(n1), E1), sl(range(n1, n1 + n2), E2s)
    d = {}
    for e in E1 + E2s:
        for x in e: d[x] = d.get(x, 0) + 1
    A1 = [x for x in range(n1) if d.get(x, 0) <= 2]; A2 = [x for x in range(n1, n1 + n2) if d.get(x, 0) <= 2]
    in1 = lambda p: any(set(p) <= set(g) for g in E1); in2 = lambda p: any(set(p) <= set(g) for g in E2s)
    V1 = list(range(n1)); V2 = list(range(n1, n1 + n2))
    # pattern (e): P1 in F1, P2 in F2, P3 = {e,f} split
    for P1 in itertools.combinations(A1, 2):
        if in1(P1): continue
        for e in A1:
            if e in P1: continue
            for P2 in itertools.combinations(A2, 2):
                if in2(P2): continue
                for f in A2:
                    if f in P2: continue
                    cnt['e_conf'] += 1
                    H = E1 + E2s + [(v,) + P1, (v,) + P2, (v, e, f)]
                    if tau(H) != t1 + t2 + 1: continue
                    cnt['e_star'] += 1
                    if not (sl(V1 + [v, f], H) == s1 - 1 and sl(V2 + [v, e], H) == s2 - 1):
                        cnt['fail'] += 1; print('FAIL e', c1, c2, P1, e, P2, f)
    # pattern (f): P1 in F1, P2 = {c,d}, P3 = {e,f}, c,e in F1, d,f in F2
    for P1 in itertools.combinations(A1, 2):
        if in1(P1): continue
        for c, e in itertools.permutations([x for x in A1 if x not in P1], 2):
            if c > e: continue
            for dd, f in itertools.permutations(A2, 2):
                cnt['f_conf'] += 1
                H = E1 + E2s + [(v,) + P1, (v, c, dd), (v, e, f)]
                if tau(H) != t1 + t2 + 1: continue
                cnt['f_star'] += 1
                if not (sl(V1 + [v, dd], H) == s1 - 1 and sl(V1 + [v, f], H) == s1 - 1):
                    cnt['fail'] += 1; print('FAIL f', c1, c2, P1, c, e, dd, f)
print(cnt)
