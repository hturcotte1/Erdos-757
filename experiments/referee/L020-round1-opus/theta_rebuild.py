"""Rebuild Theta(X) for every X in the stored (22,17,9,3) list (own code): triangle T with each of its
f-configurations ({a,b};{c,e}), every NC pair {d,f} of X (both orientations); keep K in C with Delta<=3 and
tau = tau(T)+tau(X)+1; classes compared with the 45 of Theorem 1."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from roles_check import read_cell, analyse
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
T = [(0, 1, 2), (2, 3, 4), (4, 5, 0)]
TLt, dt, NCt, bt, et, ft, Bt = analyse(6, T, 2)
L = [g for g in read_cell(I + 'cell_22_17_9.txt') if max(hg.degrees(g[0], g[3])) <= 3]
built = []
for n, m, t, es in L:
    TL, d, NC, b_any, e_cfg, f_cfg, B = analyse(n, es, t)
    for (x, y) in NC:
        for dd, f in ((x, y), (y, x)):
            for (a, b), (c, e) in ft:
                K = list(T) + [tuple(z + 6 for z in ed) for ed in es]
                v = 6 + n
                K += [tuple(sorted((v, a, b))), tuple(sorted((v, c, dd + 6))), tuple(sorted((v, e, f + 6)))]
                N = v + 1
                if max(hg.degrees(N, K)) > 3 or not hg.in_C(N, K):
                    continue
                tk = hg.tau_bb(K)
                if tk == 2 + t + 1:
                    built.append((N, K))
print('built near-tight graphs:', len(built), 'sizes', sorted(set((N, len(K)) for N, K in built)))
cls = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
table = {}
inv = {}
for i, c in enumerate(cls):
    inv[hg.wl_invariant(29, [tuple(e) for e in c['edges']], table)[0]] = i
hit = set(); new = 0
for N, K in built:
    k = hg.wl_invariant(N, K, table)[0]
    if k in inv and hg.iso_exact(N, K, 29, [tuple(e) for e in cls[inv[k]]['edges']]) is not None:
        hit.add(inv[k])
    else:
        new += 1
print('classes of the 45 hit:', len(hit), ' built graphs NOT among the 45:', new)
