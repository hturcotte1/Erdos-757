"""Referee check of L020 Theorem 3 and Proposition 6 on the stored near-tight graphs (own code).
For every stored graph K with Delta<=3 in the slack<=1 lists (inputs/), every degree-3 vertex v:
  (i)   tau(K-v) = tau(K)-1; the co-vertex pairs are disjoint, degrees <=2 in G, not inside an edge of G;
  (ii)  isolated vertices Y: |Y|<=1; Y nonempty => s(K)=1 and all components tight; sum s(F_i) = s(K)+2-3|Y|;
        components: connected, in C (linear, F7, P3-hall), Delta<=3, contain a co-vertex;
  (iii) free choice in every component; pair richness for the pairs P_j inside one component (checked via (*)),
  (iv)/(v) pattern classification; r<=2 if Y empty, r<=3 otherwise; no two pairs in one component when r>=2;
        the pattern conditions (NC pairs, e-configurations, b-configurations) hold, since (*) holds (K = G+v);
        in (f): F1 + w(P1,{c,e}) not in C.
Proposition 6: for every NC pair {x,y} of K: tau(K-x-y) = tau(K)-1; s(K-x-y) = s(K)+5-2|d(x,y)| >= 0; if both have
degree 2: they share an edge, s(K)=1, K-x-y is a union of <=5 tight components.
Usage: python3 thm3_check.py [sample_per_cell]"""
import sys, time, itertools, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-fable')
import ref3 as R

I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
CELLS = ['cell_3_1_1', 'cell_10_7_4', 'cell_14_12_6', 'cell_17_13_7', 'cell_8_5_3', 'cell_12_10_5', 'cell_15_11_6',
         'cell_19_16_8', 'cell_22_17_9', 'cell_26_22_11']

def in_C(n, E):
    return R.is_linear(E) and not R.contains_F7_direct(n, E) and R.p3_hall(n, E)

def slack(n, E, t):
    return 3 * n + 2 * len(E) - 11 * t

def mintrans_set(n, E):
    Ts, t = R.all_min_transversals(R.edge_masks(E), n)
    return Ts, t

def cotrans_enum(Ts, X):
    mk = 0
    for x in X:
        mk |= 1 << x
    return any((T & mk) == mk for T in Ts)

