"""Referee re-check (own code) of the three role facts used in L020 Step 4.3 on the 483 small near-tight graphs:
 (1) three pairwise NC vertices of degree <= 2 (b-configuration, edges allowed) only in E_1;
 (2) e-configurations only in the two (8,5,3) graphs;
 (3) f-configurations (pair {a,b} not inside an edge, c,e, all four cross pairs NC) in none;
also: NC pairs of the 45 K29 classes (expected none), and Observation 7 (triangle chains) by own canonical forms."""
import sys, time, itertools, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-fable')
import ref3 as R

I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
CELLS = ['cell_3_1_1', 'cell_10_7_4', 'cell_14_12_6', 'cell_17_13_7', 'cell_8_5_3', 'cell_12_10_5', 'cell_15_11_6',
         'cell_19_16_8', 'cell_22_17_9', 'cell_26_22_11']

def load(cell):
    out = []
    for l in open(I + cell + '.txt').read().split('\n'):
        if l.strip():
            n, m, t, E = R.parse_line(l)
            if max(R.degrees(n, E)) <= 3:
                out.append((n, m, t, E))
    return out

def nc_pairs(n, E):
    Ts, t = R.all_min_transversals(R.edge_masks(E), n)
    deg = R.degrees(n, E)
    low = [x for x in range(n) if deg[x] <= 2]
    nc = set()
    for x, y in itertools.combinations(low, 2):
        mk = (1 << x) | (1 << y)
        if not any((T & mk) == mk for T in Ts):
            nc.add((x, y))
    return nc, t, deg

def roles(n, E, nc):
    share = set()
    for e in E:
        for x, y in itertools.combinations(e, 2):
            share.add((x, y))
    def isnc(x, y):
        return (min(x, y), max(x, y)) in nc
    verts = sorted(set(u for p in nc for u in p))
    b = [tr for tr in itertools.combinations(verts, 3) if all(isnc(x, y) for x, y in itertools.combinations(tr, 2))]
    e_cfg = []
    for z in verts:
        part = [u for u in verts if u != z and isnc(z, u)]
        for a, c in itertools.combinations(part, 2):
            if (min(a, c), max(a, c)) not in share:
                e_cfg.append((z, a, c))
    f_cfg = []
    for a, b2 in itertools.combinations(verts, 2):
        if (a, b2) in share:
            continue
        part = [u for u in verts if u not in (a, b2) and isnc(a, u) and isnc(b2, u)]
        for c, e in itertools.combinations(part, 2):
            f_cfg.append(((a, b2), (c, e)))
    return b, e_cfg, f_cfg

def main():
    t0 = time.time()
    summary = {}
    stored = {}
    for cell in CELLS:
        gs = load(cell)
        stored[cell] = gs
        nb = ne = nf = nnc = 0
        for (n, m, t, E) in gs:
            nc, tt, deg = nc_pairs(n, E)
            b, e_cfg, f_cfg = roles(n, E, nc)
            nb += bool(b); ne += bool(e_cfg); nf += bool(f_cfg); nnc += bool(nc)
        summary[cell] = dict(classes=len(gs), with_NC=nnc, with_b=nb, with_e=ne, with_f=nf)
        print(cell, summary[cell], '(%.0fs)' % (time.time() - t0), flush=True)
    # the 45 K29 classes
    cls = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
    k29 = []
    withnc = 0
    for d in cls:
        n = d['n']; E = [tuple(sorted(e)) for e in d['edges']]
        nc, tt, deg = nc_pairs(n, E)
        withnc += bool(nc)
        k29.append((n, len(E), tt, E))
    print('K29 classes with an NC pair (degree<=2 vertices):', withnc, 'of', len(cls))

    # ---------------- Observation 7: Theta chains with the triangle T
    T = [(0, 1, 2), (2, 3, 4), (4, 5, 0)]  # relabelled triangle (6,3,2)
    nT = 6
    ncT, tT, degT = nc_pairs(nT, T)
    bT, eT, fT = roles(nT, T, ncT)
    print('triangle: tau', tT, 'NC pairs', sorted(ncT), 'b-configs', len(bT), 'e-configs', len(eT), 'f-configs', len(fT), fT)
    chain = [('cell_8_5_3', 'cell_15_11_6'), ('cell_12_10_5', 'cell_19_16_8'), ('cell_15_11_6', 'cell_22_17_9'),
             ('cell_19_16_8', 'cell_26_22_11'), ('cell_22_17_9', 'K29')]
    for src, dst in chain:
        t1 = time.time()
        built = set()
        nbuilt = 0
        for (n, m, t, E) in stored[src]:
            nc, tt, deg = nc_pairs(n, E)
            for (d, f) in nc:
                for (P1, (c, e)) in fT:
                    off = nT
                    E2 = list(T) + [tuple(sorted(x + off for x in g)) for g in E]
                    v = nT + n
                    E2 += [tuple(sorted((v,) + P1)), tuple(sorted((v, c, d + off))), tuple(sorted((v, e, f + off)))]
                    n2 = v + 1
                    if max(R.degrees(n2, E2)) > 3:
                        continue
                    if not (R.is_linear(E2) and not R.contains_F7_direct(n2, E2) and R.p3_hall(n2, E2)):
                        continue
                    t2 = R.tau(n2, E2)
                    if t2 != tT + t + 1:
                        continue
                    nbuilt += 1
                    built.add(R.canon(n2, E2))
        if dst == 'K29':
            target = set(R.canon(n, E) for (n, m, t, E) in k29)
        else:
            target = set(R.canon(n, E) for (n, m, t, E) in stored[dst])
        print('Theta(%s) -> %s: built %d near-tight graphs, %d classes; target classes %d; hit %d; outside target %d (%.0fs)' % (
            src, dst, nbuilt, len(built), len(target), len(built & target), len(built - target), time.time() - t1), flush=True)

if __name__ == '__main__':
    main()
