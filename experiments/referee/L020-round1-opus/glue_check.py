"""Independent rebuild of the Theorem 1 construction: e-configurations in the stored (20,15,8) and (8,5,3)
lists (own transversal code), all pattern-(e) gluings F + X + v, membership in C, Delta, tau, and the
isomorphism classes (own WL invariant + exact test) compared with K29_classes.json."""
import sys, json, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from roles_check import read_cell, analyse
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
t0 = time.time()
A = [g for g in read_cell(I + 'cell_20_15_8.txt') if max(hg.degrees(g[0], g[3])) <= 3]
X = read_cell(I + 'cell_8_5_3.txt')
def econfs(L):
    out = []
    for idx, (n, m, t, es) in enumerate(L):
        tt = hg.tau_bb(es); assert tt == t
        TL, d, NC, b_any, e_cfg, f_cfg, B = analyse(n, es, t)
        out.append((idx, e_cfg, b_any, f_cfg))
    return out
eA = econfs(A)
eX = econfs(X)
print('(20,15,8): classes', len(A), 'with e-config', sum(1 for z in eA if z[1]), 'e-config counts', sorted(len(z[1]) for z in eA if z[1]),
      'with b-config', sum(1 for z in eA if z[2]), 'with f-config', sum(1 for z in eA if z[3]), f'{time.time()-t0:.0f}s', flush=True)
print('(8,5,3): e-config counts', [len(z[1]) for z in eX], 'b', [len(z[2]) for z in eX], 'f', [len(z[3]) for z in eX])
built = []
for ia, ea, _, _ in eA:
    for (e, a, b) in ea:
        for ix, ex, _, _ in eX:
            for (f, c, d) in ex:
                nA, _, _, esA = A[ia]
                nX, _, _, esX = X[ix]
                es = list(esA) + [tuple(x + nA for x in ed) for ed in esX]
                v = nA + nX
                es += [tuple(sorted((v, a, b))), tuple(sorted((v, c + nA, d + nA))), tuple(sorted((v, e, f + nA)))]
                n = v + 1
                inC = hg.in_C(n, es)
                p3x = hg.p3_exhaustive_min(es)[0] >= 2
                t = hg.tau_bb(es)
                built.append(dict(n=n, es=es, inC=inC, p3x=p3x, maxdeg=max(hg.degrees(n, es)), tau=t, conn=hg.is_connected(n, es)))
print('gluings', len(built), 'in C (Hall)', sum(b['inC'] for b in built), 'P3 exhaustive', sum(b['p3x'] for b in built),
      'Delta<=3', sum(b['maxdeg'] <= 3 for b in built), 'tau=12', sum(b['tau'] == 12 for b in built),
      'connected', sum(b['conn'] for b in built), f'{time.time()-t0:.0f}s', flush=True)
table = {}
inv = {}
for b in built:
    k = hg.wl_invariant(b['n'], b['es'], table)[0]
    inv.setdefault(k, []).append(b)
print('distinct WL classes among gluings:', len(inv))
# exact check that gluings with equal invariants are isomorphic
noniso = 0
for k, lst in inv.items():
    for b in lst[1:]:
        if hg.iso_exact(lst[0]['n'], lst[0]['es'], b['n'], b['es']) is None:
            noniso += 1
print('gluings with equal WL invariant but non-isomorphic:', noniso)
cls = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
match = 0
for c in cls:
    k = hg.wl_invariant(c['n'], [tuple(e) for e in c['edges']], table)[0]
    if k in inv and hg.iso_exact(c['n'], [tuple(e) for e in c['edges']], inv[k][0]['n'], inv[k][0]['es']) is not None:
        match += 1
print('prover classes matched by an own gluing class:', match, 'of', len(cls))