def main():
    sample = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    random.seed(7)
    stats = {'graphs': 0, 'deg3': 0, 'patterns': {}, 'fails': [], 'nc_pairs': 0, 'nc_types': {}, 'crosscheck': 0}
    for cell in CELLS:
        lines = [l for l in open(I + cell + '.txt').read().split('\n') if l.strip()]
        graphs = []
        for l in lines:
            n, m, t, E = R.parse_line(l)
            if max(R.degrees(n, E)) <= 3:
                graphs.append((n, m, t, E))
        if sample and len(graphs) > sample:
            graphs = random.sample(graphs, sample)
        t0 = time.time()
        for (n, m, tcl, E) in graphs:
            stats['graphs'] += 1
            tK = R.tau(n, E)
            assert tK == tcl, (cell, tK, tcl)
            sK = slack(n, E, tK)
            assert sK in (0, 1)
            deg = R.degrees(n, E)
            TsK, _ = mintrans_set(n, E)
            # ---------- Proposition 6: NC pairs
            low = [x for x in range(n) if deg[x] <= 2]
            for x, y in itertools.combinations(low, 2):
                co = cotrans_enum(TsK, [x, y])
                if stats['crosscheck'] < 400:  # cross-check enumeration against direct tau
                    co2 = R.cotransversal(n, E, [x, y], tK)
                    stats['crosscheck'] += 1
                    if co != co2:
                        stats['fails'].append((cell, 'crosscheck', x, y))
                if co:
                    continue
                stats['nc_pairs'] += 1
                sig = 1 if any(x in e and y in e for e in E) else 0
                bd = deg[x] + deg[y] - sig
                typ = (min(deg[x], deg[y]), max(deg[x], deg[y]), sig)
                stats['nc_types'][typ] = stats['nc_types'].get(typ, 0) + 1
                n2, E2, _ = R.sub(n, E, [x, y])
                t2 = R.tau(n2, E2)
                s2 = slack(n2, E2, t2)
                if t2 != tK - 1 or s2 != sK + 5 - 2 * bd or s2 < 0:
                    stats['fails'].append((cell, 'prop6-identity', x, y, t2, tK, s2, sK, bd))
                if deg[x] == 2 and deg[y] == 2:
                    if sig != 1 or sK != 1:
                        stats['fails'].append((cell, 'prop6-22', x, y, sig, sK))
                    comps = R.components(n2, E2)
                    if len(comps) > 5:
                        stats['fails'].append((cell, 'prop6-5comps', x, y, len(comps)))
                    for c in comps:
                        Ec = [e for e in E2 if e[0] in c]
                        nc, Ecc, _ = R.sub(n2, E2, [u for u in range(n2) if u not in c])
                        if slack(nc, Ecc, R.tau(nc, Ecc)) != 0:
                            stats['fails'].append((cell, 'prop6-nontight', x, y))
            # ---------- Theorem 3 at every degree-3 vertex
            for v in range(n):
                if deg[v] != 3:
                    continue
                stats['deg3'] += 1
                Pv = [tuple(sorted(u for u in e if u != v)) for e in E if v in e]
                six = [u for p in Pv for u in p]
                if len(set(six)) != 6:
                    stats['fails'].append((cell, v, 'pairs not disjoint')); continue
                n2, E2, keep = R.sub(n, E, [v])
                new = {x: i for i, x in enumerate(keep)}
                tG = R.tau(n2, E2)
                sG = slack(n2, E2, tG)
                if tG != tK - 1 or sG != sK + 2:
                    stats['fails'].append((cell, v, 'tau/slack of G', tG, tK, sG, sK))
                dG = R.degrees(n2, E2)
                P = [tuple(sorted(new[u] for u in p)) for p in Pv]
                for p in P:
                    if any(dG[u] > 2 for u in p) or any(set(p) <= set(e) for e in E2):
                        stats['fails'].append((cell, v, 'pair degree/inside edge', p))
                comps = R.components(n2, E2)
                Y = [c[0] for c in comps if len(c) == 1]
                Fs = [c for c in comps if len(c) > 1]
                if len(Y) > 1:
                    stats['fails'].append((cell, v, '|Y|>1'))
                if Y and sK != 1:
                    stats['fails'].append((cell, v, 'Y nonempty but s(K)!=1'))
                # components: data
                comp_data = []
                for c in Fs:
                    cs = set(c)
                    nc, Ec, keepc = R.sub(n2, E2, [u for u in range(n2) if u not in cs])
                    newc = {x: i for i, x in enumerate(keepc)}
                    tc = R.tau(nc, Ec); sc = slack(nc, Ec, tc)
                    if not (R.connected(nc, Ec) and in_C(nc, Ec) and max(R.degrees(nc, Ec)) <= 3 and 0 <= sc <= 3):
                        stats['fails'].append((cell, v, 'component property', nc, len(Ec), tc, sc))
                    if Y and sc != 0:
                        stats['fails'].append((cell, v, 'Y nonempty but component not tight'))
                    if not (cs & set(six)):
                        stats['fails'].append((cell, v, 'component without co-vertex'))
                    Tsc, _ = mintrans_set(nc, Ec)
                    # free choice
                    for x in range(nc):
                        if not cotrans_enum(Tsc, [x]):
                            stats['fails'].append((cell, v, 'free choice fails', nc, len(Ec)))
                            break
                    comp_data.append((cs, nc, Ec, newc, tc, sc, Tsc))
                ssum = sum(cd[5] for cd in comp_data) + 3 * len(Y)
                if ssum != sK + 2:
                    stats['fails'].append((cell, v, 'slack sum', ssum, sK))
                r = len(Fs)
                # which component holds each vertex
                def comp_of(u):
                    for i, cd in enumerate(comp_data):
                        if u in cd[0]:
                            return i
                    return None  # isolated
                def nc_pair(ci, a, b):  # NC pair in component ci (degrees <=2 guaranteed by (i))
                    cd = comp_data[ci]
                    return not cotrans_enum(cd[6], [cd[3][a], cd[3][b]])
                def share_edge(ci, a, b):
                    cd = comp_data[ci]
                    return any(cd[3][a] in e and cd[3][b] in e for e in cd[2])
                def e_config(ci, z, a, b):
                    return nc_pair(ci, z, a) and nc_pair(ci, z, b) and not share_edge(ci, a, b)
                def b_config(ci, a, b, c):
                    return nc_pair(ci, a, b) and nc_pair(ci, a, c) and nc_pair(ci, b, c)
                if not Y:
                    if r > 2:
                        stats['fails'].append((cell, v, 'r>2 with Y empty', r))
                    types = []
                    for p in P:
                        c0, c1 = comp_of(p[0]), comp_of(p[1])
                        types.append('in%d' % c0 if c0 == c1 else 's')
                    if r >= 2 and any(types.count('in%d' % i) >= 2 for i in range(r)):
                        stats['fails'].append((cell, v, 'two pairs in one component, r>=2'))
                    if r == 1:
                        pat = 'a'
                    elif types.count('s') == 3:
                        pat = 'b'
                        for ci in range(r):
                            xs = [u for p in P for u in p if comp_of(u) == ci]
                            if len(xs) != 3 or not b_config(ci, *xs):
                                stats['fails'].append((cell, v, 'pattern b condition'))
                    elif types.count('s') == 1:
                        pat = 'e'
                        ps = P[types.index('s')]
                        for ci in range(r):
                            pin = [p for p, ty in zip(P, types) if ty == 'in%d' % ci][0]
                            z = [u for u in ps if comp_of(u) == ci][0]
                            if not e_config(ci, z, pin[0], pin[1]):
                                stats['fails'].append((cell, v, 'pattern e condition'))
                    elif types.count('s') == 2:
                        pat = 'f'
                        pin = [p for p, ty in zip(P, types) if ty != 's'][0]
                        ci = comp_of(pin[0]); cj = 1 - ci
                        ce = [u for p, ty in zip(P, types) if ty == 's' for u in p if comp_of(u) == ci]
                        df = [u for p, ty in zip(P, types) if ty == 's' for u in p if comp_of(u) == cj]
                        ok = all(nc_pair(ci, x, y) for x in pin for y in ce) and nc_pair(cj, df[0], df[1])
                        if not ok:
                            stats['fails'].append((cell, v, 'pattern f condition'))
                        # F1 + w(P1,{c,e}) not in C
                        cd = comp_data[ci]
                        w = cd[1]
                        Ew = list(cd[2]) + [tuple(sorted((w, cd[3][pin[0]], cd[3][pin[1]]))), tuple(sorted((w, cd[3][ce[0]], cd[3][ce[1]])))]
                        if in_C(w + 1, Ew):
                            stats['fails'].append((cell, v, 'pattern f: F1+w(P1,{c,e}) in C'))
                    else:
                        pat = 'other:' + ','.join(types)
                        stats['fails'].append((cell, v, 'unclassified', types))
                else:
                    if r > 3:
                        stats['fails'].append((cell, v, 'r>3 with Y'))
                    y = Y[0]
                    P3 = [p for p in P if y in p][0]
                    f = [u for u in P3 if u != y][0]
                    others = [p for p in P if y not in p]
                    types = []
                    for p in others:
                        c0, c1 = comp_of(p[0]), comp_of(p[1])
                        types.append('in%d' % c0 if c0 == c1 else 's')
                    if r >= 2 and types[0] == types[1] and types[0] != 's':
                        stats['fails'].append((cell, v, 'two pairs in one component, r>=2 (Y case)'))
                    cf = comp_of(f)
                    if r == 1:
                        pat = 'i1'
                    elif r == 3:
                        pat = 'i3'
                        pin = [p for p, ty in zip(others, types) if ty != 's']
                        if len(pin) != 1 or comp_of(pin[0][0]) != cf or not (nc_pair(cf, pin[0][0], f) and nc_pair(cf, pin[0][1], f)):
                            stats['fails'].append((cell, v, 'pattern i3 condition'))
                    else:
                        pat = 'i2'
                        # generic verification of the equivalence via the stated NC conditions:
                        # (i2-1),(i2-2): some pair inside the component of f: {a,f},{b,f} NC;  (i2-3): pair inside F1, c in F1, d,f in F2:
                        # {a,c},{b,c} NC in F1 and {d,f} NC in F2; (i2-4): a,c,f in F1; b,d in F2: {f,a},{f,c} NC, {b,d} NC
                        pin = [p for p, ty in zip(others, types) if ty != 's']
                        if pin and comp_of(pin[0][0]) == cf:
                            a, b = pin[0]
                            if not (nc_pair(cf, a, f) and nc_pair(cf, b, f)):
                                stats['fails'].append((cell, v, 'pattern i2-1/i2-2 condition'))
                        elif pin:
                            a, b = pin[0]; ci = comp_of(a); cj = cf
                            sp = [p for p, ty in zip(others, types) if ty == 's'][0]
                            c = [u for u in sp if comp_of(u) == ci][0]; d = [u for u in sp if comp_of(u) == cj][0]
                            if not (nc_pair(ci, a, c) and nc_pair(ci, b, c) and nc_pair(cj, d, f)):
                                stats['fails'].append((cell, v, 'pattern i2-3 condition'))
                        else:
                            ci = cf; cj = 1 - cf
                            A = [u for p in others for u in p if comp_of(u) == ci]
                            B = [u for p in others for u in p if comp_of(u) == cj]
                            if not (all(nc_pair(ci, f, a) for a in A) and nc_pair(cj, B[0], B[1])):
                                stats['fails'].append((cell, v, 'pattern i2-4 condition'))
                stats['patterns'][pat] = stats['patterns'].get(pat, 0) + 1
        print(cell, 'graphs', len(graphs), 'done in %.0fs' % (time.time() - t0), '| running: deg3', stats['deg3'], 'patterns', stats['patterns'], 'NC pairs', stats['nc_pairs'], 'fails', len(stats['fails']), flush=True)
    print('SUMMARY graphs', stats['graphs'], 'deg3 vertices', stats['deg3'], 'patterns', stats['patterns'])
    print('NC pairs', stats['nc_pairs'], 'types (dmin,dmax,sigma):', stats['nc_types'], 'crosschecks', stats['crosscheck'])
    print('FAILS', len(stats['fails']), stats['fails'][:20])

if __name__ == '__main__':
    main()
