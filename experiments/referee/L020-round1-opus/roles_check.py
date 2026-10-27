"""Re-check (own code) of the role statements of L017 C5 used in L020 Step 4.3, on the 483 stored
near-tight graphs with <= 26 vertices (Delta <= 3 part of the ten slack <= 1 lists), plus Proposition 6
(L020) on every NC pair found.  Usage: python3 roles_check.py <cell files>"""
import sys, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg


def read_cell(path):
    out = []
    for line in open(path):
        a = [int(x) for x in line.split()]
        if not a:
            continue
        n, m, t = a[:3]
        es = [tuple(sorted(a[3 + 3 * i:6 + 3 * i])) for i in range(m)]
        out.append((n, m, t, es))
    return out


def analyse(n, es, t):
    TL = hg.all_min_transversals(es, t)
    d = hg.degrees(n, es)
    B = [0] * n
    for k, T in enumerate(TL):
        for x in hg.bits(T):
            B[x] |= 1 << k
    low = [x for x in range(n) if d[x] <= 2]
    NC = set((x, y) for x, y in itertools.combinations(low, 2) if B[x] & B[y] == 0)
    def nc(x, y):
        return (min(x, y), max(x, y)) in NC
    share = set()
    for e in es:
        for p in itertools.combinations(sorted(e), 2):
            share.add(p)
    def sh(x, y):
        return (min(x, y), max(x, y)) in share
    b_any = [tr for tr in itertools.combinations(low, 3) if nc(tr[0], tr[1]) and nc(tr[0], tr[2]) and nc(tr[1], tr[2])]
    e_cfg = []
    for z in low:
        for x, y in itertools.combinations(low, 2):
            if z in (x, y) or sh(x, y):
                continue
            if nc(z, x) and nc(z, y):
                e_cfg.append((z, x, y))
    f_cfg = []
    for a, b in itertools.combinations(low, 2):
        if sh(a, b):
            continue
        for c, e in itertools.combinations([u for u in low if u not in (a, b)], 2):
            if nc(a, c) and nc(a, e) and nc(b, c) and nc(b, e):
                f_cfg.append(((a, b), (c, e)))
    return TL, d, NC, b_any, e_cfg, f_cfg, B


if __name__ == '__main__':
    totals = {}
    nctypes = {}
    prop6_fail = 0
    nnc = 0
    for path in sys.argv[1:]:
        L = read_cell(path)
        t0 = time.time()
        cnt = dict(classes=0, with_b=0, with_e=0, with_f=0, with_nc=0, all_vertices_covered=0, tau_ok=0, inC=0, connected=0)
        for n, m, t, es in L:
            d0 = hg.degrees(n, es)
            if max(d0) > 3:
                continue
            cnt['classes'] += 1
            tt = hg.tau_bb(es)
            cnt['tau_ok'] += (tt == t)
            cnt['inC'] += hg.in_C(n, es)
            cnt['connected'] += hg.is_connected(n, es)
            TL, d, NC, b_any, e_cfg, f_cfg, B = analyse(n, es, tt)
            cnt['all_vertices_covered'] += all(B[x] for x in range(n))
            cnt['with_b'] += bool(b_any)
            cnt['with_e'] += bool(e_cfg)
            cnt['with_f'] += bool(f_cfg)
            cnt['with_nc'] += bool(NC)
            s = hg.slack(n, m, tt)
            # Proposition 6 on every NC pair
            for x, y in NC:
                nnc += 1
                sig = 1 if any(x in e and y in e for e in es) else 0
                key = (min(d[x], d[y]), max(d[x], d[y]), sig)
                nctypes[key] = nctypes.get(key, 0) + 1
                rest = [v for v in range(n) if v not in (x, y)]
                es2 = [e for e in es if x not in e and y not in e]
                n2, es2r, _ = hg.relabel(rest, es2)
                t2 = hg.tau_bb(es2r)
                dpart = sum(1 for e in es if x in e or y in e)
                assert dpart == d[x] + d[y] - sig
                s2 = hg.slack(n2, len(es2r), t2)
                ok = (t2 == tt - 1) and (s2 == s + 5 - 2 * dpart) and s2 >= 0
                if d[x] == 2 and d[y] == 2:
                    comps = hg.components(rest, es2)
                    ok &= sig == 1 and s == 1 and s2 == 0 and len(comps) <= 5
                    for vs, ce in comps:
                        nn, cer, _ = hg.relabel(vs, ce)
                        tc = hg.tau_bb(cer)
                        ok &= hg.slack(nn, len(cer), tc) == 0 and max(hg.degrees(nn, cer) or [0]) <= 3 and len(cer) > 0
                if not ok:
                    prop6_fail += 1
                    print('PROP6 FAIL', path, es, (x, y))
        print(path.split('/')[-1], cnt, f'{time.time()-t0:.1f}s', flush=True)
        totals[path.split('/')[-1]] = cnt
    print('NC pairs total', nnc, 'types (dmin,dmax,sigma):', dict(sorted(nctypes.items())), 'Prop6 failures', prop6_fail)
