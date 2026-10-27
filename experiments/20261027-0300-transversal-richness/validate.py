"""Independent pure-Python (pyverify.py, from L014) re-computation of the rich.cpp statistics on the first K classes of a cell; asserts equality."""
import sys, json, subprocess, itertools
from pyverify import in_C, linear, has_f7, p3, all_covers_exact
cell, K = sys.argv[1], int(sys.argv[2])
lines = open('inputs/cell_%s.txt' % cell).read().split('\n')[:K]
cpp = [json.loads(l) for l in subprocess.run(['./rich'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()]
for line, c in zip(lines, cpp):
    a = list(map(int, line.split())); n, m, tau = a[:3]; E = [tuple(a[3+3*i:6+3*i]) for i in range(m)]
    Ts = all_covers_exact(E, tau); assert len(Ts) == c['nT'], (len(Ts), c['nT'])
    V = range(n); deg = [sum(v in e for e in E) for v in V]
    inedge = lambda x, y: any(x in e and y in e for e in E)
    p2tot = [0]*12; p2fail = [0]*12
    for x, y in itertools.combinations(V, 2):
        k = min(11, deg[x]+deg[y]-(1 if inedge(x, y) else 0)); p2tot[k] += 1
        if not any(x in T and y in T for T in Ts): p2fail[k] += 1
    assert p2tot == c['p2tot'] and p2fail == c['p2fail']
    pairs = list(itertools.combinations(V, 2)); pp = ppc = 0
    for p, q in itertools.combinations(pairs, 2):
        if set(p) & set(q): continue
        pp += 1; ppc += any((set(p) & T) and (set(q) & T) for T in Ts)
    assert (pp, ppc) == (c['pp_all'], c['pp_all_cov'])
    nt = ncov = nadm = nadm_unc = unc = 0; combo = [0]*8
    for p1, p2, p3_ in itertools.combinations(pairs, 3):
        if len(set(p1)|set(p2)|set(p3_)) < 6: continue
        nt += 1; cov = any((set(p1)&T) and (set(p2)&T) and (set(p3_)&T) for T in Ts); ncov += cov
        H = E + [(n, *p1), (n, *p2), (n, *p3_)]
        L = linear(H); F = has_f7(H) if True else False; P = p3(H)
        adm = L and (not F) and P
        nadm += adm
        if not cov:
            unc += 1; nadm_unc += adm
            combo[(0 if L else 1) | (2 if (F and L) else 0) | (0 if P else 4)] += 1   # F-flag compared only when linear (distinctness conventions)
    assert (nt, ncov, nadm, nadm_unc, unc) == (c['ntrip'], c['ncov'], c['nadm'], c['nadm_unc'], c['unc_total']), ((nt, ncov, nadm, nadm_unc, unc), c)
    cc = list(c['unc_combo']); 
    # compare combos ignoring the F bit when non-linear
    cc2 = [0]*8
    for i, x in enumerate(cc): cc2[i if (i & 1) == 0 else i & ~2] += x
    assert cc2 == combo, (cc2, combo)
    print(cell, 'ok', 'nT', c['nT'], 'ntrip', nt, 'adm', nadm, 'unc', unc)
