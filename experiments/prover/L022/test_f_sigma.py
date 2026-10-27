"""Exercise of Theorem 2(iv) of L022 (pattern (f), d and f sharing an edge g={d,f,z} of F2): whenever (*) holds for
H = F1 + F2 + v (pattern (f): P1={a,b} in F1, c,e in F1, d,f in F2 with {d,f,z} an edge of F2), check
tau(H[V(F1) u {v,d,f,z}]) = tau(F1) + 2, i.e. slack s(F1) - 2.  Pieces: E_1, (8,5,3) x2, (10,7,4) x5, (12,10,5) first 40.
Exact.  usage: python3 test_f_sigma.py"""
import itertools
import lib22
from hyp import tau_masks, masks
INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_%s.txt'
pieces = []
for c, lim in [('3_1_1', 9), ('8_5_3', 9), ('10_7_4', 9), ('12_10_5', 40)]:
    for i, l in enumerate(open(INP % c)):
        if i >= lim: break
        t = list(map(int, l.split()))
        if t: pieces.append((c, t[0], [tuple(t[3 + 3 * j:6 + 3 * j]) for j in range(t[1])]))
def tau(E): return tau_masks(masks(E)) if E else 0
def sl(S, E):
    S = set(S); F = [e for e in E if all(x in S for x in e)]
    return 3 * len(S) + 2 * len(F) - 11 * tau(F)
cnt = dict(conf=0, star=0, fail=0)
small = [p for p in pieces if p[1] <= 10]
for (c1, n1, E1) in pieces:
    for (c2, n2, E2) in small:
        E2s = [tuple(x + n1 for x in e) for e in E2]; v = n1 + n2
        t1, t2 = tau(E1), tau(E2); s1 = sl(range(n1), E1)
        d = {}
        for e in E1 + E2s:
            for x in e: d[x] = d.get(x, 0) + 1
        A1 = [x for x in range(n1) if d.get(x, 0) <= 2]
        V1 = list(range(n1))
        for g in E2s:
            for dd, f in itertools.permutations(g, 2):
                if d[dd] > 2 or d[f] > 2: continue
                z = [x for x in g if x not in (dd, f)][0]
                for P1 in itertools.combinations(A1, 2):
                    if any(set(P1) <= set(h) for h in E1): continue
                    for c, e in itertools.combinations([x for x in A1 if x not in P1], 2):
                        for (cc, ee) in ((c, e), (e, c)):
                            cnt['conf'] += 1
                            H = E1 + E2s + [(v,) + P1, (v, cc, dd), (v, ee, f)]
                            if tau(H) != t1 + t2 + 1: continue
                            cnt['star'] += 1
                            if sl(V1 + [v, dd, f, z], H) != s1 - 2:
                                cnt['fail'] += 1; print('FAIL', c1, c2, P1, cc, ee, dd, f, z, flush=True)
print(cnt)
