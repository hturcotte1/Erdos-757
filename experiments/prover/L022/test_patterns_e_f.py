"""Direct test of the two new steps of Theorem 2 (patterns (e) and (f)) on two-piece graphs built from stored
low-slack pieces (E_1, (8,5,3), (10,7,4), (12,10,5), (14,12,6), (15,11,6), (17,13,7): the stored lists, Delta<=3 and Delta<=4).
For random choices of pieces F1, F2 and of three disjoint pairs in pattern (e) or (f) (attachment vertices of piece-degree
<=2, inside pairs not inside an edge), compute exactly whether (*) holds: tau(H) = tau(F1)+tau(F2)+1 for H = F1+F2+v.
Whenever (*) holds, check the sub-extension identities used in the proof:
  (e): tau(H[V(F1) u {v,f}]) = tau(F1)+1 and tau(H[V(F2) u {v,e}]) = tau(F2)+1;
  (f): tau(H[V(F1) u {v,d}]) = tau(F1)+1 and tau(H[V(F1) u {v,f}]) = tau(F1)+1.
Exact.  usage: python3 test_patterns_e_f.py seed trials"""
import sys, random
import lib22
from hyp import tau_masks, masks
INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_%s.txt'
cells = ['3_1_1', '8_5_3', '10_7_4', '12_10_5', '14_12_6', '15_11_6', '17_13_7']
pieces = []
for c in cells:
    for l in open(INP % c):
        t = list(map(int, l.split()))
        if not t: continue
        n, m, tau = t[:3]; E = [tuple(t[3 + 3 * i:6 + 3 * i]) for i in range(m)]
        pieces.append((c, n, E, tau))
def tau(E): return tau_masks(masks(E)) if E else 0
def ind(E, S): S = set(S); return [e for e in E if all(x in S for x in e)]
rnd = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
cnt = dict(e=0, f=0, e_star=0, f_star=0, fail=0)
for t in range(trials):
    (c1, n1, E1, t1), (c2, n2, E2, t2) = rnd.choice(pieces), rnd.choice(pieces)
    E2s = [tuple(x + n1 for x in e) for e in E2]
    v = n1 + n2
    d1 = [0] * n1; d2 = [0] * n2
    for e in E1:
        for x in e: d1[x] += 1
    for e in E2:
        for x in e: d2[x] += 1
    A1 = [x for x in range(n1) if d1[x] <= 2]; A2 = [x + n1 for x in range(n2) if d2[x] <= 2]
    pat = rnd.choice('ef')
    try:
        if pat == 'e':
            a, b, e = rnd.sample(A1, 3); c, d, f = rnd.sample(A2, 3)
            if any({a, b} <= set(g) for g in E1) or any({c, d} <= set(g) for g in E2s): continue
            P = [(a, b), (c, d), (e, f)]
        else:
            a, b, c, e = rnd.sample(A1, 4); d, f = rnd.sample(A2, 2)
            if any({a, b} <= set(g) for g in E1): continue
            P = [(a, b), (c, d), (e, f)]
    except ValueError:
        continue
    cnt[pat] += 1
    H = E1 + E2s + [tuple(sorted((v,) + p)) for p in P]
    if tau(H) != t1 + t2 + 1: continue
    cnt[pat + '_star'] += 1
    V1 = list(range(n1)); V2 = list(range(n1, n1 + n2))
    if pat == 'e':
        ok = tau(ind(H, V1 + [v, f])) == t1 + 1 and tau(ind(H, V2 + [v, e])) == t2 + 1
    else:
        ok = tau(ind(H, V1 + [v, d])) == t1 + 1 and tau(ind(H, V1 + [v, f])) == t1 + 1
    if not ok:
        cnt['fail'] += 1; print('FAIL', pat, c1, c2, P, flush=True)
print(cnt)
