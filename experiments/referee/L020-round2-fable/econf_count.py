"""Own count of e-configurations in cell(20,15,8,3) and cell(8,5,3), rebuild of the pattern-(e) gluings and
an isomorphism-invariant comparison with the 45 stored classes."""
import sys, itertools, json, time
from ref4 import *
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
def nc_pairs(edges, verts, tK, deg):
    low = [v for v in verts if deg[v] <= 2]
    return {tuple(sorted((x, y))) for x, y in itertools.combinations(low, 2) if tau(induced(edges, {x, y})) != tK - 2}
def e_configs(edges, verts, tK, deg):
    NC = nc_pairs(edges, verts, tK, deg)
    out = []
    low = [v for v in verts if deg[v] <= 2]
    for z in low:
        nb = [x for x in low if x != z and tuple(sorted((z, x))) in NC]
        for x, y in itertools.combinations(nb, 2):
            if not any({x, y} <= set(e) for e in edges): out.append((z, x, y))
    return out
def invariant(edges, verts):
    """colour refinement on vertices (multiset of neighbour colours through edges), 4 rounds; returns a hashable string"""
    col = {v: 0 for v in verts}
    for _ in range(4):
        sig = {}
        for v in verts:
            s = sorted(tuple(sorted(col[u] for u in e if u != v)) for e in edges if v in e)
            sig[v] = (col[v], tuple(s))
        keys = sorted(set(sig.values())); idx = {k: i for i, k in enumerate(keys)}
        col = {v: idx[sig[v]] for v in verts}
    return str(sorted(col.values())) + '|' + str(sorted(sorted(tuple(sorted(col[u] for u in e)) for e in edges)))
t0 = time.time()
X = []
for (n, m, t, edges) in parse_cell_file(I + 'cell_8_5_3.txt'):
    verts = set().union(*map(set, edges)); deg = degrees(edges, verts); assert tau(edges) == t
    ec = e_configs(edges, verts, t, deg); X.append((edges, verts, ec)); print('(8,5,3) class: e-configs', len(ec), ec)
F = []; nwith = 0; total = 0
for ci, (n, m, t, edges) in enumerate(parse_cell_file(I + 'cell_20_15_8.txt')):
    verts = set().union(*map(set, edges)); deg = degrees(edges, verts)
    if max(deg.values()) > 3: continue
    total += 1
    ec = e_configs(edges, verts, t, deg)
    if ec:
        nwith += 1; F.append((ci, edges, verts, ec))
        print(f'(20,15,8) class {ci}: {len(ec)} e-config(s) {ec}  ({time.time()-t0:.0f}s)', flush=True)
print('(20,15,8): classes', total, 'with an e-configuration', nwith, 'total e-configs', sum(len(f[3]) for f in F))
# gluings
invs = {}; ngl = 0; bad = 0
for (ci, fe, fv, fec) in F:
    for (z, a, b) in fec:
        for (xe, xv, xec) in X:
            off = 50
            xe2 = [tuple(sorted(u + off for u in e)) for e in xe]; xv2 = {u + off for u in xv}
            for (f, c, d) in xec:
                v = 99
                K = fe + xe2 + [tuple(sorted((v, a, b))), tuple(sorted((v, c + off, d + off))), tuple(sorted((v, z, f + off)))]
                KV = fv | xv2 | {v}
                ngl += 1
                degK = degrees(K, KV)
                ok = max(degK.values()) <= 3 and in_C(K, KV) and tau(K) == 12 and len(components(K, KV)[0]) == 1
                if not ok: bad += 1
                invs.setdefault(invariant(K, KV), []).append((ci, z, a, b))
print('gluings', ngl, 'not (in C, Delta<=3, tau 12, connected):', bad, 'distinct invariants', len(invs))
stored = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
sinv = {invariant([tuple(e) for e in r['edges']], set(range(29))) for r in stored}
print('stored 45 classes: distinct invariants', len(sinv), '| equal to the gluing invariant set:', sinv == set(invs))
print(f'done {time.time()-t0:.0f}s')
